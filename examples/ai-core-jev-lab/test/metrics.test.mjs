import test from 'node:test';import assert from 'node:assert/strict';import {percentile,money,summarize} from '../src/metrics.mjs';
const p={jevInputPerMillionUSD:0.042,jevOutputPerMillionUSD:0,baselineInputPerMillionUSD:0.5,baselineOutputPerMillionUSD:2,infrastructurePerTaskUSD:0,reviewHourlyUSD:0,assumedReviewSeconds:0,reworkPerWrongAutoTaskUSD:0};
test('nearest-rank percentiles',()=>{assert.equal(percentile([4,1,3,2],0.5),2);assert.equal(percentile([4,1,3,2],0.95),4)});
test('empty percentile unknown',()=>assert.equal(percentile([],0.95),null));
test('missing usage unknown cost',()=>assert.equal(money({provider:'jev',usage:null,costComplete:true},p),null));
test('unobserved SDK attempts unknown',()=>assert.equal(money({provider:'jev',usage:{input:100,output:0},costComplete:false},p),null));
test('million token arithmetic',()=>assert.equal(money({provider:'jev',usage:{input:1e6,output:4},costComplete:true},p),0.042));
test('no successes is undefined',()=>assert.equal(summarize([],p).cost.costPerSuccessfulTaskUSD,null));
