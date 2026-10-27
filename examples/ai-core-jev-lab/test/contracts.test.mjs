import test from 'node:test';import assert from 'node:assert/strict';import {readFile} from 'node:fs/promises';
import {parseJev,parseBaseline,probability,tokenUsage,validateTicket} from '../src/contracts.mjs';
const f=JSON.parse(await readFile(new URL('../data/predictions.mock.json',import.meta.url),'utf8')),valid=()=>structuredClone(f['T-001'].jev.value);
test('valid pinned Choice and Noul',()=>assert.equal(parseJev(valid()).route,'billing'));
for(const n of [-1,1.1,NaN,Infinity,'0.9',null])test(`reject probability ${String(n)}`,()=>assert.throws(()=>probability(n,'test')));
test('unknown route rejected',()=>{const v=valid();v.answers.route.choice='admin';assert.throws(()=>parseJev(v))});
test('missing Noul rejected',()=>{const v=valid();delete v.answers.wantsHuman;assert.throws(()=>parseJev(v))});
test('Noul needs no confidence',()=>assert.equal(parseJev(valid()).wantsHuman,0.03));
test('incomplete distribution rejected',()=>{const v=valid();delete v.answers.route.probabilities.other;assert.throws(()=>parseJev(v))});
test('bad distribution sum rejected',()=>{const v=valid();v.answers.route.probabilities.other=0.8;assert.throws(()=>parseJev(v))});
test('unpinned response rejected',()=>{const v=valid();v.model='jev-latest';assert.throws(()=>parseJev(v))});
test('malformed baseline rejected',()=>assert.throws(()=>parseBaseline('not JSON')));
test('missing usage stays unknown',()=>assert.equal(tokenUsage({usage:{input_tokens:null,output_tokens:null}}),null));
test('known zero is distinct',()=>assert.deepEqual(tokenUsage({usage:{input_tokens:0,output_tokens:0}}),{input:0,output:0}));
test('IDs cannot be paths',()=>assert.throws(()=>validateTicket({id:'../../secret',text:'x'})));

test('inconsistent confidence rejected',()=>{const v=valid();v.answers.route.confidence=1;assert.throws(()=>parseJev(v))});

test('baseline out-of-set route rejected',()=>assert.throws(()=>parseBaseline(JSON.stringify({route:'admin',wantsHuman:false})),/invalid baseline schema/));
