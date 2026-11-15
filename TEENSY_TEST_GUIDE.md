# Teensy test guide: try the idea on your dad with hardware you already own

Written 2026-11-08. **Nothing here has been run on the real Teensy yet.** The new test firmware is written and
being compile-checked; it has not been flashed. Read the safety section first.

## What this test answers

Does taking a specific frequency (or a few) out of a sound make that sound less bothersome for your dad?
That is the core Haven idea. It costs nothing but an afternoon, and it tells you whether the $500 of boards is worth it.
It does **not** test the final device: the Teensy path has several milliseconds of delay and sealed earbuds block the
room, so it is for playing recorded or phone sounds through a filter, not for wearing around the house.

## What you need

| Item | Notes |
|---|---|
| Teensy 4.1 with the PJRC Audio Shield (SGTL5000) | You have it. Check the shield has its headers/pads soldered (line-in pads, headphone jack) |
| Wired earbuds with a **3.5 mm plug** | Any cheap pair. Not USB-C, Lightning or Bluetooth. 16-32 ohm is right. **Avoid sensitive in-ear monitors**: they get much louder for the same signal. Open-back headphones are a gentler first try |
| A phone, plus a 3.5 mm cable to the shield's line-in | Lets you play recorded sounds into the filter. The line-in is solder pads or header pins, not a jack, so you may need a small cable with jumper ends |
| A computer with Teensy Loader or PlatformIO | USB (micro-USB) from the Teensy to the computer, also used to send commands |

If the line-in is awkward, say so and I will write a variant that plays a test sound from the Teensy itself.

## Safety: do this before anyone wears it

1. **Do not use the old sketch** (`teensy_hearing_shield`): it sets microphone gain 36 dB and headphone volume 0.6 with no
   limit. Use `legacy_prototypes/teensy_safe_test/` instead. It has a fixed digital ceiling of -20 dB, a low start volume
   (0.10), a hard maximum volume (0.35), and mutes while a filter changes.
2. **Those numbers are guesses.** I do not know what sound level they give at your earbuds. Treat them as "probably quiet",
   not as safe.
3. **You go first, with earbuds not in your ear.** Hold them a little way off, volume at the starting step, and listen
   as you raise it one step at a time. Stop at comfortable. Write the step number down.
4. **Real level check.** A phone sound-meter app is a rough guide only. A real check needs a sound level meter in an ear
   coupler (see `BRINGUP_PLAN.md` stage 7). Until then keep the volume at or below your comfortable step and never use the
   `VOL_MAX` step for a person.
5. **Your dad stays in control:** he holds the earbud and can pull it out any time; unplugging USB mutes everything.
   Start him at the lowest step. Stop at once on any pain, a jump in tinnitus, or if he feels worse afterwards.
6. Avoid the **mic** mode for him in the first round: a sealed earbud next to a live microphone can squeal, and the room
   sound is blocked. Line-in with recorded sounds is the safe first test.

## Steps

### Step 1: Get his sounds on a phone
Record 1-2 minutes of the sound that bothers him (the basement geothermal system at night, for example) with the phone's
voice memo app, held near where he hears it. Also record 30 seconds of a sound that does NOT bother him for comparison.
Save the files in `~/projects/active/haven_workspace/` somewhere under a folder you pick, and tell me the path.

### Step 2: I find the frequencies
I will run the analysis tools already in the repo (`firmware/haven_zephyr_app/ml/`: `analyze.py`, `rolling_analyze.py`,
`sound_signature.py`) on those recordings and give you up to five frequencies and widths to try, with plain-language
reasons. This also gives me the first real-recording test of the sound-learning prototype.

### Step 3: Flash the safe firmware
From a terminal: `cd ~/projects/active/haven_workspace/legacy_prototypes/teensy_safe_test && pio run -t upload`
(or open `src/main.cpp` in Arduino IDE with Teensyduino, board Teensy 4.1). Press the button on the Teensy if it asks.
Open the serial monitor at 115200 baud. You should see "Haven Teensy safe test ready".

### Step 4: Wire up and check, with you listening
- Phone audio out -> shield line-in (left channel is used) and common ground.
- Earbuds in the shield's headphone jack, **held away from the ear**.
- Type `line` then `s`, play a quiet sound, type `u` one step at a time until you hear it comfortably. Note the volume.

### Step 5: The A/B test with your dad
1. Play his bothersome recording with the filter **bypassed** (`b`), then with the filter on (`clear`, then `n 4500 10` etc.
   with the frequencies from step 2). Do not tell him which is which: you press, he rates.
2. Use short plays (10-20 seconds), a rest between, and a 0-10 discomfort score each time. Repeat each condition three
   times in a random order. Write the scores in a table.
3. If one filter helps, try making it wider (lower Q) or adding a second frequency. If nothing helps, that is an answer too.

### Step 6: Write it down
Save the scores, the frequencies and the volume step. Tell me and I will log them in the project files and use them to
decide what the first real prototype needs to do.

## What the results mean

| Result | Meaning |
|---|---|
| Clear, repeatable drop in discomfort with the filter | The idea has real support for him. Worth building the pod |
| No difference | Frequency filtering of this sound may not be the lever for him. Try level reduction or a different sound before spending |
| Worse, or any pain | Stop. Not a reason to continue; we rethink |

One person, one sound, a few trials is **weak evidence**. It cannot tell you whether this works for hyperacusis in
general. It tells you whether it is worth the next step for him.
