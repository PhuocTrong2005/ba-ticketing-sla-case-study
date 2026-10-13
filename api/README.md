# Postman — API mô phỏng

[Clean-start clone origin/main tại `7c35b2c`](../tests/evidence/portfolio-clean-start-report-20261013.md): setup tooling và runner nguyên bản chạy bằng venv/Node/cache/database mới; **191 request/514 assertion, 0 lỗi, exit 0**. Không cần tooling/config của repo tác giả hoặc workaround ngoài hướng dẫn Postman. [Lần clone thứ hai](../tests/evidence/portfolio-clean-start-repeat-20261013.md) tái hiện kết quả; DOC-CS-01 thuộc hướng dẫn auditor prototype ở commit cũ, không thuộc collection/backend.

Mốc D-48, 13/10/2026: chủ dự án chấp nhận kết quả Newman 191 request/514 assertion đã báo và cho phép commit/push Postman cùng tài liệu portfolio. “Chưa commit/push” trong phạm vi D-47 bên dưới là lịch sử. Source/collection/helper không đổi sau run cuối, không chạy lại để lặp kết quả; [audit xuất bản](../tests/evidence/portfolio-publication-report-20261013.md), [release checklist](../docs/release-checklist.md) ghi trạng thái/giới hạn. Không suy chủ dự án tự chạy mọi request; quyết định phát hành portfolio hiện hành là D-51.

Collection v2.1 và environment trong thư mục này phục vụ kiểm tra HTTP thật theo [API contract](../docs/04-data-api/api-contract.md), [OpenAPI](openapi.json), BR/codes hiện hành. Customer 1/2, Agent 3/4/5, Manager 6 dùng `X-Demo-User-Id`; đây không phải đăng nhập production. Client chỉ gửi payload được contract cho phép. Kỳ/as_of của báo cáo là query đọc, không đặt timestamp sự kiện hay điều khiển clock backend.

## Phạm vi được yêu cầu — 13/10/2026

Chủ dự án yêu cầu tạo collection/environment, chạy thật Postman/Newman trên database mới riêng và lưu bằng chứng; chưa commit/push, không làm video hoặc viết lại README tổng thể. Không đổi BR/backend/dependencies/prototype/83 fixture để phục vụ collection. Giữ `Run Project.txt`, thay đổi có sẵn và mọi evidence trước nhiệm vụ. Các request là kiểm tra giao dịch/contract API, không thêm fixture SLA verified hoặc tự xác nhận AC.

Collection chia sáu nhóm: database rỗng/identity/báo cáo rỗng; tạo và validation; luồng công khai/nội bộ/Waiting/reject/review/Closed; tải 3 và Customer return quá tải; M-01…M-07/quyền/kỳ/filter; cấu trúc payload và thứ tự lỗi BR-33. ID ticket và review lấy từ response, không hardcode ID. Dữ liệu và thứ tự giao dịch xác định, không ngẫu nhiên. Mỗi request có mã PM, trace AC/BR, expected HTTP/error_code và assertion; không có trường verified/expected fixture SLA mới.

## Giới hạn

Chạy tuần tự không chứng minh hai race. Không chờ nhiều giờ/ngày, sửa timestamp database hoặc dùng clock prototype. API dùng thời gian server thật; assertion không phụ thuộc giờ/ngày cố định. Biên lịch/deadline/83 fixture/race giữ [bằng chứng pytest riêng](../tests/evidence/backend-test-report.md). Không cộng assertion Newman với 181 pytest thành số tình huống độc lập hoặc gán PASS toàn bộ AC chỉ từ danh sách coverage.

## Import và Collection Runner

1. Import [collection v2.1](ticketing-sla.postman_collection.json) và [environment](ticketing-sla.postman_environment.json) vào Postman.
2. Chọn environment **BA Ticketing SLA · Local isolated API**. `base_url` mặc định `http://127.0.0.1:8001`; đặt đúng host/port của backend thử riêng. Customer 1/2, Agent 3/4/5, Manager 6 đã cấu hình; không có token/mật khẩu/đường dẫn riêng máy.
3. Khởi động backend trên database **chưa tồn tại** như phần dưới. Không chạy seed. Request PM-001 kiểm tra database rỗng và dừng chuỗi nếu đã có ticket; mọi lần chạy lại cần database mới.
4. Chạy **toàn collection**, một iteration, giữ thứ tự sáu folder. Các folder sau phụ thuộc ID/giao dịch trước; không chạy riêng folder rồi coi là kết quả đủ. PM-001 xóa biến runtime cũ; request tạo giữ alias riêng, `ticket_id` luôn là ticket workflow chính; `review_key` lấy từ response.
5. Export kết quả nếu dùng Postman UI. Nhiệm vụ này thực thi bằng Newman thật, không dùng UI Runner và không gán kết quả cho UI Runner.

`period_from`/`period_to` sinh từ HTTP Date server (khoảng ±7 ngày), `future_as_of` chỉ kiểm tra query đọc bị từ chối; `observed_created_at` lấy từ response. Biến query local `_url` encode offset `+07:00`, không gửi timestamp ghi sự kiện. Không assertion theo một giờ cố định hoặc sửa clock. localStorage/prototype không tham gia.

## Chạy Newman trên Windows — cách đã kiểm tra

Từ root repo, dùng virtualenv Python hiện có. Không cài lại requirements hoặc chạy pytest chỉ để chạy collection. Nếu máy chưa có Node/Newman, helper cài Node portable từ nodejs.org, đối chiếu SHA-256 chính thức và cài Newman 6.2.1 vào `.postman-tools/` bị ignore; không đổi PATH/dependencies Python/backend:

```powershell
& .\.venv\Scripts\python.exe tests/postman/setup_tools.py
& .\.venv\Scripts\python.exe tests/postman/run_newman.py
```

Helper thứ hai chọn port loopback trống, tạo thư mục `.postman-runs/<UTC-stamp>/`, xác nhận `ticketing.sqlite3` chưa tồn tại, đặt `TICKETING_DB` trong môi trường subprocess **trước khi import app**. Sau readiness, so OpenAPI live với file tracked, gọi CLI Newman thật với `--bail failure`, timeout 10 giây/request và reporters `cli,json,junit`. Python chỉ orchestration/ghi metadata; assertion nằm trong script Postman. CLI tương đương khi Node/Newman có trên PATH và backend thử đã chạy:

```powershell
newman run api/ticketing-sla.postman_collection.json `
  -e api/ticketing-sla.postman_environment.json `
  --bail failure --timeout-request 10000 --reporters cli,json,junit `
  --reporter-json-export tests/evidence/newman-NEW-STAMP.json `
  --reporter-junit-export tests/evidence/newman-NEW-STAMP.xml
```

Thay `NEW-STAMP` bằng tên mới; không ghi đè report cũ. `run_newman.py` tự đặt tên riêng và dừng đúng PID Uvicorn nó tạo trong `finally`; không dừng server khác. Nó giữ database/server log dưới `.postman-runs/`, không xóa database demo hiện có. Không export environment runtime vào repo; environment dùng để chia sẻ giữ các ID rỗng.

## Backend riêng cho Postman UI / Newman thủ công

Chạy từ root trong terminal riêng. Nếu port 8001 đang được dùng, chọn port trống khác và đổi `base_url`; không dừng server đang có:

```powershell
$taskStamp = [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss-fffffff')
$taskRunDir = Join-Path (Get-Location) ".postman-runs/$taskStamp"
New-Item -ItemType Directory -Path $taskRunDir -ErrorAction Stop | Out-Null
$taskDb = Join-Path $taskRunDir 'ticketing.sqlite3'
if (Test-Path -LiteralPath $taskDb) { throw 'Database thử phải chưa tồn tại' }
$taskPreviousDb = $env:TICKETING_DB
$env:TICKETING_DB = $taskDb
try {
  & .\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8001
} finally {
  $env:TICKETING_DB = $taskPreviousDb
}
```

Mở `http://127.0.0.1:8001/docs` để kiểm tra server. Sau chạy collection, Ctrl+C **terminal server này**; không xóa database. Không import app trước khi đặt biến môi trường, không dùng `--reload` hoặc database demo.

## Bộ dữ liệu và kết quả mong đợi

Agent 3 hoàn thành ticket High chính, ba lần từ chối tạo một review, Customer resume khi review còn mở không gỡ chặn Resolved, Manager hoàn tất khi Waiting rồi ticket Closed. Agent 4 có return ticket Normal đã Resolved trước khi nhận ba ticket khác; return tăng tải 3 → 4 hợp lệ, nhận mới bị chặn; hai Waiting giảm tải 4 → 3 → 2, sau đó nhận mới thành 3. Agent 5 dùng riêng cho ticket Resolved chờ xác nhận. Customer 2 có một New để kiểm tra ownership.

Cuối run có 8 ticket: 1 Closed, 3 In Progress, 2 Waiting, 1 Resolved, 1 New. M-01 có 5 kết quả phản hồi đầu/3 pending; M-02/03 mẫu số 1 và 7 unclosed, M-03 tử số 1. Không ép tử số SLA met theo giờ cố định. M-06 tải 3/4/5 = 0/3/0; M-05 có một Resolved; M-07 có review đã hoàn tất. Mẫu số 0 kiểm tra cả database rỗng và filter Normal + Agent 3 phù hợp dataset. Kỳ/filter/as_of/422 sai cấu trúc/ưu tiên lỗi có request riêng.

Lần thực hiện cuối ngày 13/10/2026: **191 request, 514 assertion đạt; 0 lỗi; exit code 0**, một iteration. Node v22.23.3, Newman 6.2.1, Python 3.12.10. Backend/OpenAPI/dependencies/prototype/83 fixture giữ nguyên. [Báo cáo và giới hạn](../tests/evidence/postman-report-20261013.md), [run record](../tests/evidence/newman-20261013-004259-750031-run.json), [Newman JSON](../tests/evidence/newman-20261013-004259-750031.json), [JUnit](../tests/evidence/newman-20261013-004259-750031.xml).

Expected số lượng trên áp dụng toàn collection hiện hành, fresh database và một iteration; assertion không phải tình huống độc lập. [Generator](../tests/postman/build_collection.py) tạo hai file JSON xác định; chỉ dùng khi sửa collection và phải chạy lại trên database mới. [Hướng dẫn Newman chính thức](https://learning.postman.com/docs/collections/using-newman-cli/installing-running-newman), [reporters chính thức](https://learning.postman.com/latest-v-12/docs/reference/newman-cli/newman-built-in-reporters).
