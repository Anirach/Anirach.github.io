# Exercise2: Define Contracts Before Models

Companion: https://github.com/Anirach/ai-core-functional-tutorial. Work in a disposable copy.

## Goal

Add a contract test for a wrong model, then a negative probability. Confirm both are rejected while a valid Noul without confidence still passes. Do not fix the exercise by adding a fictional API field.

เพิ่ม test สำหรับ model ผิดรุ่นและ probability ติดลบ ให้ทั้งสองถูกปฏิเสธ แต่ Noul ที่ไม่มี confidence ยังผ่าน อย่าแก้แบบฝึกด้วยการเพิ่มฟิลด์ API ที่ไม่มีจริง

## Files

- `src/contracts.mjs`
- `test/`

## Reference commands

```sh
node --test --test-reporter=spec test/contracts.test.mjs
node src/cli.mjs request --stage input --case V001
node src/cli.mjs judge --stage input --case V005
```

## Expected reference behavior

All contract tests pass; deliberately mutated response variants throw. V005 returns human_review rather than reject or accept. The fixture model field is the pinned version, so a moving alias response is refused by this example.

## Failure to preserve

A fallback such as answer.injection?.noul ?? 0 turns missing data into evidence for no injection. The missing-answer test exists to prevent that convenient-looking but unsafe default.

## Checkpoint

Run the matching tests, inspect the gate reasons and restore the original. Do not tune on held-out cases or enable paid calls.
