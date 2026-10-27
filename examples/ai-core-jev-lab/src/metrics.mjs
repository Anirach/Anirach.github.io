export function percentile(values,p) {if(!values.length)return null;const s=[...values].sort((a,b)=>a-b);return s[Math.max(0,Math.ceil(p*s.length)-1)];}
export function money(attempt,prices) {
  if(!attempt.usage||!attempt.costComplete)return null;const p=attempt.provider==='jev'?'jev':'baseline';
  return (attempt.usage.input*prices[p+'InputPerMillionUSD']+attempt.usage.output*prices[p+'OutputPerMillionUSD'])/1e6;
}
export function summarize(rows,prices) {
  const n=rows.length,auto=rows.filter(r=>r.result.status==='proposed');
  const correct=r=>r.result.decision?.route===r.ticket.goldRoute,success=r=>correct(r)&&!r.ticket.goldHuman;
  const successful=auto.filter(success).length,valid=rows.filter(r=>r.result.decision),human=rows.filter(r=>r.ticket.goldHuman);
  const costs=rows.flatMap(r=>r.result.attempts).map(a=>money(a,prices));
  const reviews=n-auto.length,wrongAuto=auto.length-successful;
  const knownInferenceUSD=costs.reduce((s,c)=>s+(c??0),0);
  const modeledOverheadUSD=n*prices.infrastructurePerTaskUSD+reviews*prices.assumedReviewSeconds/3600*prices.reviewHourlyUSD+wrongAuto*prices.reworkPerWrongAutoTaskUSD;
  const complete=costs.every(c=>c!==null);
  const latencies=rows.map(r=>{const xs=r.result.attempts.map(a=>a.scenarioLatencyMs);return xs.every(Number.isFinite)?xs.reduce((a,b)=>a+b,0):null;});
  const calibration=rows.filter(r=>r.result.decision?.probabilities),bins=[];
  for(let k=0;k<5;k++) {
    const members=calibration.filter(r=>Math.min(4,Math.floor(r.result.decision.probabilities[r.result.decision.route]*5))===k);
    if(members.length)bins.push({n:members.length,meanTopProbability:members.reduce((s,r)=>s+r.result.decision.probabilities[r.result.decision.route],0)/members.length,accuracy:members.filter(correct).length/members.length});
  }
  const ece=calibration.length?bins.reduce((s,b)=>s+b.n/calibration.length*Math.abs(b.meanTopProbability-b.accuracy),0):null;
  const ratio=(a,b)=>b?a/b:null;
  return {evidence:'OFFLINE FIXTURE SIMULATION — NOT MEASURED JEV PERFORMANCE OR SAVINGS',n,
    rawRouteAccuracy:ratio(valid.filter(correct).length,valid.length),coverage:ratio(auto.length,n),selectiveAccuracy:ratio(successful,auto.length),abstentionRate:ratio(reviews,n),
    humanRequestMissRate:ratio(human.filter(r=>r.result.status==='proposed').length,human.length),fallbackRate:ratio(rows.filter(r=>r.result.attempts.some(a=>a.provider==='baseline')&&r.result.attempts.some(a=>a.provider==='jev')).length,n),
    successfulAutomatedTasks:successful,unresolvedReviewTasks:reviews,
    latency:{label:'fictional per-attempt scenario milliseconds, summed for sequential fallback',p50:percentile(latencies.filter(Number.isFinite),0.5),p95:percentile(latencies.filter(Number.isFinite),0.95)},
    calibration:{metric:'5-bin ECE of selected-option probability; not Choice confidence',n:calibration.length,ece,bins,note:'Synthetic cases only; no production calibration claim.'},
    cost:{currency:'USD',knownInferenceUSD,modeledOverheadUSD,allAttemptsKnown:complete,modeledTotalUSD:complete?knownInferenceUSD+modeledOverheadUSD:null,
      costPerSuccessfulTaskUSD:complete&&successful?(knownInferenceUSD+modeledOverheadUSD)/successful:null,
      denominator:'correct automatic routing tasks that did not ignore a human request; reviews unresolved',note:'All usage/latencies/review/rework inputs are scenario fixtures. Unknown usage or hidden retries makes total unknown.'}};
}
