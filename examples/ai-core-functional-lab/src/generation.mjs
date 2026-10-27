export function traditionalReply(input,facts) {
  // An ordinary deterministic function is preferable when a template is enough.
  return {action:'draft_reply',language:input.language,
    text:facts.facts.map(f=>f[input.language]).join(' '),citations:['export-csv','no-send']};
}
// The mock generator is separate from Jev. No live text generation is configured.
