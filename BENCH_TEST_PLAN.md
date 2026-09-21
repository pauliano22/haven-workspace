# Bench test plan — what you can test before the new board arrives

Written 2026-09-21. Everything here uses hardware you already have (Teensy 4.1
prototype + SGTL5000 audio shield), a phone or laptop, and earbuds. None of it
needs the new board. Software-only checks are in section 0.

## 0. No hardware at all (already done, re-runnable)

| Check | Command (in `mobile_app/haven_custom_app`) | Last result (2026-09-21) |
|---|---|---|
| App unit tests (safety caps, LDL tone, preview tone, tolerance plan, BLE queue) | `npx jest` | 8 suites, 47 tests pass |
| App type check | `npx tsc --noEmit` | clean |
| Web build renders, tabs work | `npx expo start --web` then open localhost | Home, Tune, Hearing, and "Match your sound" screens render, no page errors |

Limit: the web build has no real device. `sendPayload` is a no-op there, so this
proves screens render, not that sound changes. The guided tests that play tones
need a connected device.

## 1. Teensy prototype: what it can and can't do

The Teensy firmware (`legacy_prototypes/teensy_hearing_shield/src/main.cpp`)
reads newline-terminated JSON on **`Serial1`** (hardware UART, 115200 baud), not
USB. It has no Bluetooth. So:

- **Phone app to Teensy needs a BLE-to-UART module** (for example an HM-10 or
  Adafruit Bluefruit UART module) wired to Serial1. Do you have one attached?
  If not, the app can't drive it.
- **Without a BLE module**, you can still test the DSP: wire a USB-serial
  adapter (3.3 V logic) to Serial1 and send lines from a laptop, for example
  `{"type":"MULTI_FILTER","bands":[{"f0":4500,"Q":10}]}` followed by a newline.
  USB `Serial` (9600) prints confirmations like "MULTI_FILTER applied: 1 band(s)".
- The Teensy does not implement `BYPASS` or the tone messages (`TONE_START` etc.),
  so the LDL test and Match-your-sound flows can't run against it.

## 2. Notch depth test (does the filter do what the app says?)

Needs: Teensy running, a signal source, a way to record output.
1. Play a sine sweep (200 Hz to 8 kHz) or steady tones into the audio shield input.
2. Record the shield output (line out or headphone out) on a laptop, once with no
   filter and once with a 4500 Hz, Q=10 notch sent.
3. Compare levels at 4500 Hz and at 1 kHz and 8 kHz. Expected: a clear dip at
   4500 Hz and roughly unchanged levels elsewhere.
4. Repeat for Q=2 and Q=20 to check width. Note that `atten_db` is a newer field,
   and the Teensy prototype only computes a pure notch.
Record: measured dip in dB, and the width at -3 dB.

## 3. Hear-through latency (the core product risk)

Needs: Teensy, a tone or click source, a phone or laptop that records stereo.
1. Feed a click train into the shield input. Put the input signal on one recorder
   channel and the shield output on the other.
2. Record, then measure the delay between the same click in both channels in an
   audio editor (Audacity works).
3. Repeat with the Teensy's audio buffer at its normal size.
Reference points: the ADAU1860 hardware DSP target is about 50-150 microseconds
(from datasheet-level reasoning, not measured). The concern threshold from the
earlier analysis was a few milliseconds, where comb filtering with the direct
sound becomes audible. The Teensy's number is only a baseline. It is not the
answer for the new board, because the Teensy codec path is different.
Record: delay in ms.

## 4. Comfort and usability tests you can do with no electronics

- **3D-printed fit test**: print `hardware/mechanical_cad/haven_dev_board_enclosure_v1/fit_test_prints/`
  (S, M, L). See its README for the protocol. Do this with your dad if possible.
- **Match-your-sound on the app**: needs a connected device to play tones. Until
  then, you can review the screens and wording in the web build.

## 5. What each result feeds

| Test | Decides |
|---|---|
| Notch depth | Whether the filter math is right before it goes on the ADAU1860 |
| Latency baseline | Whether the hear-through requirement is realistic |
| Fit test | Size and shape of the first real shell |
