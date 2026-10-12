from .conftest import create,act,headers
from .test_api import third_rejection


def get_report(client,metric,**params):
    return client.get('/reports/'+metric,headers=headers(6),params=params)


def test_ratio_cohort_pending_zero_and_unclosed_snapshot(env):
    client,clock,store=env
    a=create(client)
    assert act(client,a,'claim').status_code==200
    clock.set('2026-10-05T09:30:00+07:00')
    assert act(client,a,'resolve',3,{'resolution_summary':'Fixed A'}).status_code==200
    assert act(client,a,'confirm',1).status_code==200
    clock.set('2026-10-05T09:00:00+07:00')
    b=create(client)
    assert act(client,b,'claim',4).status_code==200
    clock.set('2026-10-05T10:00:01+07:00')
    assert act(client,b,'resolve',4,{'resolution_summary':'Late response, resolution on time'}).status_code==200
    assert act(client,b,'reject',1,{'reason':'Not fixed'}).status_code==200
    clock.set('2026-10-05T10:30:00+07:00')
    assert act(client,b,'resolve',4,{'resolution_summary':'Now fixed'}).status_code==200
    clock.set('2026-10-06T09:00:00+07:00')
    assert act(client,b,'confirm',1).status_code==200
    clock.set('2026-09-30T09:00:00+07:00')
    old_open=create(client,'NORMAL')
    clock.set('2026-10-06T09:00:00+07:00')
    pending=create(client)
    clock.set('2026-10-07T09:00:00+07:00')
    future=create(client)
    clock.set('2026-10-08T09:00:00+07:00')
    period={'from':'2026-10-05T00:00:00+07:00','to':'2026-10-06T00:00:00+07:00','as_of':'2026-10-06T09:30:00+07:00'}
    p=get_report(client,'M-01',**period).json()
    assert (p['numerator'],p['denominator'],p['pending_count'])==(1,2,0)
    p2={**period,'to':'2026-10-07T00:00:00+07:00'}
    p=get_report(client,'M-01',**p2).json()
    assert (p['numerator'],p['denominator'],p['pending_count'])==(1,2,1)
    g=get_report(client,'M-02',**period).json()
    assert (g['numerator'],g['denominator'])==(1,1)
    assert g['unclosed_count']==2  # includes old open, excludes future, no created-date restriction
    g=get_report(client,'M-02',**p2).json()
    assert (g['numerator'],g['denominator'])==(2,2)
    reject=get_report(client,'M-03',**p2).json()
    assert (reject['numerator'],reject['denominator'])==(1,2)
    zero=get_report(client,'M-02',**{'from':'2026-09-01T00:00:00+07:00','to':'2026-09-02T00:00:00+07:00'}).json()
    assert zero['ratio'] is None and zero['display']=='không có dữ liệu'
    assert get_report(client,'M-01',**{'from':period['to'],'to':period['from']}).status_code==422
    assert get_report(client,'M-02').status_code==422
    assert get_report(client,'M-07',as_of='2026-10-09T00:00:00+07:00').status_code==422
    assert client.get('/reports/M-06',headers=headers(3)).status_code==403


def test_m04_m05_and_historical_states(env):
    client,clock,store=env
    tid=create(client)
    assert act(client,tid,'claim').status_code==200
    clock.set('2026-10-05T17:00:01+07:00')
    assert act(client,tid,'resolve',3,{'resolution_summary':'Late at close'}).status_code==200
    clock.set('2026-10-06T09:00:00+07:00')
    assert act(client,tid,'confirm',1).status_code==200
    clock.set('2026-10-07T09:00:00+07:00')
    asof='2026-10-05T18:00:00+07:00'
    breach=get_report(client,'M-04',as_of=asof).json()['items']
    assert breach==[{'id':tid,'first_response_breached':True,'resolution_breached':True}]
    waiting=get_report(client,'M-05',as_of=asof).json()['items']
    assert waiting[0]['wait_calendar_seconds']==3599
    assert get_report(client,'M-04').json()['items']==[]
    assert get_report(client,'M-05').json()['items']==[]


def test_m06_capacity_all_priorities_and_filter(env):
    client,clock,store=env
    first=create(client,'NORMAL')
    assert act(client,first,'claim').status_code==200
    assert act(client,first,'resolve',3,{'resolution_summary':'Temporary'}).status_code==200
    for priority in ('HIGH','HIGH','NORMAL'):
        assert act(client,create(client,priority),'claim').status_code==200
    assert act(client,first,'reject',1,{'reason':'Again'}).status_code==200
    report=get_report(client,'M-06',agent_id=3).json()
    assert len(report['items'])==1
    assert report['items'][0]['in_progress_count']==4
    assert report['items'][0]['capacity_state']=='overloaded'
    assert get_report(client,'M-06',priority='HIGH').status_code==422
    assert get_report(client,'M-06',agent_id=999).status_code==422
    assert get_report(client,'M-04',priority='WRONG').status_code==422


def test_m07_excludes_future_review_completion_and_overlap(env):
    client,clock,store=env
    tid=create(client)
    third_rejection(client,tid)
    clock.set('2026-10-05T09:30:00+07:00')
    assert act(client,tid,'waiting').status_code==200
    clock.set('2026-10-05T10:00:00+07:00')
    payload={'handling_plan':{'unresolved_reason':'Cause','next_action':'New plan','needs_expert_input':False}}
    assert act(client,tid,'reviews/complete',6,payload).status_code==200
    clock.set('2026-10-05T11:00:00+07:00')
    assert get_report(client,'M-07',as_of='2026-10-05T08:59:59+07:00').json()['items']==[]
    historical=get_report(client,'M-07',as_of='2026-10-05T09:45:00+07:00').json()['items'][0]
    assert historical['completed_at'] is None
    assert historical['wait_calendar_seconds']==2700 and historical['wait_overlap_seconds']==1800
    current=get_report(client,'M-07').json()['items'][0]
    assert current['completed_at']=='2026-10-05T10:00:00+07:00'
    assert current['wait_calendar_seconds']==3600 and current['wait_overlap_seconds']==1800
    assert current['breach_context']=='none'
