# Rà soát phạm vi backend trước commit/push — 12/10/2026

Chủ dự án cho phép commit/push backend đã duyệt và bằng chứng bước 1 lên `origin/main`. Đã đọc AGENTS.md; không sửa nghiệp vụ, source, dependencies, fixture hoặc test. Báo cáo này ghi rà soát trước commit; kết quả push/commit hash được báo riêng sau khi thực hiện.

## Phạm vi và remote

`git fetch origin main` thành công. `main` và `origin/main` đều ở `9688b7889df0d91b1bb9d26d3626b283945d9d5e`; `git rev-list --left-right --count main...origin/main` trả `0 0`. Không có remote mới cần hòa giải, không reset/force-push. Toàn bộ file chưa theo dõi được kiểm kê; môi trường/source-copy địa phương được phân loại riêng, không stage theo thư mục gốc.

Bao gồm 48 file backend/tài liệu/bằng chứng có từ trước bước 1: backend FastAPI/SQLite/SLA/reports/seed, SQL, OpenAPI, requirements/pytest config, tests, yêu cầu/BR/codes/decision log đã duyệt, README/TASKS/traceability, bằng chứng Linux và Windows ban đầu. Không viết lại nội dung đã duyệt. README/TASKS/traceability phân biệt kết quả backend với prototype/Postman/video chưa thực hiện và v1.0 chưa hoàn thành; các dòng chưa commit/push của bước 1 và báo cáo cũ là lịch sử tại lúc chạy.

## Quyết định cho 28 file bước 1

Giữ **18 file**: runner, report, baseline, final-check, inventory, install metadata, run record, hai JUnit, hai bộ log install/pip-check/freeze/pytest và server log. Chúng giải thích nguồn thực thi, lệnh/exit code, môi trường, workflow/quyền, phiên bản dependency và bảo toàn dữ liệu. Đã đối chiếu JUnit 181/181 của repo và clean-start, run record 26 request HTTP, hash fixture, source manifest và final-check. Đây là rà soát evidence có sẵn, không phải lần chạy lại test.

Giữ tại máy, **không commit 10 file**:

- `step1-windows-20261012-162259-python-install.log` và 7 log `_000_core`…`_006_pip`: khoảng 8 MB chẩn đoán MSI, dư thừa cho việc chia sẻ; install.json đã ghi nguồn chính thức/chữ ký/hash/exit code và run record ghi Python thực dùng.
- `step1-windows-20261012-162259-repo-venv.log`, `step1-windows-20261012-162259-clean-venv.log`: rỗng; argv và exit code đã nằm trong run record.

Manifest final-check bước 1 vẫn liệt kê cả 28 file vì đó là kiểm kê artefact tại máy vào thời điểm chạy; không có nghĩa cả 28 được publish. Nguồn evidence, hash và path lịch sử giữ nguyên, không tạo bản làm sạch. Rà nội dung không phát hiện credential/token hoặc dữ liệu doanh nghiệp trong phần stage; path máy, identity demo và dữ liệu kiểm tra xác định được giữ để truy nguồn. Không coi kiểm tra mẫu secret là bảo đảm phát hiện mọi loại secret.

Không commit `.venv`, `.venv-backup-20261012-162259`, `.clean-start-20261012-162259`, database, cache, bộ cài EXE, file tạm hay dữ liệu nhạy cảm. `.gitignore` bổ sung các môi trường/file bị loại mà không xóa chúng.

## Bảo toàn và kiểm tra

`core.autocrlf=true` có thể đổi byte của evidence khi stage/checkout. `.gitattributes` bổ sung `-text` cho các file `tests/evidence/backend-*`, `tests/evidence/step1-windows-*` và chỉ mục `tests/evidence/history/README.md` mới, để blob Git trùng byte nguồn đã hash; không đổi attribute fixture hoặc bằng chứng lịch sử đã tracked. Chỉ mục README mới được stage lại bằng `git add --renormalize -- tests/evidence/history/README.md` để index áp dụng attribute mới và khớp byte nguồn. Không renormalize fixture/bằng chứng lịch sử đã tracked hoặc sửa nguồn evidence.

Các đường dẫn evidence này dùng `cr-at-eol` cho whitespace check vì nguồn Windows có CRLF; vẫn kiểm tra dấu cách cuối dòng, cuối file và space-before-tab. Lần staged check đầu nhận diện CR của CRLF là whitespace; sửa attribute để nhận đúng line ending, không sửa byte nguồn.

Run record bước 1 ghi PID đối tượng launcher `11576`; server log ghi PID interpreter Uvicorn `2484`. Đây là hai mức tiến trình trên Windows, không sửa log/record để ép khớp. Final-check bước 1 xác nhận cổng đã đóng sau khi terminate/wait đối tượng đã tạo; không suy chỉ từ PID launcher rằng server đang lắng nghe đã dừng.

[Kết quả kiểm tra máy đọc được](step2-backend-publication-audit-20261012.json) ghi danh sách file chọn/loại, đối chiếu hash, JUnit, source, OpenAPI và liên kết. Link lịch sử có tám đường dẫn cũ đã được [chỉ mục lịch sử](history/README.md) ghi rõ; không sửa nguồn đã hash. Liên kết mới/sửa được kiểm tra theo phạm vi file đã chọn vào commit. Kiểm tra staged blob, staged whitespace và staged diff thực hiện sau khi stage; chỉ commit khi đạt.

Không chạy lại toàn bộ pytest: source/backend/test/requirements và evidence thực chạy giữ nguyên. Chỉ thay Git ignore/attribute và thêm báo cáo rà soát xuất bản. Bằng chứng gần nhất vẫn là [repo 181/181](step1-windows-20261012-162259-repo-junit.xml) và [clean-start 181/181](step1-windows-20261012-162259-clean-junit.xml), không suy một lần chạy mới.

Phần còn lại: prototype tĩnh, Postman và video/demo; không deploy và v1.0 chưa hoàn thành.
