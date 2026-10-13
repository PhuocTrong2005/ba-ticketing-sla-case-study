# Xuất bản prototype — 13/10/2026 (UTC+7)

Nguồn chấp nhận: chủ dự án phê duyệt yêu cầu/kịch bản và các chỉnh UX, chấp nhận kết quả và ảnh bằng chứng từ kiểm thử tự động, cho phép commit/push main thường và triển khai Pages trong nhiệm vụ này. [D-46](../../docs/decision-log.md), [spec](../../docs/05-prototype/prototype-spec.md#10-xuất-bản-pages-được-duyệt--13102026). Không ghi rằng chủ dự án tự thao tác mọi kịch bản hoặc chạy công cụ; không tuyên bố toàn bộ v1.0 hoàn thành.

## Source và kiểm thử local

Đầu nhiệm vụ `HEAD=eb8d483`, working tree có prototype/UX/docs/evidence chưa commit và `Run Project.txt`. Giữ mọi thay đổi. Fetch origin/main thành công; `HEAD...origin/main=0/0`. Baseline [pages-baseline-20261013.json](pages-baseline-20261013.json) lưu hash backend/dependencies/BR/codes/83 fixture và 228 evidence có trước nhiệm vụ. Audit bảo toàn sẽ ghi trong record cuối.

UX đã đủ phạm vi: controls thu gọn, chữ dễ đọc, hướng dẫn theo vai trò, nhãn SLA/report và navigation Manager. Chỉ sửa footer nguồn dự án thành URL GitHub để không liên kết tới README ngoài artifact runtime. Không sửa expected/assertion/nghiệp vụ. Sau thay đổi đã chạy `& .\.venv\Scripts\python.exe tests/prototype/run_browser.py`: [run đầu](prototype-ux-20261013-002125.json) và [run cuối sau bổ sung công cụ/docs](prototype-ux-20261013-002503.json) đều **110 PASS / 0 FAIL**, `ux_browser_passed=true`, không lỗi JavaScript, không API. Có ảnh mới sáu DEMO và các phần UX. Fixture SHA-256 `6e75371714e5589eb78c45b0df3eb69595f2dfcc9362c9398b8c11989c0756ee`. Backend/dependencies không đổi, không chạy lại backend 181 test. Server local có thông báo connection reset khi Edge hủy kết nối; không phải lỗi JavaScript hay assertion, runner exit 0.

## Cấu hình triển khai

[Workflow](../../.github/workflows/pages.yml) dùng checkout/configure-pages/upload-pages-artifact/deploy-pages theo [hướng dẫn GitHub](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages). Artifact có đúng `index.html`, `styles.css`, `app.js`, `domain.js`, `guidance.js`, `reports.js`, `seeds.js`, `sla.js`, `storage.js`, `.nojekyll`. `seeds.js` là runtime bộ mẫu xác định phục vụ demo; fixture kiểm thử 83 ca không được upload. Không có backend, SQLite, tests/evidence, log, profile hoặc secrets. ES modules/CSS dùng relative; index đặt tại gốc project subpath.

Credential GitHub sẵn có chỉ dùng trong bộ nhớ qua Git Credential Manager; không lưu token ra file/log. Tài khoản có admin/push; Pages trước đó chưa bật. Đã bật riêng Pages `build_type=workflow`, HTTPS và public theo repo public hiện có; không thay quyền repo hoặc cấu hình không liên quan. GitHub trả `html_url=https://phuoctrong2005.github.io/ba-ticketing-sla-case-study/`. Chưa suy kết quả deploy từ bước cấu hình. `.gitattributes` giữ byte runtime/công cụ/evidence prototype mới giữa Windows và Linux; không đổi attributes backend/fixture cũ. Log Edge giữ local và ignore; không xóa lịch sử chạy. `Run Project.txt` có sẵn vẫn giữ nguyên, ngoài commit vì là lệnh riêng máy.

## Kiểm tra công khai

Đang chờ commit/push và workflow triển khai đầu tiên. Kết quả cuối, URL thực, workflow, public smoke và bảo toàn được bổ sung sau thực thi. Sáu nhóm chạy đầy đủ ở local; trên Pages chỉ định thực hiện smoke ban đầu sáu nhóm, một luồng DEMO-01 đầy đủ, bốn view, danh tính/quyền, kịch bản/khôi phục/clock, localStorage và network. Không gán 110 PASS local thành 110 ca trên Pages.

Postman và video ngoài nhiệm vụ. Không xác nhận cross-browser hoặc thiết bị vật lý; dữ liệu trình duyệt đọc được qua DevTools, danh tính mô phỏng không phải đăng nhập production.
