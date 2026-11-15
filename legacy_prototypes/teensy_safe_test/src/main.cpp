// Haven Teensy safe listening test.
//
// Same idea as ../teensy_hearing_shield (audio in -> notch filters -> headphones) but built so
// it can be used on a person: a fixed digital output ceiling, small codec volume steps, a hard
// volume maximum, the sound muted while a filter changes, and USB-serial control (no BLE module).
//
// NOT a medical device. The ceilings below are a starting point; measure the real level at the
// earbud before anyone wears it (see TEENSY_TEST_GUIDE.md at the haven_workspace root).
//
// Serial monitor (USB, 115200 baud), one command per line:
//   n <hz> <q>   add a notch filter (up to 5), e.g.  n 4500 10
//   clear        remove all filters
//   b            toggle bypass (filters off / on)
//   u / d        codec volume up / down one step (limited to VOL_MAX)
//   line / mic   choose input: line-in (use this first) or the microphone
//   s            print status
//   m            mute / unmute
#include <Arduino.h>
#include <Audio.h>
#include <Wire.h>
#include <SPI.h>

// ---- Safety numbers: change only after measuring ------------------------------------------
static const float DIGITAL_CEILING = 0.10f;  // 0.10 = -20 dB below full scale, applied after the filters
static const float VOL_START       = 0.10f;  // codec headphone volume at boot (0..1)
static const float VOL_MAX         = 0.35f;  // 'u' can never go above this
static const float VOL_STEP        = 0.025f;
static const int   MIC_GAIN_DB     = 12;     // microphone preamp, low on purpose (feedback)
static const int   LINE_LEVEL      = 13;     // SGTL5000 line-in level (0..15), 13 = about 1.3 Vpp
// ----------------------------------------------------------------------------------------------

static const int    MAX_BANDS   = 5;
static const double SAMPLE_RATE = 44100.0;

struct Biquad { double b0, b1, b2, a1, a2; };

static void notchCoeffs(double f0, double fs, double Q, Biquad &c) {
  double w0 = 2.0 * PI * (f0 / fs), alpha = sin(w0) / (2.0 * Q), a0 = 1.0 + alpha;
  c.b0 = 1.0 / a0; c.b1 = (-2.0 * cos(w0)) / a0; c.b2 = 1.0 / a0;
  c.a1 = (-2.0 * cos(w0)) / a0; c.a2 = (1.0 - alpha) / a0;
}

class NotchBank : public AudioStream {
public:
  NotchBank() : AudioStream(1, inQ) { clearAll(); }
  void clearAll() { AudioNoInterrupts(); n = 0; memset(z, 0, sizeof(z)); AudioInterrupts(); }
  bool add(double f0, double Q) {
    if (n >= MAX_BANDS || f0 < 100.0 || f0 > 12000.0 || Q < 0.5 || Q > 50.0) return false;
    Biquad c; notchCoeffs(f0, SAMPLE_RATE, Q, c);
    AudioNoInterrupts(); f[n] = c; z[n][0] = z[n][1] = 0; n++; AudioInterrupts();
    return true;
  }
  int count() const { return n; }
  virtual void update(void) {
    audio_block_t *blk = receiveWritable();
    if (!blk) return;
    if (!bypass) {
      for (int i = 0; i < AUDIO_BLOCK_SAMPLES; i++) {
        double s = (double)blk->data[i] / 32768.0;
        for (int b = 0; b < n; b++) {
          double o = s * f[b].b0 + z[b][0];
          z[b][0] = s * f[b].b1 - o * f[b].a1 + z[b][1];
          z[b][1] = s * f[b].b2 - o * f[b].a2;
          s = o;
        }
        if (s > 1.0) s = 1.0; if (s < -1.0) s = -1.0;
        blk->data[i] = (int16_t)(s * 32767.0);
      }
    }
    transmit(blk); release(blk);
  }
  volatile bool bypass = false;
private:
  audio_block_t *inQ[1];
  Biquad f[MAX_BANDS];
  double z[MAX_BANDS][2];
  int n = 0;
};

AudioInputI2S i2s_in;
NotchBank     notch;
AudioAmplifier ceiling_amp;   // fixed digital attenuation: the output can never exceed DIGITAL_CEILING
AudioOutputI2S i2s_out;
AudioControlSGTL5000 codec;
AudioConnection c1(i2s_in, 0, notch, 0);
AudioConnection c2(notch, 0, ceiling_amp, 0);
AudioConnection c3(ceiling_amp, 0, i2s_out, 0);
AudioConnection c4(ceiling_amp, 0, i2s_out, 1);

static float vol = VOL_START;
static bool muted = false;
static bool useMic = false;

static void applyInput() {
  if (useMic) { codec.inputSelect(AUDIO_INPUT_MIC); codec.micGain(MIC_GAIN_DB); }
  else        { codec.inputSelect(AUDIO_INPUT_LINEIN); codec.lineInLevel(LINE_LEVEL); }
}
static void applyGain() { ceiling_amp.gain(muted ? 0.0f : DIGITAL_CEILING); }
static void quietly(void (*fn)()) { ceiling_amp.gain(0.0f); delay(40); fn(); delay(40); applyGain(); }

static void status() {
  Serial.print("input="); Serial.print(useMic ? "mic" : "line");
  Serial.print(" volume="); Serial.print(vol, 3); Serial.print("/"); Serial.print(VOL_MAX, 3);
  Serial.print(" ceiling="); Serial.print(DIGITAL_CEILING, 2);
  Serial.print(" bands="); Serial.print(notch.count());
  Serial.print(" bypass="); Serial.print(notch.bypass ? "yes" : "no");
  Serial.print(" muted="); Serial.println(muted ? "yes" : "no");
}

void setup() {
  Serial.begin(115200);
  AudioMemory(16);
  codec.enable();
  codec.volume(0.0f);          // silent while starting
  ceiling_amp.gain(0.0f);
  applyInput();
  delay(200);
  codec.volume(vol);
  applyGain();
  Serial.println("Haven Teensy safe test ready. Commands: n <hz> <q>, clear, b, u, d, line, mic, m, s");
  status();
}

void loop() {
  static String line;
  while (Serial.available()) {
    char ch = (char)Serial.read();
    if (ch != '\n' && ch != '\r') { if (line.length() < 40) line += ch; continue; }
    line.trim();
    if (line.length() == 0) continue;
    if (line == "u") { vol = min(VOL_MAX, vol + VOL_STEP); codec.volume(vol); }
    else if (line == "d") { vol = max(0.0f, vol - VOL_STEP); codec.volume(vol); }
    else if (line == "b") { notch.bypass = !notch.bypass; }
    else if (line == "m") { muted = !muted; applyGain(); }
    else if (line == "clear") { ceiling_amp.gain(0.0f); delay(40); notch.clearAll(); delay(40); applyGain(); }
    else if (line == "line") { ceiling_amp.gain(0.0f); delay(40); useMic = false; applyInput(); delay(40); applyGain(); }
    else if (line == "mic")  { ceiling_amp.gain(0.0f); delay(40); useMic = true;  applyInput(); delay(40); applyGain(); }
    else if (line.startsWith("n ")) {
      float hz = 0, q = 0;
      if (sscanf(line.c_str() + 2, "%f %f", &hz, &q) == 2) {
        ceiling_amp.gain(0.0f); delay(40);
        bool ok = notch.add(hz, q);
        delay(40); applyGain();
        if (!ok) Serial.println("rejected (limits: up to 5 notches, 100-12000 Hz, Q 0.5-50)");
      } else Serial.println("usage: n <hz> <q>");
    }
    else if (line != "s") Serial.println("unknown command");
    status();
    line = "";
  }
}
