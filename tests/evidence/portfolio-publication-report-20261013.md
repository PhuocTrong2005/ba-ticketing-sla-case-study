# Rà soát/xuất bản Postman và tài liệu portfolio — 13/10/2026

Chủ dự án chấp nhận kết quả Postman đã báo và cho phép commit/push tài liệu theo D-48. Không suy việc chủ dự án tự chạy mọi test, không tuyên bố v1.0 hoàn thành hoặc tạo tag. [Baseline](portfolio-baseline-20261013.json) giữ working tree đầu nhiệm vụ gồm Postman chưa commit và Run Project.txt. Không đổi BR/backend/prototype/dependencies/83 fixture; không ghi đè audit chưa đạt.

## Đối chiếu nguồn

- Windows repo và clean-start JUnit đều 181 testcase, 0 failure/error/skipped. Backend/tests-backend/SQL query/requirements/pytest.ini/OpenAPI hiện hành khớp 20 hash trong manifest Windows. Backend-run Linux cũ có khác byte xuống dòng ở schema/requirements/SQL sau checkout Windows; không dùng hash cũ đó làm bằng chứng source hiện hành.
- Prototype run cuối: 110 PASS/0 FAIL; runtime/harness khớp. Chỉ auditor Pages thay đổi sau run, đã ghi riêng trong Pages evidence, không thay source giao diện.
- Pages record: 74 check, tất cả passed, ảnh Customer Closed từ public smoke này làm ảnh README; 9 asset hash khớp runtime hiện tại.
- Newman JSON: 191 executions/requests, 514 assertions, 0 failed/pending/failure; JUnit nguồn có 514 testcase assertion, không phải 191 request. Run record exit 0/source hashes khớp collection/environment/generator/runner/backend. Không chạy lại Newman/pytest/JS chỉ để lặp số đếm.
- Collection đã validate với schema v2.1 chính thức bằng Ajv có sẵn trong tooling Newman, không cài thêm backend dependencies. Environment đúng Customer 1/2, Agent 3/4/5, Manager 6, không token/mật khẩu/đường dẫn riêng máy. Rà ID/payload và replay DB mới: helper đặt TICKETING_DB trước import, không seed; report giữ PID/stop và fresh DB.

## Tài liệu và nghiệm thu

README viết lại theo thứ tự yêu cầu, vai trò BA/giả định, Pages/ảnh thật, As-Is→To-Be/BPMN, quyết định, điều hướng, chạy ngắn, số đếm/giới hạn/video/roadmap. Lịch sử/hash truy xuất qua evidence index/record và README Git tại commit cũ; không xóa nguồn evidence để làm trang bìa ngắn.

[AC matrix](../../docs/ac-traceability.md) có từng AC-01…34, implementation/test/request/evidence/giới hạn, tách chức năng/quyền, race/dữ liệu, SLA, UI/báo cáo và tái lập. [Checklist](../../docs/release-checklist.md) giữ tiêu chí gốc. Video Chưa có; README portfolio chưa clean-start toàn bộ từ checkout mới sau xuất bản. Một số AC có bằng chứng nhánh nhưng chưa exhaustive error/cross-browser; không blanket PASS.

API README/TASKS/traceability phân biệt D-47 “chưa commit” lịch sử với D-48 được chấp nhận/xuất bản. Giữ Postman audit chưa đạt nhận nhầm URL `https://` thành drive Windows; lỗi auditor, không backend; không sửa assertion/expected để đạt.

## Kiểm tra xuất bản

[Audit đọc nguồn](portfolio-publication-audit-20261013-010911.json) PASS: 376 protected files, 305 evidence trước nhiệm vụ giữ nguyên; chỉ API README cập nhật trạng thái được chấp nhận. Khớp source Windows 20 file, runtime/harness local, 9 runtime Pages, source/collection/environment/helper Newman; schema valid, 34 AC đúng một lần, không thiếu test/request được dẫn; 262 links/images hợp lệ, diff-check exit 0. Đây là rà evidence/schema/docs, không phải lần test runtime mới. Bản staged được audit tiếp trước commit.

Tái lập audit: sau `& .\.venv\Scripts\python.exe tests/postman/setup_tools.py`, gọi `& .\.venv\Scripts\python.exe tests/portfolio/audit_publication.py`; auditor dùng Ajv đã có cùng Newman và cache schema v2.1 chính thức ở tooling ignored, tự tải nếu chưa có. Auditor publication so baseline/staged tại thời điểm xuất bản; sau commit hoặc có thay đổi source, không dùng lại nó để tự nhận PASS từ baseline cũ. Không thay helper run Newman hoặc collection để phục vụ audit.

[Audit staged](portfolio-publication-audit-20261013-011023.json) PASS: 263 links/images, counts/schema/AC names/source match đạt; không file cấm/secret-pattern/byte mismatch, diff thường và staged đều exit 0. Staged scope gồm bộ Postman đã duyệt, README/tài liệu/checklist và công cụ/evidence review; không stage Run Project.txt, backend/prototype/fixture/dependencies hoặc workflow. Link audit bổ sung sau lần này được kiểm tra tồn tại riêng trước commit.

Giữ [audit mở rộng chưa đạt](portfolio-publication-audit-20261013-011206.json): scanner private-path nhận các chuỗi regex `/Users/` nằm trong source auditor như nội dung riêng máy. Đã làm rõ bộ quét phải có segment tên người dùng thực, không bỏ quét hoặc sửa source Postman/backend. Tên test prototype được dẫn đều có trong run thật. Đây là lỗi phân loại của auditor publication, không phải bug backend hoặc test failure Newman.

[Audit staged cuối](portfolio-publication-audit-20261013-011238.json) PASS: 265 links/images hợp lệ, mọi tên test backend/JS và request được dẫn tồn tại; không private path/Bearer/secret/file cấm/byte mismatch, diff check exit 0. Chỉ bổ sung link record này sau audit và kiểm tra tồn tại; không thay collection/helper/application nên không chạy lại runtime suite.

Fetch origin/main đầu nhiệm vụ: 0/0 với HEAD `41d0ebf`; fetch lại trước commit, push thường. Run Project.txt giữ nguyên ngoài commit; tools/database/log/profile/cache/temp không stage. Chỉ source Postman/docs/công cụ audit/bằng chứng cần thiết được xuất bản. Attributes chỉ bổ sung các pattern Postman/portfolio mới để giữ byte khi commit; rule backend/fixture cũ giữ nguyên.

Workflow Pages lọc paths chỉ prototype/** và workflow; lần này không đổi hai path đó. Nếu không có run mới, không trigger thủ công hoặc coi việc push là lần test mới. Trạng thái cuối/commit/local-remote được báo sau push; public smoke 74 vẫn là lần cũ đã đối chiếu, không đổi timestamp/record.
