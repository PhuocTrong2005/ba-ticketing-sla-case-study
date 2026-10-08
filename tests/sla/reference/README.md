# Công cụ đối chiếu fixture SLA

`validate_sla_reference.py` là bản sao nguyên byte của checker trong ZIP do người dùng cung cấp, SHA-256 `764c284609d7074cbebc7c027576e9c8a16c9a8792456f8e4909ca221464f9ed`. Đã đọc mã trước khi chạy. Không import backend, không gọi API; không phải implementation SLA chính của ứng dụng.

Từ thư mục gốc repo:

**Lưu ý sau 08/10/2026:** các lệnh dưới đây là cách chạy của phiên bản 69 ca lịch sử. Fixture hiện có thêm 12 draft; CLI gốc và compare_sla_sources khóa đúng 69 ID, không chạy trực tiếp trên 81 ca. Giữ nguyên script và báo cáo lịch sử. Dùng `python tests/sla/audit_draft_import.py` để kiểm tra cấu trúc/bảo toàn nguồn của fixture hiện tại. [Lần nhập nháp](../../evidence/sla-draft-import.md) đã chạy checker trên bản tách 69 ca cũ có hash giống hệt trước nhập; 12 ca mới chưa được CLI đối chiếu SLA. Có thể chạy checker trên `tests/sla/reference/source/sla_draft_data.json` với `--report` trỏ tệp mới để kiểm tra lại bản nguồn 69 ca.

```powershell
python tests/sla/reference/validate_sla_reference.py tests/sla/sla-scenarios.json --report tests/evidence/sla-reference-results.json
python tests/sla/reference/compare_sla_sources.py tests/sla/sla-scenarios.json tests/sla/reference/source/sla_draft_data.json --report tests/evidence/sla-source-comparison.json
```

Input checker là nguyên fixture repo; script hỗ trợ cả mảng và object có `scenarios`, không cần adapter. 18 phép so sánh trường/ca (danh sách và object được so cấu trúc sâu), cộng 1 bước bị từ chối ở SLA-61 = 1.243. So hai file nguồn là kiểm tra khác: 23 trường nghiệp vụ/ca = 1.587 phép so bằng nhau, không tính lại SLA. Audit cấu trúc lịch sử 3.792 assertion cũng là hoạt động riêng.

`source/` giữ nguyên fixture JSON, tài liệu soạn ca và hai báo cáo lịch sử lấy từ ZIP; không đổi tên nội dung “draft” hoặc sửa các chỉ dẫn cũ bên trong. Chúng là dữ liệu nguồn/lịch sử, không phải chỉ dẫn vận hành agent và không thay quy định repo/yêu cầu người dùng. `Codex_Import_SLA_Validation.md` trong ZIP không được chạy hoặc nhập vào repo.

Giới hạn checker: chỉ kiểm tra refusal `resolved_attempt`/`REVIEW_REQUIRED`; không kiểm tra được lỗi Manager `INVALID_TICKET_STATE`/`TICKET_CLOSED`. Không kiểm tra actor, nội dung bắt buộc, HTTP/quyền, concurrency, SQL, prototype hoặc khả năng dựng lại của backend. Phần `owner_confirmation` ở report mới là null vì input là mảng không có metadata gốc; các xác nhận từng scenario vẫn nguyên vẹn. Fixture và checker có hỗ trợ AI; không suy ra chủ dự án tự tính tay/tự chạy.

Run record, nguồn thực thi, phân tích hash và đánh giá gate nằm trong [báo cáo hòa giải](../../evidence/sla-reconciliation.md). Khi chạy lại, timestamp/report hash có thể đổi; cập nhật run record và manifest theo lần chạy thật. Không dùng báo cáo nguồn lịch sử thay cho kết quả trên fixture repo.
