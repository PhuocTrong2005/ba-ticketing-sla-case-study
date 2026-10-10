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

### Trạng thái hiện hành — mốc commit 4769e84

Fixture hiện có **83 verified, 0 draft**. Theo [báo cáo đối chiếu 83 ca](tests/evidence/sla-verification-83.md), checker tham chiếu đạt **83 PASS, 0 FAIL, 1.496 phép so sánh**; đối chiếu phụ SLA-83 tại **08:00:00 đạt 5 phép so sánh**, ghi riêng với kết quả chính tại `as_of=08:00:01`. Đây là kết quả đã ghi nhận ở commit `4769e84`, không phải lần chạy mới khi cập nhật README.

Theo [coverage hiện hành ngày 10/10/2026](docs/spec/scenario-coverage.md#nhập-sla-82-và-sla-83--10102026), **gate logic SLA chính đã mở cho việc viết logic**; **gate tính bối cảnh M-07 đủ điều kiện viết logic**. SLA-82/SLA-83 đã phủ hai nhánh Waiting còn thiếu và biên 08:00:01. Gate mở không đồng nghĩa backend đã được triển khai hoặc kiểm thử.

Xác nhận đáp án của chủ dự án qua hội thoại được ghi riêng với kết quả chạy công cụ tham chiếu do Codex thực hiện; không suy ra phương pháp tự tính hoặc bằng chứng chủ dự án tự chạy công cụ. A1/A2, HTTP `REVIEW_REQUIRED`, quyền/nội dung và tính nguyên tử vẫn cần API test riêng. Workflow review không bị gate phép tính chặn theo D-33. Trạng thái truy vết tại [docs/traceability.md](docs/traceability.md).

Hướng dẫn chạy checker cho các mốc 69/81/83 và audit cấu trúc hiện hành nằm trong [README công cụ tham chiếu](tests/sla/reference/README.md). Audit cấu trúc không tính SLA; đối chiếu fixture không phải test implementation.

### Bằng chứng lịch sử — mốc 69 và 81 ca

Bộ 69 fixture SLA đã được chủ dự án xác nhận lúc `2026-10-06T09:42:31+07:00`. Báo cáo lịch sử D-40 ghi trợ lý AI chạy tham chiếu thay chủ dự án: 69/69 PASS, 1.243 so sánh; SHA-256 nguồn `91c3163a6dcb6707832e2e3c2f6ada4677a8f01e0e67ae6a8f0b5ad0af4c569f`, script `764c284609d7074cbebc7c027576e9c8a16c9a8792456f8e4909ca221464f9ed`. Hai hash đã được xác minh khớp byte trong ZIP người dùng cung cấp tại `D:\Download\SLA_Verification_Package.zip`.

Fixture 69 ca trước lần nhập nháp có SHA-256 `4bcad90141b1d6b86a28804b93a961cea2862d84011c6b463439c370c17397b9`. [Đối chiếu nguồn lịch sử](tests/evidence/sla-source-comparison.json) xác nhận cả 69 scenario khớp toàn bộ; khác hash do nguồn có wrapper metadata, repo là mảng và định dạng JSON khác. Lúc `2026-10-06T12:51:30+07:00`, checker gốc chạy trực tiếp trên repo đạt [69 PASS, 0 FAIL, 1.243 phép so sánh](tests/evidence/sla-reference-results.json), exit code 0; [run record](tests/evidence/sla-reference-run.json) lưu stdout/stderr, Python và hash. [Audit cấu trúc lịch sử](tests/evidence/sla-fixture-audit.json) giữ nguyên 69/69, 3.792 assertion. [Báo cáo hòa giải](tests/evidence/sla-reconciliation.md) và [manifest SHA-256](tests/evidence/sla-reconciliation.sha256) là bằng chứng của phiên bản 69 ca, không phải toàn bộ fixture 83 ca hiện hành.

Ngày 08/10/2026, sau [lần nhập nháp](tests/evidence/sla-draft-import.md), chủ dự án xác nhận S1–S12 = SLA-70…SLA-81 thành `verified`. Tại mốc này, fixture có **81 verified, 0 draft**; 69 object đầu giữ nguyên byte. S12 có G due `2026-10-06T08:30:00+07:00`. [Báo cáo lịch sử 81 ca](tests/evidence/sla-verification-81.md): checker gốc trên nguồn 69 ca đạt 69 PASS / 0 FAIL, 1.243 phép so sánh; checker 81 ca dùng lại engine gốc đạt 81 PASS / 0 FAIL, 1.460 phép so sánh (12 ca mới: 217). Audit cấu trúc 81/81 PASS, không tính SLA. Gate logic SLA chính chưa mở tại mốc 81; kết luận này đã được thay thế bởi trạng thái hiện hành ở trên.

## Phần đã làm, mô phỏng và giới hạn

Hiện repository có tài liệu nền, decision log, open questions, fixture, audit cấu trúc và checker tham chiếu độc lập đã chạy. Chưa có backend/API, SQL, prototype, test implementation hoặc workflow thực thi. Khi được xây dựng, prototype sẽ mô phỏng dữ liệu trong trình duyệt; backend là mô phỏng dùng dữ liệu demo cố định, không có đăng nhập thật.

Giới hạn đã biết: Ticket High có SLA phản hồi đầu 3.600 giây; ngưỡng cảnh báo cố định 3.600 giây nên cảnh báo nhẹ xuất hiện sau giây làm việc đầu tiên (còn 3.599 giây) và gần như toàn bộ thời hạn phản hồi đầu của High ở trạng thái cảnh báo. SLA phản hồi đầu Normal 7.200 giây: 3.600 giây đầu chưa cảnh báo. Từ chối trong giờ với ngân sách 0 giây khiến ticket thành breached ngay sau thời điểm quay lại; M-02/M-03 chỉ gồm ticket Closed trong kỳ nên ticket chưa Closed chưa được tính và báo cáo có dòng “Còn N ticket chưa Closed, chưa tính vào các tỷ lệ này”. Escalation dùng một Manager demo, không có người thay thế; không bảo đảm giải quyết triệt để vì Customer vẫn là người xác nhận Closed. Hỗ trợ chuyên môn chỉ là cờ và ghi chú nội bộ; ngưỡng từ chối 3 là cấu hình demo.

## Roadmap (ngoài phạm vi v1.0)

- Chuyển Agent hoặc tự phân công; đổi ưu tiên sau khi tạo; mở lại Closed; tự đóng.
- CSAT; lịch ngày lễ; email/SMS thật; đa kênh; nhiều tenant; đăng nhập thật.
- Nối prototype với API; xếp hạng Agent.
- Hiển thị thời hạn dự kiến phản hồi cho Customer thay cho mức cảnh báo nội bộ.

## Tiêu chí hoàn thành v1.0

Luồng chính chạy được trên prototype và API tương ứng; quyền được kiểm tra ở backend; SLA có các ca verified; hai ca nhận đồng thời đạt; dữ liệu dẫn xuất dựng lại đúng từ sự kiện gốc; báo cáo SQL khớp dữ liệu mẫu; README đã được thử thực tế từ thư mục mới; giới hạn và phần mô phỏng được nêu trung thực. Chi tiết backlog có tại [TASKS.md](TASKS.md).
