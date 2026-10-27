import test from 'node:test';import assert from 'node:assert/strict';import {mkdtemp,rm} from 'node:fs/promises';import {tmpdir} from 'node:os';import {join} from 'node:path';import {approvalKey,effectGuard,simulate} from '../src/effects.mjs';
const proposal=()=>({status:'proposed',ticketId:'T-001',action:{kind:'route_ticket',ticketId:'T-001',queue:'billing'}});
const context=(p,approved=false)=>({knownIds:new Set(['T-001']),release:'r1',approval:approved?{key:approvalKey(p.action,'r1'),approved:true,reviewer:'demo-reviewer'}:null});
test('no approval no effect',()=>{const p=proposal();assert.equal(effectGuard(p,context(p)).allow,false)});
test('separate matching approval',()=>{const p=proposal();assert.equal(effectGuard(p,context(p,true)).allow,true)});
test('changed queue invalidates approval',()=>{const p=proposal(),c=context(p,true);p.action.queue='technical';assert.equal(effectGuard(p,c).allow,false)});
test('high confidence does not authorize refund',()=>{const p=proposal();p.action.kind='refund';p.confidence=1;assert.equal(effectGuard(p,context(p,true)).allow,false)});
test('unknown ticket denied',()=>{const p=proposal();p.action.ticketId='T-999';assert.equal(effectGuard(p,context(p,true)).allow,false)});
test('idempotent serial ledger',async()=>{const dir=await mkdtemp(join(tmpdir(),'jev-lab-'));try{const p=proposal(),c=context(p,true),ledger=join(dir,'ledger.json');assert.equal((await simulate(p,c,ledger)).status,'simulated');assert.equal((await simulate(p,c,ledger)).status,'duplicate')}finally{await rm(dir,{recursive:true})}});
