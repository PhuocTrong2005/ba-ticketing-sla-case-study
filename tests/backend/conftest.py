from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from backend.app import create_app
from backend.sla import timestamp


class Clock:
    def __init__(self, value='2026-10-05T09:00:00+07:00'):
        self.value = value
    def __call__(self):
        return datetime.fromisoformat(self.value)
    def set(self,value):
        self.value=value


def headers(user):
    return {'X-Demo-User-Id':str(user)}


def create(client,priority='HIGH',customer=1):
    response=client.post('/tickets',headers=headers(customer),json={'title':'TC demo','description':'Deterministic support case','priority':priority})
    assert response.status_code==201,response.text
    return response.json()['id']


def act(client,tid,action,user=3,payload=None):
    response=client.post(f'/tickets/{tid}/{action}',headers=headers(user),json=payload if payload is not None else {})
    return response


@pytest.fixture
def env(tmp_path):
    clock=Clock()
    app=create_app(tmp_path/'case.sqlite3',clock)
    with TestClient(app) as client:
        yield client,clock,app.state.store
