# Prototype — bằng chứng thực thi 12/10/2026

Đã dựng prototype độc lập theo D-44 và [spec nguyên bản](../../docs/05-prototype/prototype-spec.md), dựa checkout/main `eb8d483d8e3af914b487c1728b22b4108fa1397f`. Không sửa BR, backend/dependencies hoặc fixture. Không commit/push/deploy, không làm Postman/video; chưa xác nhận v1.0 hoàn thành.

## Lần chạy hiện hành

```powershell
& .\.venv\Scripts\python.exe tests/prototype/run_browser.py
```

Exit code **0**. [Run record](prototype-20261012-105312.json) chứa lệnh, commit, user-agent Edge, hashes từng file nguồn, fixture hash, kết quả từng test, network requests và các phép đo DOM. Mốc tên file là UTC `2026-10-12 10:53:12`, tương ứng UTC+7 `17:53:12`; không là timestamp phê duyệt.

**106 PASS / 0 FAIL** gồm 83 ca fixture và 23 ca nhóm bổ sung. JavaScript replay thực chạy trong Edge, so **1.494 trường top-level** (mảng interval/review so sâu); kiểm tra rejected attempts qua JS controller ghi riêng trong ca bổ sung. Con số này không dùng định nghĩa phép so sánh của checker Python. Fixture 83/83 giữ `verified`; không chuyển review_status hoặc tạo scenario SLA mới. SHA-256 fixture: `6e75371714e5589eb78c45b0df3eb69595f2dfcc9362c9398b8c11989c0756ee`.

| Phần | Kết quả thực / giới hạn |
|---|---|
| UI-01 / AC-17…22 | 83 fixture khớp các đồng hồ, deadline, warning, assignment snapshot, interval, state, rejection count, review và M-07 context. SLA-83 tại đúng 08:00 pending/due; +1 giây breached. Ngưỡng 3600/3599/900/899; sticky Waiting; timestamp truncate và lịch cuối tuần được test JS. |
| UI-02 / controller | Vai trò/ownership, 401/403/404/409/422, review resource Manager-only, report Manager-only, lỗi không mutate source/projection, payload trường dư, review trước nội dung, Closed trước assigned; same-second zero intervals, lịch sử as_of bỏ future completion. Không giả validator FastAPI hoặc HTTP thật. |
| UI-03 / sáu nhóm DEMO | Sáu test DOM thao tác qua controls/form/nút trên iframe cùng origin. Sáu test model độc lập gồm nhánh đúng hạn/trễ trên dataset riêng. Ảnh trước/sau chụp thực tại các checkpoint; không là log vận hành doanh nghiệp. |
| UI-04 / AC-32 | Screenshot desktop và mobile 390×844; mobile document width = viewport width = 390, 0 input không label; Customer detail 0 khối dữ liệu nội bộ. Tab từ identity tới scenario thực bằng CDP Input, focus-visible=true. Danh sách không có countdown giây; giây trong SLA detail và overlap M-07 được ghi đơn vị rõ. Không CSS animation/âm thanh/toast cảnh báo lặp. |
| UI-05 / AC-28…31 | M-01…07 từ cùng dataset/clock; số 0 không có dữ liệu, inclusive UI/[from,to), snapshot unclosed không giới hạn ngày tạo, filter priority/Agent, M-06 tải mọi ưu tiên, M-07 calendar/overlap. DOM Manager chứa các section báo cáo; chưa kiểm tra tay mọi tổ hợp bộ lọc. |
| UI-06 / static/storage | HTTP dưới `/case-study/`, mọi asset 200/304. Network không `/tickets`, `/reports` hoặc port FastAPI. Fixture fetch chỉ ở harness. Storage roundtrip/schema/corruption và quota/unavailable; DOM reload/reset/switch/direct navigation. `/favicon.ico` 404 là request tự động của browser, không API; không ảnh hưởng UI. |

## Ảnh UI thật

| Nhóm | Trước | Sau thao tác |
|---|---|---|
| DEMO-01 | [trước](prototype-20261012-105312-DEMO-01-before.png) | [Closed Customer](prototype-20261012-105312-DEMO-01-after.png) |
| DEMO-02 | [trước](prototype-20261012-105312-DEMO-02-before.png) | [Resolved G 5400, còn 23400](prototype-20261012-105312-DEMO-02-after.png) |
| DEMO-03 | [trước](prototype-20261012-105312-DEMO-03-before.png) | [Resolved đúng 17:00](prototype-20261012-105312-DEMO-03-after.png) |
| DEMO-04 | [trước](prototype-20261012-105312-DEMO-04-before.png) | [Customer resume](prototype-20261012-105312-DEMO-04-after.png) |
| DEMO-05 | [tải 3](prototype-20261012-105312-DEMO-05-before.png) | [nhận New sau giảm tải](prototype-20261012-105312-DEMO-05-after.png) |
| DEMO-06 | [biên 16:00](prototype-20261012-105312-DEMO-06-before.png) | [Manager sau biên 0 giây](prototype-20261012-105312-DEMO-06-after.png) |

Ảnh bổ sung: [Manager desktop](prototype-20261012-105312-manager-desktop.png), [review detail](prototype-20261012-105312-review-detail.png), [Customer mobile](prototype-20261012-105312-customer-mobile.png). Đã xem ảnh desktop Manager, Customer mobile và DEMO-02 sau thao tác để rà bố cục/nội dung; không suy tất cả screenshot đã được review tay.

## Lịch sử lần chạy / giới hạn

- [10:39:42 UTC](prototype-20261012-103942.json): Edge GPU process không chạy trong môi trường hạn chế; [log thật](prototype-20261012-103942-edge.log), chưa có test PASS.
- [10:40:07 UTC](prototype-20261012-104007.json) và [10:41:11 UTC](prototype-20261012-104111.json): renderer/CDP timeout với GPU sandbox workaround. Không có PASS; không gán thành lỗi nghiệp vụ.
- [10:41:51 UTC](prototype-20261012-104151.json): 102 PASS / 1 FAIL, assertion test mới đếm nhầm unclosed High =3, trong seed chỉ #2/#3 là High nên thực =2. Đã sửa assertion test mới thành 2, không sửa fixture/runtime để né lỗi. 83 fixture đều PASS ngay ở lần này.
- [10:43:21 UTC](prototype-20261012-104321.json): 103 PASS / 0 FAIL. Sau đó bổ sung guard quyền report, storage unavailable, hướng dẫn Customer không chứa ngữ cảnh nội bộ và screenshot đầy đủ. Lần hiện hành ở trên đạt 106/106.

Runner dùng Edge headless profile tạm riêng và `--no-sandbox` cho renderer trong môi trường hạn chế, chỉ mở HTTP localhost; Python không tính SLA và không tạo ảnh giả. [Edge log hiện hành](prototype-20261012-105312-edge.log) có cảnh báo nền registry/Windows capability; không có exception JavaScript. Hai kết nối HTTP preconnect bị reset khi đóng browser được Python in ra; tiến trình kết thúc 0 và không có request nguồn thất bại ngoài favicon.

Đây là QA tự động headless và một số ảnh được review, chưa là phê duyệt giao diện của chủ dự án, test thiết bị vật lý, reader hỗ trợ tiếp cận hoặc cross-browser. Chưa có cơ sở tuyên bố tất cả UX đã được duyệt. Hướng dẫn bàn giao tại [prototype README](../../prototype/README.md).

Không chạy lại 181 backend test vì backend/dependencies không đổi. Atomicity SQLite và hai race AC-08/09 chỉ dẫn [backend evidence](backend-test-report.md); không gán PASS prototype cho chúng. Bằng chứng cũ Windows/Linux được giữ nguyên. Kiểm tra cuối về hashes/links/source bảo toàn ghi riêng trong `prototype-audit-20261012.json`.

## Audit bàn giao

Chạy `& .\.venv\Scripts\python.exe tests/prototype/audit.py`, exit 0. [Kết quả audit](prototype-audit-20261012.json): spec khớp nguyên byte với file đính kèm; fixture hash giữ nguyên; source runtime/test khớp hash lần browser cuối; không có runtime gọi API/lookup expected, không có pattern credential được tìm thấy, links và diff-check đạt. Đối chiếu 136 file tracked ngoài bốn tài liệu cập nhật khớp byte HEAD hoặc checkout theo .gitattributes. Một audit JSON lịch sử chỉ khác LF/CRLF so Git blob, ghi riêng cùng SHA-256 hiện hành; git status ban đầu sạch và không thao tác ghi lên evidence cũ. Không tự đổi line endings của artefact cũ để làm audit đạt.

Hai mốc bổ sung được giữ: [10:45:51 UTC](prototype-20261012-104551.json) đạt 104/104; [10:50:10 UTC](prototype-20261012-105010.json) đạt 106/106 sau bổ sung state/storage-type và đối chiếu report DOM/filter/navigation guard. Lần cuối 10:53:12 UTC giữ 106/106 sau chỉnh tiêu đề ticket mẫu công khai thành lời trung lập không nhắc review/SLA nội bộ. Ảnh đã xem trong quá trình rà gồm Manager desktop và Customer mobile ở các lần trước, DEMO-02 sau thao tác, và Customer mobile lần 10:50:10; đây không là phê duyệt UX đầy đủ.
