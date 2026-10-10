# Đối chiếu SLA-01…SLA-83 — 10/10/2026

Chủ dự án cung cấp và xác nhận kết quả SLA-82/SLA-83 trong hội thoại ngày 10/10/2026, yêu cầu nhập `verified`. `verified_at=null`: không có giờ xác nhận chính xác, phương pháp tự tính hay bằng chứng chủ dự án chạy công cụ. Metadata ghi nguồn hội thoại; `calculation_note` chép diễn giải đáp án đã cung cấp, không giả định đây là tính tay của chủ dự án. Codex nhập hai ca và chạy Python tham chiếu riêng. Giữ nguyên 81 object cũ cả nội dung lẫn byte; không thêm schema, chính sách hoặc logic backend.

## Kết quả thực thi

| Công cụ / dữ liệu | PASS | FAIL | Phép so sánh SLA | Assertion cấu trúc |
|---|---:|---:|---:|---:|
| [Checker hiện hành, 83 ca](sla-reference-83-results.json) | 83 | 0 | 1.496 | — |
| Trong đó SLA-82 và SLA-83 | 2 | 0 | 36 (18 mỗi ca) | — |
| SLA-83 đối chiếu phụ tại 08:00:00, cùng events | 1 ảnh chụp | 0 | 5 | — |
| [Mốc 69 từ fixture hiện hành](sla-reference-83-milestone-69.json) | 69 | 0 | 1.243 | — |
| [Mốc 81 từ fixture hiện hành](sla-reference-83-milestone-81.json) | 81 | 0 | 1.460 | — |
| [Checker gốc trên nguồn 69 giữ nguyên](sla-reference-83-original-69.json) | 69 | 0 | 1.243 | — |
| [Audit cấu trúc 83](sla-fixture-83-audit.json) | 83 | 0 | 0 | 4.876 |

Tất cả exit code 0. Tổng lần chạy 83 là **1.501 phép** = 1.496 chính + 5 phụ; không gộp các lần chạy hồi quy thành số phép của 83 ca. Audit có 3.792 assertion cho 69 ca, 946 cho 12 ca tiếp theo, 138 cho hai ca mới; các global checks được báo riêng. Không gọi assertion cấu trúc là phép tính SLA.

Checker 83 chạy lúc `2026-10-10T08:23:55+07:00`, audit lúc `2026-10-10T08:23:55+07:00` bởi Codex; đây là giờ chạy công cụ, không phải giờ chủ dự án xác nhận. JSON report lưu command/argv, SHA-256, exit code, từng ca và giá trị tính lại. [README công cụ](../sla/reference/README.md) có lệnh tái chạy. Checker gốc chạy bằng lệnh `python -B tests/sla/reference/validate_sla_reference.py tests/sla/reference/source/sla_draft_data.json --report tests/evidence/sla-reference-83-original-69.json`; metadata xác nhận 69 ca trong report đó được chuyển nguyên từ nguồn cũ, không áp cho SLA-82/SLA-83.

## Nội dung đã đối chiếu

- SLA-82: P met/none, 600/3.000 giây; G intervals 3.600 + 1.800 = 5.400, còn 23.400, hạn 12/10 15:00, pending/none. Resume Chủ nhật 11/10 12:00 chỉ cộng giờ làm Thứ Hai.
- SLA-83: P met/none, 600/3.000 giây; G 28.800 + 1 = 28.801, còn 0, hạn 06/10 08:00:00, breached/breached tại 08:00:01. Ảnh chụp phụ đúng 08:00:00 đối chiếu status pending, warning due, deadline 08:00:00, consumed 28.800 và remaining 0. Việc pending tại hạn mới cũng kiểm chứng chưa có breach cũ bị giữ lại.
- Cả hai: In Progress, snapshot nhận pending/pending, 0 lần từ chối, không review/refusal, kết quả giải quyết chưa final. Khoảng đang chạy dùng `ended_at=null` và `business_seconds_as_of` đúng schema cũ; timestamp `+07:00`; events dùng `seq`, không dùng `event_id` client.

## Bảo toàn và hash

[Baseline trước nhập](sla-verification-83-baseline.json) ghi commit `2745ede6bd060c663e9d655176632aff0b35d8d2`, hash fixture 81, chiều dài/hash byte đến hết object SLA-81 và hash các artefact cũ. Audit so sánh 81 object với Git và hash tiền tố không đổi. [Kiểm tra bằng chứng](sla-verification-83-checks.json) kiểm tra hash report/input/script/dependencies, so kết quả từng ca với mốc lịch sử, bảo toàn artefact, link và `git diff --check`. [Manifest lần 83](sla-verification-83.sha256) hash byte JSON/Python có LF ổn định qua checkout; không ghi đè manifest hoặc report lịch sử 69/81. [Script kiểm tra](../sla/verify_sla_83_evidence.py) tạo và kiểm tra manifest từ lần chạy thật.

- Fixture 83 SHA-256: `6e75371714e5589eb78c45b0df3eb69595f2dfcc9362c9398b8c11989c0756ee`.
- Checker hiện hành SHA-256: `2363f6b1859cc4e9e0c5273a4d87f237ebc23a98333a3d2aced32cfa38393881`.
- Engine gốc SHA-256: `764c284609d7074cbebc7c027576e9c8a16c9a8792456f8e4909ca221464f9ed` (không đổi).
- Hàm so sánh CLI 81 SHA-256: `d0284a0c4bf9524f1149c623637431aa65b3d0c337b0d9bc19262d801f04d81f` (không đổi).

## Gate và giới hạn

**Gate logic SLA chính: mở cho việc viết logic theo AGENTS/D-33.** Nhóm 1–11 đều có ca verified và bảng nhóm → mã không còn nhóm trống. SLA-82 đóng nhánh Customer resume ngay cuối tuần; SLA-83 đóng nhánh resume ngoài giờ với 0 giây nhưng chưa từng breached và mốc sau hạn 08:00:01. Đối chiếu phụ cùng events tại 08:00:00 xác nhận pending/due; không thêm ca hoặc tự xác nhận đáp án. Các nhánh còn lại đã được đối soát ở mốc 81; không còn blocker coverage cho logic SLA chính. Không đổi tiêu chí gate. Gate tính M-07 tiếp tục đủ điều kiện viết logic theo đánh giá mốc 81. API A1/A2, HTTP REVIEW_REQUIRED, payload/quyền/atomicity và các tiêu chí hoàn thành v1.0 vẫn chưa kiểm thử; đây không phải blocker mới cho gate phép tính và không phải xác nhận hoàn thành backend.

[Coverage](../../docs/spec/scenario-coverage.md) và [traceability](../../docs/traceability.md) ghi nhánh → mã → bằng chứng. [Open questions](../../docs/open-questions.md) đóng khoảng thiếu coverage mốc 81, giữ phần contract/API chưa có. Không phát hiện mâu thuẫn cần thêm OQ.

Đây là đối chiếu fixture bằng công cụ tham chiếu có hỗ trợ AI, độc lập với backend; không chứng minh phương pháp kiểm tra của chủ dự án. Không chạy FastAPI, SQLite, HTTP, quyền, payload, concurrency, báo cáo SQL, prototype hoặc test dựng lại dữ liệu của backend. Gate mở chỉ cho phép bắt đầu viết logic, không chứng minh implementation đúng hoặc hoàn thành v1.0.

## T?p thay ??i

- `TASKS.md`
- `docs/decision-log.md`
- `docs/open-questions.md`
- `docs/spec/scenario-coverage.md`
- `docs/traceability.md`
- `tests/evidence/sla-fixture-83-audit.json`
- `tests/evidence/sla-reference-83-milestone-69.json`
- `tests/evidence/sla-reference-83-milestone-81.json`
- `tests/evidence/sla-reference-83-original-69.json`
- `tests/evidence/sla-reference-83-results.json`
- `tests/evidence/sla-verification-83-baseline.json`
- `tests/evidence/sla-verification-83-checks.json`
- `tests/evidence/sla-verification-83.md`
- `tests/evidence/sla-verification-83.sha256`
- `tests/sla/audit_fixture_83.py`
- `tests/sla/reference/README.md`
- `tests/sla/reference/validate_sla_reference_current.py`
- `tests/sla/sla-scenarios.json`
- `tests/sla/verify_sla_83_evidence.py`

Ki?m tra to?n v?n: 27/27 ki?m tra ??t, 37 artefact/c?ng c? l?ch s? gi? nguy?n; manifest 16 t?p JSON/Python ?? ???c ??c l?i v? kh?p SHA-256.

B?o c?o do checker g?c 69 xu?t tr?n Windows ???c chu?n h?a CRLF ? LF sau ch?y, gi? nguy?n n?i dung JSON; kh?ng s?a engine ho?c b?o c?o l?ch s?. Checker/audit m?i ghi LF tr?c ti?p. Ki?m tra b? sung x?c nh?n LF tr??c khi t?o manifest ?? hash kh?p b?n Git checkout.
