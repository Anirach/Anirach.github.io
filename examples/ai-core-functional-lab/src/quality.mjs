import {gate} from './contracts.mjs';
export const RUBRIC=['answersUser','stepsUsable','plainLanguage'];
export function qualityGate(judgments,policy,{hardFailure=false}={}) {
  if(hardFailure) return gate('reject',['hard_constraint_failed']);
  if(RUBRIC.some(k=>typeof judgments?.[k]!=='number'||!Number.isFinite(judgments[k])||judgments[k]<0||judgments[k]>1))
    return gate('human_review',['quality_schema']);
  const low=RUBRIC.filter(k=>judgments[k]<=policy.noMax);
  const uncertain=RUBRIC.filter(k=>judgments[k]>policy.noMax&&judgments[k]<policy.yesMin);
  if(uncertain.length) return gate('human_review',uncertain.map(k=>'uncertain_'+k));
  if(low.length) return gate('revise',low.map(k=>'quality_'+k));
  return gate('accept',['all_rubric_checks_pass']);
}
