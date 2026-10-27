# Exercise7: Validate Every Output Shape

Companion: https://github.com/Anirach/ai-core-functional-tutorial. Work in a disposable copy.

## Goal

In a disposable test, keep action draft_reply but remove citations, then add a nonexistent fact ID. Both should revise. Now change action to send_reply and verify the result is reject regardless of text quality.

ในสำเนา test ให้ action ยังเป็น draft_reply แต่ลบ citations แล้วลองใส่ fact ID ที่ไม่มี ทั้งคู่ควร revise จากนั้นเปลี่ยนเป็น send_reply ให้ reject ไม่ว่าข้อความจะดีเพียงใด

## Files

- `src/output.mjs`
- `test/`

## Reference commands

```sh
node src/cli.mjs output --case V001
node src/cli.mjs output --case V006
node src/cli.mjs run --case V006
node --test --test-reporter=spec test/gates.test.mjs
```

## Expected reference behavior

V001 output accepts shape. V006 output returns revise; the full run records a revision and ends with an accepted Thai template artifact. Output action send_reply still rejects and cannot be repaired into permission.

## Failure to preserve

Attaching a real citation to a fabricated claim is not caught by membership validation. Do not report output_code accept as factual correctness; the next lesson checks content against the source text.

## Checkpoint

Run the matching tests, inspect the gate reasons and restore the original. Do not tune on held-out cases or enable paid calls.
