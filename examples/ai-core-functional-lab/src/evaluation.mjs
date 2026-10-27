import {readFile} from 'node:fs/promises';
import {createHash,randomUUID} from 'node:crypto';
import {performance} from 'node:perf_hooks';
import {runPipeline} from './pipeline.mjs';
import {fixtureProvider} from './fixtures.mjs';
const load=async p=>JSON.parse(await readFile(new URL('../'+p,import.meta.url),'utf8'));
export function percentile(xs,p){if(!xs.length)return null;const s=[...xs].sort((a,b)=>a-b);return s[Math.max(0,Math.ceil(p*s.length)-1)]}
export function summarize(rows,prices) {
  for(const k of ['jevInputPerMillionUSD','jevOutputPerMillionUSD','generatorInputPerMillionUSD','generatorOutputPerMillionUSD','infrastructurePerTaskUSD','reviewSeconds','reviewHourlyUSD','falseAcceptReworkUSD'])
    if(typeof prices[k]!=='number'||!Number.isFinite(prices[k])||prices[k]<0)throw new Error('invalid price '+k);
  const n=rows.length,accepted=rows.filter(r=>r.result.state==='accept');
  const correct=accepted.filter(r=>r.case.acceptable),wrong=accepted.length-correct.length;
  const reviews=rows.filter(r=>r.result.state==='human_review').length;
  const costs=rows.flatMap(r=>r.result.attempts.map(a=>{
    if(!a.usage)return null;
    const prefix=a.stage==='generate'?'generator':'jev';
    return (a.usage.input*prices[prefix+'InputPerMillionUSD']+a.usage.output*prices[prefix+'OutputPerMillionUSD'])/1e6;
  }));
  const knownInferenceUSD=costs.reduce((s,c)=>s+(c??0),0),costComplete=costs.every(c=>c!==null);
  const modeledOverheadUSD=n*prices.infrastructurePerTaskUSD+reviews*prices.reviewSeconds/3600*prices.reviewHourlyUSD+wrong*prices.falseAcceptReworkUSD;
  const times=rows.map(r=>{const xs=r.result.attempts.map(a=>a.scenarioMs);return xs.every(Number.isFinite)?xs.reduce((s,x)=>s+x,0):null});
  const latencyComplete=times.every(Number.isFinite),total=costComplete?knownInferenceUSD+modeledOverheadUSD:null;
  const ratio=(a,b)=>b?a/b:null;
  return {n,accepted:accepted.length,acceptedCorrect:correct.length,falseAccepts:wrong,humanReview:reviews,
    coverage:ratio(accepted.length,n),acceptedPrecision:ratio(correct.length,accepted.length),
    states:Object.fromEntries(['accept','reject','revise','human_review'].map(s=>[s,rows.filter(r=>r.result.state===s).length])),
    transportRetries:rows.reduce((s,r)=>s+r.result.attempts.filter(a=>a.transportAttempt>1).length,0),
    semanticRevisions:rows.reduce((s,r)=>s+r.result.history.filter(g=>g.state==='revise').length,0),
    latency:{evidence:'FICTIONAL scenario milliseconds, not measured inference latency',complete:latencyComplete,p50:latencyComplete?percentile(times,.5):null,p95:latencyComplete?percentile(times,.95):null},
    cost:{evidence:'FICTIONAL usage/generator/review/rework assumptions; Jev unit price dated2026-10-24',complete:costComplete,knownInferenceUSD,modeledOverheadUSD,totalUSD:total,
      perAcceptedUSD:total!==null&&accepted.length?total/accepted.length:null,
      perCorrectAcceptedUSD:total!==null&&correct.length?total/correct.length:null,
      denominator:'accepted artifacts versus fixture-reference acceptable artifacts (authored teaching labels), not completed support resolutions'}};
}
export async function context() {
  const paths=['config/release.json','config/policy.json','config/prices.json','data/cases.json','data/mock.json','data/facts.json',
    ...['contracts','input','policy','questions','semantic','generation','output','quality','budget','fixtures','pipeline','live','evaluation','cli'].map(n=>'src/'+n+'.mjs')];
  const hashes={};for(const p of paths)hashes[p]=createHash('sha256').update(await readFile(new URL('../'+p,import.meta.url))).digest('hex');
  return {runId:randomUUID(),at:new Date().toISOString(),node:process.version,release:await load('config/release.json'),sourceSHA256:hashes};
}
export async function evaluate(split,{policy,facts,prices,cases,signal}={}) {
  if(!['validation','heldout','attack'].includes(split))throw new Error('invalid split');
  const start=performance.now(),rows=[];
  for(const item of cases.filter(c=>c.split===split)) {
    const provider=await fixtureProvider(item.id);
    rows.push({case:structuredClone(item),result:await runPipeline(item.input,{provider,policy,facts,signal})});
  }
  return {evidence:'OFFLINE AUTHORED FIXTURES, NOT LIVE JEV PERFORMANCE',split,context:await context(),policy:{...policy},priceAssumptions:{...prices},trustedFacts:structuredClone(facts),
    summary:summarize(rows,prices),languageSlices:Object.fromEntries([...new Set(rows.map(r=>r.case.input.language))].map(l=>[l,summarize(rows.filter(r=>r.case.input.language===l),prices)])),
    cases:rows,harnessWallMs:performance.now()-start};
}
export function releaseGate(report) {
  if(report?.split!=='heldout')return {state:'reject',reasons:['release_requires_heldout_split']};
  const invalid=releaseMetricErrors(report.summary);
  if(invalid.length)return {state:'reject',reasons:['invalid_release_metrics',...invalid]};
  if(report.summary.falseAccepts)return {state:'reject',reasons:['heldout_false_accepts']};
  if(!report.summary.cost.complete)return {state:'human_review',reasons:['unknown_total_cost']};
  if(report.summary.coverage===null||report.summary.coverage<.5)return {state:'revise',reasons:['coverage_below_teaching_gate']};
  return {state:'accept',reasons:['synthetic_release_checks_only_not_production_approval']};
}

// Validate evidence before comparisons: undefined and NaN must never open a gate.
// This checks metric consistency, not report authenticity or production readiness.
export function releaseMetricErrors(s) {
  const record=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
  if(!record(s))return ['summary_required'];
  const errors=[],add=x=>errors.push(x);
  const count=x=>Number.isSafeInteger(x)&&x>=0;
  const money=x=>typeof x==='number'&&Number.isFinite(x)&&x>=0;
  const close=(a,b)=>Math.abs(a-b)<=1e-9*Math.max(1,Math.abs(a),Math.abs(b));
  const counts=['n','accepted','acceptedCorrect','falseAccepts','humanReview','transportRetries','semanticRevisions'];
  for(const k of counts)if(!count(s[k]))add(k+'_invalid_count');
  if(!count(s.n)||s.n===0)add('nonempty_evaluation_required');
  if(errors.length)return errors;
  const states=['accept','reject','revise','human_review'];
  if(!record(s.states))add('states_required');
  else {
    if(Object.keys(s.states).some(k=>!states.includes(k)))add('unknown_state');
    for(const k of states)if(!count(s.states[k]))add('states_'+k+'_invalid_count');
    if(states.every(k=>count(s.states[k]))&&states.reduce((n,k)=>n+s.states[k],0)!==s.n)add('state_total_mismatch');
    if(s.states.accept!==s.accepted||s.states.human_review!==s.humanReview)add('state_count_mismatch');
  }
  if(['accepted','acceptedCorrect','falseAccepts','humanReview'].some(k=>count(s[k])&&s[k]>s.n))add('count_exceeds_evaluation');
  if(count(s.acceptedCorrect)&&count(s.falseAccepts)&&s.acceptedCorrect+s.falseAccepts!==s.accepted)add('accepted_count_mismatch');
  if(typeof s.coverage!=='number'||!Number.isFinite(s.coverage)||s.coverage<0||s.coverage>1)add('coverage_invalid');
  else if(s.n>0&&!close(s.coverage,s.accepted/s.n))add('coverage_count_mismatch');
  if(s.accepted===0) {if(s.acceptedPrecision!==null)add('empty_precision_must_be_null')}
  else if(typeof s.acceptedPrecision!=='number'||!Number.isFinite(s.acceptedPrecision)||s.acceptedPrecision<0||s.acceptedPrecision>1)add('precision_invalid');
  else if(!close(s.acceptedPrecision,s.acceptedCorrect/s.accepted))add('precision_count_mismatch');
  if(!record(s.latency)||typeof s.latency.complete!=='boolean')add('latency_required');
  else if(s.latency.complete) {
    if(!money(s.latency.p50)||!money(s.latency.p95)||s.latency.p50>s.latency.p95)add('latency_percentiles_invalid');
  } else if(s.latency.p50!==null||s.latency.p95!==null)add('unknown_latency_must_be_null');
  const c=s.cost;
  if(!record(c)||typeof c.complete!=='boolean')add('cost_required');
  else {
    const componentsValid=money(c.knownInferenceUSD)&&money(c.modeledOverheadUSD);
    if(!componentsValid)add('cost_components_invalid');
    if(c.complete) {
      if(!money(c.totalUSD)||!componentsValid||!close(c.totalUSD,c.knownInferenceUSD+c.modeledOverheadUSD))add('cost_total_invalid');
      for(const [k,n] of [['perAcceptedUSD',s.accepted],['perCorrectAcceptedUSD',s.acceptedCorrect]]) {
        if(n===0) {if(c[k]!==null)add(k+'_must_be_null')}
        else if(!money(c[k])||!money(c.totalUSD)||!close(c[k],c.totalUSD/n))add(k+'_invalid');
      }
    } else if(['totalUSD','perAcceptedUSD','perCorrectAcceptedUSD'].some(k=>c[k]!==null))add('unknown_cost_must_be_null');
  }
  return errors;
}
