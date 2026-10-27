import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {lessonRequest,lessonJudgment} from '../src/questions.mjs';
import {fixtureProvider} from '../src/fixtures.mjs';
import {traditionalReply} from '../src/generation.mjs';
import {facts,item} from '../support/fixtures.mjs';
const cli=(...args)=>spawnSync(process.execPath,['src/cli.mjs',...args],{cwd:new URL('..',import.meta.url),encoding:'utf8'});

test('lesson output adapter receives the generated V007 candidate and trusted facts',async()=>{
  const fixture=await fixtureProvider('V007'),seen=[];
  const provider=async(stage,request)=>{seen.push({stage,request:structuredClone(request)});return fixture(stage,request)};
  const input=item('V007').input;
  await lessonJudgment('output',input,facts,provider);
  assert.deepEqual(seen.map(x=>x.stage),['generate','output']);
  const payload=seen[1].request;
  assert.match(payload.state.candidate.text,/email/i);
  assert.notDeepEqual(payload.state.candidate,traditionalReply(input,facts));
  assert.deepEqual(payload.state.candidate,(await (await fixtureProvider('V007'))('generate',{})).value);
  assert.deepEqual(payload.state.trustedFacts,facts);
  assert.ok(!('acceptable' in payload.state));
});
test('quality adapter receives the same first generated candidate rather than a template',async()=>{
  const fixture=await fixtureProvider('V007'),seen=[];
  await lessonJudgment('quality',item('V007').input,facts,async(stage,request)=>{seen.push({stage,request});return fixture(stage,request)});
  assert.deepEqual(seen.map(x=>x.stage),['generate','quality']);
  assert.match(seen[1].request.state.candidate.text,/email/i);
});
test('input lesson does not generate a candidate',async()=>{
  let calls=0;const request=await lessonRequest('input',item('V001').input,facts,async()=>calls++);
  assert.equal(calls,0);assert.ok(!('candidate' in request.state));
});
test('CLI request shows the generator claim that the lesson output judge examines',()=>{
  const result=cli('request','--stage','output','--case','V007');assert.equal(result.status,0);
  assert.match(JSON.parse(result.stdout).state.candidate.text,/email/i);
  const judgment=cli('judge','--stage','output','--case','V007');assert.equal(judgment.status,0);
  assert.deepEqual(JSON.parse(judgment.stdout),{state:'revise',reasons:['unsupported_claim'],value:null});
});
test('held-out release rejection uses exit2 while retaining the complete JSON report',()=>{
  const result=cli('release','--split','heldout');assert.equal(result.status,2,result.stderr);
  const output=JSON.parse(result.stdout);assert.equal(output.gate.state,'reject');
  assert.deepEqual(output.gate.reasons,['heldout_false_accepts']);assert.equal(output.report.cases.length,12);
});
test('non-heldout release cannot succeed in shell automation',()=>{
  const result=cli('release','--split','validation');assert.equal(result.status,2);
  assert.deepEqual(JSON.parse(result.stdout).gate,{state:'reject',reasons:['release_requires_heldout_split']});
});
test('CLI invocation error has exit1, distinct from a computed release refusal',()=>{
  const result=cli('release','--split','unknown');assert.equal(result.status,1);assert.match(result.stderr,/invalid split/);
});
