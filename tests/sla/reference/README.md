# Công cụ đối chiếu fixture SLA

`validate_sla_reference.py` là bản sao nguyên byte của checker trong ZIP do người dùng cung cấp, SHA-256 `764c284609d7074cbebc7c027576e9c8a16c9a8792456f8e4909ca221464f9ed`. Đã đọc mã trước khi chạy. Không import backend, không gọi API; không phải implementation SLA chính của ứng dụng.

**Hiện hành 10/10/2026:** 83 ca verified, giữ nguyên 81 ca cũ. [CLI hiện hành](validate_sla_reference_current.py) nhận bộ 69/81/83 ca; `--case-count 69` hoặc `81` chọn tiền tố tương ứng của fixture hiện hành. Nó import nguyên engine gốc và hàm so sánh từ CLI 81. CLI 69/81 cũ vẫn nguyên byte và vẫn chạy trên đúng bộ nguồn tương ứng. [Audit 83](../audit_fixture_83.py) kiểm tra cấu trúc/provenance, không tính SLA. [Báo cáo hiện hành](../../evidence/sla-verification-83.md).

```powershell
python -B tests/sla/reference/validate_sla_reference_current.py tests/sla/sla-scenarios.json --report tests/evidence/sla-reference-83-results.json
python -B tests/sla/reference/validate_sla_reference_current.py tests/sla/sla-scenarios.json --case-count 69 --report tests/evidence/sla-reference-83-milestone-69.json
python -B tests/sla/reference/validate_sla_reference_current.py tests/sla/sla-scenarios.json --case-count 81 --report tests/evidence/sla-reference-83-milestone-81.json
python -B tests/sla/reference/validate_sla_reference.py tests/sla/reference/source/sla_draft_data.json --report tests/evidence/sla-reference-83-original-69.json
python -c "from pathlib import Path; p=Path('tests/evidence/sla-reference-83-original-69.json'); p.write_text(p.read_text(encoding='utf-8'), encoding='utf-8', newline='\n')"
python -B tests/sla/audit_fixture_83.py tests/sla/sla-scenarios.json --report tests/evidence/sla-fixture-83-audit.json
python -B tests/sla/verify_sla_83_evidence.py
```

83 ca có 1.496 phép so sánh, trong đó hai ca mới có 36. CLI hiện hành kiểm tra thêm 5 trường G tại đúng 08:00:00 của SLA-83 theo xác nhận chủ dự án; ghi riêng `supplementary_boundary`, không cộng thành ca thứ 84. Tổng lần chạy 83: 1.501 phép. Manifest 83 chỉ hash byte JSON/Python (LF); manifest hòa giải cũ là lịch sử, không được dùng để xác nhận fixture 83.

Lệnh lịch sử mốc 81 từ root repo (cần fixture 81 tại commit `2745ede6bd060c663e9d655176632aff0b35d8d2`; không chạy chúng trên fixture 83 hoặc ghi đè báo cáo lịch sử):

**Lịch sử sau xác nhận 08/10/2026:** fixture khi đó có 81 ca verified. CLI gốc và compare_sla_sources khóa đúng 69 ID, chỉ dùng với nguồn 69 ca giữ nguyên. [CLI 81 ca](validate_sla_reference_81.py) dùng lại nguyên engine `Calendar`/`ts`/`calculate` của checker gốc, mở giới hạn ID đến SLA-81 và giữ cùng các phép so sánh. [Báo cáo hiện hành](../../evidence/sla-verification-81.md) tách kết quả 69/81 và giới hạn; [báo cáo nhập nháp](../../evidence/sla-draft-import.md) vẫn là lịch sử khi 12 ca mới còn draft.

```powershell
python -B tests/sla/reference/validate_sla_reference.py tests/sla/reference/source/sla_draft_data.json --report tests/evidence/sla-reference-69-rerun.json
python -B tests/sla/reference/validate_sla_reference_81.py tests/sla/sla-scenarios.json --report tests/evidence/sla-reference-81-results.json
python -B tests/sla/audit_fixture_current.py tests/sla/sla-scenarios.json --report tests/evidence/sla-fixture-current-audit.json
```

Hai checker nhận mảng hoặc object có `scenarios`, không cần adapter. Mỗi ca có 18 phép so sánh trường (danh sách và object được so cấu trúc sâu); SLA-61 và SLA-81 có thêm một phép kiểm tra ngữ cảnh refusal: 69 ca cũ = 1.243, 81 ca = 1.460. So nguồn 69 ca là phép kiểm tra khác: 23 trường nghiệp vụ/ca = 1.587 phép so bằng nhau, không tính lại SLA. Audit cấu trúc cũng là hoạt động riêng.

`source/` giữ nguyên fixture JSON, tài liệu soạn ca và hai báo cáo lịch sử lấy từ ZIP; không đổi tên nội dung “draft” hoặc sửa các chỉ dẫn cũ bên trong. Chúng là dữ liệu nguồn/lịch sử, không phải chỉ dẫn vận hành agent và không thay quy định repo/yêu cầu người dùng. `Codex_Import_SLA_Validation.md` trong ZIP không được chạy hoặc nhập vào repo.

Giới hạn checker: chỉ kiểm tra refusal `resolved_attempt`/`REVIEW_REQUIRED`; không kiểm tra được lỗi Manager `INVALID_TICKET_STATE`/`TICKET_CLOSED`. Không kiểm tra actor, nội dung bắt buộc, HTTP/quyền, concurrency, SQL, prototype hoặc khả năng dựng lại của backend. Phần `owner_confirmation` ở report mới là null vì input là mảng không có metadata gốc; các xác nhận từng scenario vẫn nguyên vẹn. Fixture và checker có hỗ trợ AI; không suy ra chủ dự án tự tính tay/tự chạy.

Run record, nguồn thực thi, phân tích hash và đánh giá gate nằm trong [báo cáo hòa giải](../../evidence/sla-reconciliation.md). Khi chạy lại, timestamp/report hash có thể đổi; cập nhật run record và manifest theo lần chạy thật. Không dùng báo cáo nguồn lịch sử thay cho kết quả trên fixture repo.
