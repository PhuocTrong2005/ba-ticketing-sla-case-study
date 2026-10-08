# Open questions

## Đang mở

Không có câu hỏi quyết định nghiệp vụ mới. OQ-20/OQ-21 vẫn đã đóng.

### Giới hạn nhập nháp S1–S12 — 08/10/2026

- Không thấy mâu thuẫn đáp án với quy tắc đã chốt; SLA-61 và checker cùng dùng `expected_rejected_actions`. S11 giữ Waiting khi review hoàn tất, phù hợp BR-08/57.
- Thiếu contract tên trường payload cho kết quả công khai/lý do từ chối/phương án nội bộ. Fixture toán học hiện không lưu nội dung hay actor. Nhập phần toán học độc lập; dừng phần ánh xạ payload và kiểm tra nội dung/quyền/HTTP của S7/S10–S12 đến khi có contract. Không tự thêm field hoặc actor. API-01/API-02 theo dõi phần này; không mở lại quy tắc nội dung bắt buộc BR-08/11/55.
- Checker gốc chỉ nhận đúng 69 ID; audit cũ chỉ nhận verified. Bộ 12 draft có kiểm tra cấu trúc riêng, chưa có kết quả đối chiếu SLA từ CLI gốc. Không thay checker để tự xác nhận đáp án.
- Coverage draft và các biến thể còn mở ghi tại [bảng nhập S1–S12](spec/scenario-coverage.md#nhập-s1s12-ngày-08102026--draft-chưa-mở-gate). A1/A2 và HTTP REVIEW_REQUIRED chờ API test. Hai gate vẫn chưa được xác nhận mở.

### Blocker bằng chứng của việc 1 — 06/10/2026 (không cấp lại mã OQ)

- Đã xử lý blocker nguồn: ZIP đọc được tại `D:\Download\SLA_Verification_Package.zip` do người dùng đính kèm; đường dẫn ZIP trong repo vẫn chưa tồn tại. Checker gốc đã lưu và chạy: 69 PASS / 0 FAIL, 1.243 so sánh, exit code 0. Không cần cung cấp lại ZIP.
- Đã giải thích hash: nguồn là object `metadata` + `scenarios`, repo là mảng scenario với định dạng khác; toàn bộ 69 scenario, gồm nghiệp vụ và metadata từng ca, khớp cấu trúc. Hash fixture/script lịch sử khớp byte trong ZIP. Không còn blocker khác biệt đáp án hoặc nguồn hash.
- Bảng nhóm có đủ mã verified nhưng chưa đủ nhánh theo bảng yêu cầu → ca hiện có → phần thiếu tại [scenario coverage](spec/scenario-coverage.md#đối-soát-việc-1--06102026). Cần ca được chủ dự án xác nhận cho các nhánh còn thiếu; việc này không tự tạo ca, sửa đáp án verified hoặc thay tiêu chí gate. Đã sửa nhận định cũ về vào Waiting ngoài giờ: SLA-40 đã phủ nhánh đó.
- Checker hiện chỉ kiểm tra thao tác bị từ chối `resolved_attempt`/`REVIEW_REQUIRED`, chưa kiểm tra được `INVALID_TICKET_STATE`/`TICKET_CLOSED` cho Manager hoặc quyền/API thật; không ghi các phần này là PASS.

Ghi chú lịch sử: file mang tên `Codex_Task_1_Reconcile_SLA.md` chưa được tìm thấy; nhiệm vụ thực hiện theo nội dung người dùng đã đính kèm và yêu cầu tiếp tục mới nhất, không chạy prompt nhập liệu bên trong ZIP. Đây không phải yêu cầu xác nhận lại quyết định nghiệp vụ.

Chi tiết, kết quả kiểm tra thực tế và phạm vi tìm tệp: [báo cáo hòa giải](../tests/evidence/sla-reconciliation.md).

## Đã đóng

| OQ | Kết quả / ánh xạ |
|---|---|
| OQ-01 | BR-43, D-19 |
| OQ-02 | BR-44, D-19 |
| OQ-03 | BR-47, D-16 |
| OQ-04 | [scenario-coverage.md](spec/scenario-coverage.md) |
| OQ-05 | [scenario-coverage.md](spec/scenario-coverage.md), nhóm 4 |
| OQ-07 | D-17, BR-35 |
| OQ-08 | [scenario-coverage.md](spec/scenario-coverage.md) |
| OQ-10 | BR-45, D-19 |
| OQ-11 | BR-46, D-20 |
| OQ-12 | BR-39, D-18 |
| OQ-13 | BR-48, D-21 |
| OQ-14 | BR-49, D-22 |
| OQ-15 | BR-50, BR-51, D-23, D-24 |
| OQ-16 | BR-49, D-22 |
| OQ-17 | BR-57, D-31 |
| OQ-18 | BR-58, D-32 |
| OQ-19 | BR-59, D-38 |
| OQ-20 | BR-60, D-39 |
| OQ-21 | BR-61, D-39 |
