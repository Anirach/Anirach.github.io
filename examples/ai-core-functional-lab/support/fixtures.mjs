import {readFile} from 'node:fs/promises';
import {fixtureProvider} from '../src/fixtures.mjs';
import {runPipeline} from '../src/pipeline.mjs';
export const load=async p=>JSON.parse(await readFile(new URL('../'+p,import.meta.url),'utf8'));
export const cases=await load('data/cases.json'),facts=await load('data/facts.json'),policy=await load('config/policy.json'),prices=await load('config/prices.json'),mock=await load('data/mock.json');
export const item=id=>structuredClone(cases.find(c=>c.id===id));
export const run=async(id,p={})=>runPipeline(item(id).input,{provider:await fixtureProvider(id),facts,policy:{...policy,...p}});
