# Traceability matrix

Khung truy vết này sẽ được bổ sung khi có yêu cầu, API/màn hình, kịch bản verified và bằng chứng hợp lệ. Không tự tạo bằng chứng hay gán trạng thái verified.

Sau xác nhận ngày 08/10/2026, fixture có **SLA-01…SLA-81 verified**. Chủ dự án xác nhận SLA-70…SLA-81 qua hội thoại; Codex chạy checker tham chiếu 81/81 PASS, 1.460 phép so sánh và [audit cấu trúc](../tests/evidence/sla-fixture-current-audit.json) 81/81 PASS. [Báo cáo hiện hành](../tests/evidence/sla-verification-81.md) phân biệt xác nhận, đối chiếu fixture và các kiểm thử implementation chưa có. Gate SLA chính còn chặn bởi hai biến thể Waiting; gate tính bối cảnh M-07 đủ điều kiện viết logic theo D-33. A1/A2 và HTTP `REVIEW_REQUIRED` chờ API test. Chưa gán test backend hoặc trạng thái duyệt cho stories/FR/NFR.

Lịch sử lúc nhập nháp ngày 08/10/2026: S1–S12 → SLA-70…SLA-81 khi đó đều draft; [ánh xạ nhóm/nhánh](spec/scenario-coverage.md#nhập-s1s12-ngày-08102026--draft-chưa-mở-gate) và [báo cáo nhập](../tests/evidence/sla-draft-import.md) giữ nguyên trạng thái tại thời điểm đó. 69 object verified không đổi. Kiểm tra cấu trúc mới 12/12 lúc đó không phải PASS SLA/API; checker gốc chỉ chạy được 69 ca cũ. Kết luận hiện hành ở đoạn trên.

| Yêu cầu (US/FR/NFR) | Quy tắc (BR) | API / màn hình | Test (TC) | Bằng chứng | Trạng thái |
|---|---|---|---|---|---|
| _Chưa lập_ | _Chưa lập_ | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-39 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | D-34; BR-39 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | D-35; BR-39 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | D-36; BR-25 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | D-37 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | D-38; BR-59 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | D-39; BR-60; BR-61 | SLA-01…SLA-69 fixture | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | D-40 | SLA-01…SLA-69 fixture | _Chưa lập_ | Chủ dự án xác nhận; AI chạy checker gốc trên fixture repo: [69 PASS / 0 FAIL, 1.243 so sánh](../tests/evidence/sla-reference-results.json), exit code 0. [Đối soát](../tests/evidence/sla-reconciliation.md) chứng minh scenario khớp nguồn và giải thích hash. Audit cấu trúc 3.792 assertion giữ riêng. | Owner-confirmed fixture; reference rerun passed; coverage incomplete |
| _Chưa lập_ | BR-40 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-41 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-42 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-43 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-44 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-45 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-46 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-47 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-48 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-49 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-50 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-51 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-52 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-53 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-54 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-55 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-56; M-07 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-57 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |
| _Chưa lập_ | BR-58 | _Chưa lập_ | _Chưa lập_ | _Chưa có_ | Draft |

## Ma trận yêu cầu v1.0 (nháp)

Artefact việc 1: [audit cấu trúc lịch sử](../tests/evidence/sla-fixture-audit.json), [checker tham chiếu gốc](../tests/sla/reference/validate_sla_reference.py), [run record](../tests/evidence/sla-reference-run.json), [đối chiếu nguồn](../tests/evidence/sla-source-comparison.json), [manifest SHA-256](../tests/evidence/sla-reconciliation.sha256). Audit không tính SLA; checker tính và đối chiếu fixture độc lập với backend. Cả hai không phải test backend/API/SQL/prototype/concurrency. Bảng verified đủ 12 nhóm nhưng còn thiếu nhánh theo [scenario coverage](spec/scenario-coverage.md); chưa xác nhận mở gate SLA chính/M-07. Stories/FR/NFR và các ma trận nháp giữ nguyên trạng thái, chưa được duyệt bởi lần chạy này.

Không có liên kết code hoặc test đã tồn tại trong bảng này. “Kiểm chứng dự kiến” là hoạt động sẽ lập sau khi implementation được phép.

| BR | Story / AC | FR / NFR | Kiểm chứng dự kiến |
|---|---|---|---|
| BR-03…BR-11, BR-36, BR-50 | US-01; AC-01…AC-05 | FR-01, FR-04 | Contract theo role/trạng thái và dữ liệu bắt buộc |
| BR-04, BR-12…BR-16, BR-34, BR-37, BR-45, BR-51 | US-02; AC-06…AC-11 | FR-03; NFR-02 | Ca nhận, tải và cạnh tranh; kiểm tra trạng thái dữ liệu cuối |
| BR-06, BR-32…BR-34, BR-49, BR-54, BR-58 | US-01/03/05; AC-03, AC-12…AC-13, AC-16, AC-21, AC-27 | FR-02; NFR-01 | Contract lỗi, thứ tự kiểm tra và lọc dữ liệu theo role |
| BR-16…BR-26, BR-38…BR-39, BR-46…BR-49, BR-59…BR-61 | US-04; AC-17…AC-22 | FR-05; NFR-04, NFR-05 | Fixture SLA và ca dựng lại sau khi logic được phép |
| BR-27…BR-31, BR-47 | US-04; AC-22 | FR-08; NFR-03, NFR-04 | Kiểm tra append-only và dựng lại dữ liệu dẫn xuất |
| BR-40…BR-41 | US-04; AC-21 | FR-09; NFR-06 | Review giao diện prototype sau khi được xây |
| BR-52…BR-58 | US-05; AC-23…AC-27 | FR-06; NFR-02 | Contract review, lỗi và tính nguyên tử từ chối/review |
| BR-13, BR-35, BR-42, BR-56 | US-06; AC-28…AC-31 | FR-07; NFR-05 | Đối chiếu report với dữ liệu mẫu sau khi triển khai |

## Phân loại BR chưa có AC trực tiếp

| BR | Phân loại | Nơi ghi nhận | Kiểm chứng dự kiến |
|---|---|---|---|
| BR-01, BR-02 | Thuộc phạm vi / kiến trúc | FR-01; NFR-06, NFR-07; scope | Review phạm vi, công nghệ và tuyên bố mô phỏng |
| BR-06 | Được bao phủ bằng FR/NFR | FR-02; NFR-01 | Contract quyền backend |
| BR-27…BR-31, BR-47 | Thuộc thiết kế dữ liệu / kiến trúc | FR-08; NFR-03, NFR-04 | Dựng lại từ event và kiểm tra dữ liệu |
| BR-32, BR-33 | Được bao phủ bằng FR/NFR | FR-01…FR-04; NFR-01 | Contract lỗi và thứ tự kiểm tra |
| BR-40, BR-41 | Cần bổ sung AC hành vi khi có prototype | FR-09; NFR-06 | Review prototype; chưa tạo AC chỉ để đủ số lượng |
| BR-53 | Được bao phủ bằng FR | FR-04, FR-06; AC-24 | Contract `REVIEW_REQUIRED` và hành vi sau review |
