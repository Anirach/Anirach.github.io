import {readFile} from 'node:fs/promises';
import {performance} from 'node:perf_hooks';
import {requestShape,ROUTES,ROUTE_QUESTION,HUMAN_QUESTION} from './questions.mjs';
import {tokenUsage} from './contracts.mjs';
export async function fixtureProviders() {
  const fixtures=JSON.parse(await readFile(new URL('../data/predictions.mock.json',import.meta.url),'utf8'));
  async function call(kind,ticket) {
    const f=fixtures[ticket.id]?.[kind];if(!f)throw new Error('fixture not found');
    return {value:structuredClone(f.value),attempt:{provider:kind,mode:'MOCK / FICTIONAL SCENARIO',usage:f.usage,scenarioLatencyMs:f.scenarioLatencyMs,wallMs:null,httpAttempts:1,costComplete:true}};
  }
  return {jev:t=>call('jev',t),baseline:t=>call('baseline',t)};
}
export async function liveJev(ticket,{live=false}={}) {
  if(!live)throw new Error('Live API requires explicit --live');
  if(!process.env.TYPESAFE_API_KEY)throw new Error('TYPESAFE_API_KEY is not set');
  // Offline mode never resolves the SDK or reads a secret.
  const {choice,noul,TypeSafeClient}=await import('@typesafe-ai/sdk');
  const client=new TypeSafeClient({defaultModel:'jev-1.13.0'});
  const started=performance.now();
  const value=await client.systemOne({state:requestShape(ticket).state,questions:{route:choice(ROUTE_QUESTION,{...ROUTES}),wantsHuman:noul(HUMAN_QUESTION)}});
  return {value,attempt:{provider:'jev',mode:'LIVE / NOT VERIFIED BY THE AUTHOR',usage:tokenUsage(value),wallMs:performance.now()-started,scenarioLatencyMs:null,httpAttempts:null,costComplete:false}};
  // SDK retries may occur internally. No outer retry loop is added. Final
  // response usage alone cannot establish the total bill across failed attempts.
}
