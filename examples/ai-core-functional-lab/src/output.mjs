import {gate,plain} from './contracts.mjs';
import {authorizeDraft} from './policy.mjs';
export function checkOutput(raw,input,facts) {
  const permission=authorizeDraft(raw);
  if(permission.state!=='accept') return permission; // Hard failure is never scored away.
  if(!plain(raw)||Object.keys(raw).sort().join()!==['action','citations','language','text'].sort().join())
    return gate('revise',['invalid_output_fields']);
  if(raw.language!==input.language||typeof raw.text!=='string'||raw.text.trim().length<10||raw.text.length>600)
    return gate('revise',['invalid_output_text']);
  const allowed=new Set(facts.facts.map(f=>f.id));
  if(!Array.isArray(raw.citations)||!raw.citations.length
    ||raw.citations.some(x=>typeof x!=='string'||!allowed.has(x))) return gate('revise',['invalid_citation']);
  return gate('accept',[],structuredClone(raw));
}
