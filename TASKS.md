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
| SLA-01 | Chốt kịch bản verified tối thiểu và bảng quyết định SLA: nhóm 1 đến 11 mở khóa logic tính SLA chính; nhóm 12 mở khóa logic tính bối cảnh M-07; hoàn thành v1.0 cần đủ 12 nhóm. | `docs/spec/scenario-coverage.md` | Chờ kịch bản verified |
| DATA-01 | Thiết kế schema và dựng lại dữ liệu dẫn xuất từ sự kiện; lưu số giây còn lại tại mỗi lần Resolved để kiểm chứng quy tắc không quy lỗi Agent khi Customer từ chối lúc hết ngân sách. | SLA-01 | Chưa bắt đầu |
| DATA-02 | Thiết kế bảng `ticket_reviews`; lưu số giây còn lại tại mỗi lần Resolved nếu DATA-01 chưa bao phủ. | SLA-01 | Chưa bắt đầu |
| API-01 | Xác định hợp đồng API và kiểm tra phân quyền backend. | DOC-01, SLA-01 | Chưa bắt đầu |
| API-02 | Kiểm tra `REVIEW_REQUIRED`; Agent chuyển Waiting khi review mở; Manager ghi phương án ở Waiting; Manager/Agent/Customer ghi phương án (Customer 404, Agent 403); `INVALID_TICKET_STATE`/`TICKET_CLOSED` khi không có review mở; tính nguyên tử từ chối và tạo review. | DOC-01, SLA-01 | Chưa bắt đầu |
| PROTO-01 | Xây prototype tĩnh cho luồng chính. | DOC-01 | Chưa bắt đầu |
| CON-01 | Chứng minh hai ca nhận đồng thời. | DATA-01, API-01 | Chưa bắt đầu |
| RPT-01 | Báo cáo SQL khớp dữ liệu mẫu. | DATA-01 | Chưa bắt đầu |
| RPT-02 | Báo cáo M-07 về chờ Manager review. | DATA-02 | Chưa bắt đầu |
| EVD-01 | Thu thập bằng chứng kiểm thử hợp lệ và hoàn chỉnh ma trận truy vết. | Các hạng mục liên quan | Chưa bắt đầu |
