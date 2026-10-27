import test from 'node:test';import assert from 'node:assert/strict';import {liveDecision} from '../src/live.mjs';
test('optional live adapter refuses without opt-in before fetch/key access',async()=>{let calls=0;const previous=globalThis.fetch;globalThis.fetch=async()=>calls++;try{await assert.rejects(()=>liveDecision('input',{}),/opt-in/);assert.equal(calls,0)}finally{globalThis.fetch=previous}});
test('Jev generator route is unavailable before credentials',async()=>await assert.rejects(()=>liveDecision('generate',{}, {live:true}),/does not generate/));
test('moving model alias refused before credentials',async()=>await assert.rejects(()=>liveDecision('input',{model:'jev-latest'}, {live:true}),/pinned model/));
