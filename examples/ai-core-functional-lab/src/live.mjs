import {MODEL} from './contracts.mjs';
/** Optional TEXT-ONLY REST adapter. Not wired into the offline CLI or tests. */
export async function liveDecision(stage,request,{live=false,signal}={}) {
  if(!live) throw new Error('explicit live opt-in required');
  if(stage==='generate') throw new Error('Jev does not generate text; no live generator configured');
  if(request.model!==MODEL) throw new Error('pinned model required');
  const key=process.env.TYPESAFE_API_KEY;
  if(!key) throw new Error('provider environment is not configured');
  // One HTTP attempt, no internal retry stack. Pass through the shared CallBudget.
  const response=await fetch('https://api.typesafe.ai/v1/systemone',{
    method:'POST',headers:{Authorization:'Bearer '+key,'Content-Type':'application/json'},
    body:JSON.stringify(request),signal
  });
  if(!response.ok){const e=new Error('provider_http_'+response.status);if([429,529].includes(response.status))e.code='E_TRANSIENT';throw e}
  const value=await response.json(),u=value.usage;
  return {value,usage:u?{input:u.input_tokens,output:u.output_tokens}:null,scenarioMs:null,evidence:'LIVE PATH UNTESTED; actual billing completeness must be independently checked'};
}
