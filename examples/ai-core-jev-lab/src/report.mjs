import {readFile} from 'node:fs/promises';
import {createHash,randomUUID} from 'node:crypto';
import {summarize} from './metrics.mjs';

// Fixed local artifacts only: never serialize the environment or API credentials.
export async function auditContext() {
  const paths=['config/release.json','config/policy.json','config/prices.example.json',
    'data/tickets.json','data/predictions.mock.json','src/questions.mjs',
    'src/contracts.mjs','src/providers.mjs','src/pipeline.mjs','src/metrics.mjs',
    'src/report.mjs','src/cli.mjs','package.json'];
  const hashes={};
  for(const path of paths) hashes[path]=createHash('sha256')
    .update(await readFile(new URL('../'+path,import.meta.url))).digest('hex');
  const release=JSON.parse(await readFile(new URL('../config/release.json',import.meta.url),'utf8'));
  return {runId:randomUUID(),createdAt:new Date().toISOString(),release,
    node:process.version,sourceSHA256:hashes,
    evidence:'Authored synthetic fixtures, not an untouched blind study or live Jev benchmark.'};
}

export function evaluationRecord(rows,prices,{mode,split,policy,context}) {
  const languages=[...new Set(rows.map(r=>r.ticket.language))].sort();
  return {mode,split,context,policy:{...policy},priceAssumptions:{...prices},
    summary:summarize(rows,prices),
    languageSlices:Object.fromEntries(languages.map(language=>[language,
      summarize(rows.filter(r=>r.ticket.language===language),prices)])),
    // Gold labels are attached by the evaluator AFTER inference, never in state.
    cases:rows.map(({ticket,result})=>({ticket:{...ticket},result,
      routeCorrect:result.decision?result.decision.route===ticket.goldRoute:null,
      successfulAutomaticProposal:result.status==='proposed'&&
        result.decision?.route===ticket.goldRoute&&!ticket.goldHuman}))};
}
