# Bàn giao UX prototype — 13/10/2026 (UTC+7)

Phê duyệt: yêu cầu trực tiếp chủ dự án, [D-45](../../docs/decision-log.md), [spec mục 9](../../docs/05-prototype/prototype-spec.md#9-ux-đã-duyệt--13102026). Chỉ đổi trình bày, hướng dẫn và điều hướng. Chưa commit/push/deploy Pages, Postman hoặc video; chờ chủ dự án xem trước.

## Thay đổi

- Controls native details/summary mở mặc định, thao tác chuột hoặc Tab + Enter/Space. Thu gọn vẫn hiện danh tính, DEMO/biến thể, giờ UTC+7 có giây và clock đứng yên. Không ghi event hoặc đổi dữ liệu/danh tính/clock. Banner mô phỏng luôn hiện.
- Nội dung/ghi chú/nhãn bảng lên 14–16px; màu chữ phụ đậm hơn, giữ bảng màu và bố cục. Focus-visible/label form được giữ; bảng dài cuộn riêng tại 390px. Không thêm animation, âm thanh hoặc cảnh báo lặp.
- Hướng dẫn sáu DEMO theo Customer/Agent/Manager và năm biến thể DEMO-06, gần nội dung và vẫn hiện khi controls đóng. Chỉ text, không tự thao tác. Customer không nhận hướng dẫn note/SLA/review/phương án Manager. Customer 2/Agent khác có nhắc quyền ticket mẫu.
- Nhãn SLA bằng lời, có Đang chạy/Tạm dừng và giữ Vi phạm SLA khi Waiting. Đến hết ngày, nhãn M-02/M-03, Chưa có kết quả phản hồi đầu; N có giải thích ngắn và phần kỹ thuật mở rộng; M-06 ghi tải thực qua tất cả ưu tiên; M-07 diễn đạt bối cảnh, không quy lỗi.
- Manager có bốn liên kết nhảy với heading nhận focus; giữ filter/clock/source, M-04 cạnh M-01…03. Công thức, inclusive → [from,to), as_of và bộ lọc không đổi.

## File sửa/thêm

| File | Mục đích |
|---|---|
| [prototype/app.js](../../prototype/app.js) | Render nhãn, summary, hướng dẫn theo vai trò, xử lý nhảy heading |
| [prototype/index.html](../../prototype/index.html) | Summary có thông tin; vùng hướng dẫn ngoài controls |
| [prototype/styles.css](../../prototype/styles.css) | Chữ/tương phản, focus, bảng cuộn và layout mobile |
| [prototype/guidance.js](../../prototype/guidance.js) — mới | Nội dung hướng dẫn theo spec/seeds, không tác động domain |
| [prototype/README.md](../../prototype/README.md) | Cách xem/thao tác và kiểm chứng UX |
| [prototype-spec.md](../../docs/05-prototype/prototype-spec.md), [decision-log.md](../../docs/decision-log.md), [traceability.md](../../docs/traceability.md) | Phạm vi UX được duyệt, D-45, ca bổ sung và kết quả thực |
| [test.js](../prototype/test.js), [run_browser.py](../prototype/run_browser.py) | Giữ ca cũ, thêm UX-01…04, ảnh và phím CDP |
| [audit_ux.py](../prototype/audit_ux.py) — mới | So baseline nhiệm vụ, links, source hashes và diff; ghi audit mới |
| Report này, baseline/run/audit/ảnh mới tại tests/evidence | Bằng chứng thực, không ghi đè lịch sử |

README.md/TASKS.md và Run Project.txt ở root đã có thay đổi trước nhiệm vụ và không bị sửa lần này. Không reset working tree; các nội dung cũ trong tài liệu được giữ và bổ sung theo phạm vi đã duyệt.

## Chạy thực và kết quả

Từ root trên Windows, dùng môi trường Python hiện có; không cài dependency:

```powershell
& .\.venv\Scripts\python.exe tests/prototype/run_browser.py
& .\.venv\Scripts\python.exe tests/prototype/audit_ux.py
```

Runner phục vụ source dưới `/case-study/` bằng static HTTP, Edge headless với profile tạm, CDP. Harness chạy JavaScript engine/controller/DOM thực. Phím Tab/Enter/Space phát qua Input.dispatchKeyEvent; thao tác workflow qua control/form UI, không sửa storage/DOM để dựng đáp án hoặc ảnh. Ảnh desktop đầy trang từ iframe 1280px (runner chỉ điều chỉnh chiều cao frame để chụp đủ nội dung); preview trực tiếp 1440×1080; mobile 390×844. Timestamp tên file/run là UTC, ngày bàn giao ở đây là UTC+7.

Lần cuối: [prototype-ux-20261012-235015.json](prototype-ux-20261012-235015.json), exit code 0:

- Harness **110 PASS / 0 FAIL**: 106 ca hiện hành + UX-01…04. 83 fixture verified giữ nguyên, 1.494 so sánh top-level có so sâu. Không đổi expected/review_status.
- Quyền/controller/lỗi không mutate, storage/reload/reset/schema, reports/filter và sáu luồng DEMO vẫn được chạy. Không bỏ assertion nghiệp vụ hoặc giảm coverage.
- Thu gọn bằng click trong harness; Enter thu gọn và Space mở lại trong browser, source storage không đổi. Tab tới selector có focus-visible; Enter liên kết Tải Agent đưa focus-visible tới heading manager-load. Bốn liên kết trong harness giữ filter và storage.
- Customer mobile: innerWidth/document_width = 390/390, 0 block nội bộ, 0 field thiếu label. Manager mobile cũng 390/390, 0 field thiếu label; bảng có clientWidth 328 và scrollWidth tới 613, cuộn trong vùng riêng.
- `runtime_errors=[]`, `no_api_calls=true`; source và fixture hash được lưu trong run record. Rà trực quan ảnh Customer mobile, Agent detail, Manager dashboard, Manager detail và controls thu gọn.
- Backend 181 test **không chạy lại** vì backend/dependencies không đổi. Không gán PASS race/atomicity/database event_id từ prototype.

Các lần trước giữ nguyên: [234608](prototype-ux-20261012-234608.json) không hoàn tất harness do lỗi mã hóa Unicode của lệnh chỉnh file; đã sửa bằng file UTF-8. [234732](prototype-ux-20261012-234732.json) harness 110/0 nhưng kiểm tra phím runner chưa đạt do thiếu text Enter và focus trước hash render; không ghi cả run này PASS. [234837](prototype-ux-20261012-234837.json) đạt suite/browser; sau bổ sung nhãn N đã chạy lại toàn bộ lần cuối nêu trên. Không sửa các record chưa đạt thành đạt.

## Sáu ảnh bàn giao mới

| Ảnh | Dữ liệu / thao tác thật |
|---|---|
| [Customer Resolved](prototype-ux-20261012-235015-ux-customer-resolved.png) | DEMO-05 #1, Customer 1; nút xác nhận/form từ chối; hội thoại công khai, không block nội bộ |
| [Agent detail](prototype-ux-20261012-235015-ux-agent-detail.png) | DEMO-04 #1, Agent 3; hai SLA, hội thoại, note gửi qua form, R1 mở và Resolved disabled |
| [Manager detail](prototype-ux-20261012-235015-ux-manager-review-detail.png) | DEMO-04 #1, Manager 6; R1 đang mở và form nguyên nhân/hướng xử lý |
| [Manager dashboard](prototype-ux-20261012-235015-ux-manager-dashboard.png) | DEMO-04; #1 có review mở; #2 được Customer tạo, Agent nhận/nhắn/Resolved, Customer xác nhận qua UI cùng clock 11:10. M-01 2/2, M-02 1/1, M-03 0/1; tải Agent/M-07 có dữ liệu. Không thêm seed/nhóm thứ bảy |
| [Mobile 390px](prototype-ux-20261012-235015-customer-mobile.png) | DEMO-05 Customer Resolved, trang không tràn ngang |
| [Controls thu gọn](prototype-ux-20261012-235015-ux-controls-collapsed.png) | DEMO-04 Agent 3; summary còn danh tính/DEMO/11:10 UTC+7; hướng dẫn và ticket vẫn hiện |

Runner còn lưu ảnh trước/sau sáu DEMO với tiền tố mới, giữ mọi ảnh cũ. Ảnh là capture trình duyệt thật, không ghép, tạo raster giả hoặc sửa nội dung DOM.

## Bảo toàn và giới hạn

Baseline đầu nhiệm vụ: [ux-baseline-20261013.json](ux-baseline-20261013.json), bao gồm thay đổi chưa commit sẵn có. Đối chiếu protected files không phát hiện thay đổi; 157 tệp evidence cũ giữ nguyên byte. BR/codes, backend/dependencies, 83 fixture và prototype domain.js/sla.js/reports.js/seeds.js/storage.js giữ nguyên byte. Fixture SHA-256: `6e75371714e5589eb78c45b0df3eb69595f2dfcc9362c9398b8c11989c0756ee`.

[Audit thực](prototype-ux-audit-20261012-235146.json), exit code 0, `passed=true`: 157 evidence cũ giữ nguyên, 0 thay đổi protected ngoài phạm vi, 0 source hash mismatch; 88 link local hợp lệ, `git diff --check` exit 0. Hai liên kết tới audit được bổ sung sau lần chạy này và kiểm tra tồn tại riêng; không đổi source đã kiểm thử. Kiểm tra này dùng Edge headless; chưa kiểm tra browser khác hoặc thiết bị vật lý, chưa có chủ dự án duyệt UX cuối. Prototype vẫn là demo dữ liệu trình duyệt; dữ liệu có thể xem qua DevTools, không chứng minh bảo mật production. Không phát hiện thay đổi chạm nghiệp vụ ngoài phạm vi được duyệt.
