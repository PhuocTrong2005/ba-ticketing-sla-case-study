# Bước 1 — ổn định Python và clean-start Windows

Kết quả thực chạy: **PASS — hoàn tất bước 1**. Ngày 12/10/2026, múi giờ Asia/Ho_Chi_Minh; mã lần chạy `20261012-162259`. Không kết luận toàn bộ v1.0 hoàn thành.

## Môi trường và nguồn thực thi

- Hệ điều hành thực thi: `Windows-11-10.0.26300-SP0`, x64. Codex chạy công cụ trên máy Windows thay chủ dự án; không suy chủ dự án tự chạy.
- Repo nguồn: `C:\Users\ASUS\ba-ticketing-sla-case-study`, gồm đúng 48 file thay đổi ban đầu. [Baseline SHA-256/status](step1-windows-20261012-162259-baseline.json) ghi trạng thái trước thao tác; mục `.step1-stamp` là file tạm của nhiệm vụ và đã được bỏ sau chạy.
- Python nền cũ: `C:\Users\ASUS\AppData\Local\Temp\ba-ticketing-sla-windows-tools\python\cpython-3.12.15-windows-x86_64-none\python.exe`, phiên bản 3.12.15. `.venv` cũ được đổi tên sang `.venv-backup-20261012-162259`; vẫn giữ nguyên nội dung. Bản dự phòng vẫn phụ thuộc Python nền trong Temp, không bảo đảm hoạt động nếu Temp bị dọn.
- Python ổn định mới: `C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe`, **3.12.10**, `[MSC v.1943 64 bit (AMD64)]`. `sys.base_prefix` ở cả hai virtualenv là `C:\Users\ASUS\AppData\Local\Programs\Python\Python312`.
- `sys.executable` repo: `C:\Users\ASUS\ba-ticketing-sla-case-study\.venv\Scripts\python.exe`; clean-start: `C:\Users\ASUS\ba-ticketing-sla-case-study\.clean-start-20261012-162259\.venv\Scripts\python.exe`. Giá trị đầy đủ `sys.version`, `sys.executable`, `sys.base_prefix`, `_base_executable` nằm trong [run record](step1-windows-20261012-162259-run.json).
- Kiểm tra PATH, Python launcher, registry HKCU/HKLM/WOW6432Node, Program Files, vị trí cài theo người dùng/uv và thư mục công cụ trước đó. Không có `py` launcher; PATH trỏ Python 3.13. Có Python 3.12.2 đi kèm MySQL Workbench và 3.12.15 trong Temp. Chọn bản độc lập chính thức theo người dùng; không thay Python của MySQL, Python 3.13 hay PATH. [Inventory và giới hạn tìm kiếm](step1-windows-20261012-162259-inventory.json).
- Bộ cài từ [trang phát hành Python chính thức](https://www.python.org/downloads/release/python-31210/), URL tải `https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe`. Authenticode `Valid`, người ký Python Software Foundation; [hash/exit code và nguồn tải](step1-windows-20261012-162259-install.json). Lần tải sandbox bị chặn mạng; tải/cài lại qua quyền thực thi mở rộng thành công, exit 0.

## Lệnh đã thực thi

Đã đọc `AGENTS.md`, nguồn sự thật và open questions. Kiểm tra môi trường bằng `Get-Content .venv\pyvenv.cfg`, `Get-Command python,py,uv`, `py -0p` (không có launcher), `Get-ChildItem` tại các vị trí ghi trong inventory và `Get-ItemProperty` các nhánh registry PythonCore. Baseline dùng `git ls-files --cached --others --exclude-standard`, `git status --short --untracked-files=all`, `Get-FileHash`, `Get-ExecutionPolicy -List`.

Tải bằng `Invoke-WebRequest`, kiểm tra `Get-AuthenticodeSignature`, chạy bộ cài với `/quiet InstallAllUsers=0 TargetDir=<Python312> PrependPath=0 Include_launcher=0 Include_test=0 Include_pip=1 AssociateFiles=0 Shortcuts=0 /log <log mới>`. Không activation, không thay ExecutionPolicy.

Sau khi giữ `.venv` cũ, chạy trực tiếp Python nền 3.12.10 `-m venv .venv`. Tại mỗi thư mục, dùng Python riêng của virtualenv để chạy:

```powershell
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -m pip check
& .\.venv\Scripts\python.exe -m pip freeze
& .\.venv\Scripts\python.exe -m pytest --junitxml=<đường dẫn evidence mới>
```

[Runner thực thi](step1_windows_runner.py) dùng Python host 3.13 để điều phối, không dùng host đó chạy pytest/Uvicorn. Lệnh gọi lần này: `C:\Program Files\Python313\python.exe tests/evidence/step1_windows_runner.py 20261012-162259`. Runner không chạy lại đè các thư mục đã tồn tại. Toàn bộ argv/cwd/exit code và log của lệnh con nằm trong run record.

## Kết quả

| Kiểm tra thực chạy | Kết quả | Bằng chứng |
|---|---|---|
| Cài requirements và pip check repo gốc | PASS, exit 0 | repo-install.log, repo-pip-check.log |
| Toàn bộ pytest theo pytest.ini tại repo | PASS, 181 passed; 0 failures/errors/skipped | [JUnit repo](step1-windows-20261012-162259-repo-junit.xml), repo-pytest.log |
| Cài requirements và pip check thư mục mới | PASS, exit 0 | clean-install.log, clean-pip-check.log |
| Toàn bộ pytest theo pytest.ini tại source mới | PASS, 181 passed; 0 failures/errors/skipped | [JUnit clean-start](step1-windows-20261012-162259-clean-junit.xml), clean-pytest.log |
| HTTP `/docs` và `/openapi.json` | PASS, 200; HTML Swagger UI và schema có `/tickets` | [26 request/response thực](step1-windows-20261012-162259-run.json) |
| ENV-STEP1-01: Customer tạo → Agent nhận → Agent Resolved có kết quả → Customer Closed | PASS, 201/200, NEW → IN_PROGRESS → RESOLVED → CLOSED | run record, [server log](step1-windows-20261012-162259-server.log) |
| Customer không nhận SLA/cảnh báo/note/review nội bộ | PASS trên create/confirm/detail/list; reviews endpoint trả 404 | run record |
| ENV-STEP1-02: review có nội dung thực | PASS; 3 vòng resolve/reject tạo review, Manager ghi phương án; Agent thấy, Customer không thấy | run record |
| Dừng đúng server của nhiệm vụ | PASS, chỉ terminate đối tượng subprocess đã tạo và đợi kết thúc | PID/argv/cwd trong run record và kiểm tra cuối |
| Fixture 83 verified, expected/review_status | PASS, cùng hash toàn file trước/sau/copy | baseline, run record, kiểm tra cuối |
| File cũ/bằng chứng Linux và Windows trước đó | PASS, giữ nguyên byte; chỉ thêm nội dung vào 3 tài liệu được yêu cầu | baseline và kiểm tra cuối |
| `git diff --check` | PASS, exit 0 | [Kiểm tra cuối](step1-windows-20261012-162259-final-check.json) |

Hai lần pytest đều có 1 `DeprecationWarning` từ Starlette TestClient/AnyIO về alias `BlockingPortal`; không có test failure. Dependency thực cài được ghi trong hai freeze log; requirements giữ nguyên, không thêm pin phụ thuộc gián tiếp.

SHA-256 toàn bộ `tests/sla/sla-scenarios.json`: `6e75371714e5589eb78c45b0df3eb69595f2dfcc9362c9398b8c11989c0756ee`. Cả 83 object, `expected_*` và `review_status` được bảo toàn bằng kiểm tra byte toàn file; không sửa test/fixture hay tạo đáp án/bằng chứng giả.

## Clean-start và database

Thư mục mới còn được giữ: `C:\Users\ASUS\ba-ticketing-sla-case-study\.clean-start-20261012-162259`. Copy 62 file nguồn/tài liệu/test từ working tree hiện tại, gồm backend/API/SQL/test chưa commit; không clone origin/main. Manifest từng file và SHA-256 trong run record. Chính sách allowlist chỉ lấy root config cần thiết và phần backend/api/sql/docs/tests với đuôi mã nguồn/tài liệu cho phép; loại evidence cũ, `.git`, virtualenv, cache, database, env/credential và dữ liệu local khác. Không dùng database demo repo gốc. Không copy prototype/database placeholder không cần để chạy backend.

Pytest dùng database tạm riêng cho từng ca; biến `TICKETING_DB` của repo trỏ vào `.venv/step1-import.sqlite3` để việc import app không mở database demo. Clean pytest trỏ `data/step1-http.sqlite3` trong thư mục mới; HTTP dùng file mới khác `data/step1-workflow.sqlite3`, kiểm tra chưa tồn tại trước khi khởi động. Store chỉ tự tạo identity/policy xác định; không chạy demo seed.

Uvicorn chạy tại clean-start với `--host 127.0.0.1 --port 65134`; PID lần chạy `11576`. Server đã dừng. ENV-STEP1-01/02 là mã kiểm tra môi trường/workflow có dữ liệu xác định, không phải ca SLA mới hoặc fixture được xác nhận. Manager chỉ ghi phương án; không nhận ticket, gửi tin công khai hay Resolved. Không mô phỏng thông báo/phân công/hỗ trợ chuyên môn.

## File riêng và giới hạn

Chỉ sửa thêm nội dung vào `README.md`, `TASKS.md`, `docs/traceability.md`; mọi nội dung thay đổi ban đầu của chủ dự án được giữ. Không đổi source/test/requirements/quy tắc nghiệp vụ/decision log.

File mới của nhiệm vụ trong `tests/evidence/`: `step1_windows_runner.py` và toàn bộ file mang tiền tố `step1-windows-20261012-162259-`. Gồm baseline, inventory, install metadata, log bộ cài chính và 7 log MSI thành phần, run record, report, final-check, hai JUnit; log venv/install/pip-check/freeze/pytest của mỗi môi trường và server log. [Danh sách file đầy đủ với hash](step1-windows-20261012-162259-final-check.json) ghi riêng artefact nhiệm vụ. File stamp tạm đã bỏ. Giữ hai virtualenv, virtualenv dự phòng, thư mục kiểm tra và bộ cài trong Temp; không tự dọn.

Giới hạn: chỉ máy Windows này, source working tree tại thời điểm copy và toàn bộ suite cấu hình hiện có; không chứng minh mọi cài đặt Windows, deploy, production auth hoặc toàn bộ v1.0. Tìm Python theo vị trí chuẩn đã ghi, không quét mọi ổ đĩa. Bản source clean-start phản ánh tài liệu trước phần bổ sung báo cáo cuối; đoạn hướng dẫn PowerShell mới mô tả đúng các lệnh đã thực chạy. Bằng chứng trước đây giữ nguyên và không gán kết quả lần này vào lịch sử.

Chưa làm prototype, Postman, video hoặc deploy. Chưa commit/push. Không còn trở ngại cho bước 1.
