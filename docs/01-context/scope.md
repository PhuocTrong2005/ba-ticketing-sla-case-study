# Scope v1.0

## 1. Trong phạm vi
- Khách hàng tạo ticket với mức ưu tiên High hoặc Normal, xem ticket của mình (BR-03, BR-36).
- Agent xem hàng đợi ticket chưa nhận và tự nhận khi còn khả năng xử lý (BR-04, BR-12, BR-13).
- Trao đổi tin nhắn công khai; Agent ghi chú nội bộ (BR-10).
- Năm trạng thái và các chuyển trạng thái hợp lệ (BR-07, BR-08).
- Hai đồng hồ SLA: phản hồi đầu tiên và giải quyết, tính đến giây (BR-17 đến BR-26).
- Khách xác nhận hoặc từ chối kết quả (BR-08, BR-09).
- Escalation: từ lần từ chối thứ 3, mỗi lần tạo một lượt review; Manager ghi phương án xử lý nội bộ; review mở chặn Agent báo Resolved (BR-52 đến BR-58).
- Manager xem ticket, tải công việc và báo cáo, và ghi phương án cho review đang mở (BR-05, BR-35, BR-54).
- Lịch sử sự kiện để dựng lại diễn biến (BR-27 đến BR-31).
- Prototype, mock API, dữ liệu mẫu, SQL và kiểm thử.

## 2. Ngoài phạm vi v1.0
- Chuyển Agent, tự động phân công theo tải hoặc kỹ năng.
- Thay đổi mức ưu tiên sau khi tạo ticket.
- Mở lại ticket đã Closed.
- Tự động đóng ticket; khảo sát CSAT.
- Lịch ngày lễ.
- Email/SMS thật, đa kênh, nhiều doanh nghiệp độc lập.
- Đăng nhập, đăng ký, quản lý mật khẩu thật.
- Kết nối prototype online với backend.
- Xếp hạng Agent hoặc điểm tổng hợp.
- Mô phỏng hỗ trợ chuyên môn: tạo yêu cầu, gửi thông báo, phân công nhóm kỹ thuật, chuyển Agent (BR-55 chỉ lưu cờ và ghi chú nội bộ).
- Người thay thế Manager, tự leo thang cấp cao hơn.
- Trạng thái thứ sáu cho escalation (D-26).

Hướng phát triển sau v1.0 nằm ở Roadmap trong README; không phải mục nào ngoài phạm vi cũng là hướng phát triển.

## 3. Sản phẩm bàn giao
| Hạng mục | Vị trí |
|---|---|
| Project brief, scope, stakeholder | `docs/01-context/` |
| Quy trình As-Is/To-Be, BPMN, trạng thái | `docs/02-process/` |
| User stories, acceptance criteria, FR/NFR | `docs/03-requirements/` |
| ERD, data dictionary, API specification | `docs/04-data-api/` |
| Quy tắc nghiệp vụ, bộ mã, phạm vi kịch bản | `docs/spec/` |
| Decision log, open questions, traceability | `docs/` |
| Prototype 4 màn hình | `prototype/` |
| Backend FastAPI, logic SLA | `backend/` |
| Schema, dữ liệu mẫu, truy vấn SQL | `database/` |
| Postman collection và environment | `api/` |
| Test SLA, API, đồng thời; bằng chứng | `tests/` |
| README, video demo | gốc repo |

## 4. Điều kiện hoàn thành v1.0
- Luồng chính chạy được trên prototype và trên API tương ứng.
- Quyền được kiểm tra ở backend, gồm quyền ghi phương án của Manager.
- Các ca bao phủ đủ 12 nhóm có đáp án được chủ dự án xác nhận `verified` (tự tính độc lập) và kết quả kiểm thử thực tế tương ứng đạt.
- Hai ca nhận đồng thời đạt; lần từ chối tạo review chạy trong một giao dịch.
- Dữ liệu dẫn xuất dựng lại đúng từ sự kiện gốc.
- Báo cáo SQL, gồm M-07, khớp dữ liệu mẫu có kết quả biết trước.
- README đã được thử thực tế từ thư mục mới.
- Phần chạy thật, phần mô phỏng và giới hạn được nêu trung thực.

## 5. Giới hạn đã chấp nhận
- Prototype không gọi API thật; backend chạy local.
- Chưa xử lý ngày lễ.
- Từ chối trong giờ khi còn 0 giây khiến ticket breached ngay sau thời điểm quay lại (BR-46).
- M-02 và M-03 chỉ gồm ticket Closed trong kỳ (BR-35).
- High phản hồi đầu nằm trong vùng cảnh báo gần như toàn bộ thời hạn; dưới 15 phút chuyển sang mức nhấn mạnh (BR-39).
- Một Manager demo, không có người thay thế; ticket có thể chờ review lâu nếu Manager không phản hồi.
- Escalation không bảo đảm giải quyết triệt để: cơ chế chỉ buộc xem xét lại cách giải quyết, khách vẫn là người xác nhận Closed.
- Hỗ trợ chuyên môn chỉ là cờ và ghi chú nội bộ.
- Ngưỡng 3 lần từ chối là cấu hình demo.

## 6. Quy tắc escalation đã chốt liên quan phạm vi
- Agent được chuyển Waiting for Customer khi review đang mở; chỉ Resolved bị chặn (BR-57).
- Manager ghi phương án khi không có review mở nhận 409 `INVALID_TICKET_STATE`; ticket Closed nhận 409 `TICKET_CLOSED` (BR-58).
- Điều kiện chặn viết logic: nhóm 1 đến 11 chặn logic SLA chính, nhóm 12 chặn logic bối cảnh M-07, workflow review không bị chặn (D-33).
