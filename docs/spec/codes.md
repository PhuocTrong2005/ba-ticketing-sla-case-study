# Bộ mã và quy ước v1.0

Tài liệu này quy định các mã dùng thống nhất trong case study. Nguồn quy tắc nghiệp vụ là [business-rules.md](business-rules.md).

## Trạng thái ticket

| Mã | Nhãn hiển thị |
|---|---|
| `NEW` | New |
| `IN_PROGRESS` | In Progress |
| `WAITING_FOR_CUSTOMER` | Waiting for Customer |
| `RESOLVED` | Resolved |
| `CLOSED` | Closed |

## Vai trò

| Mã | Nhãn |
|---|---|
| `CUSTOMER` | Customer |
| `AGENT` | Agent |
| `MANAGER` | Manager |

## Mức ưu tiên và SLA policy

| Mã | Nhãn | Phản hồi đầu | Giải quyết |
|---|---|---:|---:|
| `HIGH` | High | 3.600 `business_seconds` | 28.800 `business_seconds` |
| `NORMAL` | Normal | 7.200 `business_seconds` | 57.600 `business_seconds` |

`policy_id` là định danh chính sách được dùng để tính và dựng lại dữ liệu.

## Trạng thái SLA

| Mã | Ý nghĩa |
|---|---|
| `PENDING` | Đồng hồ chưa hoàn thành và chưa vi phạm, hoặc đang tạm dừng khi chưa vi phạm. |
| `MET` | Hoàn thành đúng hạn; với giải quyết tại Resolved, đây là kết quả tạm thời đến khi Closed. |
| `BREACHED` | Hoàn thành trễ, hoặc đồng hồ đang chạy đã quá hạn. Vi phạm không bị xóa khi tiếp tục. |

## HTTP và error_code

| HTTP | `error_code` | Khi dùng |
|---:|---|---|
| 401 | — | Thiếu hoặc sai danh tính demo. |
| 403 | — | Sai vai trò hoặc Agent không phải người phụ trách. |
| 404 | — | Ticket không tồn tại, hoặc Customer truy cập ticket không thuộc mình. |
| 409 | `INVALID_TICKET_STATE` | Sai trạng thái. |
| 409 | `TICKET_ALREADY_ASSIGNED` | Ticket đã được nhận. |
| 409 | `AGENT_CAPACITY_REACHED` | Agent đạt giới hạn tải. |
| 409 | `TICKET_CLOSED` | Ticket đã Closed. |
| 409 | `REVIEW_REQUIRED` | Agent chuyển Resolved khi còn review chưa hoàn thành. |
| 422 | — | Dữ liệu sai/thiếu; gồm nội dung hoặc lý do bắt buộc. FastAPI có thể trả 422 do payload sai cấu trúc trước handler. |

Mọi trường hợp mã lỗi hiện đã chốt tại [business-rules.md](business-rules.md); điểm mới phải ghi vào [open-questions.md](../open-questions.md).

## Quy ước dữ liệu thời gian và thời lượng

- Timestamp dùng ISO 8601 với offset `+07:00`, độ chính xác giây, ví dụ `2026-10-05T08:00:00+07:00`.
- Khi ghi sự kiện, phần dưới giây bị cắt bỏ, không làm tròn.
- Các thời lượng là giây nguyên; tên trường có hậu tố `_seconds`, như `business_seconds`, `consumed_seconds`, `remaining_seconds`.
- Sự kiện cùng giây được sắp theo `event_id` do database cấp; client không gửi `event_id`.

## Trường dẫn xuất cho M-04

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| `first_response_breached` | boolean, dẫn xuất | Cờ cho biết đồng hồ phản hồi đầu đã breached. |
| `resolution_breached` | boolean, dẫn xuất | Cờ cho biết đồng hồ giải quyết đã breached. |

## Trường escalation và review

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| `rejection_count` | số nguyên, dẫn xuất | Số lần Customer từ chối ở Resolved, cộng dồn từ `ticket_events`. |
| `needs_manager_review` | boolean, dẫn xuất | Đúng khi ticket có review đang mở. |
| `review_requested_at` | timestamp | Thời điểm bắt đầu yêu cầu review và chặn Resolved. |
| `review_completed_at` | timestamp hoặc `null` | Thời điểm Manager ghi phương án hợp lệ và gỡ chặn. |
| `reviewed_by` | định danh Manager hoặc `null` | Manager đã ghi phương án. |
| `handling_plan` | cấu trúc nội bộ | Gồm nguyên nhân chưa giải quyết được, hướng xử lý tiếp theo, `needs_expert_input` và ghi chú ý kiến chuyên môn tùy chọn. |
| `resolution_cycle_id` | định danh | Lượt xử lý gắn với review. |
| `needs_expert_input` | boolean | Cờ nội bộ, không tạo hành động hệ thống. |

Các trường escalation và review không có trong phản hồi dành cho Customer.

## Mức hiển thị cảnh báo SLA

Các mức là dẫn xuất và không lưu. Áp dụng riêng cho từng đồng hồ SLA `first_response` và `resolution`, dựa trên số giây làm việc còn lại của chính đồng hồ đó khi đang chạy. Customer không nhận mức cảnh báo theo BR-49.

| Mã | Ý nghĩa |
|---|---|
| `none` | Không cảnh báo; gồm đúng 3.600 giây còn lại, đồng hồ tạm dừng hoặc đã hoàn tất. |
| `soft` | Còn từ 900 đến 3.599 giây làm việc. |
| `emphasized` | Còn từ 1 đến 899 giây làm việc. |
| `due` | Đúng deadline. |
| `breached` | Sau deadline. |

## Tiền tố mã tài liệu

| Tiền tố | Loại |
|---|---|
| `US` | User story |
| `FR` | Functional requirement |
| `NFR` | Non-functional requirement |
| `API` | API requirement/contract |
| `TC` | Test case |
| `A` | Acceptance criterion |
| `D` | Decision log |
| `M` | Metric báo cáo |
| `BR` | Business rule |
| `OQ` | Open question |
