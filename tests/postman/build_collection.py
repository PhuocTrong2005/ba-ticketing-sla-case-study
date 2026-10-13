"""Generate a readable Postman v2.1 collection from explicit ordered API cases.

No random data, SLA fixture changes, injected clock or backend imports.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GROUPS = []
VARIABLES = ['ticket_id', 'review_key', 'missing_ticket_id', 'capacity_return_id',
             'capacity_one_id', 'capacity_two_id', 'capacity_three_id', 'capacity_new_id',
             'customer_two_ticket_id', 'resolved_ticket_id', 'period_from', 'period_to',
             'future_as_of', 'observed_created_at', 'resolution_before_review', 'waiting_consumed_seconds']

HELPERS = r'''
const body = pm.response.json();
function assertCase(label, fn) { pm.test(label, fn); }
function same(label, actual, expected) { assertCase(label, () => pm.expect(actual).to.deep.equal(expected)); }
function stamp(value) { pm.expect(value).to.be.a('string').and.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+07:00$/); }
function seconds(value) { pm.expect(value).to.be.a('number'); pm.expect(Number.isInteger(value) && value >= 0).to.equal(true); }
function customerPrivacy(ticket) {
  for (const field of ['sla','notes','reviews','assignment_snapshot','rejection_count','needs_manager_review','handling_plan','warning_level']) pm.expect(ticket).not.to.have.property(field);
  pm.expect(ticket.messages).to.be.an('array');
  ticket.messages.forEach(message => pm.expect(message.visibility).to.equal('PUBLIC'));
  pm.expect(JSON.stringify(ticket)).not.to.include('PM-INTERNAL-NOTE');
  pm.expect(JSON.stringify(ticket)).not.to.include('PM-REVIEW-PLAN');
}
function ticketContract(ticket, internal, list = false) {
  const common = ['title','description','priority','policy_id','customer_id','id','status','assignee_id','created_at','assigned_at','closed_at'];
  const expected = common.concat(internal ? ['sla','rejection_count','needs_manager_review','reviews','assignment_snapshot'] : []);
  if (!internal || !list) expected.push('messages');
  pm.expect(Object.keys(ticket).sort()).to.deep.equal(expected.sort());
  pm.expect(ticket.id).to.be.a('number'); pm.expect(Number.isInteger(ticket.id) && ticket.id > 0).to.equal(true);
  pm.expect(ticket.title).to.be.a('string'); pm.expect(ticket.description).to.be.a('string');
  pm.expect(['HIGH','NORMAL']).to.include(ticket.priority); pm.expect(ticket.policy_id).to.equal(ticket.priority);
  pm.expect(['NEW','IN_PROGRESS','WAITING_FOR_CUSTOMER','RESOLVED','CLOSED']).to.include(ticket.status);
  stamp(ticket.created_at); if (ticket.assigned_at !== null) stamp(ticket.assigned_at); if (ticket.closed_at !== null) stamp(ticket.closed_at);
  if (!internal) customerPrivacy(ticket);
  else {
    pm.expect(ticket.needs_manager_review).to.be.a('boolean'); seconds(ticket.rejection_count);
    pm.expect(ticket.reviews).to.be.an('array');
    pm.expect(Object.keys(ticket.sla).sort()).to.deep.equal(['first_response','resolution']);
    for (const clock of Object.values(ticket.sla)) {
      pm.expect(['pending','met','breached']).to.include(clock.status);
      pm.expect(['none','soft','emphasized','due','breached']).to.include(clock.warning_level);
      if (clock.due_at !== null) stamp(clock.due_at);
      if (list) { pm.expect(clock.remaining_display).to.be.a('string'); pm.expect(clock).not.to.have.property('remaining_seconds'); }
      else { seconds(clock.remaining_seconds); seconds(clock.consumed_seconds); pm.expect(clock.running).to.be.a('boolean'); }
    }
  }
}
function reportContract(report, metric) {
  const keys = ['metric_code','as_of','period','filters','numerator','denominator'];
  if (['M-01','M-02','M-03'].includes(metric)) keys.push('ratio','display', ...(metric === 'M-01' ? ['pending_count'] : ['unclosed_count','unclosed_note']));
  else keys.push('items');
  pm.expect(Object.keys(report).sort()).to.deep.equal(keys.sort());
  pm.expect(report.metric_code).to.equal(metric); stamp(report.as_of);
  pm.expect(report.period.boundary).to.equal('[from,to)'); pm.expect(report.period.timezone).to.equal('Asia/Ho_Chi_Minh');
  pm.expect(Object.keys(report.filters).sort()).to.deep.equal(['agent_id','priority']);
  if (metric <= 'M-03') {
    seconds(report.numerator); seconds(report.denominator); pm.expect(report.numerator <= report.denominator).to.equal(true);
    if (!report.denominator) { pm.expect(report.ratio).to.equal(null); pm.expect(report.display).to.equal('không có dữ liệu'); }
    else { pm.expect(report.ratio).to.equal(report.numerator/report.denominator); pm.expect(report.display).to.equal(report.numerator+'/'+report.denominator); }
    if (metric === 'M-01') seconds(report.pending_count);
    else { seconds(report.unclosed_count); pm.expect(report.unclosed_note).to.include('không giới hạn ngày tạo'); }
  } else {
    pm.expect(report.numerator).to.equal(null); pm.expect(report.denominator).to.equal(null); pm.expect(report.items).to.be.an('array');
    for (const item of report.items) {
      if (metric === 'M-04') { pm.expect(Object.keys(item).sort()).to.deep.equal(['first_response_breached','id','resolution_breached']); pm.expect(item.first_response_breached).to.be.a('boolean'); pm.expect(item.resolution_breached).to.be.a('boolean'); }
      if (metric === 'M-05') { pm.expect(Object.keys(item).sort()).to.deep.equal(['id','resolved_at','wait_calendar_seconds']); stamp(item.resolved_at); seconds(item.wait_calendar_seconds); }
      if (metric === 'M-06') {
        pm.expect(Object.keys(item).sort()).to.deep.equal(['agent_id','capacity_state','counts_by_status','display_name','in_progress_count']);
        seconds(item.in_progress_count); pm.expect(Object.keys(item.counts_by_status).sort()).to.deep.equal(['CLOSED','IN_PROGRESS','NEW','RESOLVED','WAITING_FOR_CUSTOMER']);
        Object.values(item.counts_by_status).forEach(seconds); pm.expect(item.in_progress_count).to.equal(item.counts_by_status.IN_PROGRESS);
        pm.expect(item.capacity_state).to.equal(item.in_progress_count<3?'available':item.in_progress_count===3?'at_limit':'overloaded');
      }
      if (metric === 'M-07') { pm.expect(item.ticket_id).to.be.a('number'); pm.expect(item.review_key).to.be.a('string'); stamp(item.requested_at); if (item.completed_at !== null) stamp(item.completed_at); seconds(item.wait_calendar_seconds); seconds(item.wait_overlap_seconds); pm.expect(['none','before_request','during_wait']).to.include(item.breach_context); }
    }
  }
}
'''.strip()


def group(name, description):
    folder = {'name': name, 'description': description, 'item': []}
    GROUPS.append(folder)
    return folder


def request(folder, case, label, method, path, identity, expected=200, payload=None,
            code=None, structural=False, kind=None, state=None, save=None,
            tests='', refs='BR-32, BR-33, BR-62 / AC-16', pre='', raw=None):
    desc = f'{case}: {label}. Trace: {refs}. Expected HTTP {expected}; error_code={code if code else "null (handler)" if expected >= 400 and not structural else "detail list (FastAPI structure)" if structural else "n/a"}. Run in folder/collection order on a fresh database.'
    headers = [{'key': 'Accept', 'value': 'application/json'}]
    if identity is not None:
        headers.append({'key': 'X-Demo-User-Id', 'value': '{{' + identity + '}}' if identity in IDENTITY else identity})
    for variable in ['period_from','period_to','future_as_of','observed_created_at']:
        path = path.replace('{{' + variable + '}}', '{{' + variable + '_url}}')
    req = {'method': method, 'header': headers, 'url': '{{base_url}}' + path, 'description': desc}
    if payload is not None or raw is not None:
        req['header'].append({'key': 'Content-Type', 'value': 'application/json'})
        req['body'] = {'mode': 'raw', 'raw': raw if raw is not None else json.dumps(payload, ensure_ascii=False), 'options': {'raw': {'language': 'json'}}}
    script = HELPERS + f'\nsame("{case} HTTP {expected}", pm.response.code, {expected});\n'
    if expected >= 400:
        if structural:
            script += 'assertCase("FastAPI structural 422 before handler is allowed by BR-33", () => { pm.expect(body.detail).to.be.an("array").that.is.not.empty; body.detail.forEach(e=>{pm.expect(e.loc).to.be.an("array");pm.expect(e.msg).to.be.a("string");pm.expect(e.type).to.be.a("string");}); });\n'
        else:
            script += f'assertCase("Handler error envelope and code", () => {{pm.expect(Object.keys(body)).to.deep.equal(["detail"]);pm.expect(Object.keys(body.detail).sort()).to.deep.equal(["error_code","message"]);pm.expect(body.detail.error_code).to.equal({json.dumps(code)});pm.expect(body.detail.message).to.be.a("string");}});\n'
    elif kind in ('customer', 'internal'):
        script += f'assertCase("{kind} ticket response contract",()=>ticketContract(body,{str(kind == "internal").lower()}));\n'
        if state:
            script += f'same("Ticket state {state}",body.status,{json.dumps(state)});\n'
        if save:
            script += f'if(pm.response.code==={expected} && Number.isInteger(body.id)){{pm.environment.set({json.dumps(save)},body.id);}}\n'
    script += tests
    events = [{'listen': 'test', 'script': {'type': 'text/javascript', 'exec': script.splitlines()}}]
    if pre:
        events.insert(0, {'listen': 'prerequest', 'script': {'type': 'text/javascript', 'exec': pre.splitlines()}})
    folder['item'].append({'name': f'{case} · {label} → {expected}' + (f' {code}' if code else ''), 'request': req, 'event': events})


IDENTITY = {'customer_1': '1', 'customer_2': '2', 'agent_3': '3', 'agent_4': '4', 'agent_5': '5', 'manager_6': '6'}
CREATE = {'title': 'PM-FLOW-01 High', 'description': 'Deterministic HTTP workflow scenario', 'priority': 'HIGH'}
PLAN = {'handling_plan': {'unresolved_reason': 'PM review cause', 'next_action': 'PM-REVIEW-PLAN next action', 'needs_expert_input': True, 'expert_note': 'Record only; no simulated assignment or communication'}}
FLOW = '/tickets/{{ticket_id}}'


def create(folder, case, variable, priority='HIGH', owner='customer_1'):
    request(folder, case, 'Create ' + variable, 'POST', '/tickets', owner, 201,
            {'title': case + ' ' + variable, 'description': 'Deterministic scenario ' + case, 'priority': priority},
            kind='customer', state='NEW', save=variable, refs='AC-01 / BR-03, BR-62',
            tests='same("No assignee on create",body.assignee_id,null);')


def action(folder, case, label, action_name, identity='agent_3', payload=None, expected=200,
           state='IN_PROGRESS', variable='ticket_id', **kwargs):
    request(folder, case, label, 'POST', '/tickets/{{' + variable + '}}/' + action_name,
            identity, expected, payload, kind=('customer' if identity.startswith('customer') else 'internal') if expected < 400 else None,
            state=state if expected < 400 else None, **kwargs)


def report(folder, case, metric, tests='', query='', identity='manager_6', expected=200):
    if metric in ['M-01','M-02','M-03']:
        query = '?from={{period_from}}&to={{period_to}}' + ('&' + query if query else '')
    elif query:
        query = '?' + query
    request(folder, case, metric + (' ' + query if query else ''), 'GET', '/reports/' + metric + query,
            identity, expected, tests=(f'assertCase("{metric} report contract",()=>reportContract(body,"{metric}"));\n' if expected == 200 else '') + tests,
            refs='AC-28…31 / BR-35, BR-62, BR-63')


def build():
    fresh = group('01 · Fresh database, identity and empty reports', 'Start with a new empty DB. Stop on failure. Server Date defines read-only report bounds, not operation timestamps.')
    request(fresh, 'PM-001', 'Fresh database precondition', 'GET', '/tickets', 'manager_6',
            pre='\n'.join('pm.environment.unset('+json.dumps(v)+');' for v in VARIABLES),
            tests='''same("Fresh DB has no tickets",body,[]);
const serverDate=Date.parse(pm.response.headers.get('Date'));
assertCase("Server Date is available",()=>pm.expect(Number.isFinite(serverDate)).to.equal(true));
function boundary(delta){const shifted=new Date(serverDate+7*3600000+delta*86400000);return shifted.toISOString().slice(0,10)+'T00:00:00+07:00';}
pm.environment.set('period_from',boundary(-7));pm.environment.set('period_to',boundary(7));pm.environment.set('future_as_of',boundary(366));
if(body.length) pm.execution.setNextRequest(null);''', refs='D-47 / BR-02, BR-63')
    for n, uid in [('PM-002', None), ('PM-003', 'not-a-user'), ('PM-004', '999')]:
        request(fresh, n, 'Missing/invalid demo identity', 'GET', '/tickets', uid, 401)
    for i in range(1, 8):
        tests = 'same("Empty numerator/denominator",[body.numerator,body.denominator],[0,0]);' if i <= 3 else 'same("Empty snapshot",body.items,[]);' if i != 6 else 'same("Three demo Agents",body.items.map(x=>x.agent_id),[3,4,5]);same("All loads zero",body.items.map(x=>x.in_progress_count),[0,0,0]);'
        report(fresh, f'PM-01{i}', f'M-{i:02}', tests)

    validation = group('02 · Create validation and New ticket permissions', 'No forbidden timestamp/actor/assignee/event_id fields are sent, including negative cases. Structural tests use invalid types/unknown ordinary fields.')
    bad = [('missing title', {'description': 'D', 'priority': 'HIGH'}, False),
           ('blank title', {'title': ' ', 'description': 'D', 'priority': 'HIGH'}, False),
           ('numeric title', {'title': 42, 'description': 'D', 'priority': 'HIGH'}, True),
           ('missing description', {'title': 'T', 'priority': 'HIGH'}, False),
           ('blank description', {'title': 'T', 'description': ' ', 'priority': 'HIGH'}, False),
           ('object description', {'title': 'T', 'description': {}, 'priority': 'HIGH'}, True),
           ('missing priority', {'title': 'T', 'description': 'D'}, False),
           ('unsupported priority', {'title': 'T', 'description': 'D', 'priority': 'LOW'}, True),
           ('priority wrong type', {'title': 'T', 'description': 'D', 'priority': 42}, True),
           ('unknown field', {**CREATE, 'unexpected_field': True}, True)]
    for i, (label, payload, structural) in enumerate(bad, 20):
        request(validation, f'PM-{i:03}', 'Create: ' + label, 'POST', '/tickets', 'customer_1', 422, payload,
                structural=structural, refs='AC-01, AC-16 / BR-33, BR-62')
    request(validation, 'PM-030', 'Agent create role before missing text', 'POST', '/tickets', 'agent_3', 403, {})
    create(validation, 'PM-031', 'ticket_id')
    request(validation, 'PM-032', 'Owner sees New ticket', 'GET', FLOW, 'customer_1', kind='customer', state='NEW',
            tests="pm.environment.set('missing_ticket_id',body.id+1000000);pm.environment.set('observed_created_at',body.created_at);")
    request(validation, 'PM-033', 'Other Customer gets 404', 'GET', FLOW, 'customer_2', 404, refs='AC-03 / BR-34')
    request(validation, 'PM-034', 'Missing ticket derived from response ID', 'GET', '/tickets/{{missing_ticket_id}}', 'manager_6', 404)
    request(validation, 'PM-035', 'Agent cannot view unclaimed New', 'GET', FLOW, 'agent_3', 403, refs='AC-06, AC-13 / BR-34, BR-50')
    action(validation, 'PM-036', 'Agent cannot reply to unclaimed New', 'messages', payload={'content': 'Before assignment'}, expected=403)
    action(validation, 'PM-037', 'Customer cannot claim', 'claim', 'customer_1', expected=403, refs='AC-27 / BR-04, BR-33')
    action(validation, 'PM-038', 'Manager cannot claim', 'claim', 'manager_6', expected=403, refs='AC-27 / BR-05, BR-54')
    request(validation, 'PM-039', 'Agent queue exact allowed fields', 'GET', '/tickets/queue', 'agent_3', tests='''assertCase('Queue contract',()=>{pm.expect(body).to.be.an('array');same('Queue has workflow ticket',body.map(x=>x.id),[Number(pm.environment.get('ticket_id'))]);body.forEach(x=>{pm.expect(Object.keys(x).sort()).to.deep.equal(['created_at','first_response_due_at','id','priority','title']);stamp(x.created_at);stamp(x.first_response_due_at);});});''', refs='AC-06 / BR-34, BR-62')
    request(validation, 'PM-040', 'Customer cannot read Agent queue', 'GET', '/tickets/queue', 'customer_1', 403)

    flow = group('03 · Workflow, privacy, review escalation and Closed', 'Agent 3 only. Creates and closes the main ticket before capacity cases use Agent 4. Review identity saved from response; no fixed times.')
    action(flow, 'PM-041', 'Customer public message at New', 'messages', 'customer_1', {'content': 'PM-CUSTOMER-NEW'}, state='NEW', refs='AC-02 / BR-06, BR-62')
    action(flow, 'PM-042', 'A1 Manager without open review before content', 'reviews/complete', 'manager_6', {}, 409, code='INVALID_TICKET_STATE', refs='A1, AC-26 / BR-33, BR-58')
    action(flow, 'PM-043', 'Claim and assignment snapshot', 'claim', tests="assertCase('Snapshot captures assignment',()=>{pm.expect(body.assignee_id).to.equal(Number(pm.environment.get('agent_3')));pm.expect(body.assignment_snapshot.assigned_at).to.equal(body.assigned_at);pm.expect(body.assignment_snapshot.assignment_event_id).to.be.a('number');});", refs='AC-07 / BR-07, BR-25')
    action(flow, 'PM-044', 'Waiting before first public reply blocked', 'waiting', expected=409, code='INVALID_TICKET_STATE', refs='AC-14 / BR-08, BR-62')
    for i, (name, pl, st) in enumerate([('messages', {}, False), ('messages', {'content': ' '}, False), ('notes', {}, False), ('resolve', {}, False), ('messages', {'content': 42}, True)], 45):
        action(flow, f'PM-{i:03}', name + ' missing/invalid content', name, payload=pl, expected=422, structural=st, refs='AC-16 / BR-33, BR-62')
    for i, name in enumerate(['messages', 'notes', 'resolve'], 50):
        action(flow, f'PM-{i:03}', 'Other Agent denied before business content', name, 'agent_4', {}, 403, refs='AC-12, AC-16 / BR-33, BR-34')
    request(flow, 'PM-053', 'Other Agent detail denied', 'GET', FLOW, 'agent_4', 403, refs='AC-12 / BR-34')
    action(flow, 'PM-054', 'Manager cannot public message', 'messages', 'manager_6', {}, 403, refs='AC-27 / BR-05, BR-54')
    action(flow, 'PM-055', 'Manager cannot Resolved', 'resolve', 'manager_6', {}, 403, refs='AC-27 / BR-05, BR-54')
    action(flow, 'PM-056', 'Customer cannot internal note', 'notes', 'customer_1', {'content': 'Not permitted'}, 403)
    action(flow, 'PM-057', 'Internal note does not end first response', 'notes', payload={'content': 'PM-INTERNAL-NOTE'}, tests='same("First response still running",body.sla.first_response.running,true);', refs='AC-18, AC-21 / BR-19, BR-31')
    request(flow, 'PM-058', 'Manager sees Agent note', 'GET', FLOW, 'manager_6', kind='internal', tests='assertCase("Manager sees internal note",()=>pm.expect(body.messages.some(m=>m.visibility==="INTERNAL" && m.content==="PM-INTERNAL-NOTE")).to.equal(true));', refs='AC-21 / BR-31, BR-62')
    request(flow, 'PM-059', 'Customer detail excludes internal data', 'GET', FLOW, 'customer_1', kind='customer', refs='AC-21 / BR-31, BR-62')
    action(flow, 'PM-060', 'Agent public reply ends first response', 'messages', payload={'content': 'PM-AGENT-REPLY'}, tests='same("First response ended",body.sla.first_response.running,false);', refs='AC-18 / BR-19')
    action(flow, 'PM-061', 'Waiting after reply', 'waiting', state='WAITING_FOR_CUSTOMER', tests='same("Resolution paused",body.sla.resolution.running,false);', refs='AC-14 / BR-08, BR-20')
    action(flow, 'PM-062', 'Agent public message keeps Waiting', 'messages', payload={'content': 'PM-AGENT-WAITING'}, state='WAITING_FOR_CUSTOMER', refs='AC-02, AC-14 / BR-20')
    action(flow, 'PM-063', 'Agent note keeps Waiting', 'notes', payload={'content': 'PM-INTERNAL-NOTE Waiting'}, state='WAITING_FOR_CUSTOMER')
    action(flow, 'PM-064', 'Customer resume from Waiting', 'messages', 'customer_1', {'content': 'PM-CUSTOMER-RESUME'}, refs='AC-02 / BR-20, BR-21')
    action(flow, 'PM-065', 'Confirm outside Resolved', 'confirm', 'customer_1', expected=409, code='INVALID_TICKET_STATE', refs='AC-05 / BR-50')
    action(flow, 'PM-066', 'Reject outside Resolved before missing reason', 'reject', 'customer_1', {}, 409, code='INVALID_TICKET_STATE', refs='AC-05, AC-16 / BR-33, BR-50')
    for cycle in range(1, 4):
        base = 70 + (cycle - 1) * 10
        action(flow, f'PM-{base:03}', f'Resolved cycle {cycle}', 'resolve', payload={'resolution_summary': f'PM public result {cycle}'}, state='RESOLVED', refs='AC-04, AC-15 / BR-08, BR-21')
        if cycle == 1:
            action(flow, 'PM-071', 'Resolved Customer message state before content', 'messages', 'customer_1', {}, 409, code='INVALID_TICKET_STATE', refs='AC-13, AC-16 / BR-33, BR-50')
            action(flow, 'PM-072', 'Resolved Agent note state before content', 'notes', payload={}, expected=409, code='INVALID_TICKET_STATE')
            action(flow, 'PM-073', 'Reject missing reason in valid state', 'reject', 'customer_1', {}, 422, refs='AC-04, AC-16 / BR-11, BR-62')
            action(flow, 'PM-074', 'Reject blank reason in valid state', 'reject', 'customer_1', {'reason': ' '}, 422)
        action(flow, f'PM-{base+5:03}', f'Customer rejection {cycle}', 'reject', 'customer_1', {'reason': f'PM still unresolved {cycle}'}, refs='AC-04, AC-23 / BR-21, BR-52')
        request(flow, f'PM-{base+6:03}', f'Inspect review threshold after rejection {cycle}', 'GET', FLOW, 'agent_3', kind='internal',
                tests=f'same("Rejection count",body.rejection_count,{cycle});same("Review threshold",body.needs_manager_review,{str(cycle == 3).lower()});same("Review count",body.reviews.length,{1 if cycle == 3 else 0});' + ("pm.environment.set('review_key',body.reviews[0].review_key);" if cycle == 3 else ''), refs='AC-23 / BR-52')
    action(flow, 'PM-097', 'Review open blocks Resolved before missing content', 'resolve', payload={}, expected=409, code='REVIEW_REQUIRED', refs='AC-24 / BR-33, BR-53')
    for case, uid, status in [('PM-098','customer_1',404),('PM-099','agent_3',403)]:
        request(flow, case, 'Review resource restricted', 'GET', FLOW + '/reviews', uid, status, refs='AC-27 / BR-54')
    request(flow, 'PM-100', 'Customer missing review resource still 404', 'GET', '/tickets/{{missing_ticket_id}}/reviews', 'customer_1', 404, refs='AC-27 / BR-54')
    request(flow, 'PM-101', 'Manager reads open review', 'GET', FLOW + '/reviews', 'manager_6', tests="same('Open review key',body.map(r=>r.review_key),[pm.environment.get('review_key')]);same('Review incomplete',body[0].completed_at,null);", refs='AC-27 / BR-54')
    action(flow, 'PM-102', 'Customer cannot write review', 'reviews/complete', 'customer_1', {}, 404, refs='AC-27 / BR-54')
    action(flow, 'PM-103', 'Agent cannot write review', 'reviews/complete', payload={}, expected=403, refs='AC-27 / BR-54')
    for i, pl in enumerate([{}, {'handling_plan': {}}, {'handling_plan': {'unresolved_reason': 'Cause','needs_expert_input': False}}, {'handling_plan': {'unresolved_reason': ' ','next_action': 'Next','needs_expert_input': False}}, {'handling_plan': {'unresolved_reason': 'Cause','next_action': 'Next'}}], 104):
        action(flow, f'PM-{i:03}', 'Review missing/blank mandatory plan', 'reviews/complete', 'manager_6', pl, 422, refs='AC-25 / BR-55, BR-62')
    action(flow, 'PM-109', 'Review boolean must be strict boolean', 'reviews/complete', 'manager_6', {'handling_plan': {**PLAN['handling_plan'], 'needs_expert_input': 'yes'}}, 422, structural=True)
    action(flow, 'PM-110', 'Agent can Waiting with open review', 'waiting', state='WAITING_FOR_CUSTOMER', tests="same('Review still open',body.needs_manager_review,true);pm.environment.set('waiting_consumed_seconds',body.sla.resolution.consumed_seconds);", refs='AC-24, AC-25 / BR-57')
    action(flow, 'PM-110a', 'Customer resumes while review remains open', 'messages', 'customer_1', {'content':'PM resume before review completion'}, refs='AC-02, AC-24 / BR-57')
    request(flow, 'PM-110b', 'Assigned Agent sees open review after resume', 'GET', FLOW, 'agent_3', kind='internal', state='IN_PROGRESS', tests="same('Review survived Customer resume',body.needs_manager_review,true);same('Same review still open',body.reviews[0].review_key,pm.environment.get('review_key'));same('Review still incomplete',body.reviews[0].completed_at,null);", refs='AC-24 / BR-57')
    action(flow, 'PM-110c', 'Review still blocks well-formed Resolved after resume', 'resolve', payload={'resolution_summary':'PM still blocked'}, expected=409, code='REVIEW_REQUIRED', refs='AC-24 / BR-53, BR-57')
    action(flow, 'PM-110d', 'Return to Waiting before Manager completes plan', 'waiting', state='WAITING_FOR_CUSTOMER', tests="same('Review stays open',body.needs_manager_review,true);pm.environment.set('waiting_consumed_seconds',body.sla.resolution.consumed_seconds);", refs='AC-24, AC-25 / BR-57')
    report(flow, 'PM-111', 'M-07', "same('Open review appears',body.items.map(x=>x.review_key),[pm.environment.get('review_key')]);same('No completion yet',body.items[0].completed_at,null);")
    action(flow, 'PM-112', 'Manager completes review during Waiting', 'reviews/complete', 'manager_6', PLAN, state='WAITING_FOR_CUSTOMER',
           tests="same('Review cleared',body.needs_manager_review,false);same('Clock remains paused',body.sla.resolution.running,false);same('No resolution time accrued during Waiting',body.sla.resolution.consumed_seconds,Number(pm.environment.get('waiting_consumed_seconds')));same('Completed correct review',body.reviews[0].review_key,pm.environment.get('review_key'));assertCase('Completion server time',()=>stamp(body.reviews[0].completed_at));", refs='AC-25 / BR-55, BR-56, BR-57')
    request(flow, 'PM-113', 'Assigned Agent reads plan on ticket', 'GET', FLOW, 'agent_3', kind='internal', tests="same('Agent reads Manager plan',body.reviews[0].handling_plan.next_action,'PM-REVIEW-PLAN next action');", refs='AC-27 / BR-62')
    request(flow, 'PM-114', 'Customer cannot read completed plan/note/SLA', 'GET', FLOW, 'customer_1', kind='customer', refs='AC-21, AC-27 / BR-31, BR-62')
    action(flow, 'PM-115', 'A1 completed review cannot complete again', 'reviews/complete', 'manager_6', {}, 409, code='INVALID_TICKET_STATE', refs='A1, AC-26 / BR-58')
    action(flow, 'PM-116', 'Customer resumes after plan', 'messages', 'customer_1', {'content': 'PM customer after plan'}, refs='AC-02, AC-25 / BR-20, BR-57')
    action(flow, 'PM-117', 'Resolved after completed review', 'resolve', payload={'resolution_summary': 'PM final public result'}, state='RESOLVED', refs='AC-15, AC-25 / BR-53, BR-55')
    action(flow, 'PM-118', 'Customer confirms Closed', 'confirm', 'customer_1', state='CLOSED', refs='AC-04 / BR-09')
    action(flow, 'PM-119', 'A2 Closed before missing plan', 'reviews/complete', 'manager_6', {}, 409, code='TICKET_CLOSED', refs='A2, AC-26 / BR-33, BR-58')
    for i, (name, uid, pl) in enumerate([('reject','customer_1',{}),('messages','customer_1',{}),('notes','agent_3',{}),('resolve','agent_3',{}),('claim','agent_4',None),('confirm','customer_1',None)], 120):
        action(flow, f'PM-{i:03}', 'Closed cannot ' + name + ' before missing content', name, uid, pl, 409, code='TICKET_CLOSED', refs='AC-05, AC-11, AC-13, AC-16 / BR-33, BR-51')
    action(flow, 'PM-126', 'Other Customer access before Closed/content', 'reject', 'customer_2', {}, 404, refs='AC-03, AC-05 / BR-33, BR-50')
    action(flow, 'PM-127', 'Other Agent access before Closed/content', 'notes', 'agent_4', {}, 403, refs='AC-12 / BR-33, BR-34')
    request(flow, 'PM-128', 'Closed state remains after rejected actions', 'GET', FLOW, 'manager_6', kind='internal', state='CLOSED', tests='same("Rejections unchanged",body.rejection_count,3);same("Exactly one completed review",body.reviews.length,1);', refs='AC-05, AC-26 / BR-51, BR-58')

    capacity = group('04 · Capacity 3, return overload and claim priority', 'Agent 4 is unused so far. Resolved return ticket releases load before three claims. Return raises load to 4; Waiting frees slots. Does not claim concurrency evidence.')
    create(capacity, 'PM-130', 'capacity_return_id', 'NORMAL')
    action(capacity, 'PM-131', 'Claim return candidate', 'claim', 'agent_4', variable='capacity_return_id', refs='AC-07 / BR-07')
    action(capacity, 'PM-132', 'Resolve without prior reply releases slot', 'resolve', 'agent_4', {'resolution_summary': 'PM capacity provisional result'}, state='RESOLVED', variable='capacity_return_id', tests='same("Resolved also completes first response",body.sla.first_response.running,false);', refs='AC-15, AC-18 / BR-08, BR-19')
    for i, var in enumerate(['capacity_one_id','capacity_two_id','capacity_three_id']):
        create(capacity, f'PM-{133+i*2:03}', var, 'NORMAL' if i==2 else 'HIGH')
        action(capacity, f'PM-{134+i*2:03}', 'Fill capacity slot ' + str(i+1), 'claim', 'agent_4', variable=var, refs='AC-07, AC-10 / BR-07, BR-10')
    create(capacity, 'PM-139', 'capacity_new_id')
    report(capacity, 'PM-140', 'M-06', "same('Exactly 3 In Progress',body.items[0].in_progress_count,3);same('At limit',body.items[0].capacity_state,'at_limit');", 'agent_id={{agent_4}}')
    action(capacity, 'PM-141', 'Load 3 blocks new claim', 'claim', 'agent_4', expected=409, variable='capacity_new_id', code='AGENT_CAPACITY_REACHED', refs='AC-10 / BR-10')
    action(capacity, 'PM-142', 'Customer return allowed despite load 3', 'reject', 'customer_1', {'reason': 'PM capacity return still unresolved'}, variable='capacity_return_id', refs='AC-10 / BR-10, BR-21')
    report(capacity, 'PM-143', 'M-06', "same('Customer return overload 4',body.items[0].in_progress_count,4);same('Overloaded',body.items[0].capacity_state,'overloaded');", 'agent_id={{agent_4}}')
    action(capacity, 'PM-144', 'Load 4 blocks new claim', 'claim', 'agent_4', expected=409, variable='capacity_new_id', code='AGENT_CAPACITY_REACHED', refs='AC-10 / BR-10')
    action(capacity, 'PM-145', 'Closed beats assigned and capacity', 'claim', 'agent_4', expected=409, code='TICKET_CLOSED', refs='AC-11 / BR-33, BR-37, BR-51')
    action(capacity, 'PM-146', 'Assigned beats capacity', 'claim', 'agent_4', expected=409, variable='capacity_one_id', code='TICKET_ALREADY_ASSIGNED', refs='AC-11 / BR-37')
    action(capacity, 'PM-147', 'Other Agent claim also gets already assigned', 'claim', 'agent_5', expected=409, variable='capacity_one_id', code='TICKET_ALREADY_ASSIGNED', refs='AC-11 / BR-37')
    action(capacity, 'PM-148', 'Capacity ticket one first reply', 'messages', 'agent_4', {'content':'PM capacity one public'}, variable='capacity_one_id')
    action(capacity, 'PM-149', 'Waiting lowers load 4 to 3', 'waiting', 'agent_4', state='WAITING_FOR_CUSTOMER', variable='capacity_one_id', refs='AC-10, AC-14 / BR-10, BR-20')
    action(capacity, 'PM-150', 'Still load 3 blocks new claim', 'claim', 'agent_4', expected=409, variable='capacity_new_id', code='AGENT_CAPACITY_REACHED', refs='AC-10 / BR-10')
    action(capacity, 'PM-151', 'Capacity ticket two first reply', 'messages', 'agent_4', {'content':'PM capacity two public'}, variable='capacity_two_id')
    action(capacity, 'PM-152', 'Waiting lowers load to 2', 'waiting', 'agent_4', state='WAITING_FOR_CUSTOMER', variable='capacity_two_id')
    action(capacity, 'PM-153', 'Load 2 permits new claim', 'claim', 'agent_4', variable='capacity_new_id', refs='AC-10 / BR-10')
    create(capacity, 'PM-154', 'customer_two_ticket_id', 'NORMAL', 'customer_2')
    request(capacity, 'PM-155', 'Customer 2 list contains only own ticket', 'GET', '/tickets', 'customer_2', tests="assertCase('Customer list privacy/ownership',()=>{body.forEach(customerPrivacy);pm.expect(body.map(t=>t.id)).to.deep.equal([Number(pm.environment.get('customer_two_ticket_id'))]);});", refs='AC-03, AC-21 / BR-31, BR-34')
    request(capacity, 'PM-156', 'Agent 4 list has only assigned and minute summaries', 'GET', '/tickets', 'agent_4', tests="assertCase('Internal list contract',()=>{pm.expect(body.length).to.equal(5);body.forEach(t=>{ticketContract(t,true,true);pm.expect(t.assignee_id).to.equal(Number(pm.environment.get('agent_4')));});});", refs='AC-12 / BR-34, BR-62')
    create(capacity, 'PM-157', 'resolved_ticket_id', 'NORMAL')
    action(capacity, 'PM-158', 'Agent 5 claims separate M05 candidate', 'claim', 'agent_5', variable='resolved_ticket_id')
    action(capacity, 'PM-159', 'Leave M05 candidate Resolved', 'resolve', 'agent_5', {'resolution_summary': 'PM awaiting Customer confirmation'}, state='RESOLVED', variable='resolved_ticket_id')

    reports = group('05 · M-01…M-07 contracts, periods, filters and access', 'Final dataset: 8 tickets, 1 Closed high/Agent3; Agent4 has 3 IP + 2 Waiting; Agent5 has 1 Resolved; Customer2 has 1 New. No long waits or SLA deadline conclusions.')
    for i in range(1, 8):
        metric = f'M-{i:02}'
        test = {1:'same("Five first response results",body.denominator,5);same("Three pending first responses",body.pending_count,3);',
                2:'same("One Closed ticket",body.denominator,1);same("Seven unclosed",body.unclosed_count,7);',
                3:'same("One Closed ticket",body.denominator,1);same("Closed ticket was rejected",body.numerator,1);same("Seven unclosed",body.unclosed_count,7);',
                4:'assertCase("M04 does not contain Closed main",()=>pm.expect(body.items.map(x=>x.id)).not.to.include(Number(pm.environment.get("ticket_id"))));',
                5:'same("One Resolved awaiting confirmation",body.items.map(x=>x.id),[Number(pm.environment.get("resolved_ticket_id"))]);',
                6:'same("Actual Agent loads",body.items.map(x=>[x.agent_id,x.in_progress_count]),[[3,0],[4,3],[5,0]]);',
                7:"same('Completed review from main ticket',body.items.map(x=>[x.ticket_id,x.review_key]),[[Number(pm.environment.get('ticket_id')),pm.environment.get('review_key')]]);assertCase('Review completion retained',()=>stamp(body.items[0].completed_at));"}[i]
        report(reports, f'PM-{160+i:03}', metric, test)
        for offset, uid in [(170,'customer_1'),(180,'agent_3')]:
            report(reports, f'PM-{offset+i:03}', metric, identity=uid, expected=403)
    for i in range(1, 4):
        report(reports, f'PM-{190+i:03}', f'M-{i:02}', 'same("Filtered empty denominator",body.denominator,0);same("Filtered empty numerator",body.numerator,0);same("Empty result marker",body.ratio,null);', 'agent_id={{agent_3}}&priority=NORMAL')
    report(reports, 'PM-194', 'M-01', 'same("High/Agent3 result count",body.denominator,1);same("No pending in filter",body.pending_count,0);same("Period from",body.period.from,pm.environment.get("period_from"));same("Period to",body.period.to,pm.environment.get("period_to"));same("Filters echoed",body.filters,{priority:"HIGH",agent_id:Number(pm.environment.get("agent_3"))});', 'agent_id={{agent_3}}&priority=HIGH')
    report(reports, 'PM-195', 'M-02', 'same("No Closed in normal/Agent4",body.denominator,0);same("Two normal unclosed for Agent4",body.unclosed_count,2);', 'agent_id={{agent_4}}&priority=NORMAL')
    report(reports, 'PM-196', 'M-05', 'same("Agent filter excludes other Resolved",body.items,[]);', 'agent_id={{agent_3}}')
    report(reports, 'PM-197', 'M-07', 'same("Priority filter excludes high review",body.items,[]);', 'priority=NORMAL')
    report(reports, 'PM-198', 'M-06', 'same("M06 filter keeps one Agent",body.items.map(x=>x.agent_id),[Number(pm.environment.get("agent_4"))]);same("All priorities remain in load",body.items[0].in_progress_count,3);', 'agent_id={{agent_4}}')
    for case, path in [('PM-200','/reports/M-02'),('PM-201','/reports/M-01?from={{period_to}}&to={{period_from}}'),('PM-202','/reports/M-02?from=not-a-time&to={{period_to}}'),('PM-203','/reports/M-04?as_of={{future_as_of}}'),('PM-204','/reports/M-06?priority=HIGH'),('PM-205','/reports/M-04?priority=LOW'),('PM-206','/reports/M-06?agent_id=999'),('PM-207','/reports/M-06?agent_id={{customer_1}}')]:
        request(reports, case, 'Reject invalid report period/filter', 'GET', path, 'manager_6', 422, refs='AC-16, AC-28…31 / BR-33, BR-63')
    request(reports, 'PM-208', 'Agent filter wrong type structural exception', 'GET', '/reports/M-06?agent_id=not-an-integer', 'manager_6', 422, structural=True)
    request(reports, 'PM-209', 'Unknown metric', 'GET', '/reports/M-99', 'manager_6', 404, refs='BR-32 / API contract')
    report(reports, 'PM-210', 'M-07', 'assertCase("Read historical as_of",()=>pm.expect(Date.parse(body.as_of)).to.equal(Date.parse(pm.environment.get("observed_created_at"))));', 'as_of={{observed_created_at}}')

    structure = group('06 · BR-33 structural exceptions and final state checks', 'Well-typed missing content follows domain priority; malformed types/JSON/extra ordinary field may return FastAPI 422 before handler. No server-owned action field is ever sent.')
    action(structure, 'PM-220', 'Wrong type on Closed bypasses handler state', 'messages', payload={'content':42}, expected=422, structural=True, refs='AC-16 / BR-33 exception')
    action(structure, 'PM-221', 'Wrong type on inaccessible ticket returns structural 422', 'messages', 'agent_4', {'content':42}, 422, structural=True, refs='AC-16 / BR-33 exception')
    request(structure, 'PM-222', 'Wrong type on nonexistent ticket structural 422', 'POST', '/tickets/{{missing_ticket_id}}/messages', 'agent_3', 422, {'content':42}, structural=True, refs='AC-16 / BR-33 exception')
    action(structure, 'PM-223', 'Extra ordinary field rejected even on Closed', 'claim', payload={'unexpected_field':True}, expected=422, structural=True, refs='AC-16 / BR-33 exception, BR-62')
    request(structure, 'PM-224', 'Malformed JSON before handler', 'POST', FLOW + '/messages', 'agent_3', 422, raw='{"content":', structural=True, refs='AC-16 / BR-33 exception')
    request(structure, 'PM-225', 'Invalid path type structural 422', 'GET', '/tickets/not-an-integer', 'manager_6', 422, structural=True)
    request(structure, 'PM-226', 'Well-typed nonexistent before content', 'POST', '/tickets/{{missing_ticket_id}}/messages', 'agent_3', 404, {}, refs='AC-16 / BR-33')
    request(structure, 'PM-227', 'Missing identity before role/content', 'POST', FLOW + '/resolve', None, 401, {}, refs='AC-16 / BR-33')
    request(structure, 'PM-228', 'Manager wrong role before Closed/content', 'POST', FLOW + '/resolve', 'manager_6', 403, {}, refs='AC-27 / BR-33, BR-54')
    request(structure, 'PM-229', 'Owner Closed unchanged and private', 'GET', FLOW, 'customer_1', kind='customer', state='CLOSED', refs='AC-05, AC-21 / BR-31, BR-51')
    request(structure, 'PM-230', 'Create missing body structural 422', 'POST', '/tickets', 'customer_1', 422, structural=True, refs='AC-01, AC-16 / BR-33 exception')
    request(structure, 'PM-231', 'Create root array instead of object', 'POST', '/tickets', 'customer_1', 422, [], structural=True, refs='AC-01, AC-16 / BR-33 exception')
    action(structure, 'PM-232', 'Resolve summary wrong type on Closed', 'resolve', payload={'resolution_summary':42}, expected=422, structural=True, refs='AC-16 / BR-33 exception')
    action(structure, 'PM-233', 'Reject reason wrong type on Closed', 'reject', 'customer_1', {'reason':42}, 422, structural=True, refs='AC-16 / BR-33 exception')

    collection = {'info': {'name': 'BA Ticketing SLA · Deterministic API checks',
        'description': 'D-47. Run all folders in order on a fresh isolated DB. Real server clock only. Sequential Newman/Postman does not prove races, 83 fixture SLA/calendar boundaries or all AC. No tokens or private machine paths. See api/README.md.',
        'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'},
        'event': [{'listen':'prerequest','script':{'type':'text/javascript','exec':[
            "for (const key of ['period_from','period_to','future_as_of','observed_created_at']) pm.variables.set(key+'_url',encodeURIComponent(pm.environment.get(key)||''));"
        ]}}], 'item': GROUPS}
    env = {'name':'BA Ticketing SLA · Local isolated API',
        'values':[{'key':'base_url','value':'http://127.0.0.1:8001','type':'default','enabled':True}] +
            [{'key':k,'value':v,'type':'default','enabled':True} for k,v in IDENTITY.items()] +
            [{'key':v,'value':'','type':'default','enabled':True} for v in VARIABLES],
        '_postman_variable_scope':'environment'}
    for name, data in [('ticketing-sla.postman_collection.json',collection),('ticketing-sla.postman_environment.json',env)]:
        (ROOT / 'api' / name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Folders:',len(GROUPS),'requests:',sum(len(g['item']) for g in GROUPS))


if __name__ == '__main__':
    build()
