import {act,advance} from './domain.js';
export const SCENARIOS = [
  {id:'DEMO-01',name:'01 · Thành công',guide:'05/10: Customer tạo High 09:00 → Agent nhận 09:05 → phản hồi 09:10 → Resolved 09:30 → Customer xác nhận 09:35.'},
  {id:'DEMO-02',name:'02 · Waiting',guide:'Ticket mẫu tạo 09:00. Agent nhận 09:05, phản hồi 09:10, Waiting 10:00; nhắn/note 10:15 không resume. Customer trả lời 11:00; Resolved 11:30. Hạn sau resume: 06/10 09:00.'},
  {id:'DEMO-03',name:'03 · Từ chối',guide:'Ticket mẫu tạo 08:00. Nhận 08:05, phản hồi 08:10; Resolved 14:00; Customer từ chối 15:00. Resolved đúng 17:00; khôi phục để thử lại 17:00:01.'},
  {id:'DEMO-04',name:'04 · Manager review',guide:'Prehistory SLA-61 đến reject thứ 3 lúc 11:10. Thử Resolved 11:15 bị chặn. Waiting 11:30 → Manager phương án 12:00 (vẫn Waiting) → Customer trả lời 12:30.'},
  {id:'DEMO-05',name:'05 · Tải Agent',guide:'Agent 3 tải 3: không nhận New. Customer từ chối ticket #1 → tải 4. Agent đưa #2 Waiting → tải 3, #3 Waiting → tải 2; lúc đó mới nhận New.'},
  {id:'DEMO-06',name:'06 · Biên SLA & quyền',guide:'Chọn biến thể để thay dataset: 16:00 → hạn 17:00; thứ Sáu 16:59 → thứ Hai 08:59; SLA-83 → 08:00 due, +1 giây breached; ngưỡng cảnh báo; sticky breach SLA-40.'}
];
export const VARIANTS = [{id:'monday',name:'High T2 16:00'},{id:'friday',name:'High T6 16:59'},{id:'zero',name:'SLA-83 · resume 0 ngoài giờ'},{id:'warnings',name:'Ngưỡng 3600 / 3599 / 900 / 899'},{id:'sticky',name:'SLA-40 · Waiting giữ breach'}];
const time=(h,day='05')=>`2026-10-${day}T${h}+07:00`;
export function seed(scenario='DEMO-01',variant='monday') {
  if (!SCENARIOS.some(s=>s.id===scenario) || !VARIANTS.some(v=>v.id===variant)) throw Error('Kịch bản không hợp lệ');
  const d={schema_version:1,scenario,variant,clock:time('09:00:00'),identity:1,tickets:[],events:[]};
  const action=(h,a,id=1,p={},u=3,day='05')=>{advance(d,time(h,day));return act(d,a,id,p,u);};
  const create=(h,title='Yêu cầu hỗ trợ mẫu',priority='HIGH',day='05')=>action(h,'create',null,{title,description:`Dữ liệu mẫu dựng sẵn · ${scenario}. Khách cần hỗ trợ thao tác nghiệp vụ.`,priority},1,day);
  if (scenario==='DEMO-01') return d;
  if (scenario==='DEMO-02') create('09:00:00','Waiting · cần khách cung cấp thông tin');
  if (scenario==='DEMO-03') {d.clock=time('08:00:00');create('08:00:00','Kết quả cần kiểm tra lại');}
  if (scenario==='DEMO-04') {
    d.clock=time('08:00:00'); create('08:00:00','Kết quả chưa đáp ứng yêu cầu');
    action('08:05:00','claim');action('08:10:00','message',1,{content:'Đã tiếp nhận thông tin.'});
    for(const h of ['09','10','11']) {action(`${h}:00:00`,'resolve',1,{resolution_summary:'Đề xuất kết quả xử lý mẫu.'});action(`${h}:10:00`,'reject',1,{reason:'Vấn đề vẫn còn.'},1);}
  }
  if (scenario==='DEMO-05') {
    d.clock=time('08:00:00');create('08:00:00','Kết quả chờ xác nhận','NORMAL');action('08:01:00','claim');action('08:02:00','resolve',1,{resolution_summary:'Mời khách kiểm tra kết quả.'});
    for(let n=2;n<=4;n++) {create(`08:0${n+1}:00`,`Ticket đang xử lý ${n}`,n===4?'NORMAL':'HIGH');action(`08:0${n+1}:10`,'claim',n);action(`08:0${n+1}:20`,'message',n,{content:'Đã phản hồi đầu, có thể chuyển Waiting.'});}
    create('08:08:00','New · thử giới hạn nhận');advance(d,time('09:00:00'));d.identity=3;
  }
  if (scenario==='DEMO-06') {
    if(variant==='monday' || variant==='friday') {const day=variant==='friday'?'09':'05',h=variant==='friday'?'16:59:00':'16:00:00';d.clock=time(h,day);create(h,'Yêu cầu hỗ trợ cuối ngày','HIGH',day);action(h,'claim',1,{},3,day);}
    if(variant==='zero' || variant==='sticky') {
      create('09:00:00',variant==='zero'?'Thông tin bổ sung sau khi chờ':'Chờ khách bổ sung thông tin');action('09:05:00','claim');action('09:10:00','message',1,{content:'Phản hồi đầu.'});
      action(variant==='zero'?'17:00:00':'17:30:00','waiting');
      if(variant==='zero') action('18:00:00','message',1,{content:'Khách cung cấp thông tin.'},1);
    }
    if(variant==='warnings') {create('09:00:00','Yêu cầu hỗ trợ cần phản hồi');action('09:00:00','claim');}
    d.identity=3;
  }
  return d;
}
