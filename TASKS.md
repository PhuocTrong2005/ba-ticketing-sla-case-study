# Backlog v1.0

## Tiêu chí hoàn thành v1.0

- Luồng chính chạy được trên prototype và API tương ứng.
- Quyền được kiểm tra ở backend.
- SLA có các ca verified.
- Hai ca nhận đồng thời đạt.
- Dữ liệu dẫn xuất dựng lại đúng từ sự kiện gốc.
- Báo cáo SQL khớp dữ liệu mẫu.
- README đã được thử thực tế từ thư mục mới.
- Giới hạn và phần mô phỏng được nêu trung thực.

## Backlog khung

| Mã | Hạng mục | Phụ thuộc | Trạng thái |
|---|---|---|---|
| DOC-01 | Hoàn thiện yêu cầu, traceability và decision log. | Quyết định chủ dự án | Đang có khung |
| SLA-01 | Chốt kịch bản verified tối thiểu và bảng quyết định SLA. | `docs/spec/scenario-coverage.md` | Chờ kịch bản verified |
| DATA-01 | Thiết kế schema và dựng lại dữ liệu dẫn xuất từ sự kiện; lưu số giây còn lại tại mỗi lần Resolved để kiểm chứng quy tắc không quy lỗi Agent khi Customer từ chối lúc hết ngân sách. | SLA-01 | Chưa bắt đầu |
| API-01 | Xác định hợp đồng API và kiểm tra phân quyền backend. | DOC-01, SLA-01 | Chưa bắt đầu |
| PROTO-01 | Xây prototype tĩnh cho luồng chính. | DOC-01 | Chưa bắt đầu |
| CON-01 | Chứng minh hai ca nhận đồng thời. | DATA-01, API-01 | Chưa bắt đầu |
| RPT-01 | Báo cáo SQL khớp dữ liệu mẫu. | DATA-01 | Chưa bắt đầu |
| EVD-01 | Thu thập bằng chứng kiểm thử hợp lệ và hoàn chỉnh ma trận truy vết. | Các hạng mục liên quan | Chưa bắt đầu |
