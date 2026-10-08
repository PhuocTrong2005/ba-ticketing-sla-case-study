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

Bộ 69 fixture SLA đã được chủ dự án xác nhận lúc `2026-10-06T09:42:31+07:00`. Báo cáo lịch sử D-40 ghi trợ lý AI chạy tham chiếu thay chủ dự án: 69/69 PASS, 1.243 so sánh; SHA-256 nguồn `91c3163a6dcb6707832e2e3c2f6ada4677a8f01e0e67ae6a8f0b5ad0af4c569f`, script `764c284609d7074cbebc7c027576e9c8a16c9a8792456f8e4909ca221464f9ed`. Hai hash đã được xác minh khớp byte trong ZIP người dùng cung cấp tại `D:\Download\SLA_Verification_Package.zip`.

Fixture 69 ca trước lần nhập nháp có SHA-256 `4bcad90141b1d6b86a28804b93a961cea2862d84011c6b463439c370c17397b9`. [Đối chiếu nguồn lịch sử](tests/evidence/sla-source-comparison.json) xác nhận cả 69 scenario khớp toàn bộ; khác hash do nguồn có wrapper metadata, repo là mảng và định dạng JSON khác. Lúc `2026-10-06T12:51:30+07:00`, checker gốc chạy trực tiếp trên repo đạt [69 PASS, 0 FAIL, 1.243 phép so sánh](tests/evidence/sla-reference-results.json), exit code 0; [run record](tests/evidence/sla-reference-run.json) lưu stdout/stderr, Python và hash. [Audit cấu trúc lịch sử](tests/evidence/sla-fixture-audit.json) giữ nguyên 69/69, 3.792 assertion. [Báo cáo hòa giải](tests/evidence/sla-reconciliation.md) và [manifest SHA-256](tests/evidence/sla-reconciliation.sha256) là bằng chứng của phiên bản 69 ca, không phải toàn bộ fixture 81 ca hiện tại.

Ngày 08/10/2026 nhập S1–S12 thành SLA-70…SLA-81, toàn bộ `draft`; 69 ca verified giữ nguyên cả byte của object. [Báo cáo nhập](tests/evidence/sla-draft-import.md): cấu trúc cũ 69 PASS / 0 FAIL (3.792 assertion), mới 12 PASS / 0 FAIL (850 assertion). Checker gốc chạy lại riêng 69 ca cũ: 69 PASS / 0 FAIL, 1.243 so sánh. CLI chỉ nhận 69 ID nên từ chối bộ 81 ca trước khi đối chiếu; **12 ca mới có 0 phép so sánh SLA, chưa có kết luận PASS/FAIL SLA**. S12 có G due `2026-10-06T08:30:00+07:00`. Chưa mở gate.

Chạy lại checker gốc trên bản nguồn 69 ca (kết quả mới ghi vào tệp riêng):

```powershell
python tests/sla/reference/validate_sla_reference.py tests/sla/reference/source/sla_draft_data.json --report tests/evidence/sla-source-reference-rerun.json
```

Chạy audit cấu trúc fixture hiện hành từ thư mục repo (không tính SLA). Audit lịch sử chỉ nhận 69 ca verified, giữ nguyên:

```powershell
python tests/sla/audit_draft_import.py
```

Cả 12 nhóm đã có mã verified; bảng yêu cầu → ca hiện có → phần chưa kiểm chứng nằm tại [scenario coverage](docs/spec/scenario-coverage.md). Gate logic SLA chính và gate tính bối cảnh M-07 **chưa được xác nhận mở** do các nhánh thiếu; blocker thiếu ZIP/hash đã được giải quyết. Không đổi tiêu chí gate. Workflow review không bị gate này chặn theo D-33. Checker chưa kiểm tra được lỗi Manager `INVALID_TICKET_STATE`/`TICKET_CLOSED`, quyền/nội dung/API thật. Fixture/reference check chưa chứng minh backend/API/SQL/prototype/concurrency đã chạy đúng. Trạng thái truy vết tại [docs/traceability.md](docs/traceability.md).

## Phần đã làm, mô phỏng và giới hạn

Hiện repository có tài liệu nền, decision log, open questions, fixture, audit cấu trúc và checker tham chiếu độc lập đã chạy. Chưa có prototype, backend, SQL, test implementation hoặc workflow thực thi. Khi được xây dựng, prototype sẽ mô phỏng dữ liệu trong trình duyệt; backend là mô phỏng dùng dữ liệu demo cố định, không có đăng nhập thật.

Giới hạn đã biết: Ticket High có SLA phản hồi đầu 3.600 giây; ngưỡng cảnh báo cố định 3.600 giây nên cảnh báo nhẹ xuất hiện sau giây làm việc đầu tiên (còn 3.599 giây) và gần như toàn bộ thời hạn phản hồi đầu của High ở trạng thái cảnh báo. SLA phản hồi đầu Normal 7.200 giây: 3.600 giây đầu chưa cảnh báo. Từ chối trong giờ với ngân sách 0 giây khiến ticket thành breached ngay sau thời điểm quay lại; M-02/M-03 chỉ gồm ticket Closed trong kỳ nên ticket chưa Closed chưa được tính và báo cáo có dòng “Còn N ticket chưa Closed, chưa tính vào các tỷ lệ này”. Escalation dùng một Manager demo, không có người thay thế; không bảo đảm giải quyết triệt để vì Customer vẫn là người xác nhận Closed. Hỗ trợ chuyên môn chỉ là cờ và ghi chú nội bộ; ngưỡng từ chối 3 là cấu hình demo.

## Roadmap (ngoài phạm vi v1.0)

- Chuyển Agent hoặc tự phân công; đổi ưu tiên sau khi tạo; mở lại Closed; tự đóng.
- CSAT; lịch ngày lễ; email/SMS thật; đa kênh; nhiều tenant; đăng nhập thật.
- Nối prototype với API; xếp hạng Agent.
- Hiển thị thời hạn dự kiến phản hồi cho Customer thay cho mức cảnh báo nội bộ.

## Tiêu chí hoàn thành v1.0

Luồng chính chạy được trên prototype và API tương ứng; quyền được kiểm tra ở backend; SLA có các ca verified; hai ca nhận đồng thời đạt; dữ liệu dẫn xuất dựng lại đúng từ sự kiện gốc; báo cáo SQL khớp dữ liệu mẫu; README đã được thử thực tế từ thư mục mới; giới hạn và phần mô phỏng được nêu trung thực. Chi tiết backlog có tại [TASKS.md](TASKS.md).
