# Exercise11: Evaluate Adversaries and Full Cost

Companion: https://github.com/Anirach/ai-core-functional-tutorial. Work in a disposable copy.

## Goal

Add an independently labeled case to a new validation dataset version, not the frozen held-out set. Define what constitutes a false accept and which cost inputs you would measure. Do not replace null usage with a guessed zero.

เพิ่มเคสที่ติดป้ายอิสระใน validation รุ่นใหม่ ไม่ใช่ held-out ที่ตรึง กำหนดว่า false accept คืออะไรและต้นทุนใดต้องวัด อย่าแทน usage null ด้วยศูนย์เดา

## Files

- `src/evaluation.mjs`
- `test/`

## Reference commands

```sh
node src/cli.mjs tune --split validation
node src/cli.mjs evaluate --split heldout --save
node src/cli.mjs evaluate --split attack --save
node src/cli.mjs cost --case V001
node src/cli.mjs cost --case V010
node --test --test-reporter=spec test/evaluation.test.mjs
```

## Expected reference behavior

The reference held-out run has12 cases,12 accepts and one deliberate false accept; total cost is null due to missing usage. Single V001 modeled cost per correct accepted artifact is approximately USD0.00037024, while V010 is null. These are fictional scenario calculations only.

## Failure to preserve

Optimizing cost per accept can reward accepting wrong answers. The false-accept example makes that failure concrete. Compare costs only after equal acceptable quality and coverage constraints are satisfied on appropriate data.

## Checkpoint

Run the matching tests, inspect the gate reasons and restore the original. Do not tune on held-out cases or enable paid calls.
