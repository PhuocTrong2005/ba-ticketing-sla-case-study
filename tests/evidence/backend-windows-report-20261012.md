# Backend trên Windows — 12/10/2026

Codex áp dụng `D:\Download\Backend_SLA.patch` và chạy thực tế trên máy Windows của chủ dự án. Đây là bằng chứng mới, tách biệt với bằng chứng Linux do patch cung cấp; không suy ra chủ dự án tự chạy hoặc toàn bộ v1.0 hoàn thành.

Baseline: `9688b7889df0d91b1bb9d26d3626b283945d9d5e`, branch `main`, working tree ban đầu sạch và không có staged. Patch SHA-256: `11bbcb9ec6ce288935221cf1161e9ef59f0713c71f132ce41a98371f65f568d2`.

- `git apply --check 'd:\Download\Backend_SLA.patch'`: exit 0; không có xung đột.
- `git apply 'd:\Download\Backend_SLA.patch'`: exit 0; nhập đúng 43 file trong patch, không sửa thêm implementation.
- `git apply --reverse --check 'd:\Download\Backend_SLA.patch'`: exit 0; các thay đổi của patch vẫn áp dụng nguyên vẹn.
- `git diff --check`: exit 0. Không stage, commit hoặc push.

## Môi trường và cài đặt

Windows 11 (`Windows-11-10.0.26300-SP0`), CPython 3.12.15 AMD64; virtualenv `.venv`, không dùng system site-packages. Đã chạy `.venv\Scripts\python.exe -m pip install -r requirements.txt`, exit 0. `pip check`: không có dependency hỏng. Danh sách phiên bản đầy đủ nằm trong run record.

PowerShell chặn `Activate.ps1` bằng execution policy hiện có. Lần đầu lệnh tiếp tục sau lỗi activation nên cài nhầm vào Python 3.13 của user. Đã gỡ các gói vừa thêm và khôi phục ba phiên bản bị thay đổi: uvicorn 0.46.0, starlette 1.0.0, typing-extensions 4.13.2. Lần cài hợp lệ và toàn bộ kiểm thử sử dụng trực tiếp executable trong `.venv`; tiến trình con được đặt `VIRTUAL_ENV` và PATH tương ứng. Không đổi execution policy hệ thống.

Python nền 3.12.15 được tải riêng bằng uv tại `%TEMP%\ba-ticketing-sla-windows-tools\python\cpython-3.12.15-windows-x86_64-none`; `.venv\pyvenv.cfg` trỏ tới đường dẫn này. Không xóa thư mục Python nền khi còn sử dụng virtualenv; nếu dọn thư mục tạm, cần tạo lại virtualenv từ Python 3.12. Các script ghi bằng chứng và SQLite kiểm tra nằm trong `.venv`, được Git ignore.

## Kết quả thực chạy

- Pytest: **181 passed, 0 failed, 0 errors, 0 skipped**, một DeprecationWarning từ Starlette/AnyIO; 13,76 giây. Chạy `python -m pytest --junitxml=...` bằng Python 3.12 của virtualenv. [Run record](backend-windows-20261012-131256.json), [JUnit](backend-windows-20261012-131256-junit.xml).
- Uvicorn: chạy `python -m uvicorn backend.app:app --port 8000` bằng cùng virtualenv, database riêng `.venv/windows-http-smoke.sqlite3`. `/docs` trả 200, HTML có SwaggerUIBundle; `/openapi.json` trả 200, parse được, khớp cấu trúc JSON với `api/openapi.json` và có header `X-Demo-User-Id`.
- HTTP đọc `/tickets` với demo Customer 1/2, Agent 3/4/5, Manager 6 đều trả 200; không có header trả 401. Hàng đợi `/tickets/queue` trả 200 cho ba Agent, 403 cho hai Customer và Manager. Smoke dùng database trống, không tạo dữ liệu ngẫu nhiên hoặc giả lập đăng nhập thật.
- [HTTP record](backend-windows-http-20261012-131408.json), [server log](backend-windows-http-20261012-131408-server.log). Đã dừng tiến trình Uvicorn do nhiệm vụ tạo sau khi kiểm tra.
- Fixture nguyên byte trước/sau: SHA-256 `6e75371714e5589eb78c45b0df3eb69595f2dfcc9362c9398b8c11989c0756ee`; đủ 83 ca verified, không đổi `expected_*` hoặc `review_status`. Run record xác nhận bằng chứng Linux không đổi.

## Giới hạn và phần còn thiếu

Không kiểm tra Swagger tương tác bằng trình duyệt; chỉ kiểm tra HTTP/HTML và OpenAPI. Không chạy lại clean-start trong checkout mới trên Windows. Chưa xây/kiểm tra prototype, Postman/Newman, video hoặc triển khai; các kiểm thử đồng thời trong bộ test không phải benchmark tải. Requirements khóa năm dependency trực tiếp; phiên bản dependency gián tiếp của Windows được ghi trong run record và có thể khác Linux. Không tuyên bố v1.0 hoàn thành.

## Danh sách thay đổi

Patch thêm backend FastAPI/SQLite/SLA/reports/seed, OpenAPI, schema/SQL, test implementation và bằng chứng Linux; cập nhật tài liệu yêu cầu, BR/codes, decision log, contract, traceability, README và TASKS. Ngoài patch chỉ thêm năm file bằng chứng Windows (báo cáo này, JSON/JUnit pytest, JSON/log HTTP). Danh sách đầy đủ của 43 file patch:

- `.gitignore`
- `README.md`
- `TASKS.md`
- `api/openapi.json`
- `backend/__init__.py`
- `backend/app.py`
- `backend/reports.py`
- `backend/schema.sql`
- `backend/seed.py`
- `backend/sla.py`
- `backend/store.py`
- `docs/01-context/scope.md`
- `docs/03-requirements/functional-requirements-draft.md`
- `docs/03-requirements/non-functional-requirements-draft.md`
- `docs/03-requirements/user-stories-draft.md`
- `docs/04-data-api/api-contract.md`
- `docs/04-data-api/data-design.md`
- `docs/04-data-api/implementation-handoff.md`
- `docs/decision-log.md`
- `docs/open-questions.md`
- `docs/spec/business-rules.md`
- `docs/spec/codes.md`
- `docs/traceability.md`
- `pytest.ini`
- `requirements.txt`
- `sql/README.md`
- `sql/queries/m01.sql`
- `sql/queries/m02.sql`
- `sql/queries/m03.sql`
- `sql/queries/m06.sql`
- `tests/__init__.py`
- `tests/backend/__init__.py`
- `tests/backend/conftest.py`
- `tests/backend/test_api.py`
- `tests/backend/test_integrity.py`
- `tests/backend/test_reports.py`
- `tests/backend/test_sla.py`
- `tests/evidence/backend-clean-junit.xml`
- `tests/evidence/backend-clean-start.json`
- `tests/evidence/backend-junit.xml`
- `tests/evidence/backend-run.json`
- `tests/evidence/backend-test-report.md`
- `tests/evidence/history/README.md`
