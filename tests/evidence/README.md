# Chỉ mục bằng chứng

Các file là lịch sử thực thi; không ghi đè audit chưa đạt hoặc sửa record để thành PASS. Chủ dự án phê duyệt yêu cầu/kịch bản và chấp nhận kết quả tự động; công cụ do Codex chạy. Không suy thành kiểm thử doanh nghiệp thật hoặc toàn bộ AC đã PASS.

| Phạm vi | Nguồn và cách đọc |
|---|---|
| Backend/Windows hiện hành | [Báo cáo môi trường](step1-windows-20261012-162259-report.md), [manifest/lệnh](step1-windows-20261012-162259-run.json), [181 case repo JUnit](step1-windows-20261012-162259-repo-junit.xml), [181 case clean-start JUnit](step1-windows-20261012-162259-clean-junit.xml). Source backend/test/SQL/dependencies khớp manifest Windows; không cộng hai lần. |
| Backend ban đầu | [Report](backend-test-report.md), [run/hashes](backend-run.json), [JUnit](backend-junit.xml), [clean-start](backend-clean-start.json). Giới hạn Windows/prototype chưa làm ở report này là lịch sử, được thay bằng evidence sau. |
| Prototype local hiện hành | [Run 110/0](prototype-ux-20261013-002503.json), [UX và ảnh](prototype-ux-report-20261013.md), [Pages report](pages-report-20261013.md). Runtime + harness test khớp run cuối; `audit_pages.py` thay đổi sau run nhưng không đổi runtime/harness. |
| Pages thực | [74 smoke check/10 ảnh](pages-public-smoke-20261013-002741.json), [deployment metadata](pages-deployment-20261013-002812.json), [báo cáo](pages-report-20261013.md). Sáu nhóm chỉ smoke, DEMO-01 full workflow; không là 110 test local trên site. |
| Newman hiện hành | [191 request/514 assertion JSON](newman-20261013-004259-750031.json), [514 assertion JUnit](newman-20261013-004259-750031.xml), [lệnh/hashes/exit 0](newman-20261013-004259-750031-run.json), [báo cáo](postman-report-20261013.md). Một iteration; JUnit đếm assertion, không đếm request. |
| Newman trước mở rộng coverage | [Run đầu 183/491](newman-20261013-004148-848348-run.json). Khác hash collection hiện hành; chỉ là lịch sử, không cộng hai lần. |
| Audit chưa đạt | [Postman false-positive URL](postman-audit-20261013-004813-573406.json), [Pages CRLF](pages-audit-20261013-002555.json). Lỗi auditor/chuẩn bị Git, không gán thành bug backend; record giữ nguyên. [Audit Postman đã sửa](postman-audit-20261013-004951-140523.json). |
| 83 fixture verified | [Đối chiếu 83](sla-verification-83.md), [coverage](../../docs/spec/scenario-coverage.md), [fixture gốc](../sla/sla-scenarios.json). Fixture được tái sử dụng giữa các suite. |
| Lịch sử 69/81 và hash | [Reconciliation](sla-reconciliation.md), [source comparison](sla-source-comparison.json), [manifest](sla-reconciliation.sha256), [81 ca](sla-verification-81.md), [import draft](sla-draft-import.md), [checker](../sla/reference/README.md), [chỉ mục lịch sử](history/README.md). Không xóa hoặc sửa nguồn lịch sử. |

Traceability: [ma trận từng AC](../../docs/ac-traceability.md); nghiệm thu: [release checklist](../../docs/release-checklist.md). Hash chi tiết giữ trong từng record. Pytest, JavaScript, smoke và Newman có đơn vị khác nhau; không cộng thành một số tình huống độc lập.
