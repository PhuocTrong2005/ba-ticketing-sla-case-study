"""SQLite transactions, append-only events and replayable projections."""
import json
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from .sla import replay, timestamp, iso, STATES

SCHEMA = Path(__file__).with_name('schema.sql')
USERS = [(1,'Customer A','CUSTOMER'),(2,'Customer B','CUSTOMER'),(3,'Agent A','AGENT'),(4,'Agent B','AGENT'),(5,'Agent C','AGENT'),(6,'Manager','MANAGER')]


class DomainError(Exception):
    def __init__(self, status, message, code=None):
        self.status, self.message, self.code = status, message, code


def fail(status, message, code=None):
    raise DomainError(status, message, code)


class Store:
    def __init__(self, path):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as setup:
            setup.execute('PRAGMA journal_mode=WAL')
            setup.executescript(SCHEMA.read_text())
        with self.connect(write=True) as conn:
            conn.executemany('INSERT OR IGNORE INTO users VALUES (?,?,?)', USERS)
            conn.executemany('INSERT OR IGNORE INTO sla_policies VALUES (?,?,?)', [('HIGH',3600,28800),('NORMAL',7200,57600)])

    @contextmanager
    def connect(self, write=False):
        conn = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys=ON')
        try:
            conn.execute('BEGIN IMMEDIATE' if write else 'BEGIN')
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def identity(self, user_id):
        with self.connect() as conn:
            try:
                uid = int(user_id)
            except (ValueError, TypeError):
                fail(401,'Missing or invalid demo identity')
            user = conn.execute('SELECT * FROM users WHERE id=?',(uid,)).fetchone()
            if not user:
                fail(401,'Missing or invalid demo identity')
            return dict(user)

    @staticmethod
    def role(user, roles, review=False):
        if review and user['role'] == 'CUSTOMER':
            fail(404,'Not found')
        if user['role'] not in roles:
            fail(403,'Role not permitted')

    @staticmethod
    def ticket(conn, ticket_id, user, claim=False):
        ticket = conn.execute('SELECT * FROM tickets WHERE id=?',(ticket_id,)).fetchone()
        if not ticket or (user['role'] == 'CUSTOMER' and ticket['customer_id'] != user['id']):
            fail(404,'Not found')
        if user['role'] == 'AGENT' and not claim and ticket['assignee_id'] != user['id']:
            fail(403,'Not assigned to this Agent')
        return dict(ticket)

    @staticmethod
    def events(conn, ticket_id):
        rows = conn.execute('SELECT * FROM ticket_events WHERE ticket_id=? ORDER BY occurred_at,event_id',(ticket_id,)).fetchall()
        return [{'event_id':r['event_id'],'type':r['event_type'],'at':r['occurred_at'],'actor_id':r['actor_id'],'state_before':r['state_before'],'state_after':r['state_after'],'payload':json.loads(r['payload'])} for r in rows]

    def project(self, conn, ticket_id, as_of):
        events = self.events(conn,ticket_id)
        source = next(e for e in events if e['type'] == 'ticket_created')
        data = source['payload']
        policy = conn.execute('SELECT * FROM sla_policies WHERE id=?',(data['policy_id'],)).fetchone()
        result = replay(source['at'],data['policy_id'],events,as_of,(policy['first_response_seconds'],policy['resolution_seconds']))
        result['source'] = data
        result['created_at'] = source['at']
        return result

    @staticmethod
    def text(payload, key):
        value = payload.get(key)
        if not isinstance(value,str) or not value.strip():
            fail(422,f'{key} must be nonblank')
        return value.strip()

    def refresh(self, conn, ticket_id, at):
        result = self.project(conn,ticket_id,at)
        data = result['source']
        conn.execute('UPDATE tickets SET customer_id=?,policy_id=?,priority=?,title=?,description=?,created_at=?,status=?,assignee_id=?,assigned_at=?,closed_at=?,rejection_count=? WHERE id=?',(data['customer_id'],data['policy_id'],data['priority'],data['title'],data['description'],result['created_at'],STATES[result['state']],result['assignee_id'],result['assigned_at'],result['closed_at'],result['rejection_count'],ticket_id))
        for table in ('messages','sla_intervals','ticket_sla','assignment_snapshots','ticket_reviews'):
            conn.execute(f'DELETE FROM {table} WHERE ticket_id=?',(ticket_id,))
        for message in result['messages']:
            conn.execute('INSERT INTO messages VALUES (?,?,?,?,?,?)',(message['source_event_id'],ticket_id,message['actor_id'],message['created_at'],message['visibility'],message['content']))
        events = self.events(conn,ticket_id)
        starts, ends = [events[0]['event_id']], []
        p_end = None
        for event in events:
            typ, eid = event['type'],event['event_id']
            if typ in ('agent_public_reply','resolved') and p_end is None:
                p_end = eid
            if typ in ('status_waiting','resolved'):
                ends.append(eid)
            if typ == 'customer_reject' or (typ == 'customer_public_message' and event['state_before'] == 'WAITING_FOR_CUSTOMER'):
                starts.append(eid)
        for clock, intervals in [('first_response',result['first_response_intervals']),('resolution',result['resolution_intervals'])]:
            for ordinal, interval in enumerate(intervals):
                start_id = events[0]['event_id'] if clock == 'first_response' else starts[ordinal]
                end_id = p_end if clock == 'first_response' else ends[ordinal] if ordinal < len(ends) else None
                conn.execute('INSERT INTO sla_intervals VALUES (?,?,?,?,?,?,?,?)',(ticket_id,clock,ordinal,interval['started_at'],interval['ended_at'],interval.get('business_seconds'),start_id,end_id))
            sla = result['sla'][clock]
            conn.execute('INSERT INTO ticket_sla VALUES (?,?,?,?,?,?)',(ticket_id,clock,sum(x.get('business_seconds',0) for x in intervals),sla['due_at'],sla['status'],sla['remaining_seconds']))
        if result['snapshot']:
            snap = result['snapshot']
            conn.execute('INSERT INTO assignment_snapshots VALUES (?,?,?,?,?)',(ticket_id,snap['assignment_event_id'],snap['assigned_at'],snap['first_response_sla_status_at_assignment'],snap['resolution_sla_status_at_assignment']))
        for review in result['reviews']:
            conn.execute('INSERT INTO ticket_reviews VALUES (?,?,?,?,?,?,?,?,?)',(ticket_id,review['review_key'],review['resolution_cycle_id'],review['requested_event_id'],review['completed_event_id'],review['requested_at'],review['completed_at'],review['reviewed_by'],json.dumps(review['handling_plan']) if review['handling_plan'] else None))
        return result

    @staticmethod
    def append(conn, ticket_id, user, kind, raw, before, after, policy, payload):
        raw_dt = raw if isinstance(raw,str) else raw.isoformat()
        at = iso(timestamp(raw))
        last = conn.execute('SELECT occurred_at FROM ticket_events WHERE ticket_id=? ORDER BY event_id DESC LIMIT 1',(ticket_id,)).fetchone()
        if last and timestamp(last['occurred_at']) > timestamp(at):
            fail(422,'Clock cannot precede latest ticket event')
        conn.execute('INSERT INTO ticket_events(ticket_id,actor_id,occurred_at,occurred_at_raw,event_type,state_before,state_after,policy_id,payload) VALUES (?,?,?,?,?,?,?,?,?)',(ticket_id,user['id'],at,raw_dt,kind,before,after,policy,json.dumps(payload,ensure_ascii=False)))
        return at

    def create(self,user,payload,raw):
        self.role(user,('CUSTOMER',))
        title, description = self.text(payload,'title'),self.text(payload,'description')
        priority = payload.get('priority')
        if priority not in ('HIGH','NORMAL'):
            fail(422,'priority must be HIGH or NORMAL')
        at = iso(timestamp(raw))
        source = {'customer_id':user['id'],'title':title,'description':description,'priority':priority,'policy_id':priority}
        with self.connect(write=True) as conn:
            tid = conn.execute('INSERT INTO tickets(customer_id,policy_id,priority,title,description,created_at,status) VALUES (?,?,?,?,?,?,?)',(user['id'],priority,priority,title,description,at,'NEW')).lastrowid
            self.append(conn,tid,user,'ticket_created',raw,None,'NEW',priority,source)
            self.refresh(conn,tid,at)
            return self.view(conn,tid,user,at)

    def action(self,user,ticket_id,action,payload,raw):
        roles = {'claim':('AGENT',),'messages':('CUSTOMER','AGENT'),'notes':('AGENT',),'waiting':('AGENT',),'resolve':('AGENT',),'confirm':('CUSTOMER',),'reject':('CUSTOMER',),'complete':('MANAGER',)}
        self.role(user,roles[action],review=action=='complete')
        at = iso(timestamp(raw))
        with self.connect(write=True) as conn:
            ticket = self.ticket(conn,ticket_id,user,claim=action=='claim')
            state, policy = ticket['status'],ticket['policy_id']
            if state == 'CLOSED':
                fail(409,'Ticket Closed','TICKET_CLOSED')
            latest = conn.execute('SELECT occurred_at FROM ticket_events WHERE ticket_id=? ORDER BY event_id DESC LIMIT 1',(ticket_id,)).fetchone()
            if timestamp(latest['occurred_at']) > timestamp(at):
                fail(422,'Clock cannot precede latest ticket event')
            projected = self.project(conn,ticket_id,at)
            data, after = {}, state
            if action == 'claim':
                if ticket['assignee_id'] is not None:
                    fail(409,'Already assigned','TICKET_ALREADY_ASSIGNED')
                if state != 'NEW':
                    fail(409,'Invalid state','INVALID_TICKET_STATE')
                count = conn.execute("SELECT COUNT(*) FROM tickets WHERE assignee_id=? AND status='IN_PROGRESS'",(user['id'],)).fetchone()[0]
                if count >= 3:
                    fail(409,'Agent capacity reached','AGENT_CAPACITY_REACHED')
                kind, after = 'agent_assigned','IN_PROGRESS'
            elif action in ('messages','notes'):
                if state not in ('NEW','IN_PROGRESS','WAITING_FOR_CUSTOMER'):
                    fail(409,'Invalid state','INVALID_TICKET_STATE')
                data['content'] = self.text(payload,'content')
                kind = 'internal_note' if action == 'notes' else 'agent_public_reply' if user['role']=='AGENT' else 'customer_public_message'
                if kind == 'customer_public_message' and state == 'WAITING_FOR_CUSTOMER':
                    after = 'IN_PROGRESS'
            elif action == 'waiting':
                if state != 'IN_PROGRESS' or projected['sla']['first_response']['running']:
                    fail(409,'Waiting requires first public reply','INVALID_TICKET_STATE')
                kind, after = 'status_waiting','WAITING_FOR_CUSTOMER'
            elif action == 'resolve':
                if state != 'IN_PROGRESS':
                    fail(409,'Invalid state','INVALID_TICKET_STATE')
                if projected['open_review']:
                    fail(409,'Manager review required','REVIEW_REQUIRED')
                data['resolution_summary'] = self.text(payload,'resolution_summary')
                resolution = projected['sla']['resolution']
                data['resolution_snapshot'] = {
                    'remaining_seconds':resolution['remaining_seconds'],
                    'consumed_seconds':resolution['consumed_seconds'],
                    'due_at':resolution['due_at'],
                    'status':'breached' if resolution['status']=='breached' else 'met'}
                kind, after = 'resolved','RESOLVED'
            elif action in ('confirm','reject'):
                if state != 'RESOLVED':
                    fail(409,'Invalid state','INVALID_TICKET_STATE')
                kind, after = ('customer_confirm','CLOSED') if action == 'confirm' else ('customer_reject','IN_PROGRESS')
                if action == 'reject':
                    data['reason'] = self.text(payload,'reason')
            else:
                if not projected['open_review']:
                    fail(409,'No open review','INVALID_TICKET_STATE')
                plan = payload.get('handling_plan') or {}
                plan['unresolved_reason'] = self.text(plan,'unresolved_reason')
                plan['next_action'] = self.text(plan,'next_action')
                if type(plan.get('needs_expert_input')) is not bool:
                    fail(422,'needs_expert_input must be boolean')
                data['handling_plan'] = plan
                kind = 'review_completed'
            self.append(conn,ticket_id,user,kind,raw,state,after,policy,data)
            self.refresh(conn,ticket_id,at)
            return self.view(conn,ticket_id,user,at)

    def view(self,conn,ticket_id,user,at,list_view=False):
        self.ticket(conn,ticket_id,user)
        result = self.project(conn,ticket_id,at)
        src = result['source']
        view = {k:src[k] for k in ('title','description','priority','policy_id','customer_id')}
        view.update(id=ticket_id,status=STATES[result['state']],assignee_id=result['assignee_id'],created_at=result['created_at'],assigned_at=result['assigned_at'],closed_at=result['closed_at'])
        view['messages'] = [m for m in result['messages'] if user['role'] != 'CUSTOMER' or m['visibility'] == 'PUBLIC']
        if user['role'] != 'CUSTOMER':
            view.update(sla=result['sla'],rejection_count=result['rejection_count'],needs_manager_review=bool(result['open_review']),reviews=result['reviews'],assignment_snapshot=result['snapshot'])
            if list_view:
                view.pop('messages')
                view['sla'] = {clock:{'status':v['status'],'warning_level':v['warning_level'],'remaining_display':display_duration(v['remaining_seconds']),'due_at':v['due_at']} for clock,v in result['sla'].items()}
        return view


def display_duration(seconds):
    if seconds < 60:
        return 'Dưới 1 phút'
    minutes = seconds // 60
    return f'{minutes} phút' if minutes < 60 else f'{minutes//60} giờ {minutes%60} phút'
