import {gate,probability} from './contracts.mjs';
export function validatePolicy(p) {
  probability(p.choiceMin);probability(p.yesMin);probability(p.noMax);
  if(p.noMax>=p.yesMin||p.noMax>=.5||p.yesMin<=.5) throw new Error('invalid uncertainty band');
  for(const k of ['maxCalls','maxDrafts','timeoutMs'])
    if(!Number.isSafeInteger(p[k])||p[k]<1) throw new Error('invalid '+k);
  if(!Number.isSafeInteger(p.transportRetries)||p.transportRetries<0||p.transportRetries>2)
    throw new Error('invalid retry bound');
  if(typeof p.fallback!=='boolean') throw new Error('invalid fallback');
  return p;
}
export function authorizeInput(input) {
  return input.requestedAction==='draft_reply'?gate('accept'):gate('reject',['action_not_authorized']);
}
export function authorizeDraft(draft) {
  return draft?.action==='draft_reply'?gate('accept'):gate('reject',['output_action_not_authorized']);
}
