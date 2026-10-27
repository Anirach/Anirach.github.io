# Exercise8: Ground Outputs in Trusted Facts

Companion: https://github.com/Anirach/ai-core-functional-tutorial. Work in a disposable copy.

## Goal

In a disposable copy, replace only the candidate with an unsupported claim while keeping real citation IDs. Observe that canned judgments stay fixed; add a clearly labeled mock response for the teaching path and specify the independent labeling needed for a live test.

ในสำเนาทดลอง เปลี่ยน candidate เป็นข้ออ้างไร้หลักฐานแต่เก็บ citation IDs จริง สังเกตว่า judgment จำลองยังคงเดิม เพิ่ม mock ที่ติดป้ายชัดเพื่อสอนเส้นทาง และระบุการติดป้ายอิสระที่ต้องใช้เมื่อทดสอบ live

## Files

- `src/semantic.mjs`
- `test/`

## Reference commands

```sh
node src/cli.mjs request --stage output --case V001
node src/cli.mjs judge --stage output --case V007
node src/cli.mjs run --case V007
node src/cli.mjs run --case A003
node --test --test-reporter=spec test/gates.test.mjs
node --test --test-reporter=spec test/cli.test.mjs
```

## Expected reference behavior

The direct V007 judge returns revise with unsupported_claim; the full pipeline can accept after bounded fallback. A003 rejects self_advocating_candidate. These fixture observations establish control flow only, not the live Jev1.14 model’s factual accuracy.

## Failure to preserve

A candidate that quotes the right fact ID while claiming a new emailing feature passes structural citations but contradicts source text. A candidate’s own assurance that it is grounded must not become another trusted source.

## Checkpoint

Run the matching tests, inspect the gate reasons and restore the original. Do not tune on held-out cases or enable paid calls.
