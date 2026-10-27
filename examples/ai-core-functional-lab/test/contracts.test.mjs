import test from 'node:test';import assert from 'node:assert/strict';
import {parseDecision,probability,gate} from '../src/contracts.mjs';import {checkInput} from '../src/input.mjs';import {mock,item} from '../support/fixtures.mjs';
const valid=()=>structuredClone(mock.V001.input[0]);
test('documented pinned Choice and Noul',()=>assert.equal(parseDecision('input',valid()).purpose.choice,'how_to'));
for(const n of [NaN,Infinity,-Infinity,-.01,1.01,'0.8',null,undefined])test('reject nonprobability '+String(n),()=>assert.throws(()=>probability(n)));
for(const mutate of [v=>delete v.answers.injection,v=>v.answers.purpose.type='score',v=>v.answers.purpose.choice='admin',v=>v.answers.injection.type='choice',v=>v.answers.injection.noul=Infinity,v=>v.model='jev-latest',v=>v.answers.purpose.confidence=.1,v=>v.answers.purpose.probabilities.how_to=.1])
 test('reject altered contract '+mutate.toString(),()=>{const v=valid();mutate(v);assert.throws(()=>parseDecision('input',v))});
test('Noul accepts documented shape without confidence',()=>assert.equal(parseDecision('input',valid()).injection,.01));
test('gate state closed union',()=>assert.throws(()=>gate('execute')));
for(const x of [null,[],{},'raw text',{...item('V001').input,id:'../../secret'},{...item('V001').input,request:''},{...item('V001').input,extra:'override'},{...item('V001').input,request:'x'.repeat(2001)}])
 test('malformed input refused '+JSON.stringify(x).slice(0,40),()=>assert.equal(checkInput(x).state,'reject'));
test('normalization preserves input object',()=>{const x=item('V001').input;x.request='  Cafe\u0301 export  ';const r=checkInput(x);assert.equal(r.value.request,'Café export');assert.ok(x.request.startsWith('  '))});
