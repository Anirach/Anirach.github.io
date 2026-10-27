import {gate} from './contracts.mjs';
export function semanticInput(d,p) {
  if(d.injection>=p.yesMin) return gate('reject',['semantic_injection']);
  if(d.injection>p.noMax||d.purpose.confidence<p.choiceMin)
    return gate('human_review',['uncertain_input']);
  if(d.purpose.choice==='account_action') return gate('reject',['semantic_scope']);
  if(d.purpose.choice!=='how_to') return gate('human_review',['unknown_purpose']);
  return gate('accept');
}
export function semanticOutput(d,p) {
  if(d.hiddenInstructions>=p.yesMin) return gate('reject',['self_advocating_candidate']);
  if(d.hiddenInstructions>p.noMax) return gate('human_review',['uncertain_candidate_instructions']);
  if(d.grounded<=p.noMax) return gate('revise',['unsupported_claim']);
  if(d.grounded<p.yesMin) return gate('human_review',['uncertain_grounding']);
  return gate('accept');
}
