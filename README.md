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

Tài liệu quy trình đã hoàn thành theo xác nhận chủ dự án: [As-Is (giả định)](docs/02-process/as-is.md), [To-Be v1.0](docs/02-process/to-be.md) và [vòng đời ticket](docs/02-process/ticket-states.md). Hai sơ đồ BPMN nằm trong cùng [file nguồn nhiều trang](docs/02-process/support-processes.drawio), mở trang **As-Is** hoặc **To-Be**; ảnh xuất và Mermaid xem nhanh có trong từng tài liệu.

## Cách chạy

Python 3.12 (môi trường đã kiểm tra). Từ thư mục repo, tạo virtualenv rồi gọi Python của môi trường đó.

Windows PowerShell đã kiểm tra ngày 12/10/2026 với Python 3.12.10 cài theo người dùng ở vị trí ổn định. Dùng đường dẫn Python 3.12 đã cài trên máy của bạn; không chạy lệnh tạo lại nếu `.venv` đã tồn tại cần giữ:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -m pip check
& .\.venv\Scripts\python.exe -m pytest
& .\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

Không cần activation hoặc đổi ExecutionPolicy. Trên hệ thống khác, sau khi tạo và kích hoạt virtualenv:

```bash
python -m pip install -r requirements.txt
python -m pytest
python -m uvicorn backend.app:app --port 8000
```

Mở http://127.0.0.1:8000/docs. Header `X-Demo-User-Id`: Customer 1/2, Agent 3/4/5, Manager 6. Không phải đăng nhập thật. SQLite tự tạo tại data/ticketing.sqlite3; có thể đặt biến môi trường TICKETING_DB để chọn file khác.

Tùy chọn trước khi chạy API: `python -m backend.seed` tạo 4 tình huống demo trên database chưa có ticket, không xóa dữ liệu có sẵn. Seed có timestamp cố định 12/10/2026 08:00 UTC+7, không đại diện dữ liệu doanh nghiệp thật.

Thiết kế: [ERD/data dictionary](docs/04-data-api/data-design.md), [API contract](docs/04-data-api/api-contract.md), [OpenAPI](api/openapi.json), [SQL](sql/README.md). Prototype độc lập đã dựng theo [spec](docs/05-prototype/prototype-spec.md); [hướng dẫn mở](prototype/README.md).

### Prototype tĩnh — xem trước giao diện

Từ repo chạy `& .\.venv\Scripts\python.exe -m http.server 8765 --bind 127.0.0.1`, rồi mở http://127.0.0.1:8765/prototype/. Dùng điều khiển demo để đổi Customer/Agent/Manager, chọn sáu nhóm tình huống và tiến clock UTC+7 đứng yên. Tải/khôi phục kịch bản thay dữ liệu trình duyệt; không gọi API. Danh tính mô phỏng không là đăng nhập thật. Ctrl+C dừng server.

**[Mở demo GitHub Pages](https://phuoctrong2005.github.io/ba-ticketing-sla-case-study/)**. Mở **Điều khiển demo**, chọn kịch bản và Customer/Agent/Manager; làm theo hướng dẫn theo vai trò, tiến clock bằng nút/ô UTC+7. Bấm **Khôi phục bộ mẫu** để thử lại từ đầu; thao tác này thay dữ liệu demo hiện hành. Demo mô phỏng — dữ liệu trong trình duyệt, không gọi API; không cần chạy FastAPI.

JavaScript/Edge headless đạt **110 PASS / 0 FAIL**, gồm **83 fixture** nguyên bản, controller/sáu demo/DOM/storage và UX. Chủ dự án phê duyệt yêu cầu/kịch bản, các chỉnh UX và chấp nhận kết quả/ảnh bằng chứng từ kiểm thử tự động; không ghi rằng chủ dự án tự thao tác toàn bộ kịch bản hoặc chạy công cụ. [Báo cáo Pages, kiểm thử mới và public smoke](tests/evidence/pages-report-20261013.md) phân biệt kiểm thử đầy đủ local với smoke trên site. Postman/video chưa làm; chưa xác nhận v1.0 hoàn thành.

## Kiểm thử

### Backend implementation — 12/10/2026

Yêu cầu và thiết kế đã được chủ dự án duyệt. FastAPI/SQLite có workflow, quyền, hai SLA, review, sự kiện/projection và báo cáo M-01…M-07. Kết quả thực thi và giới hạn: [backend test report](tests/evidence/backend-test-report.md); không gán kết quả prototype vào backend.

Bước 1 Windows với Python nền ổn định: pytest **181/181 PASS** tại repo và thư mục source mới có cả backend chưa commit; `pip check` đạt ở cả hai môi trường. `/docs`, `/openapi.json`, luồng tạo → nhận → Resolved → Closed và kiểm tra Customer không thấy SLA/cảnh báo/ghi chú/review nội bộ đã chạy qua HTTP thật. [Báo cáo và giới hạn](tests/evidence/step1-windows-20261012-162259-report.md), [JUnit repo](tests/evidence/step1-windows-20261012-162259-repo-junit.xml), [JUnit clean-start](tests/evidence/step1-windows-20261012-162259-clean-junit.xml). Fixture 83 ca và bằng chứng cũ giữ nguyên byte; virtualenv dự phòng và thư mục kiểm tra vẫn được giữ. Kết quả này chỉ hoàn tất bước ổn định môi trường/clean-start, không xác nhận toàn bộ v1.0.

### Đối chiếu fixture trước triển khai — mốc commit 4769e84

Fixture hiện có **83 verified, 0 draft**. Theo [báo cáo đối chiếu 83 ca](tests/evidence/sla-verification-83.md), checker tham chiếu đạt **83 PASS, 0 FAIL, 1.496 phép so sánh**; đối chiếu phụ SLA-83 tại **08:00:00 đạt 5 phép so sánh**, ghi riêng với kết quả chính tại `as_of=08:00:01`. Đây là kết quả đã ghi nhận ở commit `4769e84`, không phải lần chạy mới khi cập nhật README.

Theo [coverage hiện hành ngày 10/10/2026](docs/spec/scenario-coverage.md#nhập-sla-82-và-sla-83--10102026), **gate logic SLA chính đã mở cho việc viết logic**; **gate tính bối cảnh M-07 đủ điều kiện viết logic**. SLA-82/SLA-83 đã phủ hai nhánh Waiting còn thiếu và biên 08:00:01. Gate mở không đồng nghĩa backend đã được triển khai hoặc kiểm thử.

Xác nhận đáp án của chủ dự án qua hội thoại được ghi riêng với kết quả chạy công cụ tham chiếu do Codex thực hiện; không suy ra phương pháp tự tính hoặc bằng chứng chủ dự án tự chạy công cụ. Tại mốc này A1/A2, HTTP `REVIEW_REQUIRED`, quyền/nội dung và tính nguyên tử chưa có API test; kết quả implementation hiện hành nằm trong backend test report. Workflow review không bị gate phép tính chặn theo D-33. Trạng thái truy vết tại [docs/traceability.md](docs/traceability.md).

Hướng dẫn chạy checker cho các mốc 69/81/83 và audit cấu trúc hiện hành nằm trong [README công cụ tham chiếu](tests/sla/reference/README.md). Audit cấu trúc không tính SLA; đối chiếu fixture không phải test implementation.

### Bằng chứng lịch sử — mốc 69 và 81 ca

Bộ 69 fixture SLA đã được chủ dự án xác nhận lúc `2026-10-06T09:42:31+07:00`. Báo cáo lịch sử D-40 ghi trợ lý AI chạy tham chiếu thay chủ dự án: 69/69 PASS, 1.243 so sánh; SHA-256 nguồn `91c3163a6dcb6707832e2e3c2f6ada4677a8f01e0e67ae6a8f0b5ad0af4c569f`, script `764c284609d7074cbebc7c027576e9c8a16c9a8792456f8e4909ca221464f9ed`. Hai hash đã được xác minh khớp byte trong ZIP người dùng cung cấp tại `D:\Download\SLA_Verification_Package.zip`.

Fixture 69 ca trước lần nhập nháp có SHA-256 `4bcad90141b1d6b86a28804b93a961cea2862d84011c6b463439c370c17397b9`. [Đối chiếu nguồn lịch sử](tests/evidence/sla-source-comparison.json) xác nhận cả 69 scenario khớp toàn bộ; khác hash do nguồn có wrapper metadata, repo là mảng và định dạng JSON khác. Lúc `2026-10-06T12:51:30+07:00`, checker gốc chạy trực tiếp trên repo đạt [69 PASS, 0 FAIL, 1.243 phép so sánh](tests/evidence/sla-reference-results.json), exit code 0; [run record](tests/evidence/sla-reference-run.json) lưu stdout/stderr, Python và hash. [Audit cấu trúc lịch sử](tests/evidence/sla-fixture-audit.json) giữ nguyên 69/69, 3.792 assertion. [Báo cáo hòa giải](tests/evidence/sla-reconciliation.md) và [manifest SHA-256](tests/evidence/sla-reconciliation.sha256) là bằng chứng của phiên bản 69 ca, không phải toàn bộ fixture 83 ca hiện hành.

Ngày 08/10/2026, sau [lần nhập nháp](tests/evidence/sla-draft-import.md), chủ dự án xác nhận S1–S12 = SLA-70…SLA-81 thành `verified`. Tại mốc này, fixture có **81 verified, 0 draft**; 69 object đầu giữ nguyên byte. S12 có G due `2026-10-06T08:30:00+07:00`. [Báo cáo lịch sử 81 ca](tests/evidence/sla-verification-81.md): checker gốc trên nguồn 69 ca đạt 69 PASS / 0 FAIL, 1.243 phép so sánh; checker 81 ca dùng lại engine gốc đạt 81 PASS / 0 FAIL, 1.460 phép so sánh (12 ca mới: 217). Audit cấu trúc 81/81 PASS, không tính SLA. Gate logic SLA chính chưa mở tại mốc 81; kết luận này đã được thay thế bởi trạng thái hiện hành ở trên.

## Phần đã làm, mô phỏng và giới hạn

Hiện repository có tài liệu nền, decision log, open questions, fixture, audit cấu trúc và checker tham chiếu độc lập đã chạy. Đã có backend/API, SQL tổng hợp trên snapshot và test implementation; prototype tĩnh độc lập, bằng chứng JS/DOM và cấu hình Pages chỉ xuất bản runtime. Postman collection và video demo chưa làm. Backend dùng danh tính demo cố định, không có đăng nhập thật. Chủ dự án đã chấp nhận UX/kết quả/ảnh tự động cho prototype; chưa xác nhận hoàn thành toàn bộ v1.0.

Giới hạn đã biết: Ticket High có SLA phản hồi đầu 3.600 giây; ngưỡng cảnh báo cố định 3.600 giây nên cảnh báo nhẹ xuất hiện sau giây làm việc đầu tiên (còn 3.599 giây) và gần như toàn bộ thời hạn phản hồi đầu của High ở trạng thái cảnh báo. SLA phản hồi đầu Normal 7.200 giây: 3.600 giây đầu chưa cảnh báo. Từ chối trong giờ với ngân sách 0 giây khiến ticket thành breached ngay sau thời điểm quay lại; M-02/M-03 chỉ gồm ticket Closed trong kỳ nên ticket chưa Closed chưa được tính và báo cáo có dòng “Còn N ticket chưa Closed, chưa tính vào các tỷ lệ này”. Escalation dùng một Manager demo, không có người thay thế; không bảo đảm giải quyết triệt để vì Customer vẫn là người xác nhận Closed. Hỗ trợ chuyên môn chỉ là cờ và ghi chú nội bộ; ngưỡng từ chối 3 là cấu hình demo.

## Roadmap (ngoài phạm vi v1.0)

- Chuyển Agent hoặc tự phân công; đổi ưu tiên sau khi tạo; mở lại Closed; tự đóng.
- CSAT; lịch ngày lễ; email/SMS thật; đa kênh; nhiều tenant; đăng nhập thật.
- Nối prototype với API; xếp hạng Agent.
- Hiển thị thời hạn dự kiến phản hồi cho Customer thay cho mức cảnh báo nội bộ.

## Tiêu chí hoàn thành v1.0

Luồng chính chạy được trên prototype và API tương ứng; quyền được kiểm tra ở backend; SLA có các ca verified; hai ca nhận đồng thời đạt; dữ liệu dẫn xuất dựng lại đúng từ sự kiện gốc; báo cáo SQL khớp dữ liệu mẫu; README đã được thử thực tế từ thư mục mới; giới hạn và phần mô phỏng được nêu trung thực. Chi tiết backlog có tại [TASKS.md](TASKS.md).
