# Đọc bằng chứng lưu trữ

File sla-reconciliation-before-reference.md là bản lưu nguyên byte từ vị trí cũ trước khi chuyển vào history. Tám liên kết tương đối bên trong vẫn theo vị trí ban đầu; không sửa file nguồn hoặc hash lịch sử. Dùng ánh xạ dưới đây để đọc các tài liệu được nhắc:

| Tên trong bản lưu | Liên kết đọc |
|---|---|
| sla-reconciliation-baseline.json | [baseline](../sla-reconciliation-baseline.json) |
| sla-fixture-audit-run.json | [audit run](../sla-fixture-audit-run.json) |
| sla-fixture-audit.json | [audit](../sla-fixture-audit.json) |
| audit_fixture_structure.py | [script](../../sla/audit_fixture_structure.py) |
| sla-reconciliation.sha256 | [manifest](../sla-reconciliation.sha256) |
| scenario-coverage.md | [coverage](../../../docs/spec/scenario-coverage.md) |
| open-questions.md | [questions](../../../docs/open-questions.md) |
| sla-reconciliation-checks.json | [checks](../sla-reconciliation-checks.json) |

Trạng thái backend hiện hành nằm tại [backend test report](../backend-test-report.md); không suy PASS backend từ các báo cáo tham chiếu cũ.
