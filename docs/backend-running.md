# Chạy backend và kiểm thử

FastAPI + SQLite độc lập với prototype. Requirements giữ nguyên; Python 3.12.10 đã được kiểm tra trên Windows. [Contract](04-data-api/api-contract.md), [OpenAPI](../api/openapi.json), [bằng chứng môi trường](../tests/evidence/step1-windows-20261012-162259-report.md).

## Windows PowerShell

Từ root repo, dùng Python 3.12 đã cài. Chỉ tạo virtualenv nếu `.venv` chưa tồn tại; không ghi đè môi trường cần giữ:

```powershell
py -3.12 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -m pip check
& .\.venv\Scripts\python.exe -m pytest
& .\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

Nếu không có launcher `py`, gọi executable Python 3.12 của máy bạn để tạo venv. Bằng chứng Windows cũ dùng Python nền cài theo người dùng, gọi executable trực tiếp; không coi lệnh launcher mới là đã chạy trong clean-start cũ. Không cần activate hay đổi ExecutionPolicy. Dừng server bằng Ctrl+C ở đúng terminal đó.

Mở `http://127.0.0.1:8000/docs`. Header `X-Demo-User-Id`: Customer 1/2, Agent 3/4/5, Manager 6. Đây là danh tính mô phỏng.

SQLite mặc định `data/ticketing.sqlite3`. Muốn dùng database khác, đặt `TICKETING_DB` trước khi khởi động/import app. Không xóa database hiện có. Tùy chọn `& .\.venv\Scripts\python.exe -m backend.seed` chỉ dựng bốn tình huống xác định trên database chưa có ticket, không xóa dữ liệu; mốc seed 12/10/2026 08:00 UTC+7 không là clock server thật. **Không seed database chạy collection**: xem [hướng dẫn Postman/DB mới](../api/README.md).

Trên hệ thống khác, tạo/kích hoạt virtualenv theo hệ điều hành, rồi `python -m pip install -r requirements.txt`, `python -m pytest`, `python -m uvicorn backend.app:app --port 8000`. Không suy kiểm tra Windows thành xác nhận mọi hệ điều hành.

## Tái lập và bằng chứng

Pytest dùng database thử và clock inject theo fixture; không dùng database demo hoặc clock prototype. [181 test Windows repo](../tests/evidence/step1-windows-20261012-162259-repo-junit.xml) và [181 test source mới](../tests/evidence/step1-windows-20261012-162259-clean-junit.xml) đã chạy tại mốc 12/10/2026; [manifest/lệnh](../tests/evidence/step1-windows-20261012-162259-run.json) đối chiếu source hiện hành. Không cộng hai lần chạy thành 362 tình huống.

[Collection helper](../tests/postman/run_newman.py) chọn port riêng, dùng database chưa tồn tại mỗi lần, đặt env trước import, chạy Newman thật rồi dừng đúng server; database/log giữ riêng. [Prototype](../prototype/README.md) là HTTP tĩnh với localStorage và clock đứng yên, hoàn toàn độc lập.

README đã có bằng chứng clean-start Windows cho backend tại mốc cũ. Hướng dẫn đã viết lại được rà lệnh/link và đối chiếu với mốc đó; chưa có lần clean-start mới toàn bộ bộ tài liệu portfolio bằng checkout mới sau xuất bản. Điều này được ghi riêng tại [release checklist](release-checklist.md).
