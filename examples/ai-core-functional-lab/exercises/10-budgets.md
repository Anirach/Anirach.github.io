# Exercise10: Bound Retries, Repairs, and Fallback

Companion: https://github.com/Anirach/ai-core-functional-tutorial. Work in a disposable copy.

## Goal

Set the aggregate call cap to1 and trigger a transient failure in a test. Verify only one provider invocation occurs. Then set an already-aborted signal and verify zero invocations and a human_review result.

ตั้งงบ call รวมเป็น1 แล้วจำลอง transient failure ใน test ต้องเรียก provider เพียงครั้งเดียว จากนั้นส่ง signal ที่ abort แล้ว ต้องไม่เรียกเลยและคืน human_review

## Files

- `src/budget.mjs`
- `test/`

## Reference commands

```sh
node src/cli.mjs run --case V009
node src/cli.mjs run --case V001 --max-calls 3
node src/cli.mjs run --case V007
node --test --test-reporter=spec test/budget.test.mjs
```

## Expected reference behavior

V009 accepts after one counted transport retry. V001 with three calls reviews before quality. V007 shows a revise event followed by deterministic fallback. Failed attempts retain unknown usage, so complete cost may remain unknown despite a final accepted artifact.

## Failure to preserve

Two outer semantic rounds multiplied by three SDK transport attempts can far exceed the calls visible to an application wrapper. This example avoids a hidden SDK layer; adapting it to an SDK requires counting that layer explicitly.

## Checkpoint

Run the matching tests, inspect the gate reasons and restore the original. Do not tune on held-out cases or enable paid calls.
