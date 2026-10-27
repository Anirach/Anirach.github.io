# Exercise5: Put Policy Before Confidence

Companion: https://github.com/Anirach/ai-core-functional-tutorial. Work in a disposable copy.

## Goal

Add a table-driven test for send_reply, refund and delete_account. All must reject before a provider runs. Do not add those actions to the allowlist just to make an example look successful.

เพิ่ม table-driven test สำหรับ send_reply, refund และ delete_account ทุกตัวต้อง reject ก่อน provider อย่าเพิ่มสิทธิ์เหล่านี้เพื่อให้ตัวอย่างดูสำเร็จ

## Files

- `src/policy.mjs`
- `test/`

## Reference commands

```sh
node src/cli.mjs policy --case V001
node src/cli.mjs policy --case V004
node src/cli.mjs run --case V004
node --test --test-reporter=spec test/gates.test.mjs
```

## Expected reference behavior

Policy V001 returns accept; V004 returns reject with action_not_authorized. Full V004 has calls0 and externalEffects0. The quality hard-failure test also rejects despite high rubric values.

## Failure to preserve

Checking only the input action is insufficient: a generated object can change action. The output-side guard is a distinct hard check. Removing it is a regression even if every current happy-path fixture asks only for drafts.

## Checkpoint

Run the matching tests, inspect the gate reasons and restore the original. Do not tune on held-out cases or enable paid calls.
