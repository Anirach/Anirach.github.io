# Exercise3: Check Inputs with Ordinary Code

Companion: https://github.com/Anirach/ai-core-functional-tutorial. Work in a disposable copy.

## Goal

Add a test at exactly 2000 code units and another at 2001. Then add an unknown property to an otherwise valid record. Keep these as code tests rather than asking Jev to count or inspect schema.

เพิ่ม test ที่ 2000 code units กับ 2001 แล้วเพิ่ม property ที่ไม่รู้จักใน record ที่เหลือถูกต้อง ให้เป็น code tests ไม่ต้องถาม Jev ให้นับหรือตรวจ schema

## Files

- `src/input.mjs`
- `test/`

## Reference commands

```sh
node src/cli.mjs input --case V001
node src/cli.mjs input --case V002
node src/cli.mjs input --case V003
node --test --test-reporter=spec test/contracts.test.mjs
```

## Expected reference behavior

V001 accepts shape; V002 rejects invalid_request_size; V003 rejects known_injection_pattern. Pipeline tests confirm these code-level refusals make no provider calls. No model judgment is needed to establish those particular properties.

## Failure to preserve

A permissive coercion may turn an array or number into text and allow later semantic work. That hides a caller bug and changes the test population. Refuse the malformed representation explicitly instead.

## Checkpoint

Run the matching tests, inspect the gate reasons and restore the original. Do not tune on held-out cases or enable paid calls.
