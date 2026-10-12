from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import json
import sqlite3
import pytest
from fastapi.testclient import TestClient
from backend.sla import iso,timestamp
from .conftest import create,act,headers
from .test_api import third_rejection,domain_code

TABLES=('tickets','ticket_events','messages','sla_intervals','ticket_sla','assignment_snapshots','ticket_reviews')


def dump(store):
    with store.connect() as conn:
        return {t:[tuple(r) for r in conn.execute(f'SELECT * FROM {t} ORDER BY rowid')] for t in TABLES}


def compete(client, requests):
    barrier=Barrier(2)
    def worker(pair):
        tid,user=pair
        # Real HTTP handlers in concurrent threads; each transaction opens its own connection.
        with TestClient(client.app) as local:
            barrier.wait(timeout=10)
            return local.post(f'/tickets/{tid}/claim',headers=headers(user),json={})
    with ThreadPoolExecutor(max_workers=2) as pool:
        return list(pool.map(worker,requests))


def test_concurrent_two_agents_same_ticket(env):
    client,clock,store=env
    tid=create(client)
    results=compete(client,[(tid,3),(tid,4)])
    assert sorted(r.status_code for r in results)==[200,409]
    assert domain_code(next(r for r in results if r.status_code==409))=='TICKET_ALREADY_ASSIGNED'
    with store.connect() as conn:
        ticket=conn.execute('SELECT * FROM tickets WHERE id=?',(tid,)).fetchone()
        assert ticket['assignee_id'] in (3,4) and ticket['status']=='IN_PROGRESS'
        assert conn.execute("SELECT COUNT(*) FROM ticket_events WHERE ticket_id=? AND event_type='agent_assigned'",(tid,)).fetchone()[0]==1
        assert conn.execute('SELECT COUNT(*) FROM assignment_snapshots WHERE ticket_id=?',(tid,)).fetchone()[0]==1


def test_concurrent_one_agent_two_tickets_at_capacity_two(env):
    client,clock,store=env
    for _ in range(2):
        assert act(client,create(client),'claim').status_code==200
    a,b=create(client),create(client)
    results=compete(client,[(a,3),(b,3)])
    assert sorted(r.status_code for r in results)==[200,409]
    assert domain_code(next(r for r in results if r.status_code==409))=='AGENT_CAPACITY_REACHED'
    with store.connect() as conn:
        assert conn.execute("SELECT COUNT(*) FROM tickets WHERE assignee_id=3 AND status='IN_PROGRESS'").fetchone()[0]==3
        assert conn.execute("SELECT COUNT(*) FROM tickets WHERE id IN (?,?) AND status='NEW'",(a,b)).fetchone()[0]==1


def test_rejection_atomic_rollback_on_projection_failure(env):
    client,clock,store=env
    tid=create(client)
    assert act(client,tid,'claim').status_code==200
    for _ in range(2):
        assert act(client,tid,'resolve',3,{'resolution_summary':'Result'}).status_code==200
        assert act(client,tid,'reject',1,{'reason':'Not fixed'}).status_code==200
    assert act(client,tid,'resolve',3,{'resolution_summary':'Third result'}).status_code==200
    before=dump(store)
    with store.connect(write=True) as conn:
        conn.execute("CREATE TRIGGER test_fault BEFORE INSERT ON ticket_reviews BEGIN SELECT RAISE(ABORT,'injected persistence failure'); END")
    with pytest.raises(sqlite3.IntegrityError,match='injected persistence failure'):
        act(client,tid,'reject',1,{'reason':'Third refusal'})
    assert dump(store)==before
    with store.connect(write=True) as conn:
        conn.execute('DROP TRIGGER test_fault')
    assert act(client,tid,'reject',1,{'reason':'Third refusal'}).status_code==200
    with store.connect() as conn:
        assert conn.execute('SELECT COUNT(*) FROM ticket_reviews WHERE ticket_id=?',(tid,)).fetchone()[0]==1


def test_append_only_and_rebuild_all_projections(env):
    client,clock,store=env
    tid=create(client)
    third_rejection(client,tid)
    assert act(client,tid,'notes',3,{'content':'Internal evidence'}).status_code==200
    baseline=dump(store)
    with pytest.raises(sqlite3.IntegrityError,match='append only'):
        with store.connect(write=True) as conn:
            conn.execute("UPDATE ticket_events SET payload='{}' WHERE ticket_id=?",(tid,))
    with pytest.raises(sqlite3.IntegrityError,match='append only'):
        with store.connect(write=True) as conn:
            conn.execute('DELETE FROM ticket_events WHERE ticket_id=?',(tid,))
    with pytest.raises(sqlite3.IntegrityError,match='policy immutable'):
        with store.connect(write=True) as conn:
            conn.execute("UPDATE sla_policies SET resolution_seconds=1 WHERE id='HIGH'")
    with store.connect(write=True) as conn:
        conn.execute("UPDATE tickets SET title='corrupted',rejection_count=100 WHERE id=?",(tid,))
        conn.execute('DELETE FROM messages WHERE ticket_id=?',(tid,))
        conn.execute('DELETE FROM ticket_reviews WHERE ticket_id=?',(tid,))
        conn.execute('DELETE FROM sla_intervals WHERE ticket_id=?',(tid,))
        store.refresh(conn,tid,clock())
    assert dump(store)==baseline


def test_zero_intervals_raw_clock_and_event_ids(env):
    client,clock,store=env
    clock.set('2026-10-05T09:00:00.999999+07:00')
    tid=create(client)
    assert act(client,tid,'claim').status_code==200
    assert act(client,tid,'resolve',3,{'resolution_summary':'Instant result'}).status_code==200
    with store.connect() as conn:
        events=conn.execute('SELECT * FROM ticket_events WHERE ticket_id=? ORDER BY event_id',(tid,)).fetchall()
        assert [r['event_type'] for r in events]==['ticket_created','agent_assigned','resolved']
        assert len({r['event_id'] for r in events})==3
        assert all(r['occurred_at']=='2026-10-05T09:00:00+07:00' for r in events)
        assert all('.999999' in r['occurred_at_raw'] for r in events)
        intervals=conn.execute('SELECT * FROM sla_intervals WHERE ticket_id=?',(tid,)).fetchall()
        assert len(intervals)==2 and all(r['business_seconds']==0 for r in intervals)
        assert all(r['start_event_id']==events[0]['event_id'] and r['end_event_id']==events[2]['event_id'] for r in intervals)
    before=dump(store)
    clock.set('2026-10-05T08:59:59+07:00')
    assert act(client,tid,'reject',1,{'reason':'Clock earlier'}).status_code==422
    assert dump(store)==before
