# Functional Requirements v1.0 (nháp)

Mọi FR trong tài liệu này là `draft`. Business rules là nguồn chính sách; FR chỉ diễn giải hành vi cần có, không thay thế hoặc đổi quy tắc SLA. Fixture SLA không phải test API/backend.

## FR-01 — Tạo và truy cập ticket Customer

- Hành vi: Customer tạo ticket High/Normal, xem ticket của mình và trao đổi công khai theo trạng thái hợp lệ.
- Vai trò: Customer.
- Điều kiện: Danh tính demo hợp lệ; ticket truy cập thuộc Customer.
- Đầu vào / đầu ra: ưu tiên khi tạo; trả ticket với `policy_id` cố định, trạng thái New và dữ liệu công khai được phép xem.
- Lỗi: 401 danh tính sai/thiếu; 404 ticket không tồn tại hoặc không thuộc Customer; 409 `INVALID_TICKET_STATE`/`TICKET_CLOSED` cho thao tác không hợp lệ; 422 khi thiếu nội dung/lý do bắt buộc.
- Ưu tiên: Must.
- Liên kết: BR-03, BR-07…BR-11, BR-32…BR-33, BR-36, BR-50; US-01; AC-01…AC-05.

## FR-02 — Phân quyền và che dữ liệu nội bộ

- Hành vi: Backend áp quyền Customer/Agent/Manager; giao diện không là biện pháp kiểm soát duy nhất. Customer không xem ghi chú nội bộ, cảnh báo SLA hoặc review.
- Vai trò: Customer, Agent, Manager.
- Điều kiện: Mọi truy cập/thao tác có danh tính demo hợp lệ và qua thứ tự kiểm tra BR-33.
- Đầu vào / đầu ra: ngữ cảnh danh tính/role/ticket; trả dữ liệu đúng quyền hoặc lỗi chuẩn.
- Lỗi: 401, 403, 404, 409 hoặc 422 theo BR-32; Customer truy cập review luôn 404.
- Ưu tiên: Must.
- Liên kết: BR-03…BR-06, BR-32…BR-34, BR-49, BR-54, BR-58; US-01, US-03, US-04; AC-03, AC-12…AC-13, AC-16, AC-21, AC-27.

## FR-03 — Hàng đợi, nhận ticket và tải Agent

- Hành vi: Agent xem hàng đợi New tóm tắt, tự nhận ticket khi đủ tải; hệ thống lưu snapshot SLA và bảo đảm nhận đồng thời nhất quán.
- Vai trò: Agent.
- Điều kiện: Ticket New chưa nhận, trừ các trường hợp lỗi ưu tiên Closed/đã nhận; chỉ In Progress tính tải.
- Đầu vào / đầu ra: yêu cầu nhận ticket; trả ticket đã gán/chuyển In Progress hoặc lỗi; kết quả cuối có tối đa một Agent phụ trách và tải không vượt giới hạn do nhận mới.
- Lỗi: 403 xem chi tiết New/chủ ticket khác; 409 `TICKET_CLOSED`, `TICKET_ALREADY_ASSIGNED`, `AGENT_CAPACITY_REACHED` theo thứ tự đã chốt.
- Ưu tiên: Must.
- Liên kết: BR-04, BR-12…BR-16, BR-34, BR-37, BR-45, BR-51; US-02; AC-06…AC-11.

## FR-04 — Tin nhắn, ghi chú và chuyển trạng thái

- Hành vi: Chỉ cho phép message/note và chuyển năm trạng thái theo actor, trạng thái và điều kiện có phản hồi/nội dung công khai.
- Vai trò: Customer, Agent phụ trách.
- Điều kiện: Chuyển trạng thái nằm trong bảng BR-08; Resolved cần nội dung công khai; Customer reject cần lý do.
- Đầu vào / đầu ra: nội dung công khai/nội bộ, lý do từ chối hoặc yêu cầu chuyển; trả trạng thái mới và sự kiện liên quan.
- Lỗi: 403 Agent không phụ trách/Agent thao tác ở New; 409 `INVALID_TICKET_STATE`, `TICKET_CLOSED`, `REVIEW_REQUIRED`; 422 thiếu nội dung hoặc lý do.
- Ưu tiên: Must.
- Liên kết: BR-07…BR-11, BR-33, BR-43…BR-44, BR-50, BR-53, BR-57; US-01, US-03, US-05; AC-02, AC-04…AC-05, AC-12…AC-16, AC-24.

## FR-05 — Hai đồng hồ SLA và cảnh báo nội bộ

- Hành vi: Tính/hiển thị riêng SLA phản hồi đầu và giải quyết theo lịch nghiệp vụ, policy, deadline áp dụng, trạng thái, remaining/consumed và cảnh báo.
- Vai trò: Agent, Manager; Customer chỉ thấy dữ liệu được phép.
- Điều kiện: Tính từ sự kiện gốc và `as_of`; áp dụng Waiting, Resolved, Closed, từ chối, ngoài giờ, ngân sách 0 và vi phạm sticky theo business rules.
- Đầu vào / đầu ra: `policy_id`, sự kiện, `as_of`; trả dữ liệu SLA dẫn xuất/hiển thị đúng quyền. `remaining_seconds` không âm; `consumed_seconds` giữ giá trị thật.
- Lỗi: Không có mã lỗi SLA riêng được chốt; lỗi thao tác nguồn áp dụng FR-01…FR-04.
- Ưu tiên: Must.
- Liên kết: BR-16…BR-26, BR-38…BR-41, BR-46…BR-49, BR-59…BR-61; US-04; AC-17…AC-22; SLA-01…SLA-57 fixture.

## FR-06 — Escalation và review Manager

- Hành vi: Từ chối thứ ba trở đi tạo review từng lượt; review mở chặn Resolved nhưng không chặn Waiting; Manager ghi phương án nội bộ hợp lệ để hoàn tất review.
- Vai trò: Customer, Agent phụ trách, Manager.
- Điều kiện: `rejection_count` dẫn xuất; tối đa một review mở; phương án có nguyên nhân và hướng xử lý tiếp theo.
- Đầu vào / đầu ra: reject, chuyển trạng thái, `handling_plan`; trả review mở/hoàn tất và trạng thái ticket đúng quy tắc.
- Lỗi: 403 Agent ghi phương án; 404 Customer truy cập review; 409 `REVIEW_REQUIRED`, `INVALID_TICKET_STATE`, `TICKET_CLOSED`; 422 thiếu trường bắt buộc.
- Ưu tiên: Must.
- Liên kết: BR-05, BR-21, BR-52…BR-58; US-05; AC-23…AC-27; SLA-58…SLA-69 fixture.

## FR-07 — Báo cáo M-01 đến M-07

- Hành vi: Manager xem các chỉ số/báo cáo theo kỳ, lọc, tử số/mẫu số hoặc snapshot đã chốt; M-07 cung cấp ngữ cảnh review.
- Vai trò: Manager.
- Điều kiện: Áp dụng kỳ chọn theo BR-35; M-07 tính tại `as_of`; không tạo xếp hạng/điểm Agent.
- Đầu vào / đầu ra: kỳ/bộ lọc/as_of; trả M-01…M-07 cùng ngữ cảnh và cách đọc giới hạn.
- Lỗi: Không có mã lỗi báo cáo riêng được chốt; quyền áp dụng FR-02.
- Ưu tiên: Should.
- Liên kết: BR-05, BR-13, BR-35, BR-42, BR-49, BR-56; US-06; AC-28…AC-31.

## FR-08 — Dữ liệu sự kiện và dữ liệu SLA dẫn xuất

- Hành vi: Ghi lịch sử sự kiện bổ sung; dựng/cập nhật dữ liệu dẫn xuất SLA từ lịch sử mà không sửa độc lập dữ liệu dẫn xuất.
- Vai trò: Hệ thống.
- Điều kiện: `event_id` do database cấp; timestamp/interval tuân thủ quy tắc giây; khoảng chạy 0 giây vẫn có thể lưu.
- Đầu vào / đầu ra: sự kiện gốc; trả/lưu interval, consumed, remaining, deadline và trạng thái dựng lại được.
- Lỗi: Client không được gửi `event_id`; chi tiết contract lỗi chưa được chốt, áp dụng 422 khi payload sai theo BR-32.
- Ưu tiên: Must.
- Liên kết: BR-25, BR-27…BR-31, BR-47; US-04; AC-22.

## FR-09 — Hiển thị trạng thái quá hạn và thời gian

- Hành vi: Hiển thị quá hạn và bộ đếm theo đúng quy tắc nội bộ, không nhấp nháy/âm thanh/thông báo lặp; danh sách dùng phút/giờ theo BR-41.
- Vai trò: Agent, Manager.
- Điều kiện: Dữ liệu SLA đã dẫn xuất; Customer không nhận cảnh báo.
- Đầu vào / đầu ra: trạng thái/remaining SLA; trả nhãn quá hạn và thời lượng hiển thị phù hợp bối cảnh.
- Lỗi: Không có mã lỗi riêng được chốt.
- Ưu tiên: Should.
- Liên kết: BR-40…BR-41, BR-49; US-04; AC-21.
