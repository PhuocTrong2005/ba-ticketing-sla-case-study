# Ma trận AC → implementation → kiểm tra → bằng chứng

Hiện hành 13/10/2026, theo [stories/AC đã duyệt](03-requirements/user-stories-draft.md), BR/codes và D-48. Mỗi hàng ghi nhánh đã quan sát, không tự chứng nhận toàn bộ AC PASS từ tổng suite. Source/runs đối chiếu tại [audit xuất bản](../tests/evidence/portfolio-publication-report-20261013.md). Lịch sử planned giữ trong [traceability](traceability.md).

## Cách đọc nguồn

- **B**: [JUnit Windows 181 case][B], [manifest source/lệnh][BM]. Tên `test_*` dưới đây có trong JUnit; parametrized `test_fixture_through_http[SLA-01…83]` và `test_verified_fixture[SLA-01…83]` dùng 83 fixture gốc.
- **P**: [run JavaScript local 110/0][P], [harness][PT]. **G**: [74 Pages smoke check][G], [báo cáo phạm vi][GR]. P/G không chứng minh SQLite hoặc race.
- **N**: [Newman JSON 191 request/514 assertion][N], [JUnit 514 assertion][NJ], [run/collection hashes][NR]. Mã PM lấy từ [collection][NC]. N tuần tự không chứng minh race, rollback mọi bảng hoặc SLA biên.
- **Một phần**: còn giới hạn hoặc chưa có bằng chứng cho phần nêu rõ; không đổi yêu cầu để khớp test. Các hàng còn lại cũng chỉ chứng minh nhánh mô tả, không blanket PASS.

## Chức năng, quyền và vòng đời

| AC | Implementation | Test / request cụ thể | Evidence / kết luận giới hạn |
|---|---|---|---|
| AC-01 | [Store.create][S], [Create/POST tickets][A] | `test_validation_state_order_and_forbidden_fields`; `test_fixture_through_http[SLA-01…83]`; PM-020…031/130/154/157/230/231 | [B][B], [N][N]: High/Normal/New/policy/content; Python kiểm tra event_id trường dư. Không có negative HTTP riêng cho mọi tên trường hệ thống cấm. |
| AC-02 | [Store.action messages][S], [replay][SL] | `test_fixture_through_http[SLA-01…83]`; P `DEMO-02 waiting deadline + agent message/note`; PM-041/064/110a/116 | [B][B], [P][P], [N][N]: New message, Waiting→IP, Agent giữ Waiting. Không đổi đồng hồ kiểm tra bằng fixture/controller, không suy từ status đơn lẻ. |
| AC-03 | [Store.ticket/view][S] | `test_roles_privacy_and_queue`; `test_validation_state_order_and_forbidden_fields`; PM-033/126/155 | [B][B], [N][N]: other Customer GET/action 404 trước Closed/content; [G][G] smoke Customer 2. |
| AC-04 | [Store.action confirm/reject][S], [replay][SL] | `test_fixture_through_http[SLA-01…83]`; `test_review_errors_plan_and_waiting`; PM-070/075/080/085/090/095/117/118 | [B][B], [N][N], [P][P] `UI-03 DEMO-01 DOM successful workflow + literal input`, `UI-03 DEMO-03 DOM reject without reset`: confirm/reject/reason. |
| AC-05 | [Store.action Closed/state guards][S] | `test_validation_state_order_and_forbidden_fields`; PM-065/066/120/125/128/229 | [B][B], [N][N]: invalid state, Closed chặn thao tác, read sau lỗi vẫn Closed; không có route mở lại. |
| AC-06 | [queue endpoint][A], [Store.ticket][S] | `test_roles_privacy_and_queue`; PM-035/036/039/040 | [B][B], [N][N]: queue đúng 5 field, Agent không xem New chưa nhận. |
| AC-07 | [Store.action/append/refresh][S], [schema][SC] | `test_fixture_through_http[SLA-01…83]` snapshot lưu/prefix event; `test_concurrent_two_agents_same_ticket`; PM-043 | [B][B]: assignment snapshot/pending-breached và DB cuối; [N][N] chỉ contract/state. Chưa fault injection riêng mọi điểm transaction claim. |
| AC-10 | [Store.action claim/reject][S], [M06][R] | `test_customer_return_can_overload`; `test_m06_capacity_all_priorities_and_filter`; PM-130…153 | [B][B], [N][N], [P][P] `DEMO-05 overload then below limit`: tải <3/=3/>3 và return không chặn. |
| AC-11 | [Store.action claim guards][S] | `test_validation_state_order_and_forbidden_fields`; PM-145/146/147 | [B][B], [N][N]: Closed → assigned → capacity; Agent 4 tải 4 khi thử hai lỗi đầu. |
| AC-12 | [Store.ticket/action][S] | `test_roles_privacy_and_queue`; PM-050…053/127/156 | [B][B], [N][N]: GET/message/note/resolve Agent khác 403; list chỉ assigned. |
| AC-13 | [Store.ticket/action state][S] | `test_roles_privacy_and_queue`; `test_validation_state_order_and_forbidden_fields`; PM-036/072/122/127 | [B][B], [N][N]: New 403, Resolved INVALID_TICKET_STATE, Closed TICKET_CLOSED; Agent khác chặn trước state. |
| AC-14 | [Store.action waiting][S] | `test_validation_state_order_and_forbidden_fields`; `test_review_errors_plan_and_waiting`; PM-044/060/061/110/110d | [B][B], [N][N]: trước first reply bị chặn, sau reply được Waiting, kể cả review mở. |
| AC-15 | [Store.action resolve][S], [replay resolved][SL] | `test_validation_state_order_and_forbidden_fields`; `test_review_errors_plan_and_waiting`; PM-048/070/097/110c/117/132 | [B][B], [N][N]: content bắt buộc, Resolved kết thúc first response nếu cần, review chặn. |
| AC-16 | [Pydantic payload][A], [Store.text/guards][S] | `test_validation_state_order_and_forbidden_fields`; PM-020…030/045…049/050…052/073/074/104…109/220…233 | [B][B], [N][N]: handler priority/FastAPI structural exception 422; không khẳng định mọi tổ hợp input đã kiểm tra. |
| AC-23 | [replay review creation][SL], [Store transaction][S], [unique review index][SC] | `test_review_errors_plan_and_waiting`; `test_rejection_atomic_rollback_on_projection_failure`; PM-076/086/096 | [B][B]: reject 1/2 không review, 3/reject tiếp tạo review; trigger fault rollback mọi bảng. [N][N] threshold HTTP không là proof rollback. |
| AC-24 | [Store.action resolve/waiting][S], [replay messages][SL] | `test_review_errors_plan_and_waiting`; `test_fixture_through_http[SLA-81]`; PM-097/110/110a…d | [B][B], [N][N]: REVIEW_REQUIRED, Waiting, Customer resume giữ review và chặn Resolved. |
| AC-25 | [Complete/Plan][A], [Store.action complete][S] | `test_review_errors_plan_and_waiting`; PM-104…112/116/117 | [B][B], [N][N]: thiếu plan 422, complete ở Waiting giữ state/running/consumed, resume rồi được Resolved. |
| AC-26 | [Store.action complete guards][S] | `test_review_errors_plan_and_waiting`; PM-042/115 (A1), PM-119 (A2) | [B][B], [N][N]: INVALID_TICKET_STATE không review mở; TICKET_CLOSED ưu tiên Closed. |
| AC-27 | [Store.role/view][S], [reviews endpoint][A] | `test_roles_privacy_and_queue`; `test_review_errors_plan_and_waiting`; PM-038/054/055/098…103/113/114 | [B][B], [N][N]: Customer review 404, Agent endpoint/write 403, Agent đọc plan trên ticket; Manager không claim/message/Resolved. |
| AC-33 | [Store.action messages/notes/view][S] | `test_review_errors_plan_and_waiting`; `test_roles_privacy_and_queue`; PM-057/058/062/063 | [B][B], [N][N], [P][P] `UI-03 DEMO-02 DOM Waiting no resume by Agent`: Agent message/note giữ Waiting, Manager thấy note. |

## Đồng thời và dữ liệu nguyên tử

| AC | Implementation | Test cụ thể | Evidence / kết luận giới hạn |
|---|---|---|---|
| AC-08 | [Store.connect BEGIN IMMEDIATE/action claim][S], [schema][SC] | [integrity][IT] `test_concurrent_two_agents_same_ticket`: threads/barrier, hai TestClient/connection riêng, SQLite file | [B][B]: 200/409 TICKET_ALREADY_ASSIGNED, một assignment event/snapshot và một assignee. Không suy từ Newman hoặc JS một browser. |
| AC-09 | [Store transaction/load guard][S] | [integrity][IT] `test_concurrent_one_agent_two_tickets_at_capacity_two`: Agent tải 2, hai New, barrier | [B][B]: 200/409 AGENT_CAPACITY_REACHED, DB cuối tải 3/một New. Không benchmark production. |
| AC-34 | [Store.append/action transaction][S], [replay ordering][SL] | [integrity][IT] `test_rejection_atomic_rollback_on_projection_failure`, `test_zero_intervals_raw_clock_and_event_ids`; API fixture rejected attempts giữ event_count | [B][B]: rollback fault review mọi bảng, clock lùi giữ mọi bảng, same-second/event_id/raw/zero intervals. **Một phần:** chưa dump mọi projection cho mọi lỗi HTTP có thể xảy ra. |

## SLA và khả năng dựng lại

| AC | Implementation | Test cụ thể | Evidence / kết luận giới hạn |
|---|---|---|---|
| AC-17 | [SLA replay/calendar][SL], [policy/append][S] | [SLA tests][ST] `test_verified_fixture[SLA-01…83]`, `test_exact_close_and_weekend_calendar`, `test_timezone_wheel_fallback_without_system_iana_database`; integrity raw-clock test | [B][B], [coverage][CV]: lịch/policy/as_of/giây; không thay đáp án fixture. |
| AC-18 | [replay public reply/resolved][SL] | API fixture tests; `test_roles_privacy_and_queue`; P `DEMO-02 waiting deadline + agent message/note`; PM-041/057/060/132 | [B][B], [P][P], [N][N]: Customer/note không dừng first response; Agent first reply/Resolved kết thúc. |
| AC-19 | [replay resolution intervals][SL] | `test_verified_fixture[SLA-01…83]`, `test_fixture_through_http[SLA-01…83]`; P `DEMO-02 waiting deadline + agent message/note`, `DEMO-03 reject exact and +1 separate datasets` | [B][B], [P][P]: Resolved/Closed/Waiting/reject/ngân sách/intervals; N chỉ status/paused contract. |
| AC-20 | [replay/deadline/warning][SL] | 83 fixture engine/API; P `SLA-83 due exact + truncation + calendar`, `Warnings 3600/3599/900/899 and sticky Waiting`, `DEMO-06 exact/late Friday and zero` | [B][B], [P][P], [coverage][CV]: 0/deadline/+1/sticky/truncation. Không dùng Newman clock ngắn làm proof SLA biên. |
| AC-21 | [SLA warning][SL], [Store.view][S], [prototype ticket][UI] | `test_verified_fixture[SLA-40]`; `test_roles_privacy_and_queue`; P warnings/sticky + `UX-04 real data handoff details`; PM-059/114/229 | [B][B], [P][P]: sticky Waiting; [N][N], [G][G]: Customer không SLA/note/review. Public smoke không phủ sticky. |
| AC-22 | [Store.refresh/project][S], [append-only triggers][SC] | [integrity][IT] `test_append_only_and_rebuild_all_projections`; API fixture intervals/snapshots từ prefix events | [B][B]: sửa event/policy bị chặn, hỏng projection rồi rebuild đúng; không proof production recovery/backup. |

## Báo cáo và UI

| AC | Implementation | Test / request cụ thể | Evidence / kết luận giới hạn |
|---|---|---|---|
| AC-28 | [reports M01 snapshot][R], [m01](../sql/queries/m01.sql) | [report tests][RT] `test_ratio_cohort_pending_zero_and_unclosed_snapshot`; PM-011/161/171/181/191/194 | [B][B]: cohort/pending/ratio/as_of; [N][N]: contract/counts/filter/zero/quyền, không suy mọi SQL từ N. |
| AC-29 | [reports M02/M03][R], [m02](../sql/queries/m02.sql)/[m03](../sql/queries/m03.sql) | `test_ratio_cohort_pending_zero_and_unclosed_snapshot`; PM-012/013/162/163/192/193/195; P reports period/filter case | [B][B], [P][P]: Closed kỳ và N không giới hạn created_at; [N][N]: 1 Closed/7 unclosed/filter. |
| AC-30 | [reports M04/M05/M06][R], [m06](../sql/queries/m06.sql), [Manager UI][UI] | `test_m04_m05_and_historical_states`, `test_m06_capacity_all_priorities_and_filter`; PM-164…166/196/198/204; P `UI-05 actual ratio/filter/capacity reports and navigation guard` | [B][B]: breach/Resolved giờ lịch/overload/historical; [N][N] M04 có thể rỗng, không proof breach. Không xếp hạng. |
| AC-31 | [replay review overlap/context][SL], [reports M07][R], [Manager UI][UI] | `test_m07_excludes_future_review_completion_and_overlap`; 83 fixture nhóm 12; P `DEMO-04 review block, plan Waiting, resume`; PM-111/167/197/210 | [B][B], [P][P]: as_of/future completion/overlap/context; [N][N] open/completed contract, không mọi context. M07 không SQL thuần. |
| AC-32 | [prototype app][UI], [styles](../prototype/styles.css), [guidance](../prototype/guidance.js) | P `UI-06 reload/storage/reset/schema and list seconds`, `UX-01 collapse preserves source and summary across renders`, `UX-03 localized sticky SLA and Manager labels/navigation preserve filters`, `UX-04 real data handoff details`; keyboard/mobile run | [P][P], [UX report](../tests/evidence/prototype-ux-report-20261013.md): labels/detail vs list, controls/nav/ảnh; [G][G] smoke. **Một phần:** chưa cross-browser/thiết bị vật lý/test âm thanh độc lập; code tĩnh không có hiệu ứng đó. |

## Tái lập và nghiệm thu ngoài AC

NFR-03…05: [integrity][IT], fixture/clock inject/manifest Windows. README/clean-start: [Windows report](../tests/evidence/step1-windows-20261012-162259-report.md), 181 case source copy mới; Postman DB mới được [run helper](../tests/postman/run_newman.py) tạo trước import. NFR-06: P/G và chủ dự án chấp nhận UX. NFR-07 performance/uptime chưa có tiêu chí/evidence; không thêm ngưỡng.

[Clean-start từ clone mới tại `7c35b2c`](../tests/evidence/portfolio-clean-start-report-20261013.md) có evidence install/check/181 pytest/HTTP backend/110 JS/static smoke/Newman 191–514; [lần clone thứ hai](../tests/evidence/portfolio-clean-start-repeat-20261013.md) tái hiện kết quả. DOC-CS-01 là lỗi hướng dẫn auditor lịch sử tại commit cũ, bản sửa docs đã thử riêng; không gán toàn bộ hướng dẫn commit cũ PASS hoặc suy ra đã chạy trọn suite từ commit mới. Video **Chưa có**, thuộc roadmap D-51; [release checklist](release-checklist.md) giữ tiêu chí nghiệp vụ/kỹ thuật và giới hạn.

[S]: ../backend/store.py
[A]: ../backend/app.py
[SL]: ../backend/sla.py
[SC]: ../backend/schema.sql
[R]: ../backend/reports.py
[UI]: ../prototype/app.js
[IT]: ../tests/backend/test_integrity.py
[RT]: ../tests/backend/test_reports.py
[ST]: ../tests/backend/test_sla.py
[PT]: ../tests/prototype/test.js
[B]: ../tests/evidence/step1-windows-20261012-162259-repo-junit.xml
[BM]: ../tests/evidence/step1-windows-20261012-162259-run.json
[P]: ../tests/evidence/prototype-ux-20261013-002503.json
[G]: ../tests/evidence/pages-public-smoke-20261013-002741.json
[GR]: ../tests/evidence/pages-report-20261013.md
[N]: ../tests/evidence/newman-20261013-004259-750031.json
[NJ]: ../tests/evidence/newman-20261013-004259-750031.xml
[NR]: ../tests/evidence/newman-20261013-004259-750031-run.json
[NC]: ../api/ticketing-sla.postman_collection.json
[CV]: spec/scenario-coverage.md
