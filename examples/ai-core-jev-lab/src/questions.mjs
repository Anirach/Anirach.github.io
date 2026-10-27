export const ROUTES = Object.freeze({billing:'Invoices, payments, or subscription charges',technical:'Software defects or integration failures',other:'Neither billing nor technical'});
export const ROUTE_QUESTION='Which support team best fits this ticket?';
export const HUMAN_QUESTION='Does the customer explicitly request a human agent?';
export function requestShape(ticket) {
  return {model:'jev-1.13.0',state:{ticket:ticket.text},questions:{route:{type:'choice',instructions:ROUTE_QUESTION,criteria:{...ROUTES}},wantsHuman:{type:'noul',instructions:HUMAN_QUESTION}}};
}
