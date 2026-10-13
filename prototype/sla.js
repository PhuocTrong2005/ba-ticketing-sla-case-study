// UTC+7 arithmetic is independent of the browser/host timezone.
export const POLICIES = {HIGH: [3600, 28800], NORMAL: [7200, 57600]};
const DAY = 86400, OFFSET = 25200;
export function timestamp(value) {
  if (typeof value === 'number' && Number.isFinite(value)) return Math.floor(value);
  if (typeof value !== 'string' || !/(Z|[+-]\d\d:\d\d)$/.test(value)) throw Error('Timestamp cần offset');
  const n = Date.parse(value);
  if (!Number.isFinite(n)) throw Error('Timestamp không hợp lệ');
  return Math.floor(n / 1000);
}
export function iso(value) {
  return value == null ? null : new Date((timestamp(value) + OFFSET) * 1000).toISOString().slice(0, 19) + '+07:00';
}
function session(value) {
  const day = Math.floor((value + OFFSET) / DAY) * DAY - OFFSET;
  const weekday = new Date((day + OFFSET) * 1000).getUTCDay();
  return {start: day + 28800, end: day + 61200, work: weekday !== 0 && weekday !== 6};
}
export function nextWork(value) {
  let t = timestamp(value);
  for (;;) {
    const s = session(t);
    if (s.work && t < s.end) return Math.max(t, s.start);
    t = s.start + DAY;
  }
}
export function nextSession(value) {
  const t = timestamp(value), s = session(t);
  return nextWork(s.work && t < s.start ? t : s.start + DAY);
}
export function workSeconds(start, end) {
  start = timestamp(start); end = timestamp(end);
  if (end < start) throw Error('Khoảng thời gian âm');
  let sum = 0;
  for (let t = start; t <= end;) {
    const s = session(t);
    if (s.work) sum += Math.max(0, Math.min(end, s.end) - Math.max(start, s.start));
    t = s.start + DAY;
  }
  return sum;
}
export function deadline(start, seconds) {
  let t = nextWork(start);
  for (;;) {
    const available = session(t).end - t;
    if (seconds <= available) return t + seconds;
    seconds -= available; t = nextWork(session(t).end);
  }
}
export function warning(status, running, remaining, due, at) {
  if (status === 'breached') return 'breached';
  if (status === 'met' || !running) return 'none';
  if (at === due) return 'due';
  return remaining < 900 ? 'emphasized' : remaining < 3600 ? 'soft' : 'none';
}
// Accepted events only. Test adapter removes rejected attempts before replay.
export function replay(createdAt, policy, events, asOf) {
  const created = timestamp(createdAt), at = timestamp(asOf);
  if (at < created || !POLICIES[policy]) throw Error('Replay không hợp lệ');
  const [pb, gb] = POLICIES[policy], pDue = deadline(created, pb);
  let gDue = deadline(created, gb), pDone = null, state = 'New', assignee = null;
  let assigned = null, rejects = 0, active = true, closedConsumed = 0, breached = false, breachAt = null;
  let lastResolved = null, closedAt = null, openReview = null, snapshot = null;
  const intervals = [{started_at: iso(created), ended_at: null}], reviews = [], messages = [];
  const observe = t => {if (active && !breached && t > gDue) {breached = true; breachAt = gDue + 1;}};
  const stop = t => {
    const i = intervals.at(-1); i.ended_at = iso(t); i.business_seconds = workSeconds(i.started_at, t);
    closedConsumed += i.business_seconds; active = false;
  };
  const resume = t => {
    gDue = deadline(t, Math.max(0, gb - closedConsumed));
    intervals.push({started_at: iso(t), ended_at: null}); active = true;
  };
  for (const e of [...events].sort((a,b) => timestamp(a.at)-timestamp(b.at) || (a.demo_event_seq ?? a.seq ?? 0)-(b.demo_event_seq ?? b.seq ?? 0))) {
    const t = timestamp(e.at), p = e.payload || {};
    if (t > at) continue;
    if (t < created) throw Error('Event trước ngày tạo');
    observe(t);
    switch (e.type) {
      case 'ticket_created': break;
      case 'agent_assigned':
        assigned = t; assignee = e.actor_id; state = 'In Progress';
        snapshot = {assigned_at: iso(t), first_response_sla_status_at_assignment: t > pDue ? 'breached' : 'pending', resolution_sla_status_at_assignment: breached ? 'breached' : 'pending'};
        break;
      case 'agent_public_reply': if (pDone == null) pDone = t; break;
      case 'status_waiting': stop(t); state = 'Waiting for Customer'; break;
      case 'customer_public_message': if (state === 'Waiting for Customer') {resume(t); state = 'In Progress';} break;
      case 'resolved': if (pDone == null) pDone = t; stop(t); state = 'Resolved'; lastResolved = t; break;
      case 'customer_reject':
        rejects++; resume(t); state = 'In Progress';
        if (rejects >= 3) {
          openReview = {review_key: `R${reviews.length+1}`, requested_at: iso(t), completed_at: null, handling_plan: null, _before: breached};
          reviews.push(openReview);
        }
        break;
      case 'review_completed':
        if (!openReview) throw Error('Không có review mở');
        openReview.completed_at = iso(t); openReview.handling_plan = p.handling_plan; openReview = null; break;
      case 'customer_confirm': state = 'Closed'; closedAt = t; break;
      case 'internal_note': break;
      default: throw Error(`Event không hợp lệ: ${e.type}`);
    }
    const key = {agent_public_reply:'content', customer_public_message:'content', internal_note:'content', resolved:'resolution_summary', customer_reject:'reason'}[e.type];
    if (key) messages.push({actor_id:e.actor_id, created_at:iso(t), visibility:e.type === 'internal_note' ? 'INTERNAL' : 'PUBLIC', content:p[key] || ''});
  }
  observe(at);
  const consumed = closedConsumed + (active ? workSeconds(intervals.at(-1).started_at, at) : 0);
  if (active) intervals.at(-1).business_seconds_as_of = workSeconds(intervals.at(-1).started_at, at);
  const pc = workSeconds(created, pDone ?? at), ps = (pDone ?? at) > pDue ? 'breached' : pDone == null ? 'pending' : 'met';
  const gs = breached ? 'breached' : ['Resolved','Closed'].includes(state) ? 'met' : 'pending';
  for (const r of reviews) {
    const begin = timestamp(r.requested_at), end = r.completed_at ? timestamp(r.completed_at) : at;
    r.wait_calendar_seconds = end - begin; r.wait_overlap_seconds = 0;
    for (const i of intervals) {
      const left = Math.max(begin, timestamp(i.started_at)), right = Math.min(end, i.ended_at ? timestamp(i.ended_at) : at);
      if (right >= left) r.wait_overlap_seconds += workSeconds(left, right);
    }
    r.breach_context = r._before ? 'before_request' : breachAt != null && begin <= breachAt && breachAt <= end ? 'during_wait' : 'none';
    delete r._before;
  }
  const clock = (status,running,c,b,due) => ({status,running,consumed_seconds:c,remaining_seconds:Math.max(0,b-c),due_at:iso(due),warning_level:warning(status,running,Math.max(0,b-c),due,at)});
  return {state, assignee_id:assignee, assigned_at:iso(assigned), closed_at:iso(closedAt), last_resolved_at:iso(lastResolved), rejection_count:rejects, open_review:openReview?.review_key ?? null, reviews, messages, resolution_intervals:intervals, snapshot, resolution_result_final:state === 'Closed', sla:{first_response:clock(ps,pDone == null,pc,pb,pDue),resolution:clock(gs,active,consumed,gb,active || ['Resolved','Closed'].includes(state) ? gDue : null)}};
}
