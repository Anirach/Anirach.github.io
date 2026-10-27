# Exercise6: Read Typed Decisions and Uncertainty

Companion: https://github.com/Anirach/ai-core-functional-tutorial. Work in a disposable copy.

## Goal

Change a criterion description and print the resulting body. Add a test asserting the expected answer IDs still match. The fixture answers remain unchanged; write down how you would validate the new wording with independent real data later.

แก้คำอธิบาย criterion แล้วพิมพ์ body เพิ่ม test ว่า answer IDs ยังตรงกัน คำตอบ fixture จะไม่เปลี่ยน ให้จดว่าจะยืนยันถ้อยคำใหม่ด้วยข้อมูลจริงอิสระภายหลังอย่างไร

## Files

- `src/questions.mjs`
- `test/`

## Reference commands

```sh
node src/cli.mjs request --stage input --case V001
node src/cli.mjs request --stage quality --case V001
node src/cli.mjs judge --stage input --case V005
node --test --test-reporter=spec test/contracts.test.mjs
```

## Expected reference behavior

Request output names jev-1.14.0 and the expected stage question IDs. It performs no inference. V005 reviews on valid typed output. Contract tests reject missing fields, wrong types, nonfinite values and a moving alias.

## Failure to preserve

A helper that treats Noul as an urgency score can invert product behavior. It is probability of a proposition, not magnitude. If a task needs ordered quality levels, design a documented Score rubric separately instead of relabeling Noul values.

## Checkpoint

Run the matching tests, inspect the gate reasons and restore the original. Do not tune on held-out cases or enable paid calls.
