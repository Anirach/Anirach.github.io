import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {checkInput} from './input.mjs';
import {lessonRequest,lessonJudgment} from './questions.mjs';
import {parseDecision} from './contracts.mjs';
import {semanticInput,semanticOutput} from './semantic.mjs';
import {authorizeInput} from './policy.mjs';
import {checkOutput} from './output.mjs';
import {qualityGate} from './quality.mjs';
import {traditionalReply} from './generation.mjs';
import {fixtureProvider} from './fixtures.mjs';
import {runPipeline} from './pipeline.mjs';
import {evaluate,releaseGate,summarize} from './evaluation.mjs';
const args=process.argv.slice(2),command=args[0]??'help';
const opt=(k,d)=>{const i=args.indexOf('--'+k);return i<0?d:args[i+1]};
const load=async p=>JSON.parse(await readFile(new URL('../'+p,import.meta.url),'utf8'));
const cases=await load('data/cases.json'),facts=await load('data/facts.json'),basePolicy=await load('config/policy.json'),prices=await load('config/prices.json');
const policy={...basePolicy,maxCalls:Number(opt('max-calls',basePolicy.maxCalls)),timeoutMs:Number(opt('timeout-ms',basePolicy.timeoutMs))};
const emit=x=>console.log(JSON.stringify(x,null,2));
try {
  if(args.includes('--live'))throw new Error('CLI is offline-only; optional live adapter is not enabled here');
  const item=cases.find(c=>c.id===opt('case','V001'));if(!item)throw new Error('unknown case');
  const provider=await fixtureProvider(item.id);
  const run=()=>runPipeline(item.input,{provider,facts,policy});
  if(command==='doctor') {
    const [major,minor]=process.versions.node.split('.').map(Number);if(major<22||(major===22&&minor<18))throw new Error('Node22.18+ required');
    emit({node:process.version,cases:cases.length,mode:'OFFLINE FIXTURES',sdkRequired:false,paidCalls:0,publicCompanion:'https://github.com/Anirach/ai-core-functional-tutorial'});
  } else if(command==='compare')emit({evidence:'OFFLINE, NOT A PERFORMANCE BENCHMARK',traditional:traditionalReply(item.input,facts),guarded:await run()});
  else if(command==='input')emit(checkInput(item.input));
  else if(command==='request')emit(await lessonRequest(opt('stage','input'),item.input,facts,provider));
  else if(command==='policy')emit(authorizeInput(item.input));
  else if(command==='output') {const raw=await provider('generate',{});emit(checkOutput(raw.value,item.input,facts))}
  else if(command==='judge') {const stage=opt('stage','input');const r=await lessonJudgment(stage,item.input,facts,provider);const d=parseDecision(stage,r.value);emit(stage==='input'?semanticInput(d,policy):stage==='output'?semanticOutput(d,policy):qualityGate(d,policy));}
  else if(command==='run')emit({evidence:'OFFLINE AUTHORED FIXTURES — NOT LIVE JEV',result:await run()});
  else if(command==='cost')emit({evidence:'FICTIONAL single-case accounting, not real operating cost',summary:summarize([{case:item,result:await run()}],prices)});
  else if(command==='evaluate'||command==='release') {
    const report=await evaluate(opt('split','heldout'),{policy,facts,prices,cases});
    if(args.includes('--save')){await mkdir('out',{recursive:true});await writeFile('out/'+report.split+'.json',JSON.stringify(report,null,2)+'\n')}
    if(command==='release') {
      const gate=releaseGate(report);emit({gate,report});
      if(gate.state!=='accept')process.exitCode=2;
    } else emit(report);
  } else if(command==='tune') {
    if(opt('split','validation')!=='validation')throw new Error('threshold tuning is validation-only');
    const results=[];for(const min of [.75,.8,.9]){const report=await evaluate('validation',{policy:{...policy,yesMin:min},facts,prices,cases});results.push({yesMin:min,summary:report.summary})}
    emit({evidence:'Synthetic validation workflow only; thresholds are unvalidated teaching parameters',split:'validation',results});
  } else emit({commands:['doctor','compare','input --case V002','request --stage input','policy --case V004','judge --stage input --case V005','output --case V006','judge --stage output --case V007','judge --stage quality --case V008','run --case V009','evaluate --split heldout --save','release --split heldout'],notice:'Offline CLI. Companion: https://github.com/Anirach/ai-core-functional-tutorial'});
} catch(e){console.error(JSON.stringify({state:'human_review',error:e.message}));process.exitCode=1}
