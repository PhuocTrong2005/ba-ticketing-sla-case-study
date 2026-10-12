"""Insert deterministic BA demo scenarios into an empty database; never erase data."""
import argparse
from .store import Store


def seed(path):
    store=Store(path)
    with store.connect() as conn:
        if conn.execute('SELECT COUNT(*) FROM tickets').fetchone()[0]:
            raise SystemExit('Demo seed requires an empty ticket database; existing data was preserved.')
    customer,agent,manager=(store.identity(x) for x in (1,3,6))
    at='2026-10-12T08:00:00+07:00'
    for title,priority in [('DEMO-01 New','NORMAL'),('DEMO-02 Waiting','HIGH'),('DEMO-03 Resolved','HIGH'),('DEMO-04 Review','HIGH')]:
        tid=store.create(customer,{'title':title,'description':'Designed BA demo scenario; simulated business data','priority':priority},at)['id']
        if title.startswith('DEMO-01'):
            continue
        store.action(agent,tid,'claim',{},at)
        if title.startswith('DEMO-02'):
            store.action(agent,tid,'messages',{'content':'Please provide logs'},at)
            store.action(agent,tid,'waiting',{},at)
        elif title.startswith('DEMO-03'):
            store.action(agent,tid,'resolve',{'resolution_summary':'Configuration corrected; please confirm'},at)
        else:
            for i in range(3):
                store.action(agent,tid,'resolve',{'resolution_summary':f'Attempt {i+1}'},at)
                store.action(customer,tid,'reject',{'reason':'Issue persists'},at)
    return 4


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db',default='data/ticketing.sqlite3')
    args=parser.parse_args()
    print(f'Created {seed(args.db)} scenario tickets; users 1/2 Customers, 3/4/5 Agents, 6 Manager.')
