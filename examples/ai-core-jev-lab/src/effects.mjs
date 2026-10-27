import {createHash} from 'node:crypto';import {readFile,writeFile,mkdir} from 'node:fs/promises';import {dirname} from 'node:path';
import {QUEUES} from './contracts.mjs';
export function approvalKey(action,release) {return createHash('sha256').update(JSON.stringify([release,action.ticketId,action.kind,action.queue])).digest('hex');}
export function effectGuard(proposal,{knownIds,approval,release}) {
  const a=proposal.action;
  if(proposal.status!=='proposed'||!a||a.kind!=='route_ticket')return {allow:false,reason:'unsupported_or_unready'};
  if(!knownIds.has(a.ticketId)||a.ticketId!==proposal.ticketId||!QUEUES.includes(a.queue))return {allow:false,reason:'out_of_scope'};
  const key=approvalKey(a,release);
  if(approval?.key!==key||approval?.reviewer!=='demo-reviewer'||approval?.approved!==true)return {allow:false,reason:'needs_human_approval'};
  return {allow:true,key};
}
export async function simulate(proposal,context,ledger) {
  const gate=effectGuard(proposal,context);if(!gate.allow)return {status:'blocked',reason:gate.reason};
  let rows=[];try{rows=JSON.parse(await readFile(ledger,'utf8'))}catch(e){if(e.code!=='ENOENT')throw e}
  if(rows.some(r=>r.key===gate.key))return {status:'duplicate',key:gate.key};
  rows.push({key:gate.key,release:context.release,...proposal.action,simulation:true});
  await mkdir(dirname(ledger),{recursive:true});await writeFile(ledger,JSON.stringify(rows,null,2)+'\n');return {status:'simulated',key:gate.key};
}
// Teaching ledger: serial, single-process only. Production requires authenticated
// approvals, a transactional unique key and atomic durable writes.
