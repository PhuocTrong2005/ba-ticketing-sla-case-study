import {projections,load,USERS,DemoError} from './domain.js';
import {timestamp} from './sla.js';
export function reports(data,{from='2026-10-01',to='2026-10-31',priority='',agent=''}={},user=data.identity) {
  if(!USERS[user]) throw new DemoError(401,null,'Danh tính demo không hợp lệ');
  if(USERS[user]!=='Manager') throw new DemoError(403,null,'Chỉ Manager xem báo cáo');
  if(!['','HIGH','NORMAL'].includes(priority) || !['',3,4,5,'3','4','5'].includes(agent)) throw new DemoError(422,null,'Bộ lọc không hợp lệ');
  const start=timestamp(from+'T00:00:00+07:00'), end=timestamp(to+'T00:00:00+07:00')+86400;
  if(start>=end) throw Error('Ngày đến phải từ ngày bắt đầu trở đi');
  const all=projections(data), rows=all.filter(t=>(!priority || t.priority===priority) && (!agent || t.assignee_id===Number(agent)));
  const period=t=>t>=start && t<end, created=rows.filter(t=>period(timestamp(t.created_at))), closed=rows.filter(t=>t.state==='Closed' && period(timestamp(t.closed_at)));
  const ratio=(n,d)=>({numerator:n,denominator:d,ratio:d?n/d:null,display:d?`${n}/${d} · ${(100*n/d).toFixed(1)}%`:'không có dữ liệu'});
  const unclosed=rows.filter(t=>t.state!=='Closed').length;
  return {
    'M-01':{...ratio(created.filter(t=>t.sla.first_response.status==='met').length,created.filter(t=>t.sla.first_response.status!=='pending').length),pending_count:created.filter(t=>t.sla.first_response.status==='pending').length},
    'M-02':{...ratio(closed.filter(t=>t.sla.resolution.status==='met').length,closed.length),unclosed_count:unclosed},
    'M-03':{...ratio(closed.filter(t=>t.rejection_count>0).length,closed.length),unclosed_count:unclosed},
    'M-04':rows.filter(t=>t.state!=='Closed' && Object.values(t.sla).some(s=>s.status==='breached')).map(t=>({id:t.id,first_response_breached:t.sla.first_response.status==='breached',resolution_breached:t.sla.resolution.status==='breached'})),
    'M-05':rows.filter(t=>t.state==='Resolved').map(t=>({id:t.id,resolved_at:t.last_resolved_at,wait_calendar_seconds:timestamp(data.clock)-timestamp(t.last_resolved_at)})),
    // M-06 deliberately uses all priorities, independently of ratio filters.
    'M-06':[3,4,5].filter(u=>!agent || u===Number(agent)).map(u=>({agent_id:u,in_progress_count:load(data,u),counts_by_status:Object.fromEntries(['New','In Progress','Waiting for Customer','Resolved','Closed'].map(s=>[s,all.filter(t=>t.assignee_id===u && t.state===s).length]))})),
    'M-07':rows.flatMap(t=>t.reviews.map(r=>({ticket_id:t.id,...r})))
  };
}
