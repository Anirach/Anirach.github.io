export class BudgetError extends Error {constructor(code){super(code);this.code=code}}
export async function timed(run,{signal,timeoutMs}) {
  if(signal?.aborted) throw new BudgetError('cancelled');
  const controller=new AbortController();
  let timer,listener;
  const stop=new Promise((_,reject)=>{
    timer=setTimeout(()=>{controller.abort();reject(new BudgetError('timeout'))},timeoutMs);
    listener=()=>{controller.abort();reject(new BudgetError('cancelled'))};
    signal?.addEventListener('abort',listener,{once:true});
  });
  try {return await Promise.race([Promise.resolve().then(()=>run(controller.signal)),stop])}
  finally {clearTimeout(timer);signal?.removeEventListener('abort',listener)}
}
export class CallBudget {
  constructor(policy,{signal}={}){this.policy=policy;this.signal=signal;this.attempts=[];this.used=0}
  async call(stage,request,provider) {
    for(let retry=0;retry<=this.policy.transportRetries;retry++) {
      if(this.signal?.aborted) throw new BudgetError('cancelled');
      if(this.used>=this.policy.maxCalls) throw new BudgetError('call_budget_exhausted');
      this.used++;
      const attempt={stage,transportAttempt:retry+1,evidence:'OFFLINE AUTHORED FIXTURE',usage:null,scenarioMs:null,status:'started'};
      this.attempts.push(attempt);
      try {
        const r=await timed(s=>provider(stage,request,{signal:s}),{signal:this.signal,timeoutMs:this.policy.timeoutMs});
        if(!r||!Object.hasOwn(r,'value')) throw new BudgetError('malformed_adapter');
        const u=r.usage;
        attempt.usage=u&&Number.isSafeInteger(u.input)&&u.input>=0&&Number.isSafeInteger(u.output)&&u.output>=0?{...u}:null;
        attempt.scenarioMs=Number.isFinite(r.scenarioMs)&&r.scenarioMs>=0?r.scenarioMs:null;
        attempt.evidence=r.evidence;attempt.value=structuredClone(r.value);attempt.returnedModel=r.value?.model??null;attempt.status='returned';return r.value;
      } catch(e) {
        attempt.status=e.code??'provider_error';
        if(e.code!=='E_TRANSIENT'||retry===this.policy.transportRetries) throw e;
      }
    }
  }
}
