// Presentation only: instructions never execute domain actions or change seeds.
const customer = {
  'DEMO-01':'Customer 1: tạo ticket High lúc 05/10 09:00. Khi thấy Resolved, mở ticket và xác nhận lúc 09:35; quan sát trạng thái Closed.',
  'DEMO-02':'Customer 1: mở ticket mẫu. Khi Waiting for Customer, gửi thông tin công khai lúc 05/10 11:00; quan sát ticket trở lại In Progress. Khi có kết quả, đọc hội thoại công khai.',
  'DEMO-03':'Customer 1: mở ticket mẫu; khi Resolved, từ chối với lý do lúc 05/10 15:00. Quan sát ticket trở lại In Progress và lý do trong hội thoại.',
  'DEMO-04':'Customer 1: ticket mẫu đang In Progress sau các lần từ chối. Khi Waiting for Customer, gửi thông tin công khai lúc 05/10 12:30; quan sát trở lại In Progress.',
  'DEMO-05':'Customer 1: mở ticket #1 đang Resolved, gửi lý do từ chối tại giờ mẫu 05/10 09:00; quan sát #1 trở lại In Progress.',
  'DEMO-06':'Customer 1: mở ticket của bạn để đọc hội thoại hoặc gửi thông tin khi New / In Progress / Waiting for Customer. Nếu Resolved, xác nhận hoặc từ chối với lý do; quan sát trạng thái công khai. Customer 2 chỉ xem ticket của mình.'
};
const agent = {
  'DEMO-01':'Agent 3: sau khi Customer tạo High 05/10 09:00, nhận 09:05, nhắn công khai 09:10, Resolved 09:30. Quan sát phản hồi đầu 600 giây, giải quyết 1800 giây, Đạt SLA. Customer xác nhận 09:35.',
  'DEMO-02':'Agent 3: nhận 05/10 09:05, nhắn 09:10, Waiting 10:00; nhắn và note 10:15 giữ Tạm dừng, giải quyết đã tiêu 3600 giây. Sau Customer trả lời 11:00, quan sát hạn 06/10 09:00; Resolved 11:30: đã tiêu 5400, còn 23400 giây.',
  'DEMO-03':'Agent 3: nhận 05/10 08:05, nhắn 08:10, Resolved 14:00. Sau Customer từ chối 15:00, quan sát giải quyết đã tiêu 21600, còn 7200 giây, hạn 17:00. Resolved 17:00 đạt; khôi phục và làm lại để thử 17:00:01 vi phạm.',
  'DEMO-04':'Agent 3: mở #1, tại 05/10 11:15 quan sát Resolved bị chặn bởi review mở. Chuyển Waiting 11:30; sau Manager ghi phương án 12:00, đọc phương án và quan sát vẫn Tạm dừng. Customer nhắn 12:30 mới tiếp tục giải quyết.',
  'DEMO-05':'Agent 3 tại 05/10 09:00: tải 3 chặn nhận #5 New. Sau Customer từ chối #1, tải 4. Chuyển #2 Waiting → tải 3 vẫn chặn; #3 Waiting → tải 2 rồi nhận #5. Quan sát nhãn tải và nút nhận.',
  'DEMO-06':'Agent 3: mở #1, chọn biến thể trong controls rồi tiến clock bằng tay. Đổi sang Agent 4 để quan sát quyền chi tiết bị từ chối; đổi Customer để chỉ thấy công khai.'
};
const variants = {
  monday:'High tạo 05/10 16:00: phản hồi đúng 17:00 Đạt SLA; khôi phục riêng để thử 17:00:01 Vi phạm SLA.',
  friday:'High tạo thứ Sáu 09/10 16:59: quan sát hạn phản hồi thứ Hai 12/10 08:59; tiến clock tới hạn để thử phản hồi.',
  zero:'SLA-83 đã resume ngoài giờ: tới 06/10 08:00:00 quan sát Chưa có kết quả / Đến hạn / Đang chạy; +1 giây Vi phạm SLA.',
  warnings:'05/10 09:00 còn 3600 giây: Không cảnh báo; 09:00:01 còn 3599: Sắp đến hạn; 09:45 còn 900: Sắp đến hạn; 09:45:01 còn 899: Gần đến hạn.',
  sticky:'SLA-40 ở Waiting 05/10 17:30: quan sát Vi phạm SLA và Tạm dừng cùng lúc. Tiến tới 06/10 09:00, giải quyết vẫn đã tiêu 28800 giây, vi phạm giữ nguyên.'
};
const manager = {
  'DEMO-01':'Manager 6: sau các thao tác của Customer/Agent ngày 05/10, mở báo cáo; sau xác nhận 09:35 quan sát Closed, M-01/M-02 và chi tiết hai SLA đạt.',
  'DEMO-02':'Manager 6: xem chi tiết ở Waiting 05/10 10:00 và sau Customer trả lời 11:00; quan sát Tạm dừng rồi hạn giải quyết 06/10 09:00. Sau Resolved 11:30, xem M-05 chờ xác nhận.',
  'DEMO-03':'Manager 6: sau Customer từ chối 05/10 15:00, xem chi tiết giải quyết còn 7200 giây, hạn 17:00. M-03 chỉ tính ticket đã Closed từng bị từ chối; ticket chưa đóng hiện ở N.',
  'DEMO-04':'Manager 6: từ Review mở, mở #1. Sau Agent Waiting 05/10 11:30, tới 12:00 ghi nguyên nhân và hướng xử lý để hoàn tất review. Quan sát vẫn Waiting, M-07 chờ 50 phút, chồng SLA 1200 giây; Customer nhắn 12:30 mới tiếp tục.',
  'DEMO-05':'Manager 6 tại 05/10 09:00: xem Tải Agent. Sau Customer từ chối #1, Agent 3 tải 4; sau Agent chuyển #2/#3 Waiting, tải lần lượt 3/2. M-06 tính tất cả mức ưu tiên dù lọc High.',
  'DEMO-06':'Manager 6: mở #1 để xem hai SLA và báo cáo M-04; chọn biến thể và tiến clock bằng tay để quan sát biên.'
};
export function guidance(scenario,variant,role,identity){
  if(role==='Customer')return identity===2?'Customer 2: chỉ tạo hoặc mở ticket của mình; bộ mẫu thuộc Customer 1. Chọn Customer 1 nếu muốn thao tác ticket mẫu. Quan sát hội thoại và trạng thái công khai.':customer[scenario];
  if(role==='Agent' && identity!==3)return `Agent ${identity}: chỉ nhận ticket New khi còn tải và mở ticket phụ trách. Ticket mẫu đã giao Agent 3 không thuộc quyền của bạn; chọn Agent 3 để thử hướng dẫn nhóm này.`;
  return (role==='Manager'?manager:agent)[scenario]+(scenario==='DEMO-06'?' '+variants[variant]:'');
}
