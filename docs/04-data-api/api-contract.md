# API contract — approved 12/10/2026

FastAPI/SQLite mô phỏng. `X-Demo-User-Id` tra users server; không phải đăng nhập production. Server cấp actor, timestamp, event_id; payload trường dư trả 422. OpenAPI thực tại /docs và /openapi.json.

| Method/path | Vai trò | Payload / response |
|---|---|---|
| POST /tickets | Customer | title, description không trắng, priority HIGH/NORMAL; 201 ticket |
| GET /tickets | Theo vai trò | Customer của mình, Agent được giao, Manager tất cả; 200 list |
| GET /tickets/queue | Agent | 200 đúng id/title/priority/first_response_due_at/created_at |
| GET /tickets/{id} | Theo quyền | 200 chi tiết; Customer không SLA/notes/review |
| POST /tickets/{id}/claim | Agent | {} hoặc không body; 200 ticket + snapshot nội bộ |
| POST /tickets/{id}/messages | Customer/Agent | content; 200 ticket |
| POST /tickets/{id}/notes | Agent | content; 200 ticket |
| POST /tickets/{id}/waiting | Agent | không body; 200 ticket |
| POST /tickets/{id}/resolve | Agent | resolution_summary; 200 ticket |
| POST /tickets/{id}/confirm | Customer | không body; 200 ticket |
| POST /tickets/{id}/reject | Customer | reason; 200 ticket |
| GET /tickets/{id}/reviews | Manager | 200 review list; Customer luôn 404, Agent 403 |
| POST /tickets/{id}/reviews/complete | Manager | handling_plan {unresolved_reason,next_action,needs_expert_input,expert_note?}; 200 ticket |
| GET /reports/{metric_code} | Manager | M-01…M-07; as_of, from, to, priority, agent_id; 200 report |

M-01…M-03 cần from/to timezone-aware, [from,to). Snapshot dùng as_of (mặc định clock server); không nhận as_of tương lai. agent_id và priority lọc theo trạng thái tại as_of. M-06 không nhận priority; tải luôn tất cả ưu tiên. M-02/03 có unclosed_count và câu giải thích, không gọi N là phần bù mẫu số. M-01 pending riêng. denominator=0: ratio=null, display='không có dữ liệu'.

Ticket/role/priority dùng uppercase; SLA lowercase. Chi tiết nội bộ có sla, assignment_snapshot, rejection_count, needs_manager_review, reviews; Agent đọc trên ticket của mình, không ghi review. List nội bộ bỏ bộ đếm giây chi tiết, dùng nhãn phút/giờ. Không thêm route PATCH status.

401 danh tính; 403 vai trò/Agent không phụ trách; 404 không tồn tại/Customer khác; 409 theo codes. Response lỗi handler: {detail:{error_code: CODE hoặc null, message: ...}}. 422 validation cấu trúc FastAPI có dạng detail list và có thể trước handler; validation nghiệp vụ (trường đúng kiểu nhưng thiếu/trắng) theo thứ tự BR-33, trả detail lỗi handler. Closed ưu tiên; claim Closed → assigned → capacity. Resolve IP rồi review rồi content. Review Customer luôn 404, Agent 403; Manager Closed rồi không review rồi content. Không có mã lỗi mới.
