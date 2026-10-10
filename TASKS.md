# Backlog v1.0

## Tiêu chí hoàn thành v1.0

- Luồng chính chạy được trên prototype và API tương ứng.
- Quyền được kiểm tra ở backend.
- Có ca `verified` bao phủ đủ 12 nhóm; nhóm 1 đến 11 mở khóa logic tính SLA chính, nhóm 12 mở khóa logic tính bối cảnh M-07.
- Hai ca nhận đồng thời đạt.
- Dữ liệu dẫn xuất dựng lại đúng từ sự kiện gốc.
- Báo cáo SQL khớp dữ liệu mẫu.
- README đã được thử thực tế từ thư mục mới.
- Giới hạn và phần mô phỏng được nêu trung thực.

## Backlog khung

| Mã | Hạng mục | Phụ thuộc | Trạng thái |
|---|---|---|---|
| DOC-01 | Hoàn thiện yêu cầu, traceability và decision log. | Quyết định chủ dự án | Đang có khung |
| SLA-01 | 83 fixture verified; giữ nguyên 81 ca cũ. Checker 83 PASS / 0 FAIL, 1.496 so sánh; thêm 5 phép biên SLA-83 tại 08:00:00 đạt. Mốc 69/81 lần lượt 1.243/1.460 phép, đều PASS. [Báo cáo hiện hành](tests/evidence/sla-verification-83.md). | `docs/spec/scenario-coverage.md`, D-33/D-39/D-40 | Gate SLA chính mở; gate tính M-07 đủ điều kiện viết logic; chưa triển khai code |
| DATA-01 | Thiết kế schema và dựng lại dữ liệu dẫn xuất từ sự kiện; lưu số giây còn lại tại mỗi lần Resolved để kiểm chứng quy tắc không quy lỗi Agent khi Customer từ chối lúc hết ngân sách. | SLA-01 | Chưa bắt đầu |
| DATA-02 | Thiết kế bảng `ticket_reviews`; lưu số giây còn lại tại mỗi lần Resolved nếu DATA-01 chưa bao phủ. | SLA-01 | Chưa bắt đầu |
| API-01 | Xác định hợp đồng API và kiểm tra phân quyền backend. | DOC-01, SLA-01 | Chưa bắt đầu |
| API-02 | Kiểm tra `REVIEW_REQUIRED`; Agent chuyển Waiting khi review mở; Manager ghi phương án ở Waiting; Manager/Agent/Customer ghi phương án (Customer 404, Agent 403); `INVALID_TICKET_STATE`/`TICKET_CLOSED` khi không có review mở; tính nguyên tử từ chối và tạo review. | DOC-01, SLA-01 | Chưa bắt đầu |
| PROTO-01 | Xây prototype tĩnh cho luồng chính. | DOC-01 | Chưa bắt đầu |
| CON-01 | Chứng minh hai ca nhận đồng thời. | DATA-01, API-01 | Chưa bắt đầu |
| RPT-01 | Báo cáo SQL khớp dữ liệu mẫu. | DATA-01 | Chưa bắt đầu |
| RPT-02 | Báo cáo M-07 về chờ Manager review. | DATA-02 | Chưa bắt đầu |
| EVD-01 | Thu thập bằng chứng kiểm thử hợp lệ và hoàn chỉnh ma trận truy vết. | Các hạng mục liên quan | Chưa bắt đầu |

## Bổ sung sau nhập S1–S12 — 08/10/2026 (lịch sử lúc còn draft)

- SLA-01: đã nhập SLA-70…SLA-81, **12 draft**, giữ nguyên 69 verified. [Báo cáo nhập](tests/evidence/sla-draft-import.md) có ánh xạ và kiểm tra cấu trúc; checker CLI gốc không nhận bộ 81 ca. Chưa đối chiếu SLA cho 12 draft, chưa mở gate SLA chính/M-07. Chờ review theo D-33; xác nhận con số không tự đổi review_status.
- Coverage còn mở: draft chưa là bằng chứng verified; resume Waiting ngay trong cuối tuần; resume ngoài giờ với 0 giây nhưng chưa từng breached (S5 chỉ có breach cũ). S4 không đánh giá mốc sau hạn một giây. Không tự bổ sung expected_* ngoài 12 ca được yêu cầu.
- API-01/API-02: chờ contract payload cho kết quả công khai, lý do từ chối và handling_plan; fixture toán học không lưu actor/nội dung. Khi chuyển S7/S10–S12 sang API test phải có nội dung hợp lệ cho mọi bước tương ứng.
- API-02 / A1: Manager ghi phương án khi không có review mở → 409 `INVALID_TICKET_STATE`; **chưa chạy**.
- API-02 / A2: Manager ghi phương án khi ticket Closed → 409 `TICKET_CLOSED`, kiểm tra ưu tiên lỗi Closed; **chưa chạy**.
- API-02 / S12 (SLA-81): thử Resolved sau resume Waiting khi R1 mở → HTTP 409 `REVIEW_REQUIRED`; không ghi ticket_event/không đổi interval; **chưa chạy HTTP thật**. A1/A2 không tính vào đối chiếu SLA.

## Sau xác nhận và đối chiếu 81 ca — 08/10/2026

- SLA-01: 81/81 ca `verified`, 0 draft. 69 ca cũ giữ nguyên nội dung; 12 ca mới giữ nguyên đầu vào/đáp án, `verified_at=null` vì không có giờ xác nhận chính xác. Codex chạy checker 81 ca đạt 81 PASS / 0 FAIL, 1.460 phép so sánh, trong đó 12 ca mới có 217. Checker gốc 69 ca giữ nguyên và chạy lại đạt 69 PASS / 0 FAIL, 1.243 phép so sánh. Audit cấu trúc hiện hành 81/81 PASS. Đây là đối chiếu fixture, chưa phải test backend/API. [Báo cáo](tests/evidence/sla-verification-81.md).
- Gate logic SLA chính: **chưa mở**. Cần ca verified riêng cho Customer resume Waiting ngay trong cuối tuần và cho resume Waiting ngoài giờ với 0 giây còn lại nhưng chưa từng breached; rà thêm mốc sau deadline một giây cho đúng đường Waiting còn 0 theo tiêu chí nhánh biên. Không tự tạo SLA-82 trở đi.
- Gate tính bối cảnh M-07: **đủ điều kiện mở cho việc viết logic** theo D-33; nhánh chờ Manager trong Waiting, R3/lần từ chối 5, overlap/breach/open/closed review đã có ca verified và khớp checker. Chưa viết hoặc kiểm tra implementation.
- API-01/API-02: A1/A2 và HTTP `REVIEW_REQUIRED` của SLA-81, nội dung bắt buộc/quyền/atomicity vẫn chờ contract và API test. Không cộng các bước này vào PASS SLA/M-07.

## Sau SLA-82/SLA-83 — 10/10/2026

**Gate logic SLA chính: mở cho việc viết logic theo AGENTS/D-33.** Nhóm 1–11 đều có ca verified và bảng nhóm → mã không còn nhóm trống. SLA-82 đóng nhánh Customer resume ngay cuối tuần; SLA-83 đóng nhánh resume ngoài giờ với 0 giây nhưng chưa từng breached và mốc sau hạn 08:00:01. Đối chiếu phụ cùng events tại 08:00:00 xác nhận pending/due; không thêm ca hoặc tự xác nhận đáp án. Các nhánh còn lại đã được đối soát ở mốc 81; không còn blocker coverage cho logic SLA chính. Không đổi tiêu chí gate. Gate tính M-07 tiếp tục đủ điều kiện viết logic theo đánh giá mốc 81. API A1/A2, HTTP REVIEW_REQUIRED, payload/quyền/atomicity và các tiêu chí hoàn thành v1.0 vẫn chưa kiểm thử; đây không phải blocker mới cho gate phép tính và không phải xác nhận hoàn thành backend.

Các ghi chú 08/10 phía trên giữ nguyên như lịch sử; yêu cầu hiện tại cho phép nhập đúng SLA-82/SLA-83 verified và thay kết luận gate cũ. Không tự thêm ca ngoài hai ca đã được xác nhận.
