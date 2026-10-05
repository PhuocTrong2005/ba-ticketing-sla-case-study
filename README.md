# BA Ticketing & SLA Case Study

Case study giả định về hệ thống quản lý ticket hỗ trợ khách hàng và SLA cho doanh nghiệp phần mềm B2B. Đây là giải pháp mẫu gồm prototype và backend mô phỏng, không phải sản phẩm vận hành; mọi chính sách, số liệu và quy mô đều là giả định.

## Vấn đề

Case study mô tả việc quản lý ticket, phân quyền Customer/Agent/Manager, xử lý vòng đời ticket và theo dõi SLA phản hồi đầu cùng SLA giải quyết theo giờ làm việc.

## Quyết định then chốt

- Năm trạng thái: New, In Progress, Waiting for Customer, Resolved, Closed.
- SLA theo lịch Thứ Hai–Thứ Sáu, 08:00–17:00, Asia/Ho_Chi_Minh.
- Dữ liệu gốc là lịch sử sự kiện; SLA dẫn xuất phải dựng lại được từ sự kiện.
- Prototype HTML/CSS/JS tĩnh tách biệt với backend Python FastAPI + SQLite và không gọi API thật.

Nguồn sự thật: [business rules](docs/spec/business-rules.md), [bộ mã](docs/spec/codes.md), [decision log](docs/decision-log.md). Các điểm chưa chốt: [open questions](docs/open-questions.md).

## Cách chạy

Sẽ cập nhật khi prototype, backend và hướng dẫn chạy đã được xây dựng, kiểm tra thực tế từ một thư mục mới.

## Kiểm thử

Sẽ cập nhật sau khi các kịch bản SLA verified tối thiểu được chủ dự án chốt. Phạm vi dự kiến bao gồm SLA, API/phân quyền, nhận ticket đồng thời và bằng chứng; trạng thái truy vết hiện có tại [docs/traceability.md](docs/traceability.md).

## Phần đã làm, mô phỏng và giới hạn

Hiện repository có tài liệu nền, decision log, open questions và khung cấu trúc. Chưa có prototype, backend, SQL, test hoặc workflow thực thi. Khi được xây dựng, prototype sẽ mô phỏng dữ liệu trong trình duyệt; backend là mô phỏng dùng dữ liệu demo cố định, không có đăng nhập thật.

Giới hạn đã biết: Ticket High có SLA phản hồi đầu 3.600 giây; ngưỡng cảnh báo cố định 3.600 giây nên cảnh báo nhẹ xuất hiện sau giây làm việc đầu tiên (còn 3.599 giây) và gần như toàn bộ thời hạn phản hồi đầu của High ở trạng thái cảnh báo. SLA phản hồi đầu Normal 7.200 giây: 3.600 giây đầu chưa cảnh báo. Từ chối trong giờ với ngân sách 0 giây khiến ticket thành breached ngay sau thời điểm quay lại; M-02/M-03 chỉ gồm ticket Closed trong kỳ nên ticket chưa Closed chưa được tính và báo cáo có dòng “Còn N ticket chưa Closed, chưa tính vào các tỷ lệ này”. Escalation dùng một Manager demo, không có người thay thế; không bảo đảm giải quyết triệt để vì Customer vẫn là người xác nhận Closed. Hỗ trợ chuyên môn chỉ là cờ và ghi chú nội bộ; ngưỡng từ chối 3 là cấu hình demo.

## Roadmap (ngoài phạm vi v1.0)

- Chuyển Agent hoặc tự phân công; đổi ưu tiên sau khi tạo; mở lại Closed; tự đóng.
- CSAT; lịch ngày lễ; email/SMS thật; đa kênh; nhiều tenant; đăng nhập thật.
- Nối prototype với API; xếp hạng Agent.
- Hiển thị thời hạn dự kiến phản hồi cho Customer thay cho mức cảnh báo nội bộ.

## Tiêu chí hoàn thành v1.0

Luồng chính chạy được trên prototype và API tương ứng; quyền được kiểm tra ở backend; SLA có các ca verified; hai ca nhận đồng thời đạt; dữ liệu dẫn xuất dựng lại đúng từ sự kiện gốc; báo cáo SQL khớp dữ liệu mẫu; README đã được thử thực tế từ thư mục mới; giới hạn và phần mô phỏng được nêu trung thực. Chi tiết backlog có tại [TASKS.md](TASKS.md).
