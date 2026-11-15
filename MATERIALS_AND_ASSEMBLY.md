# Haven v2: what it's made of and how it goes together

Written 2026-11-07. Plain-language plan for the behind-the-ear (BTE) design.
Every line is marked **Decided** (Paul chose it), **Proposed** (my recommendation, not yet
approved) or **Unknown** (needs a quote, a measurement, or a test). Nothing here has been
built yet. Status of what has actually been tested lives in `PROJECT_STATUS.md`.

## The parts, in one picture

Two pods and two in-ear units make a pair (one of each per ear), plus one charging case.

| Piece | What it is | Touches skin? |
|---|---|---|
| In-ear unit | Small plastic shell with the speaker, the outer microphone, a 6 mm square circuit board and a tube (nozzle) that an ear tip slides onto | Yes, for hours, inside the ear |
| Ear tip | Soft foam or silicone cone on the nozzle. It seals the ear canal | Yes, inside the canal |
| Comfort sleeve (M/L only) | Soft silicone band over the part of the in-ear shell that rests in the bowl of the ear | Yes |
| Cable | 6 hair-thin wires in a sleeve, about 55 mm, running over the top of the ear | Yes, rests on the skin at the top of the ear |
| Pod | Plastic shell behind the ear with the battery, the radio board and the charging contacts | Yes, behind the ear |
| Charging contacts on the pod | Two small metal pins | Yes, behind the ear |
| Case | Plastic box with a USB-C port, a rechargeable cell and two spring pins | No |

## Materials

### Anything worn: the skin-contact question

**Unknown, and it matters.** The current print order in `V2_ORDER.md` uses JLC3DP "9600"
resin. I found no published biocompatibility data for it (searched 2026-11-07), so it must be
treated as **not safe for hours of skin contact**. It is fine for what it is currently planned
for: a short fit test of empty shells, minutes at a time, with nothing electronic inside.

**Proposed for anything worn with electronics:** print the in-ear shell and pod shell in
Formlabs **BioMed Clear** resin.
- Formlabs says parts made and finished by its instructions meet ISO 10993-1:2018 (the
  international standard for testing materials that touch the body) for long-term skin and
  mucous-membrane contact, with passing results for cell toxicity, irritation and allergic
  sensitization.
- It was launched for hard earmolds and in-ear monitors.
- The certification only holds if the part is printed and washed exactly by Formlabs' process,
  in a dedicated tank. So we need a print service that runs Formlabs printers and uses that
  workflow. A material certificate does not certify our finished product; that is a separate
  step if Haven is ever sold.
- Sources: [Formlabs BioMed Clear](https://formlabs.com/products/biomed-clear-resin/),
  [datasheet](https://formlabs-media.formlabs.com/datasheets/2001432-TDS-JP-0.pdf).
- Not checked: price per part and which service bureau to use. Get real quotes first.

**Proposed:** a medical-grade silicone for sleeves and ear tips (off-the-shelf tips for now,
SpinFit CP145 or generic 4.5 mm-bore IEM tips). Our own molded silicone sleeves come later,
once the shape is final. JLC3DP has no flexible resin, so the fit-test sleeves will be rigid
and overstate how hard they press.

### Charging pins: nickel allergy

**Proposed change.** `V2_ORDER.md` lists "cut brass rod" for the pod's charging pins. Brass
often contains nickel, and these pins sit on skin for hours. Use gold-plated contacts, or sit
the pins behind the shell edge so skin does not touch them. This is a small change now and an
expensive recall later.

### Cable jacket

**Unknown.** A hand-built bundle of 38-40 AWG wire has no skin-safe rating. Cover it with a
medical or food-grade silicone or PTFE sleeve and check that the sleeve will bend over the
top of the ear without kinking. Build one and test it.

### Battery

**Decided:** VARTA CP1454, the larger coin cell, in the pod. It's a lithium-ion cell, so
the pod needs to be sealed so the cell is not reachable, and the charger limits its charge
current to about 40 mA. Fire and swallowing risk both argue for a pod that can only be opened
with a tool.

## How it's made: three stages

### Stage 1: fit and feel (cheap, no electronics)

1. Print the shells in 9600 resin (JLC3DP, $0.32 per part, 3-day build). Print the in-ear
   units, the pods, the M/L sleeves and the case.
2. Try them in a real ear for a few minutes. Your ear first, your dad's ear if he is willing.
3. Decide: does the in-ear unit fit, which size sleeve, which cable length (45, 55 or 57 mm)?

This stage answers the open fit question in `PROJECT_STATUS.md`. It needs no skin-safe
material because nothing is worn for long.

### Stage 2: first working pair (bench, not worn for long)

1. Order the three circuit boards (pod, in-ear, case) assembled by JLCPCB. Parts they can't
   place (the Bluetooth module and the power chip) are bought separately and either consigned
   to JLCPCB or soldered here. These parts are tiny and hard to hand-solder.
2. Program each pod through its test pads (SWD, the same method as the DK) before it goes in
   any shell.
3. Bench test, in this order, stopping at the first failure:
   power and charging, Bluetooth, codec talking, microphone, speaker, audio through the whole
   chain.
4. Build the 6-wire cable by hand. Attach it to the in-ear board and the pod.
5. Measure how loud it can get on a test coupler before it goes on a person. See Safety.

### Stage 3: wearable pair

1. Reprint shells in BioMed Clear.
2. Assembly order (**Proposed**): in-ear board into shell; speaker; cable with strain relief;
   seal the shell; pod board and battery into the pod; close the pod with screws or a snap
   plus adhesive; fit the charging contacts; fit the magnet.
3. Which adhesive and how the pod closes are **Unknown**. Use a medical-grade UV-cure
   adhesive if glue is needed, and leave the pod openable for repair on the first units.
4. Test again after closing: audio, charging, and a leak or sweat check.

## Safety, which comes before everything else

- **Decided in firmware:** a tone ceiling of 85 dB and a watchdog that silences it. This
  covers the hearing-test tone only.
- **Not done:** a measured maximum output of the finished device. `PROJECT_STATUS.md`
  lists this as required before your dad wears it.

  **Limits that exist (researched 2026-11-07):**
  - FDA over-the-counter hearing aids: output no higher than 111 dB SPL, or 117 dB SPL while
    input-controlled compression is active
    ([AAO-HNS summary](https://entnet.org/advocacy/regulatory-advocacy/over-the-counter-sale-of-hearing-aids/aao-hns-summary-fda-over-the-counter-hearing-aids-final-rule)).
    That is a ceiling for people with hearing loss and is far too high for Haven's users. I did
    not confirm the current codified text, so check the eCFR before citing it.
  - WHO-ITU safe listening (H.870): a weekly dose equal to 80 dBA for 40 hours, and 75 dBA for
    40 hours for children and sensitive users
    ([WHO](https://www.who.int/publications-detail/safe-listening-devices-and-systems-a-who-itu-standard)).
    Closer to the right order of magnitude for a hear-through device. Haven's own firmware ceiling for
    the hearing-test tones is 85 dB, so a hear-through ceiling should start lower.
  - **Proposed** (needs an audiologist's review): first-pair hear-through output capped at or below
    75 dB SPL at the eardrum equivalent, adjustable downward by the user, never upward past the cap.

  **How to measure (proposed, two stages):**
  1. Own check: a miniDSP EARS rig (reported prices $179 to $310, and its maker says it is not
     an industry-standard head) plus a sound-level calibrator. Good enough to find gross problems
     and compare settings, not to certify a number.
     ([price and caveats](https://parts-express.com/MiniDSP-EARS-Calibrated-USB-Measurement-Test-Jig-for-Headphones-230-3424))
  2. Before your dad wears it for hours: have the loudest setting measured on a standards-grade ear
     simulator (IEC 60318-4 class; new ones cost thousands of dollars, so ask a university acoustics
     lab, an audiology clinic or a hearing-aid shop to run it). **Unknown:** who will do this.
  - Whatever the measured number is, it goes in `PROJECT_STATUS.md` with the setup used.
- **Not done:** extend the same firmware ceiling to the real filter path (already noted in
  `firmware/haven_zephyr_app/PROPOSALS.md`).

## Decisions (Paul, 2026-11-07)

1. **Decided:** 9600 resin is for fit tests only. BioMed Clear is the material for the final product.
2. **Decided (Paul delegated the choice to me):** pod charging pins are gold-plated, flush with the
   shell, on a nickel-free base metal. Ask the supplier to confirm there is no nickel underplate.
   Fallback if that can't be confirmed: 316L stainless pins, a standard skin-contact medical
   alloy. Reason: pins sit on skin behind the ear for hours, and nickel allergy is common.
3. **Decided:** Paul's dad will try printed shells for a few minutes. Keep it to empty fit-test
   shells, no electronics, minutes at a time, until the loudness limit is measured.
