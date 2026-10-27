import {readFile} from 'node:fs/promises';
export async function fixtureProvider(id) {
  const map=JSON.parse(await readFile(new URL('../data/mock.json',import.meta.url),'utf8'));
  const fixture=map[id];if(!fixture) throw new Error('no fixture for '+id);
  const counters={};
  return async(stage,request,{signal}={})=>{
    const index=counters[stage]??0;counters[stage]=index+1;
    if(signal?.aborted){const e=new Error('cancelled');e.code='cancelled';throw e}
    const fault=fixture.faults?.[stage]?.[index];
    if(fault==='transient'){const e=new Error('simulated transient');e.code='E_TRANSIENT';throw e}
    if(fault==='timeout') return new Promise((_,reject)=>signal.addEventListener('abort',()=>reject(new Error('aborted')),{once:true}));
    if(fault==='malformed') return {unexpected:true};
    const values=fixture[stage],value=values[Math.min(index,values.length-1)];
    return {value:structuredClone(value),usage:fixture.unknownUsage?null:{input:240,output:stage==='generate'?60:8},scenarioMs:stage==='generate'?180:24,evidence:'OFFLINE AUTHORED FIXTURE — NOT MEASURED JEV'};
  };
}
