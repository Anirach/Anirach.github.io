import {gate,plain} from './contracts.mjs';
export function checkInput(raw) {
  if(!plain(raw)) return gate('reject',['input_not_object']);
  const keys=['id','language','request','requestedAction'];
  if(Object.keys(raw).some(k=>!keys.includes(k))) return gate('reject',['unknown_input_field']);
  if(typeof raw.id!=='string'||!/^[VHA]\d{3}$/.test(raw.id)) return gate('reject',['invalid_id']);
  if(!['en','th'].includes(raw.language)) return gate('reject',['unsupported_language']);
  if(typeof raw.request!=='string'||!raw.request.trim()||raw.request.length>2000)
    return gate('reject',['invalid_request_size']);
  if(typeof raw.requestedAction!=='string') return gate('reject',['missing_action']);
  const request=raw.request.normalize('NFC').trim();
  if(/ignore (all|previous)|system prompt|bypass the gate/i.test(request))
    return gate('reject',['known_injection_pattern']);
  // This deliberately small pattern list is not a complete injection detector.
  return gate('accept',[],{id:raw.id,language:raw.language,request,requestedAction:raw.requestedAction});
}
