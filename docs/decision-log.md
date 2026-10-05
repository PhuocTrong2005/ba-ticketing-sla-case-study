# Decision log

| Mã | Quyết định | Phương án đã bỏ | Lý do / nguồn | Trạng thái |
|---|---|---|---|---|
| D-01 | Customer từ chối thì SLA giải quyết tiếp tục với ngân sách còn lại. | Nhân đôi thời gian còn lại; reset toàn bộ SLA. | Cố vấn, chưa xác nhận: nhân đôi có thể thưởng cho giải quyết vội và cần quy tắc trần; reset dễ bị lách SLA. Phương án nhân đôi từng được đề xuất rồi rút lại. | Đã chốt |
| D-02 | Lịch Thứ Hai–Thứ Sáu 08:00–17:00, Asia/Ho_Chi_Minh; 08:00 trong giờ, 17:00 ngoài giờ; không nghỉ trưa; chưa xử lý ngày lễ, ngày lễ trong tuần tính như ngày thường. | Chưa ghi nhận. | Chưa ghi nhận. | Đã chốt |
| D-03 | High 3.600/28.800 và Normal 7.200/57.600 giây làm việc. | Chưa ghi nhận. | Ngân sách quy đổi sang giây, không đổi chính sách. | Đã chốt |
| D-04 | Dùng năm trạng thái, tách Resolved và Closed. | Gộp một trạng thái. | Chủ dự án: muốn Customer có bước phản hồi/xác nhận kết quả. | Đã chốt |
| D-05 | Không tự đóng ticket. | Chưa ghi nhận. | Chưa ghi nhận. | Đã chốt |
| D-06 | Giới hạn 3 ticket In Progress; ticket quay lại In Progress không bị chặn. | Chưa ghi nhận. | Chưa ghi nhận. | Đã chốt |
| D-07 | Phân quyền như baseline; Manager xem ghi chú nội bộ; dùng bộ mã lỗi đã định. | Chưa ghi nhận. | Chưa ghi nhận. | Đã chốt |
| D-08 | Backend FastAPI + SQLite; prototype tách riêng và không gọi API. | Chưa ghi nhận. | Chưa ghi nhận. | Đã chốt |
| D-09 | Tách dữ liệu gốc là sự kiện và dữ liệu dẫn xuất là khoảng chạy/giây/deadline. | Chưa ghi nhận. | Chưa ghi nhận. | Đã chốt |
| D-10 | Tính theo phút; cắt giây về 00; chấp nhận lệch dưới một phút có lợi cho Agent. | Tính đến giây; làm tròn. | Chủ dự án (diễn đạt lại): chênh lệch trong khoảng một phút không thể hiện chất lượng hỗ trợ, và cắt giây giúp xử lý đơn giản hơn. | Bị thay thế bởi D-16 |
| D-11 | Customer nhận 404 để che sự tồn tại; Agent nhận 403 theo phân quyền; hàng đợi New chỉ hiển thị trường tóm tắt. | Chưa ghi nhận. | Chưa ghi nhận. | Đã chốt |
| D-12 | Chốt M-01…M-06, công thức cơ bản và tách pending khỏi mẫu số M-01. | Chưa ghi nhận. | M-04 đã chốt (xem D-13); cách chọn dữ liệu theo kỳ xem D-17. | Đã chốt |
| D-13 | M-04 là một danh sách với hai cột cờ theo từng đồng hồ. | Tách M-04a/M-04b. | Chưa ghi nhận lý do của chủ dự án; cố vấn, chưa xác nhận: gọn hơn mà vẫn lọc được theo từng đồng hồ. | Đã chốt |
| D-14 | Nhận ticket là ngoại lệ của kiểm tra người phụ trách; ticket đã có người nhận trả 409 `TICKET_ALREADY_ASSIGNED`. | Để thao tác nhận đi qua kiểm tra người phụ trách (người thua ca đồng thời sẽ nhận 403). | Cố vấn, chưa xác nhận: cần để ca nhận đồng thời số 1 có đáp án rõ. | Đã chốt |
| D-15 | Tiếp tục sau từ chối ngoài giờ: deadline = bắt đầu phiên làm việc kế tiếp (xem BR-17, BR-38) + ngân sách còn lại. | Chuyển breached ngay khi còn 0 giây. | Chủ dự án (diễn đạt lại): để Agent có sự thoải mái hợp lý và không làm giảm sự hài lòng của khách hàng. Áp dụng cho từ chối ngoài giờ; trong giờ xem D-20. | Đã chốt |
| D-16 | Tính đến giây nguyên. | Cách tính cũ tại D-10. | Chủ dự án (diễn đạt lại): muốn ghi nhận chính xác; chênh lệch dù 1 giây vẫn là trễ. | Đã chốt |
| D-17 | Chỉ số theo cách lai: M-01 theo ngày tạo; M-02, M-03 theo ngày Closed; M-04, M-05, M-06 là ảnh chụp tại `as_of`. | Toàn bộ chỉ số theo ngày Closed; theo ngày tạo cho mọi chỉ số. | Cố vấn, chưa xác nhận: M-01 theo ngày tạo để không bỏ sót ticket đang trễ phản hồi đầu; M-02, M-03 chỉ ổn định khi Closed. | Đã chốt |
| D-18 | Ngưỡng cảnh báo cố định 3.600/900 giây và quy tắc hiển thị. | Ngưỡng theo tỷ lệ. | Chủ dự án (diễn đạt lại): tăng khả năng hoàn thành ticket đúng hạn cho khách. Áp dụng cho cả hai đồng hồ đang chạy; lý do: cố vấn, chưa xác nhận: tránh điểm mù ở đồng hồ còn lại. | Đã chốt |
| D-19 | Chốt BR-43…BR-45 về mã lỗi Agent. | Chưa ghi nhận. | Chủ dự án chấp nhận đề xuất của cố vấn. | Đã chốt |
| D-20 | Từ chối trong giờ với ngân sách 0 giây: deadline bằng thời điểm quay lại; ngoài giờ giữ D-15. | Áp dụng “deadline bằng thời điểm từ chối” cho cả ngoài giờ. | Chủ dự án: chấp nhận hệ quả đề xuất; ngoài giờ giữ D-15 để Agent thoải mái hợp lý và không giảm hài lòng của khách. | Đã chốt |
| D-21 | Tiếp tục sau Waiting với ngân sách giải quyết còn 0 giây theo BR-48. | Chưa ghi nhận. | Chủ dự án chấp nhận đề xuất của cố vấn. | Đã chốt |
| D-22 | Mức cảnh báo SLA là thông tin nội bộ theo BR-49; Customer không thấy mức cảnh báo. | Customer thấy mức cảnh báo. | Cố vấn, chưa xác nhận: cảnh báo là công cụ nội bộ, tránh gây hiểu lầm cho khách. | Đã chốt |
| D-23 | Mã lỗi thao tác Customer và xem chi tiết Agent theo BR-50. | Chưa ghi nhận. | Chủ dự án chấp nhận đề xuất của cố vấn. | Đã chốt |
| D-24 | Nhận ticket Closed trả `TICKET_CLOSED` theo BR-51. | `TICKET_ALREADY_ASSIGNED` cho ticket Closed. | Chủ dự án chấp nhận đề xuất của cố vấn. | Đã chốt |

Đề xuất mới không thuộc lịch sử quyết định này phải được ghi vào [open-questions.md](open-questions.md) đến khi chủ dự án chốt.
