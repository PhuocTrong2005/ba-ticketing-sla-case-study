"""Run: python -m uvicorn backend.app:app --port 8000."""
import os
from datetime import datetime
from typing import Literal
from fastapi import FastAPI, Header, Depends, Request, Query, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, StrictBool
from .sla import TZ, timestamp, iso
from .store import Store, DomainError, fail
from .reports import report


class Payload(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Create(Payload):
    title: str | None = None
    description: str | None = None
    priority: Literal['HIGH','NORMAL'] | None = None


class Message(Payload):
    content: str | None = None


class Resolve(Payload):
    resolution_summary: str | None = None


class Reject(Payload):
    reason: str | None = None


class Plan(Payload):
    unresolved_reason: str | None = None
    next_action: str | None = None
    needs_expert_input: StrictBool | None = None
    expert_note: str | None = None


class Complete(Payload):
    handling_plan: Plan | None = None


def create_app(db_path=None, clock=None):
    application = FastAPI(title='Support Ticketing & SLA demo',version='1.0.0')
    application.state.store = Store(db_path or os.getenv('TICKETING_DB','data/ticketing.sqlite3'))
    application.state.clock = clock or (lambda: datetime.now(TZ))

    @application.exception_handler(DomainError)
    async def domain_error(request: Request, error: DomainError):
        return JSONResponse(status_code=error.status,content={'detail':{'error_code':error.code,'message':error.message}})

    def identity(request: Request, demo_id: str | None = Header(default=None,alias='X-Demo-User-Id')):
        return request.app.state.store.identity(demo_id)

    def now():
        return application.state.clock()

    def read_at(value):
        if value is None:
            return timestamp(now())
        try:
            at = timestamp(value)
        except (ValueError,TypeError):
            fail(422,'as_of must include timezone')
        if at > timestamp(now()):
            fail(422,'as_of cannot be in future')
        return at

    @application.post('/tickets',status_code=201)
    def create(body: Create, user=Depends(identity)):
        return application.state.store.create(user,body.model_dump(),now())

    @application.get('/tickets/queue')
    def queue(user=Depends(identity)):
        store = application.state.store
        store.role(user,('AGENT',))
        at = timestamp(now())
        with store.connect() as conn:
            items=[]
            for ticket in conn.execute("SELECT * FROM tickets WHERE status='NEW'"):
                result=store.project(conn,ticket['id'],at)
                items.append({'id':ticket['id'],'title':ticket['title'],'priority':ticket['priority'],'first_response_due_at':result['sla']['first_response']['due_at'],'created_at':ticket['created_at']})
            return sorted(items,key=lambda x:(x['priority']!='HIGH',x['first_response_due_at'],x['created_at'],x['id']))

    @application.get('/tickets')
    def tickets(user=Depends(identity)):
        store = application.state.store
        field = 'customer_id' if user['role']=='CUSTOMER' else 'assignee_id' if user['role']=='AGENT' else None
        at = timestamp(now())
        with store.connect() as conn:
            rows = conn.execute(f'SELECT id FROM tickets'+(f' WHERE {field}=?' if field else '')+' ORDER BY id',(user['id'],) if field else ()).fetchall()
            return [store.view(conn,r['id'],user,at,list_view=True) for r in rows]

    @application.get('/tickets/{ticket_id}')
    def ticket_detail(ticket_id: int, user=Depends(identity)):
        store=application.state.store
        with store.connect() as conn:
            return store.view(conn,ticket_id,user,timestamp(now()))

    @application.post('/tickets/{ticket_id}/claim')
    def claim(ticket_id: int, body: Payload=Body(default=Payload()), user=Depends(identity)):
        return application.state.store.action(user,ticket_id,'claim',{},now())

    @application.post('/tickets/{ticket_id}/messages')
    def message(ticket_id: int, body: Message, user=Depends(identity)):
        return application.state.store.action(user,ticket_id,'messages',body.model_dump(),now())

    @application.post('/tickets/{ticket_id}/notes')
    def note(ticket_id: int, body: Message, user=Depends(identity)):
        return application.state.store.action(user,ticket_id,'notes',body.model_dump(),now())

    @application.post('/tickets/{ticket_id}/waiting')
    def waiting(ticket_id: int, body: Payload=Body(default=Payload()), user=Depends(identity)):
        return application.state.store.action(user,ticket_id,'waiting',{},now())

    @application.post('/tickets/{ticket_id}/resolve')
    def resolve(ticket_id: int, body: Resolve, user=Depends(identity)):
        return application.state.store.action(user,ticket_id,'resolve',body.model_dump(),now())

    @application.post('/tickets/{ticket_id}/confirm')
    def confirm(ticket_id: int, body: Payload=Body(default=Payload()), user=Depends(identity)):
        return application.state.store.action(user,ticket_id,'confirm',{},now())

    @application.post('/tickets/{ticket_id}/reject')
    def reject(ticket_id: int, body: Reject, user=Depends(identity)):
        return application.state.store.action(user,ticket_id,'reject',body.model_dump(),now())

    @application.get('/tickets/{ticket_id}/reviews')
    def reviews(ticket_id: int, user=Depends(identity)):
        store=application.state.store
        store.role(user,('MANAGER',),review=True)
        with store.connect() as conn:
            store.ticket(conn,ticket_id,user)
            return store.project(conn,ticket_id,timestamp(now()))['reviews']

    @application.post('/tickets/{ticket_id}/reviews/complete')
    def complete(ticket_id: int, body: Complete, user=Depends(identity)):
        return application.state.store.action(user,ticket_id,'complete',body.model_dump(),now())

    @application.get('/reports/{metric_code}')
    def reports(metric_code: str, as_of: str | None=None, start: str | None=Query(default=None,alias='from'), end: str | None=Query(default=None,alias='to'), priority: str | None=None, agent_id: int | None=None, user=Depends(identity)):
        store=application.state.store
        store.role(user,('MANAGER',))
        try:
            return report(store,user,metric_code,read_at(as_of),start,end,priority,agent_id)
        except (ValueError,TypeError):
            fail(422,'Invalid timezone-aware report timestamps')

    return application


app = create_app()
