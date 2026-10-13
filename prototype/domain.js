import {replay, iso, timestamp} from './sla.js';
export const USERS = {1:'Customer',2:'Customer',3:'Agent',4:'Agent',5:'Agent',6:'Manager'};
export class DemoError extends Error {
  constructor(status, code, message) {super(message); this.status=status; this.code=code;}
}
const fail = (s,c,m) => {throw new DemoError(s,c,m);};
const errors = {TICKET_CLOSED:'Ticket đã đóng',TICKET_ALREADY_ASSIGNED:'Ticket đã có Agent nhận',AGENT_CAPACITY_REACHED:'Agent đã đạt giới hạn nhận',REVIEW_REQUIRED:'Cần Manager hoàn tất review',INVALID_TICKET_STATE:'Thao tác không phù hợp trạng thái hiện tại'};
const conflict = c => fail(409,c,errors[c]);
const nonblank = v => typeof v === 'string' && v.trim().length > 0;
export function projections(data, at=data.clock) {
  return data.tickets.filter(t => timestamp(t.created_at) <= timestamp(at)).map(t => ({...t,...replay(t.created_at,t.priority,data.events.filter(e=>e.ticket_id===t.id),at)}));
}
export function load(data, user) {return projections(data).filter(t=>t.assignee_id===user && t.state==='In Progress').length;}
export function detail(data, id, user=data.identity) {
  const role = USERS[user]; if (!role) fail(401,null,'Danh tính demo không hợp lệ');
  const t = projections(data).find(t=>t.id===Number(id));
  if (!t || role==='Customer' && t.customer_id!==user) fail(404,null,'Không tìm thấy ticket');
  if (role==='Agent' && t.assignee_id!==user) fail(403,null,'Chỉ xem ticket được giao');
  if (role==='Customer') {
    const {id,title,description,priority,created_at,state,customer_id} = t;
    return {id,title,description,priority,created_at,state,customer_id,messages:t.messages.filter(m=>m.visibility==='PUBLIC')};
  }
  return t;
}
export function dashboard(data, user=data.identity) {
  const role = USERS[user]; if (!role) fail(401,null,'Danh tính demo không hợp lệ');
  const rows = projections(data);
  if (role==='Customer') return rows.filter(t=>t.customer_id===user).map(t=>detail(data,t.id,user));
  if (role==='Agent') return {load:load(data,user),mine:rows.filter(t=>t.assignee_id===user),queue:rows.filter(t=>t.state==='New').map(t=>({id:t.id,title:t.title,priority:t.priority,first_response_due_at:t.sla.first_response.due_at,created_at:t.created_at})).sort((a,b)=>(a.priority==='HIGH'?0:1)-(b.priority==='HIGH'?0:1) || a.first_response_due_at.localeCompare(b.first_response_due_at) || a.created_at.localeCompare(b.created_at))};
  return rows;
}
export function reviewsResource(data,id,user=data.identity) {
  if (!USERS[user]) fail(401,null,'Danh tính demo không hợp lệ');
  if (USERS[user]==='Customer') fail(404,null,'Không tìm thấy tài nguyên');
  if (USERS[user]!=='Manager') fail(403,null,'Chỉ Manager xem tài nguyên review');
  return detail(data,id,user).reviews;
}
const schemas = {create:['title','description','priority'],message:['content'],note:['content'],resolve:['resolution_summary'],reject:['reason'],review:['handling_plan'],claim:[],waiting:[],confirm:[]};
export function act(data, action, id, payload={}, user=data.identity) {
  const role = USERS[user]; if (!role) fail(401,null,'Danh tính demo không hợp lệ');
  if (!schemas[action]) fail(422,null,'Thao tác không hợp lệ');
  if (action==='review' && role==='Customer') fail(404,null,'Không tìm thấy tài nguyên');
  const allowed = {create:['Customer'],claim:['Agent'],message:['Customer','Agent'],note:['Agent'],waiting:['Agent'],resolve:['Agent'],confirm:['Customer'],reject:['Customer'],review:['Manager']}[action];
  if (!allowed.includes(role)) fail(403,null,'Vai trò không được thực hiện thao tác');
  let t;
  if (action!=='create') {
    if (action==='claim') {
      t = projections(data).find(t=>t.id===Number(id)); if (!t) fail(404,null,'Không tìm thấy ticket');
    } else t = detail(data,id,user);
    if (t.state==='Closed') conflict('TICKET_CLOSED');
    if (action==='claim') {
      if (t.assignee_id!=null) conflict('TICKET_ALREADY_ASSIGNED');
      if (t.state!=='New') conflict('INVALID_TICKET_STATE');
      if (load(data,user)>=3) conflict('AGENT_CAPACITY_REACHED');
    }
    if (['message','note'].includes(action) && !['New','In Progress','Waiting for Customer'].includes(t.state)) conflict('INVALID_TICKET_STATE');
    if (['resolve','waiting'].includes(action) && t.state!=='In Progress') conflict('INVALID_TICKET_STATE');
    if (action==='waiting' && t.sla.first_response.running) conflict('INVALID_TICKET_STATE');
    if (action==='resolve' && t.open_review) conflict('REVIEW_REQUIRED');
    if (['confirm','reject'].includes(action) && t.state!=='Resolved') conflict('INVALID_TICKET_STATE');
    if (action==='review' && !t.open_review) conflict('INVALID_TICKET_STATE');
  }
  if (!payload || typeof payload!=='object' || Array.isArray(payload) || Object.keys(payload).some(k=>!schemas[action].includes(k))) fail(422,null,'Dữ liệu không hợp lệ');
  for (const k of schemas[action].filter(k=>!['priority','handling_plan'].includes(k))) if (!nonblank(payload[k])) fail(422,null,'Vui lòng nhập nội dung bắt buộc');
  if (action==='create' && !['HIGH','NORMAL'].includes(payload.priority)) fail(422,null,'Chọn High hoặc Normal');
  if (action==='review') {
    const p = payload.handling_plan;
    if (!p || !nonblank(p.unresolved_reason) || !nonblank(p.next_action) || typeof p.needs_expert_input!=='boolean' || p.expert_note!=null && typeof p.expert_note!=='string' || Object.keys(p).some(k=>!['unresolved_reason','next_action','needs_expert_input','expert_note'].includes(k))) fail(422,null,'Nhập nguyên nhân và hướng xử lý tiếp theo');
  }
  // Every validation finishes before source mutation. No derived data persisted.
  if (action==='create') {
    id = Math.max(0,...data.tickets.map(t=>t.id))+1;
    data.tickets.push({id,title:payload.title,description:payload.description,priority:payload.priority,customer_id:user,created_at:iso(data.clock),scenario_id:data.scenario});
  }
  const type = {create:'ticket_created',claim:'agent_assigned',message:role==='Agent'?'agent_public_reply':'customer_public_message',note:'internal_note',waiting:'status_waiting',resolve:'resolved',confirm:'customer_confirm',reject:'customer_reject',review:'review_completed'}[action];
  const seq = Math.max(0,...data.events.map(e=>e.demo_event_seq))+1;
  data.events.push({demo_event_seq:seq,ticket_id:Number(id),type,at:iso(data.clock),actor_id:user,payload:structuredClone(payload)});
  return Number(id);
}
export function advance(data,value) {
  const t=timestamp(value); if (t<timestamp(data.clock)) fail(422,null,'Clock chỉ được tiến; dùng khôi phục để về đầu');
  data.clock=iso(t);
}
