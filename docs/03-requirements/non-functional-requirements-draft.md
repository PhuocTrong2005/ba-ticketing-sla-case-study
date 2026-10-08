# Non-functional Requirements v1.0 (nháp)

Mọi NFR là `draft`. Không có mục nào đặt mục tiêu hiệu năng, uptime, tải hay quy mô mới; bất kỳ ngưỡng mới nào cần được chủ dự án chốt trước khi có hiệu lực.

## NFR-01 — Bảo vệ dữ liệu và thực thi quyền

- Yêu cầu: Backend phải thực thi quyền theo BR-06 và thứ tự kiểm tra BR-33, không dựa vào việc ẩn control giao diện. Customer không nhận ghi chú nội bộ, cảnh báo SLA hoặc review.
- Kiểm chứng dự kiến: kiểm tra contract/API theo role và trạng thái; xác nhận mã 401/403/404/409/422 đã chốt.
- Liên kết: BR-03…BR-06, BR-32…BR-34, BR-49, BR-54, BR-58; FR-02; US-01/03/05.

## NFR-02 — Tính toàn vẹn và atomicity

- Yêu cầu: Nhận ticket cạnh tranh và giao dịch từ chối tạo review phải nguyên tử; không có trạng thái cuối vi phạm giới hạn tải, nhiều Agent phụ trách hoặc nhiều review mở.
- Kiểm chứng dự kiến: ca đồng thời, kiểm tra kết quả từng thao tác và trạng thái dữ liệu cuối; ca từ chối lần ba/các lần tiếp theo.
- Liên kết: BR-15, BR-52; FR-03, FR-06; US-02/05; AC-08…AC-09, AC-23.

## NFR-03 — Truy vết và khả năng dựng lại dữ liệu SLA

- Yêu cầu: Sự kiện gốc chỉ ghi bổ sung; interval/deadline/trạng thái SLA là dẫn xuất, có thể dựng lại từ lịch sử sự kiện. Không sửa riêng dữ liệu SLA dẫn xuất.
- Kiểm chứng dự kiến: xây ca kiểm tra dựng lại từ fixture/sự kiện gốc sau khi code được phép; đối chiếu interval, deadline và trạng thái.
- Liên kết: BR-27…BR-31, BR-47; FR-08; US-04; AC-22.

## NFR-04 — Chính xác thời gian và thứ tự sự kiện

- Yêu cầu: Timestamp ISO 8601 `+07:00` đến giây; phần dưới giây lưu đầu vào thô riêng và cắt khi ghi; duration là giây nguyên; sự kiện cùng giây do database sắp theo `event_id`.
- Kiểm chứng dự kiến: ca timestamp có phần dưới giây, ranh giới deadline và sự kiện cùng giây; fixture SLA chỉ là tham chiếu nghiệp vụ.
- Liên kết: BR-17, BR-22, BR-25, BR-47, BR-59; FR-05, FR-08; US-04.

## NFR-05 — Khả năng chạy lại và tính xác định

- Yêu cầu: Với cùng sự kiện gốc, policy và `as_of`, kết quả SLA/báo cáo dẫn xuất phải tái lập; thời gian thực phải inject được khi triển khai để tái lập đánh giá tại `as_of`.
- Kiểm chứng dự kiến: sau khi được phép viết logic, chạy lại cùng fixture với đồng hồ inject được và so sánh kết quả; không coi đây là kiểm chứng backend đã có.
- Liên kết: BR-18, BR-23, BR-27…BR-29; FR-05, FR-07, FR-08; D-09, D-16.

## NFR-06 — Khả dụng của prototype demo

- Yêu cầu: Prototype tĩnh phải trình bày trạng thái, bộ đếm và lỗi rõ ràng theo BR-40…BR-41; không giả vờ gọi API thật hoặc có đăng nhập thật.
- Kiểm chứng dự kiến: review giao diện theo luồng documented sau khi prototype được xây; kiểm tra mô tả mô phỏng/giới hạn.
- Liên kết: BR-01…BR-02, BR-40…BR-41, D-08; FR-09.

## NFR-07 — Giới hạn chưa chốt

- Yêu cầu: Không tự áp số liệu hiệu năng, uptime, số người dùng, giới hạn dung lượng hoặc SLA kỹ thuật. Các ngưỡng loại này là TBD và chỉ có hiệu lực sau decision log.
- Kiểm chứng dự kiến: review tài liệu/decision log trước khi triển khai.
- Liên kết: BR-01, D-08; scope v1.0.
