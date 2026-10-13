import {seed,SCENARIOS,VARIANTS} from './seeds.js';
import {timestamp,iso} from './sla.js';
import {act,USERS} from './domain.js';
export const STORAGE_KEY='ba-ticketing.prototype.v1';
export function validateStored(d) {
  if(!d || d.schema_version!==1 || !SCENARIOS.some(s=>s.id===d.scenario) || !VARIANTS.some(v=>v.id===d.variant) || !Number.isInteger(d.identity) || !USERS[d.identity] || !Array.isArray(d.tickets) || !Array.isArray(d.events) || typeof d.clock!=='string' || iso(d.clock)!==d.clock) throw Error('Dữ liệu/schema không tương thích; cần khôi phục');
  const rebuilt={schema_version:1,scenario:d.scenario,variant:d.variant,identity:d.identity,clock:null,tickets:[],events:[]};
  let seq=0,last=-Infinity;
  const map={ticket_created:'create',agent_assigned:'claim',agent_public_reply:'message',customer_public_message:'message',internal_note:'note',status_waiting:'waiting',resolved:'resolve',customer_reject:'reject',customer_confirm:'confirm',review_completed:'review'};
  for(const e of d.events) {
    if(!Number.isInteger(e.demo_event_seq) || e.demo_event_seq!==seq+1 || !Number.isInteger(e.actor_id) || !Number.isInteger(e.ticket_id) || typeof e.at!=='string' || iso(e.at)!==e.at || timestamp(e.at)<last || !map[e.type] || 'event_id' in e) throw Error('Lịch sử không hợp lệ; cần khôi phục');
    rebuilt.clock=iso(e.at); const id=act(rebuilt,map[e.type],e.ticket_id,e.payload,e.actor_id);
    if(id!==e.ticket_id || rebuilt.events.at(-1).type!==e.type) throw Error('Lịch sử không hợp lệ');
    seq=e.demo_event_seq;last=timestamp(e.at);
  }
  if(JSON.stringify(rebuilt.tickets)!==JSON.stringify(d.tickets) || timestamp(d.clock)<last || timestamp(d.clock)<timestamp(seed(d.scenario,d.variant).clock)) throw Error('Nguồn không nhất quán; cần khôi phục');
  return structuredClone(d);
}
export function readStorage(storage) {
  let raw;
  try {raw=storage.getItem(STORAGE_KEY);}
  catch {return {data:seed(),notice:'Không đọc được localStorage; demo tiếp tục trong memory.'};}
  try {return {data:raw?validateStored(JSON.parse(raw)):seed(),notice:''};}
  catch(e) {return {data:null,notice:`Không đọc được dữ liệu lưu: ${e.message}. Khôi phục để bắt đầu bộ mẫu.`};}
}
export function saveStorage(storage,data) {
  try {storage.setItem(STORAGE_KEY,JSON.stringify(data));return '';}
  catch {return 'Không lưu được localStorage; demo tiếp tục trong memory.';}
}
