# Xuất bản prototype — 13/10/2026 (UTC+7)

Nguồn chấp nhận: chủ dự án phê duyệt yêu cầu/kịch bản và các chỉnh UX, chấp nhận kết quả và ảnh bằng chứng từ kiểm thử tự động, cho phép commit/push main thường và triển khai Pages trong nhiệm vụ này. [D-46](../../docs/decision-log.md), [spec](../../docs/05-prototype/prototype-spec.md#10-xuất-bản-pages-được-duyệt--13102026). Không ghi rằng chủ dự án tự thao tác mọi kịch bản hoặc chạy công cụ; không tuyên bố toàn bộ v1.0 hoàn thành.

## Source và kiểm thử local

Đầu nhiệm vụ `HEAD=eb8d483`, working tree có prototype/UX/docs/evidence chưa commit và `Run Project.txt`. Giữ mọi thay đổi. Fetch origin/main thành công; `HEAD...origin/main=0/0`. Baseline [pages-baseline-20261013.json](pages-baseline-20261013.json) lưu hash backend/dependencies/BR/codes/83 fixture và 228 evidence có trước nhiệm vụ. Audit bảo toàn sẽ ghi trong record cuối.

UX đã đủ phạm vi: controls thu gọn, chữ dễ đọc, hướng dẫn theo vai trò, nhãn SLA/report và navigation Manager. Chỉ sửa footer nguồn dự án thành URL GitHub để không liên kết tới README ngoài artifact runtime. Không sửa expected/assertion/nghiệp vụ. Sau thay đổi đã chạy `& .\.venv\Scripts\python.exe tests/prototype/run_browser.py`: [run đầu](prototype-ux-20261013-002125.json) và [run cuối sau bổ sung công cụ/docs](prototype-ux-20261013-002503.json) đều **110 PASS / 0 FAIL**, `ux_browser_passed=true`, không lỗi JavaScript, không API. Có ảnh mới sáu DEMO và các phần UX. Fixture SHA-256 `6e75371714e5589eb78c45b0df3eb69595f2dfcc9362c9398b8c11989c0756ee`. Backend/dependencies không đổi, không chạy lại backend 181 test. Server local có thông báo connection reset khi Edge hủy kết nối; không phải lỗi JavaScript hay assertion, runner exit 0.

## Cấu hình triển khai

[Workflow](../../.github/workflows/pages.yml) dùng checkout/configure-pages/upload-pages-artifact/deploy-pages theo [hướng dẫn GitHub](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages). Artifact có đúng `index.html`, `styles.css`, `app.js`, `domain.js`, `guidance.js`, `reports.js`, `seeds.js`, `sla.js`, `storage.js`, `.nojekyll`. `seeds.js` là runtime bộ mẫu xác định phục vụ demo; fixture kiểm thử 83 ca không được upload. Không có backend, SQLite, tests/evidence, log, profile hoặc secrets. ES modules/CSS dùng relative; index đặt tại gốc project subpath.

Credential GitHub sẵn có chỉ dùng trong bộ nhớ qua Git Credential Manager; không lưu token ra file/log. Tài khoản có admin/push; Pages trước đó chưa bật. Đã bật riêng Pages `build_type=workflow`, HTTPS và public theo repo public hiện có; không thay quyền repo hoặc cấu hình không liên quan. GitHub trả `html_url=https://phuoctrong2005.github.io/ba-ticketing-sla-case-study/`. Chưa suy kết quả deploy từ bước cấu hình. `.gitattributes` giữ byte runtime/công cụ/evidence prototype mới giữa Windows và Linux; không đổi attributes backend/fixture cũ. Log Edge giữ local và ignore; không xóa lịch sử chạy. `Run Project.txt` có sẵn vẫn giữ nguyên, ngoài commit vì là lệnh riêng máy.

## Kiểm tra công khai

[Demo thực](https://phuoctrong2005.github.io/ba-ticketing-sla-case-study/) đã mở trực tiếp trong Edge headless trên origin Pages. [Workflow cuối](https://github.com/PhuocTrong2005/ba-ticketing-sla-case-study/actions/runs/38327310064) của runtime commit [`4bf3599`](https://github.com/PhuocTrong2005/ba-ticketing-sla-case-study/commit/4bf35993228ab47359737342db7c0fdf0a9cb906) kết thúc `success`; [metadata triển khai, jobs/steps và probes](pages-deployment-20261013-002812.json) ghi GitHub trả URL thật, HTTPS, build_type workflow. Commit đầu [`7c2edb3`](https://github.com/PhuocTrong2005/ba-ticketing-sla-case-study/commit/7c2edb3ff86d361623dbe381bfc8753be6b3625e) cũng deploy thành công nhưng chỉ bản sau sửa giữ byte được dùng cho public smoke.

Lệnh thực: `& .\.venv\Scripts\python.exe tests/prototype/public_smoke.py https://phuoctrong2005.github.io/ba-ticketing-sla-case-study/`. [Record public mới](pages-public-smoke-20261013-002741.json) exit 0, **74/74 kiểm tra PASS**, 10 ảnh browser thật tên mới. HTTP tải 9 assets đều 200 và SHA-256 khớp byte source. Browser tải CSS và 7 modules thành công, `runtime_errors=[]`, `network_failures=[]`, không Fetch/XHR/API. Favicon mặc định ở gốc origin trả 404, không ảnh hưởng UI/assets runtime hoặc luồng demo; không gọi FastAPI.

| Nhóm / hành vi | Local | Pages công khai |
|---|---|---|
| DEMO-01 thành công | Luồng đầy đủ trong suite | Tạo High → nhận → nhắn → Resolved → Customer xác nhận Closed; tiến clock 09:05/09:10/09:30/09:35 bằng form UI |
| DEMO-02 Waiting, DEMO-03 từ chối, DEMO-04 review, DEMO-05 tải, DEMO-06 SLA biên | Luồng/assertion đầy đủ sáu nhóm cùng 83 fixture trong 110 ca | Chỉ smoke trạng thái mẫu và đổi Customer/Agent/Manager; DEMO-06 đổi 5 biến thể, +1 giây/reset. Không chạy lại toàn bộ nhánh/expected các nhóm này trên Pages |
| Bốn view | Suite DOM/UX | Customer, Agent, Manager và chi tiết ticket đã render từ site thật |
| Quyền hiển thị | Controller + DOM | Customer không có SLA/note/review/form nội bộ; Customer 2 vào ticket Customer 1 nhận 404; Manager không có claim/message/Resolved/confirm; Agent thấy review chặn Resolved |
| Điều khiển / navigation | UX/click/keyboard/mobile | Chọn 6 nhóm, danh tính, biến thể, clock, khôi phục; 4 liên kết Manager đưa focus heading; controls thu gọn vẫn có hướng dẫn. Chưa chạy keyboard/mobile riêng trên origin Pages |
| localStorage / network | Storage/schema/quota/reload và static subpath | Namespace trên origin Pages tồn tại, giữ nguồn sau reload và vẫn render Closed; nguồn được sinh bởi thao tác UI, không sửa storage để dựng đáp án. Không Fetch/XHR/API/lỗi JavaScript chặn |

Ảnh công khai tiêu biểu: [Customer Closed](pages-public-smoke-20261013-002741-customer-closed.png), [Manager dashboard](pages-public-smoke-20261013-002741-manager-dashboard.png), [Manager review detail](pages-public-smoke-20261013-002741-manager-review-detail.png), [Agent controls thu gọn](pages-public-smoke-20261013-002741-agent-controls-collapsed.png). Còn sáu ảnh DEMO-01…06 initial trong record. Đã rà trực quan Customer Closed và Manager dashboard. Probes backend/app.py, SQLite, fixture, evidence và README local trên site đều 404, đúng artifact runtime; footer README trỏ về repo GitHub.

## Rà soát, bảo toàn và bàn giao

[Audit bảo toàn trước commit](pages-audit-20261013-002616.json) và [sau commit runtime](pages-audit-20261013-002729.json) PASS: 261 file protected, 228 evidence trước nhiệm vụ nguyên byte, không đổi backend/dependencies/BR/codes/fixture. Runtime/harness khớp hash lần local cuối. Link local hợp lệ, staged diff sạch, không virtualenv/database/profile/cache/log/secrets trong commit. Scan token/private-key là kiểm tra theo mẫu, không tuyên bố kiểm toán bảo mật toàn diện.

[Audit bàn giao](pages-audit-20261013-003014.json) PASS: 131 link local hợp lệ, 218 file index đúng byte disk, không source mismatch, diff/staged diff exit 0. Các link tới audit bổ sung sau lần này được kiểm tra tồn tại riêng. Đối chiếu Git blob của tất cả backend/tests-backend/tests-SLA/evidence/dependencies/BR/codes đã tracked tại `eb8d483` với runtime HEAD không có thay đổi. File bằng chứng có sẵn trên disk vẫn đúng hash baseline; bằng chứng prototype mới được commit đúng byte, còn log giữ local. Không coi khác biệt xuống dòng có sẵn giữa disk Windows và Git blob lịch sử là thay đổi trong nhiệm vụ.

Giữ nguyên [audit chưa đạt đầu tiên](pages-audit-20261013-002555.json): thuộc tính CRLF chưa được hoàn thiện làm staged diff check trả 2. Đã sửa rồi chạy audit mới, không đổi record cũ. Rà byte index sau commit đầu phát hiện 24 file còn bị chuẩn hóa xuống dòng vì đã stage trước attributes; commit đầu đã được tạo do chuỗi PowerShell không dừng ở lỗi assertion. Đã tạo commit thường `4bf3599` bằng Python `check=True`/assert để dừng khi lỗi, `git add --renormalize` chỉ trên 24 file liên quan, không reset/force/amend, không sửa file nguồn trên disk. Kiểm tra lại index không còn byte mismatch; asset công khai sau đó khớp byte đã kiểm thử. Audit cuối bổ sung kiểm tra byte index để phát hiện lỗi tương tự.

Commit bàn giao tiếp theo chỉ cập nhật docs/công cụ audit/evidence public; runtime không đổi nên không chạy lại suite/backend hoặc deploy lặp. README chỉ thêm link/cách dùng/kết quả/nguồn chấp nhận; TASKS/traceability cập nhật phạm vi prototype/Pages. `Run Project.txt` vẫn giữ nguyên untracked, log Edge giữ local ignored. Git status sau bàn giao phải ghi đúng phần còn lại, không gọi working tree clean.

Postman và video ngoài nhiệm vụ. Không xác nhận cross-browser hoặc thiết bị vật lý; dữ liệu trình duyệt đọc được qua DevTools, danh tính mô phỏng không phải đăng nhập production.
