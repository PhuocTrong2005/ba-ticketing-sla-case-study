# Traceability matrix

## Clean-start — D-49, 13/10/2026

[Report mới](../tests/evidence/portfolio-clean-start-report-20261013.md), [commit/OS/commands/servers](../tests/evidence/portfolio-clean-start-20261013-run.json), [JUnit 181](../tests/evidence/portfolio-clean-start-20261013-junit.xml): clone trực tiếp origin/main `7c35b2c`, không copy venv/data/cache/config; install/check/pytest/backend/docs/OpenAPI đạt. Prototype static URL docs có 24 smoke check; [JS clone 110/0](../tests/evidence/prototype-ux-20261013-012403.json); [Newman clone](../tests/evidence/newman-20261013-012500-070211-run.json) 191 request/514 assertion/0 lỗi/exit 0.

DOC-CS-01: [auditor lịch sử thất bại trước sửa tại `7c35b2c`](../tests/evidence/portfolio-clean-start-20261013-documentation-issue-before-fix.json), không là backend/UI bug. [Docs-only patch/recheck](../tests/evidence/portfolio-clean-start-20261013-doc-recheck.json) trên clone đạt 110/110, giữ auditor/assertion/fixture không đổi; prototype README hiện hành phân biệt runner tái lập và auditor lịch sử. [Clone lần 2](../tests/evidence/portfolio-clean-start-repeat-20261013.md) tái hiện lỗi hướng dẫn cũ và tách lỗi sandbox PyPI/%TEMP% khỏi backend. Run trỏ nhầm repo gốc được giữ và loại khỏi clean-start evidence. Không blanket PASS hướng dẫn commit cũ; chưa chạy trọn suite từ commit mới. [Checklist](release-checklist.md) ghi giới hạn và video còn thiếu.

## Mốc xuất bản portfolio 13/10/2026, D-48

[Ma trận AC-01…34](ac-traceability.md) có implementation, test/request/evidence/giới hạn, tách chức năng/quyền, đồng thời/dữ liệu, SLA, UI/báo cáo/tái lập; không blanket PASS. Tại mốc D-48 video và clean-start checkout mới còn thiếu; kết quả clean-start được bổ sung ở D-49 phía trên. [Release checklist](release-checklist.md) giữ video thiếu và phân biệt lỗi tài liệu commit cũ với bản sửa hiện hành.

Đã đối chiếu nguồn: Windows 181 pytest/0 lỗi; JS local 110/0; Pages 74 smoke check; Newman 191 request/514 assertion/0 lỗi. [Evidence index](../tests/evidence/README.md), [audit xuất bản](../tests/evidence/portfolio-publication-report-20261013.md). Postman được chủ dự án chấp nhận; runner/Codex thực thi, không suy chủ dự án tự thao tác mọi ca. Không chạy lại suite khi source/collection/helper và hash khớp.

Các phần dưới giữ nguyên như lịch sử từng mốc; “planned”, “chưa prototype/Postman/deploy” ở mốc cũ không là trạng thái hiện hành. Không thay BR/verified; portfolio v1.0 chưa hoàn tất.

Khung truy vết này sẽ được bổ sung khi có yêu cầu, API/màn hình, kịch bản verified và bằng chứng hợp lệ. Không tự tạo bằng chứng hay gán trạng thái verified.

## Tài liệu quy trình — 12/10/2026

Ba Markdown và sơ đồ đã hoàn thành theo xác nhận chủ dự án. Nguồn BPMN là [support-processes.drawio](02-process/support-processes.drawio), gồm hai trang **As-Is** và **To-Be**; ảnh xuất nằm trong tài liệu tương ứng. Các liên kết dưới đây là truy vết mô tả quy trình, không phải kết quả kiểm thử backend hoặc trạng thái duyệt stories/AC, FR/NFR.

| Mục liên quan | Tài liệu quy trình |
|---|---|
| BR-01; mục tiêu G-01, G-02, G-03, G-05, G-06, G-08 | [As-Is (giả định, chưa khảo sát)](02-process/as-is.md) |
| BR-07…BR-11, BR-13…BR-16; US-01…US-03 | [Vòng đời ticket](02-process/ticket-states.md); [luồng chính To-Be](02-process/to-be.md#1-luồng-chính-của-ticket) |
| BR-16…BR-26, BR-38, BR-46, BR-48, BR-59…BR-61; US-04 | [Tác động đến SLA theo bước](02-process/to-be.md#3-tác-động-đến-sla-theo-bước) |
| BR-52…BR-58; US-05 | [Review Manager](02-process/to-be.md#2-luồng-review-của-manager-chạy-song-song); [vòng đời ticket](02-process/ticket-states.md) |
| BR-56; M-07; US-06 | [Bối cảnh chờ review và Waiting](02-process/to-be.md#2-luồng-review-của-manager-chạy-song-song) |

Sau xác nhận ngày 10/10/2026, fixture có **SLA-01…SLA-83 verified**; 81 ca cũ giữ nguyên nội dung và byte object. SLA-82/SLA-83 do chủ dự án xác nhận qua hội thoại; Codex ghi `verified_at=null` và chạy công cụ riêng. Checker: **83 PASS / 0 FAIL, 1.496 phép so sánh**; đối chiếu phụ SLA-83 tại 08:00:00: 5/5 phép đạt; [audit cấu trúc](../tests/evidence/sla-fixture-83-audit.json): 83 PASS / 0 FAIL, 4.876 assertion. [Báo cáo hiện hành](../tests/evidence/sla-verification-83.md) có mốc 69/81, hash và giới hạn. Gate logic SLA chính mở theo AGENTS/D-33 sau khi đóng hai nhánh Waiting và biên 08:00:01; gate M-07 tiếp tục đủ điều kiện viết logic. Chưa gán test backend hoặc trạng thái duyệt stories/FR/NFR.

| Quy tắc / nhánh | Ca verified | Bằng chứng tham chiếu | Giới hạn |
|---|---|---|---|
| BR-17/20/23; resume Waiting ngay cuối tuần | SLA-82 | [83-case report](../tests/evidence/sla-reference-83-results.json): 18/18 phép đạt | Fixture toán học, chưa chạy backend/API |
| BR-17/23/39/48/60; resume ngoài giờ với 0 chưa breached, sau hạn một giây | SLA-83 | Cùng report: 18/18 tại 08:00:01; 5/5 riêng tại 08:00:00 | Đối chiếu phụ dùng cùng events, không phải ca thứ 84 |

Mốc 08/10/2026: [81 ca](../tests/evidence/sla-verification-81.md) đạt 81 PASS / 0 FAIL, 1.460 phép; gate chính khi đó chưa mở. Bằng chứng lịch sử giữ nguyên.

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

## Ma trận yêu cầu v1.0 — approved 12/10/2026

Artefact việc 1 (lịch sử 06/10/2026; kết luận hiện hành ở đầu tài liệu): [audit cấu trúc lịch sử](../tests/evidence/sla-fixture-audit.json), [checker tham chiếu gốc](../tests/sla/reference/validate_sla_reference.py), [run record](../tests/evidence/sla-reference-run.json), [đối chiếu nguồn](../tests/evidence/sla-source-comparison.json), [manifest SHA-256](../tests/evidence/sla-reconciliation.sha256). Audit không tính SLA; checker tính và đối chiếu fixture độc lập với backend. Cả hai không phải test backend/API/SQL/prototype/concurrency. Ở mốc lịch sử 06/10 bảng chưa đủ nhánh; kết luận này đã bị thay bởi gate mở ở mốc 83, xem [coverage](spec/scenario-coverage.md). Ở mốc lịch sử đó stories/FR/NFR chưa duyệt; chủ dự án đã duyệt ngày 12/10/2026.

Ma trận dưới đây ánh xạ yêu cầu đã duyệt; cách kiểm chứng vẫn là kế hoạch. Liên kết implementation và kết quả thực thi nằm ở cuối tài liệu; không gán kết quả prototype từ test backend.

| BR | Story / AC | FR / NFR | Kiểm chứng dự kiến |
|---|---|---|---|
| BR-03…BR-11, BR-36, BR-50 | US-01; AC-01…AC-05 | FR-01, FR-04 | Contract theo role/trạng thái và dữ liệu bắt buộc |
| BR-04, BR-12…BR-16, BR-34, BR-37, BR-45, BR-51 | US-02; AC-06…AC-11 | FR-03; NFR-02 | Ca nhận, tải và cạnh tranh; kiểm tra trạng thái dữ liệu cuối |
| BR-06, BR-32…BR-34, BR-49, BR-54, BR-58 | US-01/03/05; AC-03, AC-12…AC-13, AC-16, AC-21, AC-27 | FR-02; NFR-01 | Contract lỗi, thứ tự kiểm tra và lọc dữ liệu theo role |
| BR-16…BR-26, BR-38…BR-39, BR-46…BR-49, BR-59…BR-61 | US-04; AC-17…AC-22 | FR-05; NFR-04, NFR-05 | Fixture SLA và ca dựng lại sau khi logic được phép |
| BR-27…BR-31, BR-47 | US-04; AC-22 | FR-08; NFR-03, NFR-04 | Kiểm tra append-only và dựng lại dữ liệu dẫn xuất |
| BR-40…BR-41 | US-04; AC-32 | FR-09; NFR-06 | Review giao diện prototype sau khi được xây |
| BR-52…BR-58 | US-05; AC-23…AC-27 | FR-06; NFR-02 | Contract review, lỗi và tính nguyên tử từ chối/review |
| BR-13, BR-35, BR-42, BR-56 | US-06; AC-28…AC-31 | FR-07; NFR-05 | Đối chiếu report với dữ liệu mẫu sau khi triển khai |

## Phân loại BR chưa có AC trực tiếp

| BR | Phân loại | Nơi ghi nhận | Kiểm chứng dự kiến |
|---|---|---|---|
| BR-01, BR-02 | Thuộc phạm vi / kiến trúc | FR-01; NFR-06, NFR-07; scope | Review phạm vi, công nghệ và tuyên bố mô phỏng |
| BR-06 | Được bao phủ bằng FR/NFR | FR-02; NFR-01 | Contract quyền backend |
| BR-27…BR-31, BR-47 | Thuộc thiết kế dữ liệu / kiến trúc | FR-08; NFR-03, NFR-04 | Dựng lại từ event và kiểm tra dữ liệu |
| BR-32, BR-33 | Được bao phủ bằng FR/NFR | FR-01…FR-04; NFR-01 | Contract lỗi và thứ tự kiểm tra |
| BR-40, BR-41 | Đã có AC hành vi, chưa có prototype | FR-09; NFR-06; AC-32 | Prototype review: planned |
| BR-53 | Được bao phủ bằng FR | FR-04, FR-06; AC-24 | Contract `REVIEW_REQUIRED` và hành vi sau review |

## Backend được duyệt 12/10/2026 — planned trước triển khai

Nguồn xác nhận: chủ dự án duyệt báo cáo rà soát, BR, stories/AC, FR/NFR, thiết kế và backend trong hội thoại. Những dòng lịch sử “coverage incomplete” phía trên mô tả mốc cũ, không là gate hiện hành. Fixture vẫn 83 verified; test implementation ghi riêng.

| BR/FR/NFR | AC | Kiểm chứng dự kiến | Trạng thái ban đầu |
|---|---|---|---|
| BR-17…26,38,39,46…48,59…61 / FR-05 | AC-17…21 | tests/backend/test_sla.py: 83 fixture + các biên lịch | planned |
| BR-03…16,32…34,37,43…45,49…51,62 / FR-01…04 / NFR-01 | AC-01…16,27,33 | tests/backend/test_api.py: quyền/payload/workflow | planned |
| BR-15,52…58 / FR-06 / NFR-02 | AC-08,09,23…26,34 | tests/backend/test_integrity.py: threads/transactions/review | planned |
| BR-25,27…31,47 / FR-08 / NFR-03…05 | AC-07,22,34 | tests/backend/test_integrity.py: replay/zero/raw/event order | planned |
| BR-35,42,56,63 / FR-07 | AC-28…31 | tests/backend/test_reports.py: kỳ/filter/as_of/M-01…07 | planned |
| BR-40,41 / FR-09 / NFR-06 | AC-32 | Prototype review bằng tay, chưa triển khai | planned |

## Liên kết ca implementation đã thực thi (kết quả trong evidence, không gán cho ca planned)

- AC-01…16,27,33: [test_api.py](../tests/backend/test_api.py), gồm test_roles_privacy_and_queue, test_validation_state_order_and_forbidden_fields, test_review_errors_plan_and_waiting, test_customer_return_can_overload.
- AC-17…22: [test_sla.py](../tests/backend/test_sla.py) và test_fixture_through_http[SLA-01…SLA-83]; actor/nội dung được adapter test thêm minh bạch, không sửa fixture.
- AC-08/09/23/34, NFR-02…05: [test_integrity.py](../tests/backend/test_integrity.py); real threads, SQLite file, rào cản, transaction rollback, append-only, rebuild, zero/raw/order.
- AC-28…31: [test_reports.py](../tests/backend/test_reports.py), bốn ca về cohort, filter và snapshot quá khứ.
- AC-32/UI: planned; bộ test backend không chứng minh prototype.
- Kết quả từng test và giới hạn: [backend test report](../tests/evidence/backend-test-report.md), [JUnit](../tests/evidence/backend-junit.xml), [khởi động môi trường mới](../tests/evidence/backend-clean-start.json).

BR-62…BR-64 được cụ thể hóa trong API/data contract; AC-01/14/27/29/30 và các sửa NFR-02, FR-09 áp dụng theo các BR này. Các hàng _Chưa lập_/Draft phía trên là khung lịch sử, không là trạng thái yêu cầu hiện hành.

## Bước 1 Windows với Python nền ổn định — 12/10/2026

- Kiểm chứng cách chạy README/clean-start: Python 3.12.10, hai virtualenv riêng, `pip check` PASS; [JUnit repo 181/181](../tests/evidence/step1-windows-20261012-162259-repo-junit.xml), [JUnit source mới 181/181](../tests/evidence/step1-windows-20261012-162259-clean-junit.xml). Cả hai chạy toàn bộ suite cấu hình `pytest.ini` hiện tại, không sửa test/expected.
- FR-01…04 / NFR-01, AC-01…16 (phần luồng ngắn và riêng tư): HTTP thật Customer tạo → Agent nhận → Resolved có kết quả → Customer Closed; Customer không thấy SLA/cảnh báo/ghi chú và nội dung review/handling_plan đã tạo thực; endpoint reviews trả 404 cho Customer. Không suy luồng ngắn này phủ toàn bộ AC.
- [Run record HTTP, môi trường, lệnh và manifest source](../tests/evidence/step1-windows-20261012-162259-run.json); [báo cáo/giới hạn và kiểm tra bảo toàn](../tests/evidence/step1-windows-20261012-162259-report.md). Fixture và bằng chứng Linux/Windows trước đó giữ nguyên byte.
- AC-32/prototype, Postman, video, deploy chưa thực hiện trong bước này; không thay trạng thái planned của prototype hoặc kết luận hoàn thành v1.0.

## Prototype — D-44, planned trước triển khai 12/10/2026

| Ca UI | BR / AC | Kiểm chứng dự kiến | Trạng thái ban đầu |
|---|---|---|---|
| UI-01 | BR-17…26,38,39,46…48,59…61 / AC-17…22 | JS replay đối chiếu 83 fixture gốc và biên | planned |
| UI-02 | BR-03…16,32,33,49,54,62,64 / AC-01…16,27,33,34 | Controller quyền/lỗi không mutate; DOM role/direct navigation | planned |
| UI-03 | BR-08…24,52…58 / AC tương ứng | Sáu nhóm DEMO với thao tác thực | planned |
| UI-04 | BR-40,41,49 / AC-32 | Browser desktop/mobile/keyboard, giây chỉ detail | planned |
| UI-05 | BR-35,63 / AC-28…31 | M-01…M-07, kỳ/filter cùng dataset/clock | planned |
| UI-06 | BR-02,06 / NFR-06 | Storage/reset/schema, subpath, network không API | planned |

Không dùng một phiên browser để chứng minh SQLite atomicity hoặc race AC-08/09; dẫn [bằng chứng backend riêng](../tests/evidence/backend-test-report.md).

## Prototype thực thi — 12/10/2026

Các ca UI-01…UI-06 phía trên giữ trạng thái ban đầu planned để phân biệt kế hoạch với kết quả. Implementation: [engine](../prototype/sla.js), [controller](../prototype/domain.js), [reports](../prototype/reports.js), [seeds](../prototype/seeds.js), [storage](../prototype/storage.js), [shell/render](../prototype/app.js).

- UI-01: [harness JavaScript thực](../tests/prototype/test.js) so 83 fixture verified, 1.494 trường top-level so sâu, đạt 83/83. Rejected attempts qua controller riêng. Không thay bằng checker/backend.
- UI-02/UI-03/UI-05/UI-06: các ca controller/model và DOM sáu demo, quyền/direct navigation, report filter, storage/reload/reset đã thực thi; tổng suite 106 PASS / 0 FAIL. [Run record](../tests/evidence/prototype-20261012-105312.json), [báo cáo từng phần/giới hạn](../tests/evidence/prototype-report-20261012.md).
- UI-04/AC-32: ảnh browser thật desktop/mobile, input labels, Tab/focus-visible, danh sách không countdown giây, không API và subpath có evidence. Đây là kiểm tra tự động/headless và rà một số ảnh, chờ chủ dự án review UX; chưa xác nhận cross-browser hoặc thiết bị vật lý.
- Không gán demo PASS cho race/atomicity AC-08/09 hoặc database event_id; giữ liên kết backend riêng. Chưa commit/push/deploy Pages, Postman/video, chưa xác nhận v1.0 hoàn thành. Fixture và backend giữ nguyên.

## UX prototype — D-45, thực thi 13/10/2026

Phạm vi trình bày/hướng dẫn/điều hướng theo [spec mục 9](05-prototype/prototype-spec.md#9-ux-đã-duyệt--13102026), không thêm BR. [Hướng dẫn theo vai trò](../prototype/guidance.js) chỉ tạo text; domain/SLA/reports/seeds/storage giữ nguyên byte so baseline đầu nhiệm vụ.

| Ca bổ sung | Yêu cầu / truy vết | Kiểm tra thực |
|---|---|---|
| UX-01 | D-45 controls; AC-32, BR-02/06 | Thu gọn/mở không mutate storage; summary danh tính/nhóm/UTC+7; render giữ trạng thái thu gọn |
| UX-02 | D-45 sáu nhóm hướng dẫn; AC-32, BR-49/62 | Customer/Agent/Manager từng nhóm, Customer các biến thể không có hướng dẫn nội bộ; không tự event/clock hoặc gắn kết quả hoàn thành |
| UX-03 | D-45 nhãn/navigation; AC-28…32, BR-39/40/63 | Vi phạm sticky cùng Tạm dừng, nhãn báo cáo/N/M-06/M-07; bốn liên kết focus heading giữ filter/source; tỷ lệ có mẫu số từ thao tác UI thật |
| UX-04 | D-45 ảnh bàn giao; AC-01…16/24/32 | Agent có hai SLA/note/review chặn Resolved; Customer Resolved có hai quyết định, không block nội bộ |

[Run record cuối](../tests/evidence/prototype-ux-20261012-235015.json): 110 PASS / 0 FAIL, gồm 106 ca cũ, 83 fixture/1.494 so sánh; giữ quyền/controller, storage, reports và sáu DEMO. Kiểm tra browser riêng đạt Tab/focus-visible, Enter/Space cho summary, Enter nhảy heading; Customer và Manager 390px không tràn trang, bảng Manager cuộn riêng. [Báo cáo và ảnh](../tests/evidence/prototype-ux-report-20261013.md) ghi phương pháp, audit và các lần chưa đạt; không dùng kết quả backend thay kiểm tra UI.

Không chạy lại backend 181 test; backend/dependencies giữ nguyên. Chưa commit/push/deploy Pages, Postman/video; chưa xác nhận cross-browser, thiết bị vật lý hoặc chủ dự án duyệt UX cuối.

[Audit bảo toàn/link/diff thực](../tests/evidence/prototype-ux-audit-20261012-235146.json): PASS; 157 evidence cũ nguyên byte, không có thay đổi protected ngoài phạm vi hoặc source hash mismatch, 88 link local hợp lệ, git diff --check exit 0.

## Prototype / Pages — D-46, 13/10/2026

Chủ dự án phê duyệt yêu cầu/kịch bản và UX; chấp nhận kết quả, ảnh bằng chứng từ kiểm thử tự động. Không ghi nhận chủ dự án tự thao tác mọi kịch bản hoặc chạy công cụ. Thay trạng thái chờ UX review ở các mốc lịch sử phía trên; không xác nhận toàn bộ v1.0.

| Phạm vi | Thực thi / bằng chứng |
|---|---|
| UI-01…06, UX-01…04 / D-44…46 | Source sau sửa footer đã chạy suite 110 PASS / 0 FAIL; 83 fixture không đổi. [Run local cuối](../tests/evidence/prototype-ux-20261013-002503.json). |
| BR-02 / Pages runtime, độc lập API | [Workflow](../.github/workflows/pages.yml) chỉ upload 9 file runtime và `.nojekyll`; project subpath, Pages origin/localStorage/network được kiểm tra riêng. |
| Public smoke / bốn view và quyền Customer | [Public run](../tests/evidence/pages-public-smoke-20261013-002741.json): 74/74 kiểm tra PASS, 10 ảnh thật; bốn view, danh tính/kịch bản/reset/clock, DEMO-01 đến Closed, quyền Customer/Manager/Agent, localStorage reload, không API/lỗi JavaScript. Sáu nhóm trên Pages chỉ smoke ban đầu; không gán suite local thành suite Pages. |
| Triển khai thật | Runtime commit `4bf3599`, [workflow thành công](https://github.com/PhuocTrong2005/ba-ticketing-sla-case-study/actions/runs/38327310064), [URL Pages](https://phuoctrong2005.github.io/ba-ticketing-sla-case-study/), [metadata/exclusion probes](../tests/evidence/pages-deployment-20261013-002812.json). 9 assets khớp byte source, không upload backend/SQLite/tests/fixture/log. |
| Bảo toàn | [Audit bàn giao](../tests/evidence/pages-audit-20261013-003014.json) PASS: 261 protected, 228 evidence cũ nguyên byte, 218 file index đúng byte disk; không thay đổi fixture/backend/dependencies, không chạy lại backend. |

Postman/video chưa làm; không gán kiểm tra UI cho race/atomicity/database event_id hoặc bảo mật production.

## Postman/Newman — D-47, thực thi 13/10/2026

[Collection v2.1](../api/ticketing-sla.postman_collection.json), [environment](../api/ticketing-sla.postman_environment.json), [API README](../api/README.md). Request name/description/script có mã PM, AC/BR, HTTP status/error_code. Không đổi BR/codes/83 fixture hoặc tự tạo scenario verified. “Postman chưa làm” ở phần mốc lịch sử phía trên được thay bằng kết quả hiện hành này; video chưa làm.

| Nhánh kiểm tra | Request thực | Liên kết / giới hạn |
|---|---|---|
| Identity, role, ownership, New queue | PM-001…004,030…040,050…059,126/127,155/156,227/228 | BR-32…34/50/54/62; AC-01/03/06/12/13/21/27. 401/403/404 và queue chỉ 5 field; không là auth production |
| Create/content/structure/priority | PM-020…029,045…049,073/074,104…109,220…226,230…233 | AC-01/16, BR-33/62. Thiếu/trắng theo handler, type/JSON/extra-field có thể 422 structural trước handler; không gửi trường hệ thống cấm |
| Workflow và Waiting | PM-041/043/044,057/060…066,070/075,080/085,090/095,116…118 | AC-02/04/05/07/14/15/18/19; BR-08/19…21/50. Có state/running flag; không đối chiếu toán học SLA biên/calendar |
| Review threshold và giữ review khi resume | PM-076/086/096/097,110/110a…d/111 | AC-23/24, BR-52/53/57. Không review sau reject 1/2; reject 3 mở review; Customer resume không gỡ chặn Resolved. HTTP tuần tự không chứng minh rollback giữa giao dịch |
| Review quyền/phương án/Waiting/A1/A2 | PM-042,098…109,112…115,119 | AC-25…27; BR-54…58/62. Manager hoàn tất khi Waiting giữ status/running/consumed; Agent đọc plan trên ticket, Customer không nội bộ; A1 INVALID_TICKET_STATE, A2 TICKET_CLOSED |
| Closed và thứ tự lỗi | PM-120…128,145…147,220…229 | AC-03/05/11/12/13/16; BR-33/37/50/51. Closed → assigned → capacity khi claim; access trước state với body đúng kiểu; structural exception kiểm tra riêng |
| Tải 3 / return 4 / Waiting mở slot | PM-130…153,140/143/198 M06 | AC-10, BR-10/20/21/37/63. Các request tuần tự, không phải race AC-08/09 |
| Reports M-01…07, quyền, zero denominator và filter | PM-011…017,111,161…167,171…177,181…187,191…198,200…210 | AC-28…31, BR-35/63. Contract/counts/kỳ/filter/as_of/quyền; M04 không chứng minh breached branch tức thời; M07 không phủ mọi overlap/breach-context |

Kết quả thực theo [run record cuối](../tests/evidence/newman-20261013-004259-750031-run.json): **191 request / 514 assertion, 0 lỗi, exit 0**, Node v22.23.3/Newman 6.2.1, một iteration, mới 8 ticket qua giao dịch xác định; OpenAPI live khớp tracked. [JSON](../tests/evidence/newman-20261013-004259-750031.json), [JUnit](../tests/evidence/newman-20261013-004259-750031.xml), [báo cáo](../tests/evidence/postman-report-20261013.md) giữ cả run đầu 183/491 trước mở rộng source, không gộp hai run.

Không phát hiện implementation bug trong nhánh đã chạy. Backend/dependencies/prototype/83 fixture/bằng chứng trước và `Run Project.txt` giữ nguyên; database demo không bị thay thế; server thử đã dừng, database thử giữ local riêng. Không chạy lại 181 pytest. Không cộng assertion Newman vào số pytest hoặc tự gán PASS toàn bộ AC. Race AC-08/09, replay/atomicity AC-07/22/23, phép tính biên SLA/calendar/83 fixture giữ [bằng chứng backend riêng](../tests/evidence/backend-test-report.md). Chưa dùng Postman UI Runner; chưa commit/push/video/README tổng thể hoặc xác nhận toàn bộ v1.0.

[Audit bàn giao](../tests/evidence/postman-audit-20261013-004951-140523.json): PASS, 343 protected/291 evidence cũ/database demo nguyên byte, source/collection/environment khớp hash run cuối; 121 links hợp lệ, diff-check exit 0, không payload hệ thống/ID ticket hardcode/token/đường dẫn riêng máy trong collection/environment; requests chỉ đến loopback server thử. Audit đầu nhận nhầm URL trong regex, đã sửa auditor và giữ record lịch sử; không sửa assertion/expected/nghiệp vụ để đạt.
