import {gate,parseDecision} from './contracts.mjs';
import {checkInput} from './input.mjs';
import {authorizeInput,validatePolicy} from './policy.mjs';
import {requestShape} from './questions.mjs';
import {semanticInput,semanticOutput} from './semantic.mjs';
import {checkOutput} from './output.mjs';
import {qualityGate} from './quality.mjs';
import {traditionalReply} from './generation.mjs';
import {CallBudget} from './budget.mjs';
export async function runPipeline(raw,{provider,facts,policy,signal}={}) {
  validatePolicy(policy);
  const budget=new CallBudget(policy,{signal}),history=[];
  const finish=g=>({...g,history,attempts:budget.attempts,calls:budget.used,externalEffects:0});
  const record=(stage,g)=>{history.push({stage,state:g.state,reasons:g.reasons});return g};
  try {
    if(signal?.aborted) return finish(gate('human_review',['cancelled']));
    let g=record('input_code',checkInput(raw));if(g.state!=='accept')return finish(g);
    const input=g.value;
    g=record('authorization',authorizeInput(input));if(g.state!=='accept')return finish(g);
    const judge=async(stage,draft)=>parseDecision(stage,await budget.call(stage,requestShape(stage,input,facts,draft),provider));
    g=record('input_semantic',semanticInput(await judge('input'),policy));if(g.state!=='accept')return finish(g);
    for(let draftNo=1;draftNo<=policy.maxDrafts;draftNo++) {
      const fallback=draftNo>1&&policy.fallback;
      const draft=fallback?traditionalReply(input,facts):await budget.call('generate',{input,facts,draftNo},provider);
      history.push({stage:'generation',draftNo,provider:fallback?'deterministic_template':'mock_generator'});
      g=record('output_code',checkOutput(draft,input,facts));
      if(g.state==='reject')return finish(g);
      if(g.state==='accept') {
        g=record('output_semantic',semanticOutput(await judge('output',draft),policy));
        if(g.state==='reject'||g.state==='human_review')return finish(g);
        if(g.state==='accept') {
          g=record('quality_gate',qualityGate(await judge('quality',draft),policy));
          if(g.state==='accept')return finish(gate('accept',['artifact_accepted_not_authorized_to_send'],draft));
          if(g.state==='human_review'||g.state==='reject')return finish(g);
        }
      }
      if(draftNo===policy.maxDrafts)return finish(gate('human_review',['revision_budget_exhausted']));
    }
  } catch(e) {return finish(gate('human_review',[e.code??'invalid_response_or_provider_failure']))}
  return finish(gate('human_review',['no_terminal_result']));
}
