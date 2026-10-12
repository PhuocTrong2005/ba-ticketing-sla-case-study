"""Event replay using working-day intersections (no reference-checker imports)."""
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

TZ = ZoneInfo('Asia/Ho_Chi_Minh')
POLICIES = {'HIGH': (3600, 28800), 'NORMAL': (7200, 57600)}
STATES = {'New': 'NEW', 'In Progress': 'IN_PROGRESS', 'Waiting for Customer': 'WAITING_FOR_CUSTOMER', 'Resolved': 'RESOLVED', 'Closed': 'CLOSED'}


def timestamp(value):
    dt = datetime.fromisoformat(value) if isinstance(value, str) else value
    if dt.tzinfo is None:
        raise ValueError('Timezone offset required')
    return dt.astimezone(TZ).replace(microsecond=0)


def iso(value):
    return value.isoformat(timespec='seconds') if value is not None else None


def next_work(value):
    value = timestamp(value)
    while True:
        start = datetime.combine(value.date(), time(8), TZ)
        end = start + timedelta(hours=9)
        if value.weekday() < 5 and value < end:
            return max(value, start)
        value = start + timedelta(days=1)


def work_seconds(start, end):
    start, end = timestamp(start), timestamp(end)
    if end < start:
        raise ValueError('Negative time interval')
    total = 0
    cursor = start.date()
    while cursor <= end.date():
        if cursor.weekday() < 5:
            left = max(start, datetime.combine(cursor, time(8), TZ))
            right = min(end, datetime.combine(cursor, time(17), TZ))
            total += max(0, int((right - left).total_seconds()))
        cursor += timedelta(days=1)
    return total


def deadline(start, seconds):
    cursor = next_work(start)
    while True:
        close = datetime.combine(cursor.date(), time(17), TZ)
        available = int((close - cursor).total_seconds())
        if seconds <= available:
            return cursor + timedelta(seconds=seconds)
        seconds -= available
        cursor = next_work(close)


def warning(status, running, remaining, due, at):
    if status == 'breached':
        return 'breached'
    if status == 'met' or not running:
        return 'none'
    if at == due:
        return 'due'
    if remaining < 900:
        return 'emphasized'
    return 'soft' if remaining < 3600 else 'none'


def replay(created_at, policy, events, as_of, budgets=None):
    """Rebuild facts at as_of from ordered accepted events; no expected fields read."""
    created, at = timestamp(created_at), timestamp(as_of)
    if at < created:
        raise ValueError('as_of before ticket creation')
    pb, gb = budgets or POLICIES[policy]
    p_due, g_due = deadline(created, pb), deadline(created, gb)
    p_done = None
    state, assignee, assigned, rejects = 'New', None, None, 0
    intervals = [{'started_at': iso(created), 'ended_at': None}]
    segment_deadlines = [g_due]
    closed_consumed = 0
    active = True
    breached, breach_at = False, None
    last_resolved = closed_at = None
    reviews, open_review = [], None
    messages = []
    cycle_id = 0
    snapshot = None
    rows = sorted(events, key=lambda e: (timestamp(e['at']), e.get('event_id', e.get('seq', 0))))

    def observe(until):
        nonlocal breached, breach_at
        if active and not breached and until > g_due:
            breached = True
            breach_at = g_due + timedelta(seconds=1)

    def stop(until):
        nonlocal closed_consumed, active
        interval = intervals[-1]
        interval['ended_at'] = iso(until)
        interval['business_seconds'] = work_seconds(interval['started_at'], until)
        closed_consumed += interval['business_seconds']
        active = False

    def resume(until):
        nonlocal active, g_due
        g_due = deadline(until, max(0, gb - closed_consumed))
        intervals.append({'started_at': iso(until), 'ended_at': None})
        segment_deadlines.append(g_due)
        active = True

    for event in rows:
        t = timestamp(event['at'])
        if t > at:
            continue
        if t < created:
            raise ValueError('Event before creation')
        kind = event['type']
        payload = event.get('payload', {})
        eid = event.get('event_id', event.get('seq', 0))
        observe(t)
        if kind == 'ticket_created':
            cycle_id = eid
        elif kind == 'agent_assigned':
            assigned, assignee, state = t, event.get('actor_id'), 'In Progress'
            snapshot = {'assigned_at': iso(t), 'first_response_sla_status_at_assignment': 'breached' if t > p_due else 'pending', 'resolution_sla_status_at_assignment': 'breached' if breached else 'pending', 'assignment_event_id': eid}
        elif kind == 'agent_public_reply':
            if p_done is None:
                p_done = t
        elif kind == 'status_waiting':
            stop(t)
            state = 'Waiting for Customer'
        elif kind == 'customer_public_message':
            if state == 'Waiting for Customer':
                resume(t)
                state = 'In Progress'
        elif kind == 'resolved':
            if p_done is None:
                p_done = t
            stop(t)
            state, last_resolved = 'Resolved', t
        elif kind == 'customer_reject':
            rejects += 1
            cycle_id = eid
            resume(t)
            state = 'In Progress'
            if rejects >= 3:
                open_review = {'review_key': f'R{len(reviews)+1}', 'requested_at': iso(t), 'completed_at': None, 'resolution_cycle_id': cycle_id, 'requested_event_id': eid, 'completed_event_id': None, 'reviewed_by': None, 'handling_plan': None, '_breached_before': breached}
                reviews.append(open_review)
        elif kind == 'review_completed':
            if open_review is None:
                raise ValueError('No open review to complete')
            open_review.update(completed_at=iso(t), completed_event_id=eid, reviewed_by=event.get('actor_id'), handling_plan=payload.get('handling_plan'))
            open_review = None
        elif kind == 'customer_confirm':
            state, closed_at = 'Closed', t
        elif kind == 'internal_note':
            pass
        elif kind != 'ticket_created':
            raise ValueError(f'Unknown accepted event {kind}')
        content_key = {'agent_public_reply': 'content', 'customer_public_message': 'content', 'internal_note': 'content', 'resolved': 'resolution_summary', 'customer_reject': 'reason'}.get(kind)
        if content_key:
            messages.append({'source_event_id': eid, 'actor_id': event.get('actor_id'), 'created_at': iso(t), 'visibility': 'INTERNAL' if kind == 'internal_note' else 'PUBLIC', 'content': payload.get(content_key, '')})
    observe(at)
    consumed = closed_consumed + (work_seconds(intervals[-1]['started_at'], at) if active else 0)
    if active:
        intervals[-1]['business_seconds_as_of'] = work_seconds(intervals[-1]['started_at'], at)
    p_consumed = work_seconds(created, p_done or at)
    ps = ('met' if p_done <= p_due else 'breached') if p_done is not None else ('breached' if at > p_due else 'pending')
    gs = 'breached' if breached else 'met' if state in ('Resolved', 'Closed') else 'pending'
    p_remaining, g_remaining = max(0, pb - p_consumed), max(0, gb - consumed)
    for review in reviews:
        begin = timestamp(review['requested_at'])
        end = timestamp(review['completed_at']) if review['completed_at'] else at
        overlap = 0
        for interval in intervals:
            left = max(begin, timestamp(interval['started_at']))
            right = min(end, timestamp(interval['ended_at']) if interval['ended_at'] else at)
            if right >= left:
                overlap += work_seconds(left, right)
        review['wait_calendar_seconds'] = int((end - begin).total_seconds())
        review['wait_overlap_seconds'] = overlap
        review['breach_context'] = 'before_request' if review.pop('_breached_before') else 'during_wait' if breach_at is not None and begin <= breach_at <= end else 'none'
    clocks = {
        'first_response': {'due_at': iso(p_due), 'consumed_seconds': p_consumed, 'remaining_seconds': p_remaining, 'status': ps, 'warning_level': warning(ps, p_done is None, p_remaining, p_due, at), 'running': p_done is None},
        'resolution': {'due_at': iso(g_due) if active or state in ('Resolved', 'Closed') else None, 'consumed_seconds': consumed, 'remaining_seconds': g_remaining, 'status': gs, 'warning_level': warning(gs, active, g_remaining, g_due, at), 'running': active}}
    p_interval = {'started_at': iso(created), 'ended_at': iso(p_done)}
    p_interval['business_seconds' if p_done else 'business_seconds_as_of'] = p_consumed
    return {'state': state, 'assignee_id': assignee, 'assigned_at': iso(assigned), 'closed_at': iso(closed_at), 'last_resolved_at': iso(last_resolved), 'rejection_count': rejects, 'open_review': open_review['review_key'] if open_review else None, 'reviews': reviews, 'resolution_intervals': intervals, 'first_response_intervals': [p_interval], 'segment_deadlines': [iso(x) for x in segment_deadlines], 'snapshot': snapshot, 'messages': messages, 'sla': clocks, 'resolution_result_final': state == 'Closed'}
