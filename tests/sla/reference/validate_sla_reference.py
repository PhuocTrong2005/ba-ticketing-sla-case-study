#!/usr/bin/env python3
"""Reference fixture cross-check, not backend/API tests or proof of human execution.
Uses an explicit lattice of working seconds and event replay, no project imports.
Usage: python validate_sla_reference.py sla_draft_data.json --report sla_validation_results.json
"""
import argparse,bisect,hashlib,json
from datetime import datetime,timedelta,timezone
from pathlib import Path
TZ=timezone(timedelta(hours=7))
POLICIES={'HIGH':(3600,28800),'NORMAL':(7200,57600)}

def ts(s):
    d=datetime.fromisoformat(s)
    if d.tzinfo is None: raise ValueError('Timestamp requires timezone')
    return int(d.timestamp())
def iso(t):return datetime.fromtimestamp(t,TZ).isoformat()

class Calendar:
    def __init__(self,rows):
        dates=[datetime.fromtimestamp(ts(r[k]),TZ).date() for r in rows for k in ('created_at','as_of')]
        d=min(dates)-timedelta(days=2);end=max(dates)+timedelta(days=35);self.ticks=[]
        while d<=end:
            if d.weekday()<5:
                start=int(datetime.combine(d,datetime.min.time(),TZ).replace(hour=8).timestamp())
                self.ticks.extend(range(start,start+32400))
            d+=timedelta(days=1)
    def spent(self,a,b):
        if b<a:raise ValueError('Negative interval')
        return bisect.bisect_left(self.ticks,b)-bisect.bisect_left(self.ticks,a)
    def deadline(self,a,budget):
        i=bisect.bisect_left(self.ticks,a)
        if i>=len(self.ticks):raise ValueError('Calendar horizon exhausted')
        if budget==0:return self.ticks[i]
        if i+budget>len(self.ticks):raise ValueError('Calendar horizon exhausted')
        return self.ticks[i+budget-1]+1

def calculate(row,cal,override_asof=None):
    created=ts(row['created_at']);now=ts(override_asof or row['as_of']);pb,gb=POLICIES[row['policy_id']]
    pd=cal.deadline(created,pb);gd=cal.deadline(created,gb);segment=created;active=True;done=False;spent=0;first=None;assigned=None;intervals=[];state='New';rejects=0;reviews=[];openrv=None;breach_at=None
    events=sorted((e for e in row['events'] if ts(e['at'])<=now),key=lambda e:(ts(e['at']),e['seq']))
    def detect(t):
        nonlocal breach_at
        if active and gd is not None and t>gd and breach_at is None:breach_at=gd+1
    for e in events:
        t=ts(e['at']);kind=e['type'];detect(t)
        if kind=='agent_assigned':
            if state!='New' or assigned is not None:raise ValueError('Invalid assignment event')
            assigned=t;state='In Progress'
        elif kind=='internal_note':
            if assigned is None:raise ValueError('Internal note before assignment')
        elif kind=='agent_public_reply':
            if assigned is None or state not in ('In Progress','Waiting for Customer'):raise ValueError('Invalid public reply state')
            if first is None:first=t
        elif kind in ('status_waiting','resolved'):
            if state!='In Progress' or assigned is None:raise ValueError('Invalid transition')
            if kind=='status_waiting' and first is None:raise ValueError('Waiting without public first response')
            if kind=='resolved' and openrv is not None:raise ValueError('Resolved during required review')
            if kind=='resolved' and first is None:first=t
            seconds=cal.spent(segment,t);spent+=seconds;intervals.append({'started_at':iso(segment),'ended_at':iso(t),'business_seconds':seconds})
            active=False;done=kind=='resolved';state='Resolved' if done else 'Waiting for Customer'
            if not done:gd=None
        elif kind=='customer_public_message':
            if state=='Closed':raise ValueError('Customer message on Closed')
            if state=='Waiting for Customer':active=True;segment=t;state='In Progress';gd=cal.deadline(t,max(0,gb-spent))
        elif kind=='customer_reject':
            if state!='Resolved':raise ValueError('Reject when not Resolved')
            rejects+=1;active=True;done=False;segment=t;state='In Progress';gd=cal.deadline(t,max(0,gb-spent))
            if rejects>=3:
                if openrv is not None:raise ValueError('Multiple open reviews')
                openrv={'review_key':f'R{len(reviews)+1}','requested_at':iso(t),'completed_at':None,'_breached_before':breach_at is not None}
                reviews.append(openrv)
        elif kind=='review_completed':
            if openrv is None:raise ValueError('Review completion without request')
            openrv['completed_at']=iso(t);openrv=None
        elif kind=='customer_confirm':
            if state!='Resolved':raise ValueError('Confirm when not Resolved')
            state='Closed'
        else:raise ValueError('Unknown successful event '+kind)
    detect(now)
    if active:intervals.append({'started_at':iso(segment),'ended_at':None,'business_seconds_as_of':cal.spent(segment,now)})
    gc=spent+(cal.spent(segment,now) if active else 0);pc=cal.spent(created,first if first is not None else now)
    ps='breached' if (first if first is not None else now)>pd else 'met' if first is not None else 'pending'
    gs='breached' if breach_at is not None else 'met' if done else 'pending'
    pr=max(0,pb-pc);gr=max(0,gb-gc)
    def warning(status,running,remain,deadline):
        if status=='breached':return 'breached'
        if status=='met' or not running:return 'none'
        if now==deadline:return 'due'
        if remain<900:return 'emphasized'
        if remain<3600:return 'soft'
        return 'none'
    for rv in reviews:
        requested=ts(rv['requested_at']);end=ts(rv['completed_at']) if rv['completed_at'] else now
        overlap=0
        for it in intervals:
            a=max(requested,ts(it['started_at']));b=min(end,ts(it['ended_at']) if it['ended_at'] else now)
            if b>=a:overlap+=cal.spent(a,b)
        rv['wait_calendar_seconds']=end-requested;rv['wait_overlap_seconds']=overlap
        rv['breach_context']='before_request' if rv.pop('_breached_before') else 'during_wait' if breach_at is not None and requested<=breach_at<=end else 'none'
    return {'expected_first_response_due_at':iso(pd),'expected_resolution_due_at':iso(gd) if gd is not None else None,'expected_first_response_consumed_seconds':pc,'expected_resolution_consumed_seconds':gc,'expected_first_response_remaining_seconds':pr,'expected_resolution_remaining_seconds':gr,'expected_first_response_status':ps,'expected_resolution_status':gs,'expected_first_response_warning_level':warning(ps,first is None,pr,pd),'expected_resolution_warning_level':warning(gs,active,gr,gd),'expected_first_response_sla_status_at_assignment':None if assigned is None else 'breached' if assigned>pd else 'pending','expected_resolution_sla_status_at_assignment':None if assigned is None else 'breached' if assigned>cal.deadline(created,gb) else 'pending','expected_resolution_intervals':intervals,'expected_ticket_state':state,'expected_rejection_count':rejects,'expected_open_review':openrv['review_key'] if openrv else None,'expected_reviews':reviews,'resolution_result_final':state=='Closed'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('--report',default='sla_validation_results.json');args=ap.parse_args()
    source=Path(args.source);raw=source.read_bytes();pack=json.loads(raw);rows=pack['scenarios'] if isinstance(pack,dict) else pack
    if len(rows)!=69 or {r['scenario_id'] for r in rows}!={f'SLA-{i:02}' for i in range(1,70)}:raise ValueError('69 unique IDs required')
    cal=Calendar(rows);records=[];total_checks=0
    for row in rows:
        mismatches=[];checks=0;calculated=None
        try:
            seq=[e['seq'] for e in row['events']]
            if len(set(seq))!=len(seq):raise ValueError('Duplicate event seq')
            for e in row['events']:
                if ts(e['at'])<ts(row['created_at']):raise ValueError('Event before creation')
                if datetime.fromisoformat(e['at']).microsecond:raise ValueError('Stored event not whole-second')
                if 'at_raw' in e and ts(e['at_raw'])!=ts(e['at']):raise ValueError('Raw timestamp truncation mismatch')
            calculated=calculate(row,cal)
            for key,value in calculated.items():
                checks+=1
                if row.get(key)!=value:mismatches.append({'field':key,'expected_fixture':row.get(key),'reference_result':value})
            for act in row.get('expected_rejected_actions',[]):
                checks+=1;at_result=calculate(row,cal,act['at'])
                if act['type']!='resolved_attempt' or at_result['expected_ticket_state']!='In Progress' or at_result['expected_open_review'] is None or act['error_code']!='REVIEW_REQUIRED' or act['http_status']!=409 or act['expected_state_change'] is not False or act['expected_sla_interval_change'] is not False:mismatches.append({'field':'expected_rejected_actions','reason':'Refusal context inconsistent'})
        except (ValueError,KeyError) as exc:mismatches.append({'field':'fixture_structure_or_event_semantics','reason':str(exc)})
        total_checks+=checks;records.append({'scenario_id':row['scenario_id'],'checks':checks,'result':'PASS' if not mismatches else 'FAIL','mismatches':mismatches,'reference':calculated})
    report={'kind':'AI-assisted standalone reference cross-check','source_file':source.name,'source_sha256':hashlib.sha256(raw).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'executed_at':datetime.now(TZ).isoformat(timespec='seconds'),'execution_by':'AI assistant using Python reference checker on behalf of project owner','owner_confirmation':pack.get('metadata',{}).get('owner_confirmation') if isinstance(pack,dict) else None,'method':'Enumerate each working second in a calendar lattice, binary-search elapsed budgets/deadlines, replay source events; compare all recorded expected fields including intervals/snapshots/reviews. Does not import or invoke backend.','scenario_count':len(rows),'passed':sum(r['result']=='PASS' for r in records),'failed':sum(r['result']=='FAIL' for r in records),'field_comparisons':total_checks,'limitations':['Both fixtures and reference checker were authored with AI; method independence from backend does not establish independent human execution.','No actual FastAPI, SQLite, API permissions, concurrency, SQL reports or prototype tests executed.','Actors and required public/reject/review text are not specified in these mathematical fixtures; their permissions/content validation require separate API cases.','Group mapping does not prove every required coverage condition in the unseen repository specification.'],'scenarios':records}
    Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:report[k] for k in ['scenario_count','passed','failed','field_comparisons','source_sha256']},ensure_ascii=False))
    return 1 if report['failed'] else 0
if __name__=='__main__':raise SystemExit(main())
