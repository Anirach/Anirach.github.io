# Exercise1: From Functions to Guarded Workflows

Companion: https://github.com/Anirach/ai-core-functional-tutorial. Work in a disposable copy.

## Goal

In a disposable copy, add a third product fact in both languages and run compare again. The template changes immediately; canned model judgments do not become more intelligent. Restore the reference before continuing.

ในสำเนาทดลอง เพิ่มข้อเท็จจริงข้อที่สามสองภาษาแล้วรัน compare template จะเปลี่ยนทันที แต่คำตัดสินจำลองไม่ได้ฉลาดขึ้น คืนไฟล์ต้นฉบับก่อนตอนถัดไป

## Files

- `src/generation.mjs`
- `test/`

## Reference commands

```sh
node src/cli.mjs doctor
node src/cli.mjs compare --case V001
node src/cli.mjs run --case V004
node --test --test-reporter=spec test/pipeline.test.mjs
```

## Expected reference behavior

doctor reports OFFLINE FIXTURES and paidCalls 0. V001 accepts an artifact after four mock calls. V004 rejects with action_not_authorized and zero calls. These are reproducible fixture behaviors, not measured Jev intelligence or cost savings.

## Failure to preserve

If you return the traditional draft directly from a network endpoint, its well-formed object can hide missing policy and semantic checks. The compare command exposes that difference without claiming the model-based route is universally safer.

## Checkpoint

Run the matching tests, inspect the gate reasons and restore the original. Do not tune on held-out cases or enable paid calls.
