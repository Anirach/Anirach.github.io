# Exercise4: Ask Jev About Input Meaning

Companion: https://github.com/Anirach/ai-core-functional-tutorial. Work in a disposable copy.

## Goal

Change only the instruction wording in a disposable copy and print the request diff. The fixture answer should stay unchanged. Describe the fresh labeled validation data needed before believing a real semantic improvement.

เปลี่ยนถ้อยคำ instruction จุดเดียวในสำเนาทดลองแล้วดู request diff คำตอบ fixture ควรเหมือนเดิม อธิบายว่าต้องมีข้อมูล validation ที่ติดป้ายใหม่อย่างไรก่อนเชื่อว่าความหมายดีขึ้นจริง

## Files

- `src/semantic.mjs`
- `test/`

## Reference commands

```sh
node src/cli.mjs request --stage input --case V001
node src/cli.mjs judge --stage input --case V005
node src/cli.mjs run --case A001
node --test --test-reporter=spec test/gates.test.mjs
```

## Expected reference behavior

V005 reviews; A001 rejects with semantic_injection and stops before generation. The request shows model jev-1.14.0 and two answer IDs. All numbers are authored fixtures, not captured live API observations.

## Failure to preserve

If a developer maps every purpose other than account_action to how_to, ambiguous requests become automatic drafts. The explicit other branch and uncertainty tests prevent that accidental broadening of scope.

## Checkpoint

Run the matching tests, inspect the gate reasons and restore the original. Do not tune on held-out cases or enable paid calls.
