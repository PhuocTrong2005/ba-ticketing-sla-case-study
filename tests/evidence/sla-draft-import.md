# Nhập và rà S1–S12 — 08/10/2026

Đã nhập **12 draft** thành SLA-70…SLA-81 vào [fixture](../sla/sla-scenarios.json). Giữ nguyên 69 ca verified, gồm metadata và byte của từng object. Không chuyển trạng thái review, không thêm xác nhận/bằng chứng/phương pháp tính tay của chủ dự án. Không thay quy tắc SLA hoặc viết backend/API/SQL/prototype. Gate SLA chính và M-07 vẫn chưa được xác nhận mở theo D-33.

Nguồn đáp án: đặc tả S1–S12 trong yêu cầu chủ dự án ngày 08/10/2026; S12 đã sửa hạn G thành **2026-10-06T08:30:00+07:00**. calculation_note diễn đạt phép tính được cung cấp, không phải lời khai chủ dự án tự tính tay. `verification_basis` ghi ca nguồn và yêu cầu giữ draft; bỏ hẳn verified_by, verified_at, owner_check_result, owner_results, owner_calculation_note, owner_confirmation ở ca mới. Hai trường snapshot trạng thái dùng pending/pending tại sự kiện agent_assigned; không thêm trường số giây snapshot chưa có trong fixture.

## Ánh xạ và đáp án đã nhập

Tất cả dùng HIGH. P used/left = 600/3000, met/none; hạn P là 12/10 09:00 ở S1, 05/10 10:00 ở S2–S4/S6–S7, 05/10 09:00 ở các ca còn lại. Mọi timestamp trong fixture là ISO 8601 +07:00 đến giây. Bảng dưới ghi tháng 10/2026, mọi ca vẫn draft.

| Nguồn | ID | Hạn G | G used/left (giây) | G status/warning | Ticket / review |
|---|---|---|---|---|---|
| S1 | SLA-70 | 12/10 16:00 | 1800/27000 | pending/none | In Progress; không review |
| S2 | SLA-71 | 06/10 09:00 | 27000/1800 | pending/soft | In Progress; không review |
| S3 | SLA-72 | 06/10 15:00 | 5400/23400 | pending/none | In Progress; không review |
| S4 | SLA-73 | 06/10 09:00 | 28800/0 | pending/due | In Progress; không review |
| S5 | SLA-74 | 06/10 08:00 | 28801/0 | breached/breached | In Progress; không review |
| S6 | SLA-75 | 06/10 08:00 | 28800/0 | pending/due | In Progress; không review |
| S7 | SLA-76 | 06/10 08:00 | 28800/0 | pending/due | In Progress; 1 từ chối, không review |
| S8 | SLA-77 | 05/10 16:00 | 25200/3600 | pending/none | In Progress; không review |
| S9 | SLA-78 | 05/10 16:00 | 27900/900 | pending/soft | In Progress; không review |
| S10 | SLA-79 | 06/10 08:10 | 17400/11400 | pending/none | In Progress; 5 từ chối, R3 mở |
| S11 | SLA-80 | null | 10800/18000 | pending/none | Waiting for Customer; 3 từ chối, R1 đóng |
| S12 | SLA-81 | **06/10 08:30** | 11700/17100 | pending/none | In Progress; 3 từ chối, R1 mở |

S10 có ba review riêng: R1 lịch/trùng G 1800/1800, R2 2700/2700, R3 1200/1200 giây; S11 R1 3000/1200; S12 R1 5700/2100. Tất cả breach_context=none. S11 phù hợp BR-08/57: review hoàn tất không phải Customer trả lời, ticket tiếp tục Waiting. S12 có 10 sự kiện thành công, resolved_attempt 12:40 là step_seq=11 trong expected_rejected_actions; không có resolved_attempt trong events.

## Rà trùng và schema

Đã đọc AGENTS, business-rules, codes, scenario-coverage, decision log, open questions, fixture, checker và các script audit/so nguồn trước khi sửa. SLA-61 thực tế có `expected_rejected_actions`; checker đọc đúng tên này. Không có khác biệt với xác nhận của chủ dự án.

So mỗi draft với 69 ca cũ trên policy_id, created_at, as_of, events, resolution_result_final và **toàn bộ expected_***: 828 cặp, không có ca trùng hoàn toàn. So 66 cặp giữa các draft cũng không trùng. ID/mô tả/provenance không tham gia phép so trùng. [Audit nhập](sla-draft-import-structure.json) lưu danh sách ID trùng rỗng cho từng ca. S8/S9 có cùng events nhưng as_of và đáp án khác; SLA-56/57 là ngưỡng lệch một giây. S10 nối thêm R3 so với SLA-64; S11 hoàn tất review trong Waiting thay vì sau resume như SLA-63; S12 thêm refusal giữa resume và review đóng. Nhập đủ 12 ca, không bỏ ca nào.

Fixture hiện chỉ có seq/type/at và at_raw khi cần; không lưu actor/nội dung. Không invent field để nhét payload. Vì chưa có contract tên trường, phần payload của S7/S10–S12 dừng ở [open questions](../../docs/open-questions.md); phần toán học vẫn nhập độc lập. Khi lập API test, mỗi resolved cần kết quả công khai, customer_reject cần lý do, review_completed cần phương án nội bộ hợp lệ; resolved_attempt S12 cũng cần nội dung hợp lệ. Không tuyên bố các nội dung/actor/quyền đó đã được kiểm thử.

## Kiểm tra thực tế

Lần chạy checker lúc `2026-10-08T13:05:49+07:00`, do Codex AI assistant thực thi. [Run record](sla-draft-import-run.json) lưu argv, exit code, stdout/stderr, Python và hash.

| Kiểm tra | Ca cũ | Ca mới | Phép so sánh / assertion | Kết quả |
|---|---:|---:|---|---|
| Cấu trúc fixture, schema hiện có, ID, metadata, thứ tự, interval/review/refusal shape | 69 PASS / 0 FAIL | 12 PASS / 0 FAIL | 3792 assertion cũ; 850 assertion mới | exit 0; không tính SLA |
| Checker gốc trên bản tách nguyên byte 69 ca cũ | 69 PASS / 0 FAIL | Không chạy | 1243 so sánh SLA | exit 0 |
| Checker gốc trên fixture 81 ca | 0 ca được thực thi | 0 ca được thực thi | 0 so sánh | exit 1: `ValueError: 69 unique IDs required` |
| So 69 object với nguồn ZIP đã lưu | 69 khớp toàn bộ | Không áp dụng | 1587 trường nghiệp vụ; metadata cũng khớp | exit 0; không tính SLA |
| Rà trùng cũ/mới và mới/mới | 69 đối chứng | 12 | 828 + 66 cặp object nghiệp vụ | Không trùng |

**Ca mới chưa có kết luận PASS/FAIL SLA:** CLI gốc từ chối trước vòng lặp tính toán. Không sửa checker, không đổi ID để vượt điều kiện 69, không gọi riêng hàm tính để tạo bằng chứng thay thế. [Kết quả checker 69 ca cũ](sla-draft-import-old-reference.json) và [so nguồn](sla-draft-import-source-comparison.json) là tệp mới, không ghi đè báo cáo lịch sử. [Audit cấu trúc mới](../sla/audit_draft_import.py) không có logic tính SLA; giữ nguyên checker và audit lịch sử.

SLA-61 có 1 phép so refusal trong tổng 1243: chỉ kiểm tra ngữ cảnh In Progress/review mở và đáp án 409 REVIEW_REQUIRED/no-change; không gửi HTTP. S12 chưa được checker gốc chạy vì giới hạn ID. A1/A2 không nằm trong phép đối chiếu SLA. Chưa chạy backend, API, SQL, prototype hoặc concurrency; không tạo bug/backend PASS từ giới hạn công cụ.

Bảo toàn: [baseline](sla-draft-import-baseline.json) ghi prefix 318042 byte đến hết object SLA-69, SHA-256 `a00237a5b66bcd8450f6cd3bdb2011bb28a31b6811df895836557b942a63f8c2`, vẫn khớp sau nhập. Mảng 69 ca tái lập từ prefix có hash `4bcad90141b1d6b86a28804b93a961cea2862d84011c6b463439c370c17397b9`, đúng bản trước nhập. Fixture 81 ca có hash `4ee909bf6afecffcdd9ac9c6b63609484fcb4ceb040129243ebc1bd92e005453`. Checker nguyên byte có hash `764c284609d7074cbebc7c027576e9c8a16c9a8792456f8e4909ca221464f9ed`.

Kiểm tra liên kết tài liệu, ID và `git diff --check` được ghi riêng trong [kiểm tra cuối](sla-draft-import-checks.json). Git có cảnh báo chuẩn hóa LF/CRLF; không coi cảnh báo này là lỗi đáp án hoặc backend. Worktree đã có thay đổi trước nhiệm vụ, nên diff với HEAD không phải riêng diff lần nhập này.

## Đối chiếu 16 nhánh còn thiếu

Số dòng theo thứ tự bảng thiếu ngày 06/10 trong [scenario coverage](../../docs/spec/scenario-coverage.md). “Draft” chỉ minh họa đáp án, không đóng nhánh verified/gate.

| Dòng | Nhánh | Ca draft / trạng thái còn mở |
|---:|---|---|
| 1 | Nhận ngoài giờ và snapshot | S1 / SLA-70; quyền nhận còn chờ API |
| 2 | Tạo Chủ nhật | S1 / SLA-70 |
| 3 | Resume Waiting sau giờ/cuối tuần | S2 / SLA-71 sau 17:00; resume ngay trong cuối tuần còn thiếu |
| 4 | Resume Waiting trước 08:00 | S3 / SLA-72 |
| 5 | Resume Waiting còn 0 trong giờ | S4 / SLA-73 tại đúng hạn; mốc sau hạn một giây không nằm trong ca này |
| 6 | Resume Waiting còn 0 ngoài giờ, phiên kế tiếp | S5 / SLA-74 với breach cũ; biến thể chưa từng breached và biến thể cuối tuần còn thiếu |
| 7 | Resume Waiting còn 0 trước 08:00 | S6 / SLA-75 |
| 8 | Giữ breached sau resume Waiting | S5 / SLA-74 |
| 9 | Từ chối còn 0 trước 08:00 | S7 / SLA-76 |
| 10 | G đang chạy còn 3600 | S8 / SLA-77 |
| 11 | G đang chạy còn 900 | S9 / SLA-78 |
| 12 | Từ chối lần 5 tạo review mới | S10 / SLA-79 |
| 13 | Manager hoàn tất review trong Waiting | S11 / SLA-80; M-07 draft, HTTP chưa chạy |
| 14 | Resolved bị chặn sau resume khi review mở | S12 / SLA-81 có expected refusal; checker/HTTP chưa chạy |
| 15 | Manager ghi phương án không có review mở | A1 API/workflow chưa chạy: 409 INVALID_TICKET_STATE |
| 16 | Manager ghi phương án khi Closed | A2 API/workflow chưa chạy: 409 TICKET_CLOSED; ưu tiên lỗi Closed |

14 dòng có minh họa draft, một số mới phủ một biến thể; **0 dòng được đóng bằng ca verified mới**. Hai dòng Manager là API/workflow riêng, không tự thêm thành fixture SLA. Gate SLA chính và M-07 vẫn chưa được xác nhận mở; workflow review không bị gate này chặn theo D-33.

## Tệp thay đổi trong nhiệm vụ

- `tests/sla/sla-scenarios.json`: chỉ nối 12 object mới; 69 object cũ giữ nguyên.
- `docs/spec/scenario-coverage.md`, `docs/decision-log.md`, `docs/open-questions.md`: ánh xạ draft, phạm vi nhập và giới hạn payload/checker; không đổi quy tắc.
- `README.md`, `TASKS.md`, `docs/traceability.md`, `tests/sla/reference/README.md`: phản ánh 69 verified + 12 draft, lệnh phù hợp và backlog API.
- `tests/sla/audit_draft_import.py`: audit cấu trúc/nguồn cho bản nhập, không tính SLA.
- Bằng chứng mới trong `tests/evidence/`: `sla-draft-import-baseline.json`, `sla-draft-import-structure.json`, `sla-draft-import-old-reference.json`, `sla-draft-import-source-comparison.json`, `sla-draft-import-run.json`, `sla-draft-import-checks.json` và `sla-draft-import.md`; giữ riêng báo cáo cũ.

Diff fixture riêng nhiệm vụ: nối 12 object, tăng 44061 byte; không tính những thay đổi đã có trước nhiệm vụ trong diff với HEAD.

Không stage, commit hoặc push. Không sửa business-rules.md/codes.md, checker gốc, audit cũ, dữ liệu nguồn hoặc tài liệu stories/FR/NFR; các thay đổi cũ ở worktree được giữ lại.
