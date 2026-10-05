# Phạm vi kịch bản SLA

Tài liệu này quy định phạm vi và định dạng kịch bản SLA; không chứa bất kỳ ca kịch bản cụ thể nào. Đóng OQ-08 không có nghĩa các ca đã verified.

## Quy ước file kịch bản SLA

Mỗi ca phải có ID, mô tả, `policy_id`, `created_at`, `as_of`, và `events` ở JSON cố định. Mỗi sự kiện có `seq`, `type`, `at` ở ISO 8601 `+07:00` đến giây. Mỗi ca có các cột `expected_*`, gồm deadline, giây đã tiêu, giây còn lại, trạng thái của từng đồng hồ, `expected_first_response_warning_level`, `expected_resolution_warning_level`, `expected_first_response_sla_status_at_assignment` và `expected_resolution_sla_status_at_assignment`. Hai cột `expected_*_warning_level` dùng các giá trị `none`, `soft`, `emphasized`, `due`, `breached`; cùng `calculation_note` và `review_status` (`draft` hoặc `verified`). Mọi tính toán theo giây nguyên.

## Mười một nhóm kịch bản tối thiểu

| Nhóm | Phạm vi | Mã kịch bản verified |
|---:|---|---|
| 1 | Luồng cơ bản: High và Normal; tính riêng SLA phản hồi đầu và giải quyết; cả hai bắt đầu từ lúc tạo. | |
| 2 | Ngoài giờ: tạo trước 08:00, sau 17:00; Agent nhận, phản hồi hoặc Resolved ngoài giờ; không cộng thời gian ngoài lịch; thời điểm trước 08:00 của một ngày làm việc (phiên bắt đầu cùng ngày). | |
| 3 | Qua ngày và cuối tuần: chạy qua đêm, từ Thứ Sáu sang Thứ Hai; tạo ticket vào Thứ Bảy/Chủ nhật. | |
| 4 | Mốc biên và độ chính xác: tạo đúng 08:00/17:00; hoàn thành trước deadline 1 giây, đúng deadline, sau 1 giây; deadline đúng 17:00 không bị đẩy sang hôm sau; ghi nhận timestamp có phần dưới giây bị cắt bỏ (ví dụ `17:00:00.900` → `17:00:00`). | |
| 5 | Phản hồi đầu: tin nhắn khách và ghi chú nội bộ không tính; chỉ phản hồi công khai đầu tiên của Agent; nội dung Resolved có thể là phản hồi đầu; khách từ chối không đổi kết quả này. | |
| 6 | Waiting for Customer: một hoặc nhiều lần; vào/ra ngoài giờ hoặc qua cuối tuần; không cộng thời gian chờ; tiếp tục đúng ngân sách còn lại; thời điểm trước 08:00 của một ngày làm việc (phiên bắt đầu cùng ngày). | |
| 7 | Resolved và Closed: Resolved đúng hạn/trễ; khách xác nhận muộn hoặc chưa xác nhận; thời gian ở Resolved không cộng SLA; kết quả chỉ xác nhận cuối khi Closed. | |
| 8 | Từ chối kết quả: một hoặc nhiều lần; ngoài giờ; xen kẽ Waiting; giữ ngân sách còn lại, không reset hoặc nhân đôi. | |
| 9 | Vi phạm và hết ngân sách: đã vi phạm trước Waiting, Resolved hoặc lúc nhận; vi phạm không bị xóa. Từ chối với 0 giây còn lại: TRONG giờ → deadline bằng thời điểm ticket quay lại In Progress (BR-46); NGOÀI giờ → deadline bằng bắt đầu phiên làm việc kế tiếp: 08:00:00 cùng ngày nếu thời điểm đó trước 08:00 của một ngày làm việc; ngược lại 08:00:00 của ngày làm việc kế tiếp (BR-38). | |
| 10 | Thời điểm đánh giá và dữ liệu: đánh giá tại `as_of` khi đang chạy, Waiting, Resolved; snapshot lúc nhận; hai đồng hồ có kết quả khác nhau; lưu khoảng chạy 0 giây; sự kiện cùng giây theo `event_id`. | |
| 11 | Ngưỡng cảnh báo áp dụng cho cả hai đồng hồ SLA đang chạy: còn đúng 3.600 giây chưa cảnh báo; 3.599 cảnh báo nhẹ; đúng 900 vẫn nhẹ; 899 nhấn mạnh; đúng deadline “đến hạn”; sau 1 giây vi phạm; tạm dừng/hoàn tất không cảnh báo. Có ca High phản hồi đầu tại thời điểm tạo (còn đúng 3.600 giây → chưa cảnh báo) và sau 1 giây (3.599 → cảnh báo nhẹ). | |

## Điều kiện hoàn tất

- Mỗi nhóm có ca đại diện; nhánh có kết quả khác nhau phải có ca riêng.
- Một ca có thể phủ nhiều nhóm.
- Mỗi ca ghi đầu vào, chuỗi sự kiện, `as_of`, `expected_*` và phép tính độc lập.
- Chủ dự án tự kiểm tra và xác nhận `verified`; Codex không tự xác nhận.
- Không còn nhóm trống; không bắt buộc số ca cố định.
