/** @typedef {'accept'|'reject'|'revise'|'human_review'} GateState */
/** Gate outputs describe artifacts, never permission to execute an external effect. */
export function gate(state, reasons=[], value=null) {
  if(!['accept','reject','revise','human_review'].includes(state)) throw new Error('unknown gate state');
  return {state,reasons,value};
}
export function plain(value) {
  return value!==null && typeof value==='object' && !Array.isArray(value)
    && [Object.prototype,null].includes(Object.getPrototypeOf(value));
}
export function probability(value,name='probability') {
  if(typeof value!=='number'||!Number.isFinite(value)||value<0||value>1)
    throw new Error(`invalid ${name}`);
  return value;
}
export const MODEL='jev-1.14.0';
export const PURPOSES=['how_to','account_action','other'];
export function parseDecision(stage,response) {
  if(!plain(response)||response.model!==MODEL||!plain(response.answers))
    throw new Error('missing answers or wrong pinned model');
  const a=response.answers;
  const names=stage==='input'?['purpose','injection']:stage==='output'
    ?['grounded','hiddenInstructions']:stage==='quality'
    ?['answersUser','stepsUsable','plainLanguage']:null;
  if(!names||Object.keys(a).sort().join()!==[...names].sort().join())
    throw new Error('missing or unexpected answer IDs');
  const out={};
  for(const name of names) {
    const x=a[name];
    if(name==='purpose') {
      if(x?.type!=='choice'||!PURPOSES.includes(x.choice)||!plain(x.probabilities)
        ||Object.keys(x.probabilities).sort().join()!==[...PURPOSES].sort().join())
        throw new Error('invalid Choice label or discriminant');
      const values=PURPOSES.map(k=>probability(x.probabilities[k],k));
      if(Math.abs(values.reduce((s,v)=>s+v,0)-1)>1e-5
        ||x.probabilities[x.choice]+1e-8<Math.max(...values)) throw new Error('invalid distribution');
      const confidence=probability(x.confidence,'confidence');
      if(Math.abs(confidence-(Math.max(...values)-1/3)/(1-1/3))>1e-5)
        throw new Error('inconsistent Choice confidence');
      out.purpose={choice:x.choice,confidence,probabilities:{...x.probabilities}};
    } else {
      if(x?.type!=='noul') throw new Error('wrong Noul discriminant');
      out[name]=probability(x.noul,name); // Noul has no separate confidence field.
    }
  }
  return out;
}
