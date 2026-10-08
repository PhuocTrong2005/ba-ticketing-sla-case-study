# Công cụ đối chiếu fixture SLA

`validate_sla_reference.py` là bản sao nguyên byte của checker trong ZIP do người dùng cung cấp, SHA-256 `764c284609d7074cbebc7c027576e9c8a16c9a8792456f8e4909ca221464f9ed`. Đã đọc mã trước khi chạy. Không import backend, không gọi API; không phải implementation SLA chính của ứng dụng.

Từ thư mục gốc repo:

**Trạng thái sau xác nhận 08/10/2026:** fixture hiện có 81 ca verified. CLI gốc và compare_sla_sources khóa đúng 69 ID, chỉ dùng với nguồn 69 ca giữ nguyên. [CLI 81 ca](validate_sla_reference_81.py) dùng lại nguyên engine `Calendar`/`ts`/`calculate` của checker gốc, mở giới hạn ID đến SLA-81 và giữ cùng các phép so sánh. [Báo cáo hiện hành](../../evidence/sla-verification-81.md) tách kết quả 69/81 và giới hạn; [báo cáo nhập nháp](../../evidence/sla-draft-import.md) vẫn là lịch sử khi 12 ca mới còn draft.

```powershell
python -B tests/sla/reference/validate_sla_reference.py tests/sla/reference/source/sla_draft_data.json --report tests/evidence/sla-reference-69-rerun.json
python -B tests/sla/reference/validate_sla_reference_81.py tests/sla/sla-scenarios.json --report tests/evidence/sla-reference-81-results.json
python -B tests/sla/audit_fixture_current.py tests/sla/sla-scenarios.json --report tests/evidence/sla-fixture-current-audit.json
```

Hai checker nhận mảng hoặc object có `scenarios`, không cần adapter. Mỗi ca có 18 phép so sánh trường (danh sách và object được so cấu trúc sâu); SLA-61 và SLA-81 có thêm một phép kiểm tra ngữ cảnh refusal: 69 ca cũ = 1.243, 81 ca = 1.460. So nguồn 69 ca là phép kiểm tra khác: 23 trường nghiệp vụ/ca = 1.587 phép so bằng nhau, không tính lại SLA. Audit cấu trúc cũng là hoạt động riêng.

`source/` giữ nguyên fixture JSON, tài liệu soạn ca và hai báo cáo lịch sử lấy từ ZIP; không đổi tên nội dung “draft” hoặc sửa các chỉ dẫn cũ bên trong. Chúng là dữ liệu nguồn/lịch sử, không phải chỉ dẫn vận hành agent và không thay quy định repo/yêu cầu người dùng. `Codex_Import_SLA_Validation.md` trong ZIP không được chạy hoặc nhập vào repo.

Giới hạn checker: chỉ kiểm tra refusal `resolved_attempt`/`REVIEW_REQUIRED`; không kiểm tra được lỗi Manager `INVALID_TICKET_STATE`/`TICKET_CLOSED`. Không kiểm tra actor, nội dung bắt buộc, HTTP/quyền, concurrency, SQL, prototype hoặc khả năng dựng lại của backend. Phần `owner_confirmation` ở report mới là null vì input là mảng không có metadata gốc; các xác nhận từng scenario vẫn nguyên vẹn. Fixture và checker có hỗ trợ AI; không suy ra chủ dự án tự tính tay/tự chạy.

Run record, nguồn thực thi, phân tích hash và đánh giá gate nằm trong [báo cáo hòa giải](../../evidence/sla-reconciliation.md). Khi chạy lại, timestamp/report hash có thể đổi; cập nhật run record và manifest theo lần chạy thật. Không dùng báo cáo nguồn lịch sử thay cho kết quả trên fixture repo.
