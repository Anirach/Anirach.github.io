import {readFile,writeFile,mkdir} from 'node:fs/promises';import {performance} from 'node:perf_hooks';
import {fixtureProviders,liveJev} from './providers.mjs';import {validateTicket} from './contracts.mjs';import {requestShape} from './questions.mjs';import {decide} from './pipeline.mjs';import {auditContext,evaluationRecord} from './report.mjs';import {approvalKey,simulate} from './effects.mjs';
const args=process.argv.slice(2),command=args[0]??'help';
const option=(name,fallback)=>{const i=args.indexOf('--'+name);return i<0?fallback:args[i+1]};
const load=async path=>JSON.parse(await readFile(new URL('../'+path,import.meta.url),'utf8')),emit=value=>console.log(JSON.stringify(value,null,2));
const tickets=await load('data/tickets.json'),policy=await load('config/policy.json'),prices=await load('config/prices.example.json'),providers=await fixtureProviders(),context=await auditContext();
async function evaluate(mode,split,p=policy){const rows=[];for(const ticket of tickets.filter(t=>t.split===split))rows.push({ticket,result:await decide(ticket,{mode,providers,policy:p})});return evaluationRecord(rows,prices,{mode,split,policy:p,context})}
try {
  if(args.includes('--live')&&command!=='demo')throw new Error('--live is restricted to one-ticket demo; bulk paid evaluation is not enabled');
  const ticket=tickets.find(t=>t.id===option('ticket','T-001'));
  if(command==='doctor') {
    const [major,minor]=process.versions.node.split('.').map(Number);if(major<22||(major===22&&minor<18))throw new Error('Node 22.18+ required');
    tickets.forEach(validateTicket);emit({node:process.version,tickets:tickets.length,default:'MOCK',sdkRequiredForOffline:false,paidCalls:0});
  } else if(command==='request'){if(!ticket)throw new Error('unknown ticket');emit(requestShape(ticket))}
  else if(command==='demo') {
    if(!ticket)throw new Error('unknown ticket');const live=args.includes('--live');
    const ps=live?{jev:t=>liveJev(t,{live:true}),baseline:async()=>{throw new Error('live generative fallback not configured')}}:providers;
    const result=await decide(ticket,{mode:live?'jev':option('mode','hybrid'),providers:ps,policy});
    emit({evidence:live?'LIVE CALL PATH: not run by the author; no effect execution':'OFFLINE MOCK — NOT JEV INFERENCE',result});
  } else if(command==='evaluate') {
    const split=option('split','test');if(!['validation','test','attack'].includes(split))throw new Error('invalid split');
    const started=performance.now(),results=[];for(const mode of ['baseline','jev','hybrid'])results.push(await evaluate(mode,split));
    const report={context,notice:'FICTIONAL FIXTURE COMPARISON. No claim about real Jev performance, accuracy, calibration or savings.',harnessWallMs:performance.now()-started,results};
    if(args.includes('--save')){await mkdir('out',{recursive:true});await writeFile(`out/${split}.json`,JSON.stringify(report,null,2)+'\n')}emit(report);
  } else if(command==='sweep') {const results=[];for(const threshold of [0.4,0.55,0.7,0.85,0.95])results.push(await evaluate('hybrid','validation',{...policy,routeConfidence:threshold}));emit({context,notice:'Validation only. Predeclare constraints; do not tune on the held-out test set.',results})}
  else if(command==='actions') {
    if(!ticket)throw new Error('unknown ticket');const result=await decide(ticket,{mode:'hybrid',providers,policy}),release='draft-offline-v1';
    if(!result.action)emit({status:'needs_review',reason:result.reason});else {const approval=args.includes('--approve')?{key:approvalKey(result.action,release),reviewer:'demo-reviewer',approved:true}:null;emit(await simulate(result,{knownIds:new Set(tickets.map(t=>t.id)),approval,release},option('ledger','out/effects.json')))}
  } else emit({commands:['doctor','request --ticket T-001','demo --mode baseline','demo --mode hybrid','evaluate --split validation --save','sweep','evaluate --split test --save','evaluate --split attack','actions --ticket T-001','actions --ticket T-001 --approve','demo --ticket T-001 --live'],note:'Default offline; no credentials, SDK installation or network required.'});
} catch(error){console.error(JSON.stringify({status:'needs_review',error:error.message}));process.exitCode=1}
