export const QUEUES = Object.freeze(['billing', 'technical', 'other']);
export function probability(value, name) {
  if (typeof value !== 'number' || !Number.isFinite(value) || value < 0 || value > 1)
    throw new Error(`invalid ${name}: expected a finite number in [0,1]`);
  return value;
}
export function validateTicket(value) {
  if (!value || typeof value.id !== 'string' || !/^T-\d{3}$/.test(value.id)) throw new Error('invalid ticket id');
  if (typeof value.text !== 'string' || !value.text.trim() || value.text.length > 8000) throw new Error('invalid ticket text');
  return Object.freeze({id:value.id, text:value.text, language:value.language ?? 'en'});
}
export function parseJev(response) {
  if (!response || response.model !== 'jev-1.13.0') throw new Error('unexpected or missing pinned model');
  const route = response.answers?.route, human = response.answers?.wantsHuman;
  if (route?.type !== 'choice' || !QUEUES.includes(route.choice)) throw new Error('invalid route label/type');
  const confidence = probability(route.confidence, 'choice confidence');
  const probabilities = route.probabilities;
  if (!probabilities || Object.keys(probabilities).sort().join() !== [...QUEUES].sort().join()) throw new Error('incomplete option distribution');
  const values = QUEUES.map(k => probability(probabilities[k], `probability ${k}`));
  if (Math.abs(values.reduce((a,b)=>a+b,0)-1) > 1e-5) throw new Error('probabilities do not sum to one');
  if (probabilities[route.choice] + 1e-8 < Math.max(...values)) throw new Error('selected choice is not maximal');
  const expected=(Math.max(...values)-1/QUEUES.length)/(1-1/QUEUES.length);
  if(Math.abs(confidence-expected)>1e-5)throw new Error('inconsistent Choice confidence');
  if (human?.type !== 'noul') throw new Error('missing Noul answer');
  return Object.freeze({route:route.choice, confidence, probabilities:{...probabilities}, wantsHuman:probability(human.noul,'Noul')});
}
export function parseBaseline(raw) {
  const value=JSON.parse(raw);
  if (!QUEUES.includes(value.route) || typeof value.wantsHuman !== 'boolean') throw new Error('invalid baseline schema');
  return Object.freeze({route:value.route,wantsHuman:value.wantsHuman?1:0,confidence:null,probabilities:null});
}
export function tokenUsage(response) {
  const input=response?.usage?.input_tokens, output=response?.usage?.output_tokens;
  const valid=x=>Number.isSafeInteger(x)&&x>=0;
  return valid(input)&&valid(output) ? {input,output} : null;
}
