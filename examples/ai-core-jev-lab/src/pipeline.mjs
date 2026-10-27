import {validateTicket,parseJev,parseBaseline,probability} from './contracts.mjs';
export function validatePolicy(policy) {
  probability(policy.routeConfidence,'policy routeConfidence');probability(policy.humanNoMax,'policy humanNoMax');
  if(policy.humanNoMax>=0.5||typeof policy.fallbackOnLowConfidence!=='boolean')throw new Error('invalid abstention policy');return policy;
}
export async function decide(input,{mode='hybrid',providers,policy}) {
  const ticket=validateTicket(input);validatePolicy(policy);
  if(!['baseline','jev','hybrid'].includes(mode))throw new Error('invalid mode');
  const attempts=[];let decision=null,source=null,reason='not_evaluated';
  async function obtain(kind,parse) {
    try {const result=await providers[kind](ticket);attempts.push(result.attempt);source=kind;return parse(result.value);}
    catch(error) {
      if(attempts.at(-1)?.provider!==kind)attempts.push({provider:kind,mode:'error',usage:null,wallMs:null,scenarioLatencyMs:null,httpAttempts:null,costComplete:false});
      reason=`${kind}_failed_validation_or_call`;return null;
    }
  }
  if(mode==='baseline')decision=await obtain('baseline',parseBaseline);
  else {
    decision=await obtain('jev',parseJev);
    if(decision&&decision.wantsHuman>policy.humanNoMax)reason='human_request_or_uncertainty';
    else if(!decision||decision.confidence<policy.routeConfidence) {
      const humanProbability=decision?.wantsHuman;
      if(mode==='hybrid'&&policy.fallbackOnLowConfidence) {
        const fallback=await obtain('baseline',parseBaseline);
        decision=fallback?{...fallback,wantsHuman:Math.max(fallback.wantsHuman,humanProbability??0)}:null;
      } else reason='low_route_confidence';
    }
  }
  const auto=!!decision&&decision.wantsHuman<=policy.humanNoMax&&(source==='baseline'||decision.confidence>=policy.routeConfidence);
  if(auto)reason=source==='baseline'?'validated_baseline_proposal':'validated_jev_proposal';
  else if(decision?.wantsHuman>policy.humanNoMax)reason='human_request_or_uncertainty';
  return {ticketId:ticket.id,status:auto?'proposed':'needs_review',reason,source,decision,attempts,action:auto?{kind:'route_ticket',ticketId:ticket.id,queue:decision.route}:null};
}
