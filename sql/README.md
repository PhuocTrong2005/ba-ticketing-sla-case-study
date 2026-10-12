# SQL báo cáo

Các query được backend/reports.py chạy thật trên bảng TEMP snapshot trong cùng kết nối SQLite. snapshot được dựng từ sự kiện đến as_of trước khi tổng hợp; không đọc trạng thái hôm nay như lịch sử. `{filters}` chỉ được thay bằng điều kiện cố định phía server với bind parameters; không nhận SQL từ client.

M-01/02/03: query files tương ứng; M-04/05 dùng snapshot trong reports.py; M-06 dùng m06.sql, tất cả ưu tiên. M-07 dựng lịch sử review và phần giao SLA bằng engine khoảng thời gian, không tuyên bố mọi phép tính này là SQL thuần.

Chạy API /reports/M-xx hoặc tests/backend/test_reports.py để kiểm tra. Các file này không chạy độc lập nếu chưa tạo bảng snapshot; không có database demo đã xuất đi kèm. Schema: backend/schema.sql. Seed: python -m backend.seed.
