"""SQL aggregation over a transient, event-replayed as_of snapshot."""
from pathlib import Path
from .sla import timestamp, iso, STATES

QUERIES = Path(__file__).parents[1] / "sql/queries"
from .store import fail


def report(store, user, metric, at, start=None, end=None, priority=None, agent_id=None):
    store.role(user,('MANAGER',))
    if metric not in [f'M-{i:02}' for i in range(1,8)]:
        fail(404,'Unknown metric')
    if priority not in (None,'HIGH','NORMAL'):
        fail(422,'Invalid priority')
    if metric == 'M-06' and priority is not None:
        fail(422,'M-06 actual capacity cannot be filtered by priority')
    if metric in ('M-01','M-02','M-03'):
        if start is None or end is None or timestamp(start) >= timestamp(end):
            fail(422,'Valid from/to period required')
        start,end = iso(timestamp(start)),iso(timestamp(end))
    now = timestamp(at)
    with store.connect() as conn:
        if agent_id is not None:
            agent = conn.execute("SELECT id FROM users WHERE id=? AND role='AGENT'",(agent_id,)).fetchone()
            if not agent:
                fail(422,'Invalid agent filter')
        conn.execute('CREATE TEMP TABLE snapshot(id INTEGER, priority TEXT, assignee_id INTEGER, status TEXT, created_at TEXT, closed_at TEXT, p_status TEXT, g_status TEXT, rejection_count INTEGER, last_resolved_at TEXT)')
        states = {}
        for row in conn.execute('SELECT id FROM tickets ORDER BY id').fetchall():
            events = store.events(conn,row['id'])
            if timestamp(events[0]['at']) > now:
                continue
            value = store.project(conn,row['id'],now)
            states[row['id']] = value
            src = value['source']
            conn.execute('INSERT INTO snapshot VALUES (?,?,?,?,?,?,?,?,?,?)',(row['id'],src['priority'],value['assignee_id'],STATES[value['state']],value['created_at'],value['closed_at'],value['sla']['first_response']['status'],value['sla']['resolution']['status'],value['rejection_count'],value['last_resolved_at']))
        where, params = [],[]
        if priority:
            where.append('priority=?');params.append(priority)
        if agent_id is not None:
            where.append('assignee_id=?');params.append(agent_id)
        condition = ' AND '.join(where) or '1=1'
        matched = conn.execute(f'SELECT * FROM snapshot WHERE {condition} ORDER BY id',params).fetchall()
        unclosed = conn.execute(f"SELECT COUNT(*) FROM snapshot WHERE {condition} AND status!='CLOSED'",params).fetchone()[0]
        out = {'metric_code':metric,'as_of':iso(now),'period':{'from':start,'to':end,'boundary':'[from,to)','timezone':'Asia/Ho_Chi_Minh'},'filters':{'priority':priority,'agent_id':agent_id},'numerator':None,'denominator':None}
        if metric in ('M-01','M-02','M-03'):
            query = (QUERIES / (metric.lower().replace('-','')+'.sql')).read_text().format(filters=condition)
            counts = conn.execute(query,params+[start,end]).fetchone()
            n,d = counts['numerator'] or 0, counts['denominator'] or 0
            out.update(numerator=n,denominator=d,ratio=n/d if d else None,display=f'{n}/{d}' if d else 'không có dữ liệu')
            if metric == 'M-01':
                out['pending_count'] = counts['pending'] or 0
            else:
                out.update(unclosed_count=unclosed,unclosed_note=f'Còn {unclosed} ticket chưa Closed tại as_of, chưa tính vào các tỷ lệ này; không giới hạn ngày tạo.')
        elif metric == 'M-04':
            out['items'] = [dict(id=r['id'],first_response_breached=r['p_status']=='breached',resolution_breached=r['g_status']=='breached') for r in matched if r['status']!='CLOSED' and 'breached' in (r['p_status'],r['g_status'])]
        elif metric == 'M-05':
            out['items'] = [{'id':r['id'],'resolved_at':r['last_resolved_at'],'wait_calendar_seconds':int((now-timestamp(r['last_resolved_at'])).total_seconds())} for r in matched if r['status']=='RESOLVED']
        elif metric == 'M-06':
            agents = conn.execute("SELECT id,display_name FROM users WHERE role='AGENT' AND (? IS NULL OR id=?) ORDER BY id",(agent_id,agent_id)).fetchall()
            out['items'] = []
            for agent in agents:
                counts = {r['status']:r['n'] for r in conn.execute((QUERIES / 'm06.sql').read_text(),(agent['id'],))}
                load = counts.get('IN_PROGRESS',0)
                out['items'].append({'agent_id':agent['id'],'display_name':agent['display_name'],'counts_by_status':{s:counts.get(s,0) for s in STATES.values()},'in_progress_count':load,'capacity_state':'available' if load<3 else 'at_limit' if load==3 else 'overloaded'})
        else:
            out['items'] = [{'ticket_id':r['id'],**review} for r in matched for review in states[r['id']]['reviews']]
        return out
