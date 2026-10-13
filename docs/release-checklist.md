# Nghiệm thu portfolio v1.0

Hiện hành 13/10/2026. Giữ tiêu chí [TASKS](../TASKS.md)/[project brief](01-context/project-brief.md), không thêm feature/thay gate/bỏ tiêu chí để gán hoàn thành. [D-48](decision-log.md): chủ dự án chấp nhận Postman và cho phép xuất bản tài liệu. **Video Chưa có; portfolio v1.0 chưa hoàn tất; chưa tạo tag.**

“Có bằng chứng” áp dụng phạm vi mô tả. [Ma trận từng AC](ac-traceability.md) không tự gán tất cả AC PASS từ tổng suite.

| Tiêu chí gốc | Bằng chứng | Trạng thái / phần còn thiếu |
|---|---|---|
| Luồng chính trên prototype/API | [P 110/0](../tests/evidence/prototype-ux-20261013-002503.json), [N 191/514](../tests/evidence/newman-20261013-004259-750031-run.json), [Windows HTTP](../tests/evidence/step1-windows-20261012-162259-run.json) | Có bằng chứng workflow/Waiting/reject/review/Closed; prototype độc lập, không chứng minh tích hợp UI↔API. |
| Quyền ở backend | `test_roles_privacy_and_queue`, `test_review_errors_plan_and_waiting`: [181 case JUnit](../tests/evidence/step1-windows-20261012-162259-repo-junit.xml); PM-033/050…059/098…103/126/127 | Có bằng chứng role/ownership/privacy/error order nêu trong matrix; không auth production. |
| Verified đủ 12 nhóm/gate AGENTS/D-33 | [83 fixture](../tests/sla/sla-scenarios.json), [coverage](spec/scenario-coverage.md), [83 report](../tests/evidence/sla-verification-83.md); backend fixture tests | 83 verified/0 draft, nhóm 1…12 có mã; không sửa expected/review_status. Gate mở không là nghiệm thu sản phẩm. |
| Hai ca nhận đồng thời | `test_concurrent_two_agents_same_ticket`, `test_concurrent_one_agent_two_tickets_at_capacity_two`: [JUnit](../tests/evidence/step1-windows-20261012-162259-repo-junit.xml), [source](../tests/backend/test_integrity.py) | Có evidence threads/barrier/connection riêng/SQLite file, response và DB cuối; không Newman tuần tự. |
| Projection dựng lại từ events | `test_append_only_and_rebuild_all_projections`, raw/zero/event IDs/fault rollback: [integrity](../tests/backend/test_integrity.py), [JUnit](../tests/evidence/step1-windows-20261012-162259-repo-junit.xml) | Có evidence rebuild và lỗi được thử; AC-34 chưa dump mọi bảng cho mọi error branch; không production backup/recovery. |
| SQL khớp dữ liệu mẫu | Bốn ca [report tests](../tests/backend/test_reports.py), [JUnit](../tests/evidence/step1-windows-20261012-162259-repo-junit.xml), [SQL](../sql/README.md), PM-161…210 | Có evidence cohort/filter/as_of/zero/load/M07 theo dataset; M07 dùng engine giao khoảng, không SQL thuần. N chỉ bổ sung HTTP contract/counts. |
| README thử từ thư mục mới | [Windows clean-start](../tests/evidence/step1-windows-20261012-162259-report.md), [181 clean JUnit](../tests/evidence/step1-windows-20261012-162259-clean-junit.xml), [hướng dẫn hiện hành](backend-running.md) | **Một phần**: backend source/dependencies khớp manifest đã thử; README mới rà link/lệnh, chưa clean-start toàn bộ bằng checkout mới sau xuất bản. Giữ khoảng thiếu khi xét release cuối. |
| Giới hạn/mô phỏng trung thực | [README](../README.md), [API README](../api/README.md), [evidence index](../tests/evidence/README.md), [AC matrix](ac-traceability.md) | Đã ghi giả định/demo identity/UI không API/đơn vị đếm/local vs public smoke/race-fixture riêng và phần thiếu. |

## Hiện vật portfolio

| Hiện vật | Bằng chứng / trạng thái |
|---|---|
| BA/BPMN/rules/stories/data contract | Đã được duyệt; [điều hướng README](../README.md). Không phỏng vấn/số liệu doanh nghiệp thật. |
| Backend | 181 pytest đạt/0 lỗi; Windows JUnit/manifest khớp source, không chạy lại khi cập nhật docs. |
| Prototype local | 110 JS case đạt/0 lỗi; 83 fixture + controller/DOM/UX; chủ dự án chấp nhận UX/kết quả/ảnh tự động. |
| Pages | [Demo](https://phuoctrong2005.github.io/ba-ticketing-sla-case-study/), [74 smoke](../tests/evidence/pages-public-smoke-20261013-002741.json), [workflow runtime](https://github.com/PhuocTrong2005/ba-ticketing-sla-case-study/actions/runs/38327310064). Sáu nhóm chỉ smoke, không full local suite. |
| Postman | [Collection/environment](../api/README.md), Newman 191 request/514 assertion/0 lỗi/exit 0; chủ dự án chấp nhận D-48. Chưa Postman UI Runner, không khẳng định tự chạy mọi request. |
| Traceability/nghiệm thu | Đủ hàng AC-01…34, implementation/test/evidence/giới hạn rõ; không blanket PASS. |
| Video | **Chưa có — còn thiếu.** Không link/thumbnail giả, không làm trong nhiệm vụ. |
| Tag/release v1.0 | **Chưa tạo**, không công bố hoàn thành; xét lại sau video và bằng chứng tái lập còn thiếu. |

Cross-browser/thiết bị vật lý/performance/uptime chưa evidence; không tự thêm thành gate v1.0 hoặc đặt ngưỡng mới. Roadmap giữ ngoài v1.0. [Audit xuất bản](../tests/evidence/portfolio-publication-report-20261013.md) ghi bảo toàn/diff/hash/Git; trigger/deploy không là lần test mới.
