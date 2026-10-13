# Backlog v1.0

D-51: Chủ dự án chốt **phát hành portfolio v1.0** ngày 13/10/2026; [release checklist](docs/release-checklist.md) đối chiếu từng tiêu chí. [Demo GitHub Pages](https://phuoctrong2005.github.io/ba-ticketing-sla-case-study/) là bản tương tác hiện có. Video chưa làm/kiểm thử và chuyển sang roadmap sau v1.0; không là điều kiện phát hành.

Nghiệm thu clean-start lần 2 trên [checkout độc lập cùng origin/main tại `7c35b2c`](tests/evidence/portfolio-clean-start-repeat-20261013.md): 181 pytest, 110 prototype, 24 static smoke, Newman 191/514 đạt sau khi xử lý hai giới hạn sandbox. DOC-CS-01 tại commit cũ tái hiện; hướng dẫn prototype hiện hành sửa bước auditor và có [recheck docs](tests/evidence/portfolio-clean-start-20261013-doc-recheck.json). Chưa chạy lại trọn suite từ commit mới. Các kết quả này không gán PASS cho auditor cũ.

D-49, nghiệm thu clean-start 13/10/2026: [clone origin/main `7c35b2c`](tests/evidence/portfolio-clean-start-report-20261013.md), venv/tooling/cache/database mới; requirements/pip check/181 pytest/HTTP backend/static smoke 24 check/110 JS/Newman 191 request–514 assertion đạt. DOC-CS-01 auditor UX lịch sử không portable: giữ evidence thất bại, sửa docs, recheck đúng clone 110/110. Trạng thái chưa commit/push trong report là mốc trước D-50. Video Chưa có, không tag v1.0. Không gán run trỏ repo gốc hoặc auditor lịch sử thành PASS clean-start.

Mốc D-48, 13/10/2026: Postman được chủ dự án chấp nhận và cho phép commit/push cùng tài liệu portfolio. [README](README.md), [AC-01…34](docs/ac-traceability.md), [release checklist](docs/release-checklist.md), [audit xuất bản](tests/evidence/portfolio-publication-report-20261013.md). Ghi chú video/chưa phát hành ở mốc trước là lịch sử, được D-51 thay thế. Các ghi chú chưa commit/Postman/README trong mốc trước giữ như lịch sử.

## Tiêu chí hoàn thành v1.0

- Luồng chính chạy được trên prototype và API tương ứng.
- Quyền được kiểm tra ở backend.
- Có ca `verified` bao phủ đủ 12 nhóm; nhóm 1 đến 11 mở khóa logic tính SLA chính, nhóm 12 mở khóa logic tính bối cảnh M-07.
- Hai ca nhận đồng thời đạt.
- Dữ liệu dẫn xuất dựng lại đúng từ sự kiện gốc.
- Báo cáo SQL khớp dữ liệu mẫu.
- README đã được thử thực tế từ thư mục mới.
- Giới hạn và phần mô phỏng được nêu trung thực.

## Backlog khung

| Mã | Hạng mục | Phụ thuộc | Trạng thái |
|---|---|---|---|
| DOC-01 | Hoàn thiện yêu cầu, traceability và decision log. | Quyết định chủ dự án, D-48 | Đã duyệt; README portfolio, ma trận từng AC và release checklist hiện hành. Planned cũ giữ như lịch sử, không blanket PASS. |
| DOC-02 | Tài liệu [As-Is](docs/02-process/as-is.md), [To-Be](docs/02-process/to-be.md), [vòng đời ticket](docs/02-process/ticket-states.md); [nguồn BPMN hai trang](docs/02-process/support-processes.drawio) và ảnh xuất tương ứng. | Nội dung và sơ đồ chủ dự án cung cấp | Hoàn thành theo xác nhận chủ dự án ngày 12/10/2026; chỉ phần tài liệu quy trình và sơ đồ |
| SLA-01 | 83 fixture verified; giữ nguyên 81 ca cũ. Checker 83 PASS / 0 FAIL, 1.496 so sánh; thêm 5 phép biên SLA-83 tại 08:00:00 đạt. Mốc 69/81 lần lượt 1.243/1.460 phép, đều PASS. [Báo cáo hiện hành](tests/evidence/sla-verification-83.md). | `docs/spec/scenario-coverage.md`, D-33/D-39/D-40 | Gate mở; đã triển khai và đối chiếu 83 fixture trên backend; checker cũ giữ nguyên bằng chứng |
| DATA-01 | Thiết kế schema và dựng lại dữ liệu dẫn xuất từ sự kiện; lưu số giây còn lại tại mỗi lần Resolved để kiểm chứng quy tắc không quy lỗi Agent khi Customer từ chối lúc hết ngân sách. | SLA-01 | Đã có schema/replay và snapshot mỗi Resolved; xem backend test report |
| DATA-02 | Thiết kế bảng `ticket_reviews`; lưu số giây còn lại tại mỗi lần Resolved nếu DATA-01 chưa bao phủ. | SLA-01 | Đã triển khai review theo chu kỳ, snapshot Resolved được DATA-01 phủ |
| API-01 | Xác định hợp đồng API và kiểm tra phân quyền backend. | DOC-01, SLA-01 | Đã có contract/OpenAPI và kiểm thử HTTP; xem evidence implementation |
| API-02 | Kiểm tra `REVIEW_REQUIRED`; Agent chuyển Waiting khi review mở; Manager ghi phương án ở Waiting; Manager/Agent/Customer ghi phương án (Customer 404, Agent 403); `INVALID_TICKET_STATE`/`TICKET_CLOSED` khi không có review mở; tính nguyên tử từ chối và tạo review. | DOC-01, SLA-01 | Đã thực thi A1/A2, REVIEW_REQUIRED, quyền/nội dung và rollback; xem evidence |
| PROTO-01 | Xây prototype tĩnh cho luồng chính. | DOC-01, D-44…46 | UX đã được chấp nhận; local 110 PASS / 0 FAIL, Pages đã deploy, public smoke 74 kiểm tra PASS. Sáu nhóm trên Pages chỉ smoke; [báo cáo](tests/evidence/pages-report-20261013.md). |
| POSTMAN-01 | Collection v2.1/environment, request xác định và runner thật trên database riêng. | API-01/API-02, D-47/48 | Newman 191 request/514 assertion/0 lỗi/exit 0; chủ dự án chấp nhận và cho phép xuất bản. [Hướng dẫn](api/README.md), [audit xuất bản](tests/evidence/portfolio-publication-report-20261013.md). Không chạy lại nếu hash khớp. |
| CON-01 | Chứng minh hai ca nhận đồng thời. | DATA-01, API-01 | Đã kiểm thử hai tình huống bằng threads/kết nối riêng, SQLite file và barrier |
| RPT-01 | Báo cáo SQL khớp dữ liệu mẫu. | DATA-01 | Đã triển khai SQL trên snapshot as_of và kiểm thử dữ liệu xác định |
| RPT-02 | Báo cáo M-07 về chờ Manager review. | DATA-02 | Đã triển khai và kiểm thử M-07; không phải SQL thuần cho phép giao khoảng |
| EVD-01 | Thu thập bằng chứng kiểm thử hợp lệ và hoàn chỉnh ma trận truy vết. | Các hạng mục liên quan | Đã có backend, JS/DOM/ảnh prototype, Pages smoke và Newman JSON/JUnit/run record; video chưa làm và thuộc roadmap D-51, không dùng làm evidence v1.0. |

## Bổ sung sau nhập S1–S12 — 08/10/2026 (lịch sử lúc còn draft)

- SLA-01: đã nhập SLA-70…SLA-81, **12 draft**, giữ nguyên 69 verified. [Báo cáo nhập](tests/evidence/sla-draft-import.md) có ánh xạ và kiểm tra cấu trúc; checker CLI gốc không nhận bộ 81 ca. Chưa đối chiếu SLA cho 12 draft, chưa mở gate SLA chính/M-07. Chờ review theo D-33; xác nhận con số không tự đổi review_status.
- Coverage còn mở: draft chưa là bằng chứng verified; resume Waiting ngay trong cuối tuần; resume ngoài giờ với 0 giây nhưng chưa từng breached (S5 chỉ có breach cũ). S4 không đánh giá mốc sau hạn một giây. Không tự bổ sung expected_* ngoài 12 ca được yêu cầu.
- API-01/API-02: chờ contract payload cho kết quả công khai, lý do từ chối và handling_plan; fixture toán học không lưu actor/nội dung. Khi chuyển S7/S10–S12 sang API test phải có nội dung hợp lệ cho mọi bước tương ứng.
- API-02 / A1: Manager ghi phương án khi không có review mở → 409 `INVALID_TICKET_STATE`; **chưa chạy**.
- API-02 / A2: Manager ghi phương án khi ticket Closed → 409 `TICKET_CLOSED`, kiểm tra ưu tiên lỗi Closed; **chưa chạy**.
- API-02 / S12 (SLA-81): thử Resolved sau resume Waiting khi R1 mở → HTTP 409 `REVIEW_REQUIRED`; không ghi ticket_event/không đổi interval; **chưa chạy HTTP thật**. A1/A2 không tính vào đối chiếu SLA.

## Sau xác nhận và đối chiếu 81 ca — 08/10/2026

- SLA-01: 81/81 ca `verified`, 0 draft. 69 ca cũ giữ nguyên nội dung; 12 ca mới giữ nguyên đầu vào/đáp án, `verified_at=null` vì không có giờ xác nhận chính xác. Codex chạy checker 81 ca đạt 81 PASS / 0 FAIL, 1.460 phép so sánh, trong đó 12 ca mới có 217. Checker gốc 69 ca giữ nguyên và chạy lại đạt 69 PASS / 0 FAIL, 1.243 phép so sánh. Audit cấu trúc hiện hành 81/81 PASS. Đây là đối chiếu fixture, chưa phải test backend/API. [Báo cáo](tests/evidence/sla-verification-81.md).
- Gate logic SLA chính: **chưa mở**. Cần ca verified riêng cho Customer resume Waiting ngay trong cuối tuần và cho resume Waiting ngoài giờ với 0 giây còn lại nhưng chưa từng breached; rà thêm mốc sau deadline một giây cho đúng đường Waiting còn 0 theo tiêu chí nhánh biên. Không tự tạo SLA-82 trở đi.
- Gate tính bối cảnh M-07: **đủ điều kiện mở cho việc viết logic** theo D-33; nhánh chờ Manager trong Waiting, R3/lần từ chối 5, overlap/breach/open/closed review đã có ca verified và khớp checker. Chưa viết hoặc kiểm tra implementation.
- API-01/API-02: A1/A2 và HTTP `REVIEW_REQUIRED` của SLA-81, nội dung bắt buộc/quyền/atomicity vẫn chờ contract và API test. Không cộng các bước này vào PASS SLA/M-07.

## Sau SLA-82/SLA-83 — 10/10/2026

**Gate logic SLA chính: mở cho việc viết logic theo AGENTS/D-33.** Nhóm 1–11 đều có ca verified và bảng nhóm → mã không còn nhóm trống. SLA-82 đóng nhánh Customer resume ngay cuối tuần; SLA-83 đóng nhánh resume ngoài giờ với 0 giây nhưng chưa từng breached và mốc sau hạn 08:00:01. Đối chiếu phụ cùng events tại 08:00:00 xác nhận pending/due; không thêm ca hoặc tự xác nhận đáp án. Các nhánh còn lại đã được đối soát ở mốc 81; không còn blocker coverage cho logic SLA chính. Không đổi tiêu chí gate. Gate tính M-07 tiếp tục đủ điều kiện viết logic theo đánh giá mốc 81. API A1/A2, HTTP REVIEW_REQUIRED, payload/quyền/atomicity và các tiêu chí hoàn thành v1.0 vẫn chưa kiểm thử; đây không phải blocker mới cho gate phép tính và không phải xác nhận hoàn thành backend.

Các ghi chú 08/10 phía trên giữ nguyên như lịch sử; yêu cầu hiện tại cho phép nhập đúng SLA-82/SLA-83 verified và thay kết luận gate cũ. Không tự thêm ca ngoài hai ca đã được xác nhận.

## Hiện hành — triển khai backend 12/10/2026

Các mục chưa triển khai ở phần lịch sử 08/10 và 10/10 không còn là trạng thái backend hiện tại. Kết quả thực thi nằm trong [backend test report](tests/evidence/backend-test-report.md); prototype/Postman/video vẫn chưa làm, v1.0 chưa hoàn thành. Fixture 83 verified giữ nguyên; không tạo scenario mới.

### Bước 1 — ổn định Python và clean-start Windows, 12/10/2026

Hoàn tất phần môi trường: Python 3.12.10 chính thức cài theo người dùng ngoài Temp; giữ `.venv-backup-20261012-162259` và tạo `.venv` mới. Repo gốc và `.clean-start-20261012-162259` đều `pip check` PASS, pytest 181/181 PASS. Clean-start dùng source hiện tại gồm file chưa commit, database mới, Uvicorn riêng; HTTP docs/OpenAPI, luồng Closed và quyền riêng tư Customer đạt. SHA-256 fixture 83 ca và mọi evidence cũ giữ nguyên. [Báo cáo bước 1](tests/evidence/step1-windows-20261012-162259-report.md) ghi lệnh, kết quả, giới hạn và danh sách file riêng. Chưa làm prototype/Postman/video/deploy; chưa commit/push và chưa hoàn thành v1.0.

### Prototype — D-44, 12/10/2026

Đã dựng prototype độc lập theo spec: bốn view, sáu nhóm DEMO và biến thể, controller/SLA/M-01…07, clock đứng yên, schema storage/reset. Đã chạy JavaScript trong Edge headless với 83 fixture gốc và kiểm tra controller/DOM/sáu nhóm demo: 106 PASS / 0 FAIL; có ảnh trước/sau và mobile/keyboard/subpath/network. [Báo cáo thực và giới hạn](tests/evidence/prototype-report-20261012.md), [cách mở](prototype/README.md). Chờ chủ dự án xem giao diện; chưa commit/push/deploy Pages, Postman hoặc video. Không chạy lại backend 181 test vì backend/dependencies không đổi; fixture 83 giữ nguyên. Các đoạn “prototype chưa làm” phía trên là lịch sử. Chưa xác nhận v1.0 hoàn thành.

### Prototype / Pages — D-46, 13/10/2026

Chủ dự án đã phê duyệt yêu cầu/kịch bản, UX và chấp nhận kết quả/ảnh kiểm thử tự động; cho phép commit/push main thường và deploy Pages. Không yêu cầu thao tác lại tất cả kịch bản; không ghi chủ dự án tự chạy công cụ. UX đã đủ phạm vi D-45. Kiểm thử mới sau sửa footer nguồn: 110 PASS / 0 FAIL; 83 fixture/backend/dependencies giữ nguyên, backend không chạy lại. Workflow chỉ đóng gói runtime `prototype/` tại project subpath; trạng thái triển khai/public smoke và bằng chứng thực tại [báo cáo Pages](tests/evidence/pages-report-20261013.md). Các trạng thái chờ review/chưa deploy phía trên là lịch sử. Postman/video và README tổng thể để bước sau; toàn bộ v1.0 chưa hoàn thành.

Pages thực đã kiểm tra: [demo](https://phuoctrong2005.github.io/ba-ticketing-sla-case-study/), [workflow thành công](https://github.com/PhuocTrong2005/ba-ticketing-sla-case-study/actions/runs/38327310064), commit runtime `4bf3599`. Public smoke 74/74 PASS, 10 ảnh mới; đủ bốn view/đổi danh tính/kịch bản/reset/clock/luồng DEMO-01/quyền Customer/localStorage/network. Sáu nhóm trên Pages chỉ smoke ban đầu, sáu nhóm local chạy đầy đủ. Không có lỗi JavaScript chặn, không Fetch/XHR/API; asset runtime khớp hash source. Chỉ cập nhật README tối thiểu.

### Postman — D-47, 13/10/2026

Đã tạo collection v2.1/environment trong `api/`, sáu nhóm request tuần tự xác định, ID lấy từ response. Source/contract hiện hành đã đọc, OpenAPI live khớp tracked. Tooling portable Node/Newman nằm riêng, không đổi backend/Python dependencies. Run cuối [004259-750031](tests/evidence/newman-20261013-004259-750031-run.json) **191 request / 514 assertion đạt, 0 lỗi, exit 0**, trên database mới chưa tồn tại; server nhiệm vụ đã dừng. Run đầu 183/491 vẫn giữ như lịch sử trước mở rộng coverage, không cộng dồn hai lần.

PM-031…128 và PM-110a…d bao phủ luồng/riêng tư/review/A1/A2; PM-130…159 tải 3/return tải 4/thứ tự lỗi claim; PM-011…017,161…210 M-01…07 empty/contract/quyền/kỳ/filter; PM-020…030,220…233 validation và ngoại lệ BR-33. Chi tiết request và giới hạn tại [báo cáo](tests/evidence/postman-report-20261013.md), truy vết tại [traceability](docs/traceability.md). Không phát hiện bug implementation trong phạm vi đã chạy; chưa tự gán PASS toàn bộ AC. 83 fixture/backend/prototype/evidence cũ/database demo và `Run Project.txt` giữ nguyên; không chạy lại 181 pytest. Race/SLA biên/calendar vẫn dùng bằng chứng pytest riêng; không cộng Newman assertions với pytest thành tình huống độc lập. Chưa commit/push/video/viết lại README tổng thể. Các dòng “Postman chưa làm” trong mốc lịch sử trước đây được thay bằng trạng thái hiện hành này.
