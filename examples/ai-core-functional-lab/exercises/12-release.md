# Exercise12: Compose the Pipeline and Release Gate

Companion: https://github.com/Anirach/ai-core-functional-tutorial. Work in a disposable copy.

## Goal

Draft a release record for a hypothetical fact change. Specify what must be revalidated and how you would roll back. Keep the original held-out report unchanged and create a new validation version before considering another candidate.

เขียน release record สำหรับการเปลี่ยน fact สมมติ ระบุสิ่งที่ต้องตรวจซ้ำกับวิธี rollback เก็บ held-out report เดิมไม่แก้ แล้วสร้าง validation รุ่นใหม่ก่อนพิจารณา candidate ถัดไป

## Files

- `src/pipeline.mjs`
- `test/`

## Reference commands

```sh
node src/cli.mjs run --case V001
node src/cli.mjs run --case V008
node src/cli.mjs release --split heldout
node --test --test-reporter=spec
```

## Expected reference behavior

V001 accepts an artifact; V008 reviews after two drafts; held-out release rejects with heldout_false_accepts. The full suite should pass because it verifies those specified behaviors, including refusal. No deployment or message sending is implemented by the lab. The release command exits2 by design; the complete passing test suite exits0. Exit1 means a command/evaluator error.

## Failure to preserve

A team may mistake all tests pass for ready to release. Here a deliberately weak semantic fixture passes its runtime gates but fails the held-out release criterion. The release rejection is the intended educational result, not a broken test to delete.

## Checkpoint

Run the matching tests, inspect the gate reasons and restore the original. Do not tune on held-out cases or enable paid calls.
