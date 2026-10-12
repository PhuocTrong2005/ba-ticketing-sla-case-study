import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from backend.app import create_app
from backend.sla import timestamp, STATES
from .conftest import Clock,headers,create,act
from .test_sla import ROWS,fixture_result


def domain_code(response):
    return response.json()['detail']['error_code']


def event_count(store,tid):
    with store.connect() as conn:
        return conn.execute('SELECT COUNT(*) FROM ticket_events WHERE ticket_id=?',(tid,)).fetchone()[0]


@pytest.mark.parametrize('row',ROWS,ids=[r['scenario_id'] for r in ROWS])
def test_fixture_through_http(row,tmp_path):
    """Fixture actor/text adapter is test-only; never edits source expected values."""
    clock=Clock(row['created_at'])
    app=create_app(tmp_path/'fixture.sqlite3',clock)
    with TestClient(app) as client:
        tid=create(client,row['policy_id'])
        events=[(e['at'],e['seq'],e,False) for e in row['events']]
        events += [(e['at'],e['step_seq'],e,True) for e in row.get('expected_rejected_actions',[])]
        routes={
            'agent_assigned':('claim',3,{}),
            'agent_public_reply':('messages',3,{'content':'Scenario public response'}),
            'customer_public_message':('messages',1,{'content':'Scenario customer information'}),
            'internal_note':('notes',3,{'content':'Scenario internal note'}),
            'status_waiting':('waiting',3,{}),
            'resolved':('resolve',3,{'resolution_summary':'Scenario resolution'}),
            'resolved_attempt':('resolve',3,{'resolution_summary':'Blocked scenario resolution'}),
            'customer_reject':('reject',1,{'reason':'Scenario still unresolved'}),
            'customer_confirm':('confirm',1,{}),
            'review_completed':('reviews/complete',6,{'handling_plan':{'unresolved_reason':'Root cause','next_action':'Alternative plan','needs_expert_input':False}})}
        for _,__,event,rejected in sorted(events,key=lambda e:(timestamp(e[0]),e[1])):
            clock.set(event.get('at_raw',event['at']))
            action,user,payload=routes[event['type']]
            before=event_count(app.state.store,tid)
            response=act(client,tid,action,user,payload)
            if rejected:
                assert response.status_code==event['http_status'],response.text
                assert domain_code(response)==event['error_code']
                assert event_count(app.state.store,tid)==before
            else:
                assert response.status_code==200,(row['scenario_id'],event,response.text)
        clock.set(row['as_of'])
        response=client.get(f'/tickets/{tid}',headers=headers(6))
        assert response.status_code==200
        assert response.json()['status']==STATES[row['expected_ticket_state']]
        with app.state.store.connect() as conn:
            actual=fixture_result(app.state.store.project(conn,tid,row['as_of']))
            # Compare persisted closed/open intervals and snapshots with approved fixture.
            persisted=conn.execute("SELECT started_at,ended_at,business_seconds FROM sla_intervals WHERE ticket_id=? AND clock_type='resolution' ORDER BY ordinal",(tid,)).fetchall()
            accepted_events=app.state.store.events(conn,tid)
            latest=app.state.store.project(conn,tid,accepted_events[-1]['at'])
            # Persisted projections represent latest events, never historical as_of.
            # Historical fixture values are independently compared below.
            expected=latest['resolution_intervals'] if timestamp(accepted_events[-1]['at'])>timestamp(row['as_of']) else row['expected_resolution_intervals']
            assert len(persisted)==len(expected)
            for stored, target in zip(persisted,expected):
                assert stored['started_at']==target['started_at'] and stored['ended_at']==target['ended_at']
                assert stored['business_seconds']==target.get('business_seconds')
            snap=conn.execute('SELECT * FROM assignment_snapshots WHERE ticket_id=?',(tid,)).fetchone()
            for clock_name in ('first_response','resolution'):
                key=clock_name+'_sla_status_at_assignment'
                assert (snap[key] if snap else None)==row['expected_'+key]
            events=app.state.store.events(conn,tid)
            for event in events:
                if event['type']=='resolved':
                    # No later same-second event may be allowed to alter this event's snapshot.
                    from backend.sla import replay
                    prefix=[e for e in events if e['event_id']<=event['event_id']]
                    at_result=replay(row['created_at'],row['policy_id'],prefix,event['at'])
                    expected_snapshot={k:at_result['sla']['resolution'][k] for k in ('remaining_seconds','consumed_seconds','due_at','status')}
                    assert event['payload']['resolution_snapshot']==expected_snapshot

        for field,value in actual.items():
            assert value==row[field],(row['scenario_id'],field,value,row[field])


def test_roles_privacy_and_queue(env):
    client,clock,store=env
    tid=create(client)
    assert client.get('/tickets').status_code==401
    assert client.get('/tickets',headers=headers(999)).status_code==401
    assert client.post('/tickets',headers=headers(3),json={}).status_code==403
    assert client.get(f'/tickets/{tid}',headers=headers(2)).status_code==404
    assert client.get(f'/tickets/{tid}',headers=headers(3)).status_code==403
    queue=client.get('/tickets/queue',headers=headers(3)).json()
    assert set(queue[0])=={'id','title','priority','first_response_due_at','created_at'}
    assert act(client,tid,'messages',3,{'content':'before claim'}).status_code==403
    assert act(client,tid,'claim').status_code==200
    assert act(client,tid,'notes',3,{'content':'SECRET-NOTE'}).status_code==200
    own=client.get(f'/tickets/{tid}',headers=headers(1)).json()
    assert 'sla' not in own and 'reviews' not in own and 'SECRET-NOTE' not in str(own)
    manager=client.get(f'/tickets/{tid}',headers=headers(6)).json()
    assert 'SECRET-NOTE' in str(manager) and 'sla' in manager
    assert client.get(f'/tickets/{tid}',headers=headers(4)).status_code==403
    assert act(client,tid,'resolve',4,{}).status_code==403
    for action in ('claim','messages','notes','resolve'):
        assert act(client,tid,action,6,{}).status_code==403
    assert client.get(f'/tickets/{tid}/reviews',headers=headers(1)).status_code==404
    assert client.get('/tickets/999/reviews',headers=headers(1)).status_code==404
    assert client.get(f'/tickets/{tid}/reviews',headers=headers(3)).status_code==403


def test_validation_state_order_and_forbidden_fields(env):
    client,clock,store=env
    assert client.post('/tickets',headers=headers(1),json={'title':' ','description':'D','priority':'HIGH'}).status_code==422
    assert client.post('/tickets',headers=headers(1),json={'title':'T','description':'D','priority':'LOW'}).status_code==422
    tid=create(client)
    assert act(client,tid,'claim').status_code==200
    assert domain_code(act(client,tid,'waiting'))=='INVALID_TICKET_STATE'
    count=event_count(store,tid)
    assert act(client,tid,'resolve',3,{}).status_code==422
    assert event_count(store,tid)==count
    assert act(client,tid,'messages',3,{'content':42}).status_code==422
    assert act(client,999,'messages',3,{'content':42}).status_code==422  # accepted BR-33 exception
    assert act(client,tid,'messages',4,{'content':''}).status_code==403
    assert act(client,tid,'claim',3,{'event_id':123}).status_code==422
    assert act(client,tid,'resolve',3,{'resolution_summary':'fixed'}).status_code==200
    assert domain_code(act(client,tid,'messages',3,{}))=='INVALID_TICKET_STATE'
    assert domain_code(act(client,tid,'messages',1,{}))=='INVALID_TICKET_STATE'
    assert act(client,tid,'confirm',1).status_code==200
    assert domain_code(act(client,tid,'claim',4))=='TICKET_CLOSED'
    assert domain_code(act(client,tid,'notes',3,{}))=='TICKET_CLOSED'
    assert domain_code(act(client,tid,'reject',1,{}))=='TICKET_CLOSED'
    assert act(client,tid,'reject',2,{}).status_code==404
    assert client.get(f'/tickets/{tid}',headers=headers(1)).status_code==200


def third_rejection(client,tid):
    assert act(client,tid,'claim').status_code==200
    for n in range(3):
        assert act(client,tid,'resolve',3,{'resolution_summary':f'Result {n}'}).status_code==200
        assert act(client,tid,'reject',1,{'reason':f'Not fixed {n}'}).status_code==200


def test_review_errors_plan_and_waiting(env):
    client,clock,store=env
    tid=create(client)
    assert domain_code(act(client,tid,'reviews/complete',6,{}))=='INVALID_TICKET_STATE'  # A1
    third_rejection(client,tid)
    count=event_count(store,tid)
    assert domain_code(act(client,tid,'resolve',3,{}))=='REVIEW_REQUIRED'
    assert event_count(store,tid)==count
    assert act(client,tid,'reviews/complete',1,{}).status_code==404
    assert act(client,tid,'reviews/complete',3,{}).status_code==403
    assert act(client,tid,'reviews/complete',6,{}).status_code==422
    assert act(client,tid,'waiting').status_code==200
    clock.set('2026-10-05T10:00:00+07:00')
    assert act(client,tid,'notes',3,{'content':'Waiting internal'}).json()['status']=='WAITING_FOR_CUSTOMER'
    assert act(client,tid,'messages',3,{'content':'Waiting public'}).json()['status']=='WAITING_FOR_CUSTOMER'
    payload={'handling_plan':{'unresolved_reason':'Cause','next_action':'New plan','needs_expert_input':True,'expert_note':'External discussion only'}}
    response=act(client,tid,'reviews/complete',6,payload)
    assert response.status_code==200,response.text
    assert response.json()['status']=='WAITING_FOR_CUSTOMER'
    assert response.json()['sla']['resolution']['consumed_seconds']==0
    agent=client.get(f'/tickets/{tid}',headers=headers(3)).json()
    assert agent['reviews'][0]['handling_plan']['next_action']=='New plan'
    customer=client.get(f'/tickets/{tid}',headers=headers(1)).json()
    assert 'reviews' not in customer and 'New plan' not in str(customer)
    assert domain_code(act(client,tid,'reviews/complete',6,payload))=='INVALID_TICKET_STATE'
    assert act(client,tid,'messages',1,{'content':'More information'}).json()['status']=='IN_PROGRESS'
    assert act(client,tid,'resolve',3,{'resolution_summary':'Result 4'}).status_code==200
    # A new rejection requires a distinct new review.
    assert act(client,tid,'reject',1,{'reason':'Still broken'}).status_code==200
    assert client.get(f'/tickets/{tid}',headers=headers(6)).json()['needs_manager_review'] is True
    assert act(client,tid,'reviews/complete',6,payload).status_code==200
    assert act(client,tid,'resolve',3,{'resolution_summary':'Final'}).status_code==200
    assert act(client,tid,'confirm',1).status_code==200
    assert domain_code(act(client,tid,'reviews/complete',6,payload))=='TICKET_CLOSED'  # A2


def test_customer_return_can_overload(env):
    client,clock,store=env
    first=create(client)
    assert act(client,first,'claim').status_code==200
    assert act(client,first,'resolve',3,{'resolution_summary':'Temporary result'}).status_code==200
    for _ in range(3):
        assert act(client,create(client),'claim').status_code==200
    response=act(client,first,'reject',1,{'reason':'Still unresolved'})
    assert response.status_code==200
    with store.connect() as conn:
        assert conn.execute("SELECT COUNT(*) FROM tickets WHERE assignee_id=3 AND status='IN_PROGRESS'").fetchone()[0]==4
    assert domain_code(act(client,create(client),'claim'))=='AGENT_CAPACITY_REACHED'
