# Postman/Newman — 13/10/2026 (UTC+7)

Thực hiện theo yêu cầu chủ dự án và [D-47](../../docs/decision-log.md), [API README](../../api/README.md). Chưa commit/push; chưa làm video hoặc viết lại README tổng thể. Không thay BR/backend/dependencies/prototype/83 fixture để làm collection đạt; không phát hiện lỗi implementation trong phạm vi request đã chạy. Không tự gán PASS toàn bộ AC/v1.0.

## Source và công cụ

Đầu nhiệm vụ HEAD `41d0ebf5fc2c96b745fa65301f0f9ba7ece08221`, working tree chỉ có `?? Run Project.txt`; giữ file này nguyên byte. [Baseline](postman-baseline-20261013.json) lưu 343 file protected cùng hash database demo đang có. Nguồn đối chiếu: AGENTS, API contract, OpenAPI, store/app/reports/SLA hiện hành và BR/codes/open questions. Không có blocker nghiệp vụ mới, không đổi đáp án verified.

Máy chưa có Node/Newman trên PATH hoặc vị trí cài Node thông thường. [Helper setup](../postman/setup_tools.py) tải Node portable từ nodejs.org, kiểm tra SHA-256 archive với SHASUMS256 chính thức, cài `newman@6.2.1` bằng npm trong `.postman-tools/` bị ignore, `--ignore-scripts --no-audit --no-fund`. Không cài package vào virtualenv/backend hoặc sửa PATH global. [Metadata tooling thực](postman-tools-20261013-003746.json): Node **v22.23.3**, npm **10.9.9**, Newman **6.2.1**; archive SHA-256 `2b0ff57b049cda1bbcea2240eec20467018713c1efe1f7360c2681859b90ed71`. Python runner **3.12.10**.

[Collection v2.1](../../api/ticketing-sla.postman_collection.json), [environment](../../api/ticketing-sla.postman_environment.json), [generator](../postman/build_collection.py). Environment chỉ có loopback base_url, danh tính demo và biến ID/kỳ runtime rỗng; không chứa token/mật khẩu/đường dẫn riêng máy. Không gửi timestamp/actor/assignee/event_id trong payload, kể cả negative test; dùng `unexpected_field` cho extra-field 422. Timestamp query của reports phục vụ đọc/kỳ, không điều khiển sự kiện hoặc backend clock. ID ticket/review được lưu từ response, không hardcode ID; dữ liệu giao dịch không ngẫu nhiên.

## Chạy thật

Lệnh từ root:

```powershell
& .\.venv\Scripts\python.exe tests/postman/setup_tools.py
& .\.venv\Scripts\python.exe tests/postman/build_collection.py
& .\.venv\Scripts\python.exe tests/postman/run_newman.py
```

`run_newman.py` tạo database chưa tồn tại trong thư mục run mới, đặt TICKETING_DB trong env subprocess trước import `backend.app`, chạy Uvicorn port loopback riêng, so OpenAPI live với tracked. Python không làm HTTP assertions thay Postman; nó gọi CLI Newman thực, stdout/JSON/JUnit đều từ Newman. Command CLI, versions, UTC start/end, source/collection/environment hashes, stats, exit code và server PID/stop nằm trong record. Database/server log giữ local, không xóa hoặc sửa timestamp DB; dừng đúng Popen PID do nhiệm vụ tạo.

| Run | Source / mục đích | Thực thi |
|---|---|---|
| [004148-848348 record](newman-20261013-004148-848348-run.json) | Collection ban đầu, trước bổ sung nhánh review-resume và bốn structural cases; giữ nguyên report lịch sử | 183 request, 491 assertion, 0 lỗi, exit 0; database mới `.postman-runs/20261013-004148-848348/ticketing.sqlite3` |
| [004259-750031 record cuối](newman-20261013-004259-750031-run.json) | Collection hiện hành, hash khớp source | **191 request, 514 assertion, 0 lỗi, exit 0**, một iteration; database mới `.postman-runs/20261013-004259-750031/ticketing.sqlite3` |

Run cuối bắt đầu `2026-10-13T00:42:59.753031+00:00`, kết thúc `00:43:20.974547+00:00` (**07:42:59–07:43:20 UTC+7**); thời gian CLI Newman khoảng **17,395 giây**, response trung bình ~8,87ms. Base URL thực từ record `http://127.0.0.1:59347`; helper chọn port trống thay vì cố định base_url mặc định. OpenAPI live khớp tracked; `failures=[]`, mọi requests/assertions pending/failed=0. `owned_server_stopped=true`; Windows terminate owned server cho `server_exit_code=1`, đây là dừng process sau run, không phải exit của Newman (0). Không dừng server sẵn có.

Collection SHA-256 `aa0fee14b2c60b6745724e9610925a20aea7bbaca8e37581d8b392742319554b`. Hash environment/backend/requirements/OpenAPI/fixture/generator/runner nằm trong run record. [Newman JSON cuối](newman-20261013-004259-750031.json), [JUnit cuối](newman-20261013-004259-750031.xml), [stdout cuối](newman-20261013-004259-750031-stdout.txt). Không ghi đè lần đầu: [JSON](newman-20261013-004148-848348.json), [JUnit](newman-20261013-004148-848348.xml), [stdout](newman-20261013-004148-848348-stdout.txt).

## Request cụ thể và phạm vi chứng minh

| Folder | Số request | Request / liên kết |
|---|---:|---|
| 01 fresh/identity/empty reports | 11 | PM-001 empty DB guard; PM-002…004 401 thiếu/sai identity; PM-011…017 M-01…07 empty response/zero denominators, BR-32/63 |
| 02 create/New | 21 | PM-020…029 title/description/priority thiếu/trắng/sai kiểu/extra field; PM-030 role trước content; PM-031/032 create/get; PM-033…040 404/403/queue chính xác, AC-01/03/06/16, BR-33/34/62 |
| 03 workflow/privacy/review/Closed | 75 | PM-041 New message; PM-042 A1; PM-043 claim snapshot; PM-044 Waiting trước reply; PM-045…049 missing/wrong content; PM-050…059 role/ownership/note/Customer privacy; PM-060…066 public reply/Waiting/Agent message+note/Customer resume/state errors; PM-070/075/076,080/085/086,090/095/096 ba lần reject và threshold; PM-097 REVIEW_REQUIRED; PM-098…109 review quyền/nội dung; PM-110/110a…d resume review-open không gỡ chặn; PM-111 M07 open; PM-112 Manager hoàn tất khi Waiting không tiếp tục clock; PM-113/114 Agent đọc plan/Customer private; PM-115 A1 đã hoàn tất; PM-116…118 resume/Resolved/Closed; PM-119 A2; PM-120…128 Closed/access/error priority/state giữ nguyên |
| 04 capacity/return | 30 | PM-130…139 dựng return/ba IP/new; PM-140/141 tải 3 chặn; PM-142 return hợp lệ; PM-143/144 quá tải 4; PM-145/146/147 Closed → assigned → capacity; PM-148…153 Waiting giảm tải và nhận lại hợp lệ; PM-154…159 ownership/list/M05 candidate. AC-07/10/11/12/15, BR-10/20/21/37/51/62 |
| 05 reports/filter/access | 40 | PM-161…167 contract M-01…07 với dataset cuối; PM-171…177 Customer 403; PM-181…187 Agent 403; PM-191…193 denominator=0 theo filter; PM-194…198 kỳ/priority/Agent/M06 all priorities; PM-200…209 invalid query/future as_of/M06 priority/agent filter/unknown metric; PM-210 historical as_of đọc từ response. AC-28…31, BR-63 |
| 06 BR-33 structural/final | 14 | PM-220…225 type/extra/malformed JSON/path exception 422 trước handler; PM-226 404 trước content; PM-227 identity trước role/content; PM-228 role trước Closed/content; PM-229 owner Closed/private; PM-230…233 missing body/root array/summary+reason wrong type. AC-01/05/16/21/27, BR-33/51/62 |

AC-02/04/12…16/21/23…27 được kiểm tra các nhánh workflow/quyền/contract nêu trên. Snapshot/count/state/read sau lỗi không chứng minh transaction rollback/race bằng HTTP tuần tự; phần atomicity AC-07/23, race AC-08/09 và replay AC-22 có [bằng chứng pytest riêng](backend-test-report.md). Không ghi toàn bộ AC-17…22/28…31 PASS chỉ từ request contract: collection không tự kiểm chứng mọi phép tính SLA hoặc mọi nhánh bộ lọc/biên.

## Bảo toàn và giới hạn

[Audit thực](postman-audit-20261013-004833-626690.json) PASS: 343 file protected, 291 bằng chứng trước nhiệm vụ và database demo giữ nguyên byte; không có source hash mismatch, hardcoded ticket ID hoặc payload trường hệ thống cấm. Danh tính đúng, requests thực đúng thứ tự collection; 119 link local hợp lệ, diff-check exit 0, không whitespace lỗi source. HEAD không đổi, không staged file; server/port nhiệm vụ đã dừng. Kiểm tra read-only database thử có 8 ticket với trạng thái đúng dataset, một review và 42 event.

[Audit bàn giao cuối](postman-audit-20261013-004951-140523.json) PASS sau cập nhật docs/hygiene: 121 link local hợp lệ, 191 requests thực đều đến đúng HTTP loopback/port nhiệm vụ, không destination ngoài server thử; các kiểm tra bảo toàn/hash/payload/ID/identity/diff/server/no-commit vẫn đạt. Link tới record cuối bổ sung sau audit được kiểm tra tồn tại riêng. Collection/backend không đổi sau run cuối, không cần chạy lại Newman/pytest chỉ vì cập nhật docs/auditor.

Giữ [audit chưa đạt](postman-audit-20261013-004813-573406.json): regex đường dẫn riêng máy nhận nhầm phần `s:/` của `https://`. Đã sửa bộ quét để nhận drive prefix tại boundary, không sửa collection/request/assertion/expected hoặc record cũ. Scan token/private-key/đường dẫn theo mẫu, không tuyên bố kiểm toán secrets toàn diện. `.gitattributes` chỉ thêm rules cho collection/environment/tools/evidence Postman mới để giữ hash khi commit sau review; attributes backend/fixture cũ giữ nguyên. `.gitignore` chỉ thêm thư mục tooling/database-run riêng. Node/npm dependencies/log/database chỉ local, không đưa vào bộ source chia sẻ.

Không chạy lại 181 pytest vì backend/dependencies không đổi. Không cộng **514 assertion Newman** với **181 pytest** thành số tình huống độc lập. Collection chưa kiểm tra Postman UI import trên app; đã chạy v2.1 qua Newman thực. Không commit/push trong nhiệm vụ; HEAD vẫn `41d0ebf`, `Run Project.txt` tiếp tục untracked nguyên byte. Chỉ bổ sung api/docs/tasks/traceability/tools/bằng chứng và hygiene Git cho các file mới.

Không chờ nhiều giờ/ngày, dùng prototype clock hoặc sửa timestamp database để kiểm thử SLA. Thời gian API là clock server thật; calendar/deadline/83 fixture/race giữ bằng chứng backend riêng. M-04 kiểm tra contract/loại Closed nhưng dataset tức thời có thể không có breach; không chứng minh nhánh breached qua Newman. M-07 kiểm tra open/completed review, clock paused và contract seconds, không đối chiếu tất cả phép overlap/breach context. Không gửi actor/assignee/event_id/timestamp, nên không có negative test với chính các trường cấm đó; extra-field dùng trường thường. Không xác nhận bảo mật production hoặc toàn bộ v1.0.
