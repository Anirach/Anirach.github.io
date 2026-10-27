# Exercise9: Build a Separate Quality Gate

Companion: https://github.com/Anirach/ai-core-functional-tutorial. Work in a disposable copy.

## Goal

Add a fourth criterion in a disposable copy. Update the question contract, parser, rubric, fixtures and tests together. First make a missing-answer test fail closed; do not merely append a UI label.

เพิ่ม criterion ที่สี่ในสำเนา อัปเดต question contract, parser, rubric, fixtures และ tests พร้อมกัน เริ่มจาก test ฟิลด์ที่หายต้องปิดทาง ไม่ใช่เพิ่มแค่ label บนหน้าจอ

## Files

- `src/quality.mjs`
- `test/`

## Reference commands

```sh
node src/cli.mjs request --stage quality --case V001
node src/cli.mjs judge --stage quality --case V008
node src/cli.mjs run --case V008
node --test --test-reporter=spec test/gates.test.mjs
```

## Expected reference behavior

The direct V008 gate revises; the full workflow reviews after exhausting bounded revisions. The test with a hard failure rejects despite perfect rubric values. These are policy behaviors over mock judgments, not a calibrated quality score for real users.

## Failure to preserve

A weighted mean can accept a draft whose clarity is unusable because factuality is high. In this example the dimensions are separate acceptance conditions. If you intentionally permit tradeoffs, specify and validate them rather than hiding them in arithmetic.

## Checkpoint

Run the matching tests, inspect the gate reasons and restore the original. Do not tune on held-out cases or enable paid calls.
