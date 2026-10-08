# User stories và acceptance criteria v1.0 (nháp)

Tất cả story và AC trong tài liệu này là `draft`, chờ chủ dự án duyệt. Fixture SLA là đầu vào nghiệp vụ; không thay thế test API, backend, SQL hay prototype.

## US-01 — Customer quản lý ticket của mình

Là Customer, tôi muốn tạo, xem ticket của mình, nhắn công khai và phản hồi kết quả để theo dõi yêu cầu hỗ trợ.

Ưu tiên: Must. Quy tắc: BR-03, BR-07…BR-11, BR-36, BR-50.

- AC-01: Given Customer tạo ticket với High hoặc Normal, when dữ liệu hợp lệ, then ticket ở New và `policy_id` được cố định từ lúc tạo.
- AC-02: Given ticket thuộc Customer, when ticket ở New, In Progress hoặc Waiting for Customer, then Customer được gửi tin nhắn công khai; tại Waiting, tin nhắn đưa ticket về In Progress.
- AC-03: Given Customer truy cập ticket không thuộc mình, when xem hay thao tác, then backend trả 404 trước khi kiểm tra trạng thái.
- AC-04: Given ticket Resolved, when Customer xác nhận, then ticket chuyển Closed; when Customer từ chối với lý do bắt buộc, then ticket về In Progress theo BR-08 và BR-21.
- AC-05: Given Customer xác nhận/từ chối ngoài Resolved, when thao tác, then trả 409 `INVALID_TICKET_STATE`; Given ticket Closed, then trả 409 `TICKET_CLOSED` và không mở lại.

## US-02 — Agent xem hàng đợi và nhận ticket

Là Agent, tôi muốn xem hàng đợi tóm tắt và nhận ticket hợp lệ để quản lý tải công việc.

Ưu tiên: Must. Quy tắc: BR-04, BR-12…BR-16, BR-34, BR-37, BR-45, BR-51.

- AC-06: Given Agent xem hàng đợi New, when có quyền hợp lệ, then chỉ thấy mã, tiêu đề, ưu tiên, hạn phản hồi và thời điểm tạo; chi tiết ticket New chưa nhận không truy cập được và trả 403.
- AC-07: Given ticket New chưa có người phụ trách và Agent có dưới ba ticket In Progress, when Agent nhận, then gán Agent, lưu snapshot SLA, chuyển In Progress và tăng tải In Progress.
- AC-08: Given hai Agent nhận đồng thời cùng một ticket New chưa có người phụ trách, when hai yêu cầu cạnh tranh hoàn tất, then đúng một yêu cầu thành công, yêu cầu còn lại trả 409 `TICKET_ALREADY_ASSIGNED`, và database cuối cùng có đúng một Agent phụ trách/ticket In Progress.
- AC-09: Given một Agent đang có đúng hai ticket In Progress và nhận đồng thời hai ticket New khác nhau, when hai yêu cầu cạnh tranh hoàn tất, then đúng một yêu cầu thành công, yêu cầu còn lại trả 409 `AGENT_CAPACITY_REACHED`, và database cuối cùng có đúng ba ticket In Progress của Agent đó.
- AC-10: Given Agent có tải <3, =3 hoặc >3, when thử nhận ticket New, then chỉ trạng thái <3 được nhận; =3 và >3 trả `AGENT_CAPACITY_REACHED`. Given ticket quay lại In Progress do Customer, then việc quay lại không bị chặn theo tải.
- AC-11: Given ticket Closed, đã có Agent nhận hoặc cả hai điều kiện, when Agent nhận, then thứ tự lỗi là `TICKET_CLOSED` trước `TICKET_ALREADY_ASSIGNED`, và `TICKET_ALREADY_ASSIGNED` trước kiểm tra tải.

## US-03 — Agent xử lý ticket theo quyền và vòng đời

Là Agent phụ trách, tôi muốn phản hồi công khai, ghi chú nội bộ và chuyển trạng thái hợp lệ để xử lý ticket.

Ưu tiên: Must. Quy tắc: BR-08, BR-10…BR-11, BR-37, BR-43…BR-45.

- AC-12: Given Agent không phụ trách, when xem chi tiết, nhắn, ghi chú hoặc chuyển trạng thái ticket đã có người phụ trách, then trả 403.
- AC-13: Given ticket New, Resolved hoặc Closed, when Agent nhắn/gửi note, then lần lượt trả 403, 409 `INVALID_TICKET_STATE`, hoặc 409 `TICKET_CLOSED`.
- AC-14: Given ticket In Progress và Agent phụ trách đã có phản hồi công khai đầu tiên, when chuyển Waiting for Customer, then chuyển trạng thái hợp lệ; without phản hồi đầu, then thao tác bị chặn theo BR-08.
- AC-15: Given ticket In Progress, when Agent chuyển Resolved, then nội dung công khai cho Customer là bắt buộc; nội dung này cũng hoàn tất phản hồi đầu nếu trước đó chưa có phản hồi công khai.
- AC-16: Given payload thiếu nội dung/lý do bắt buộc, when thao tác cần trường đó, then trả 422; validation nội dung chạy sau danh tính, vai trò, quyền, người phụ trách và trạng thái theo BR-33.

## US-04 — SLA nội bộ và dữ liệu dẫn xuất

Là Agent hoặc Manager, tôi muốn xem SLA phản hồi đầu/giải quyết và cảnh báo nội bộ để ưu tiên xử lý mà không lộ dữ liệu nội bộ cho Customer.

Ưu tiên: Must. Quy tắc: BR-16…BR-26, BR-38…BR-39, BR-46…BR-49, BR-59…BR-61. Fixture liên quan: SLA-01…SLA-57.

- AC-17: Given ticket New hoặc In Progress, when tính tại `as_of`, then hai đồng hồ bắt đầu từ lúc tạo, dùng lịch nghiệp vụ và policy cố định, với timestamp đến giây theo BR-17/BR-18/BR-25.
- AC-18: Given Agent gửi phản hồi công khai đầu tiên, when phản hồi được ghi, then chỉ phản hồi đầu đó dừng SLA phản hồi đầu; customer message và internal note không dừng đồng hồ.
- AC-19: Given ticket Resolved, Closed, Customer từ chối hoặc Waiting, when tính SLA giải quyết, then Resolved dừng lượt hiện hành, Closed là kết quả cuối, từ chối tiếp tục ngân sách còn lại, Waiting tạm dừng và không cấp/reset ngân sách.
- AC-20: Given deadline đã đạt hoặc vượt, when hoàn thành/tiếp tục/tạm dừng, then so thời điểm với deadline áp dụng; vi phạm đã xảy ra được giữ. Với ngân sách còn 0, deadline tuân theo BR-38, BR-46 hoặc BR-48; `remaining_seconds` không âm nhưng `consumed_seconds` giữ giá trị thực.
- AC-21: Given Waiting sau khi đã breached, when hiển thị, then giữ trạng thái `breached`, không cộng giây và không phát cảnh báo sắp đến hạn. Given Customer nhận dữ liệu ticket, then không nhận mức cảnh báo SLA hoặc ghi chú nội bộ.
- AC-22: Given dữ liệu SLA dẫn xuất, when lưu hoặc dựng lại, then dữ liệu phải truy vết được từ sự kiện gốc và không sửa độc lập.

## US-05 — Manager review escalation

Là Manager, tôi muốn xem và ghi phương án nội bộ cho review escalation để xử lý các lần từ chối lặp lại mà không đổi SLA.

Ưu tiên: Must. Quy tắc: BR-05, BR-52…BR-58. Fixture liên quan: SLA-58…SLA-69.

- AC-23: Given Customer từ chối lần thứ nhất hoặc thứ hai, when giao dịch hoàn tất, then không tạo review; từ lần thứ ba trở đi, mỗi từ chối tạo review mới trong cùng giao dịch và mỗi ticket chỉ có tối đa một review đang mở.
- AC-24: Given review mở, when Agent thử Resolved, then trả 409 `REVIEW_REQUIRED`; when Agent chuyển Waiting với điều kiện BR-08, then được phép, Customer trả lời đưa ticket về In Progress và review vẫn mở.
- AC-25: Given Manager ghi `handling_plan` cho review mở, when nguyên nhân và hướng xử lý tiếp theo hiện diện, then hoàn tất review và gỡ chặn Resolved; thiếu trường bắt buộc trả 422.
- AC-26: Given Manager không có review mở hoặc ticket Closed, when ghi phương án, then lần lượt trả 409 `INVALID_TICKET_STATE` hoặc 409 `TICKET_CLOSED`.
- AC-27: Given tài nguyên review, when Customer truy cập, then luôn nhận 404; when Agent truy cập/ghi phương án, then nhận 403; Manager không được nhắn công khai, nhận ticket hoặc bấm Resolved.

## US-06 — Báo cáo và ngữ cảnh vận hành

Là Manager, tôi muốn xem tải và báo cáo có kỳ, bộ lọc, tử số/mẫu số hoặc ngữ cảnh rõ ràng để đọc đúng kết quả vận hành demo.

Ưu tiên: Should. Quy tắc: BR-13, BR-35, BR-42, BR-49, BR-56.

- AC-28: Given M-01, when chọn ngày tạo, then tử số/mẫu số chỉ gồm kết quả phản hồi đầu met/breached tại `as_of` và pending được báo riêng.
- AC-29: Given M-02/M-03, when chọn ngày Closed, then chỉ ticket Closed trong kỳ nằm trong mẫu số và luôn hiển thị số ticket chưa Closed chưa tính.
- AC-30: Given M-04/M-05/M-06, when xem tại `as_of`, then lần lượt hiển thị ticket chưa Closed có cờ breach từng đồng hồ, ticket Resolved chờ xác nhận theo giờ lịch, và tải Agent theo <3/=3/>3; không có xếp hạng Agent.
- AC-31: Given M-07, when xem tại `as_of`, then liệt kê từng review, thời gian chờ theo giờ lịch, phần chờ chồng SLA giải quyết đang chạy trong giờ và bối cảnh vi phạm; không dùng các giá trị này để tự quy lỗi hoặc miễn trách nhiệm cá nhân.

## Thứ tự kiểm tra và mã lỗi

Mọi AC lỗi áp dụng thứ tự BR-33: danh tính → vai trò → tìm ticket/quyền truy cập → người phụ trách → trạng thái/điều kiện nhận/tải → nội dung. Ngoại lệ nhận ticket theo BR-37/BR-51 và tài nguyên review theo BR-54/BR-58. Các mã được dùng trong các AC là 401, 403, 404, 409 (`INVALID_TICKET_STATE`, `TICKET_ALREADY_ASSIGNED`, `AGENT_CAPACITY_REACHED`, `TICKET_CLOSED`, `REVIEW_REQUIRED`) và 422; không có mã mới.

## Ma trận BR → story → AC

| Quy tắc | Story | AC |
|---|---|---|
| BR-03, BR-07…BR-11, BR-36, BR-50 | US-01 | AC-01…AC-05 |
| BR-04, BR-12…BR-16, BR-34, BR-37, BR-45, BR-51 | US-02 | AC-06…AC-11 |
| BR-08, BR-10…BR-11, BR-33, BR-37, BR-43…BR-45 | US-03 | AC-12…AC-16 |
| BR-16…BR-26, BR-38…BR-39, BR-46…BR-49, BR-59…BR-61 | US-04 | AC-17…AC-22 |
| BR-05, BR-52…BR-58 | US-05 | AC-23…AC-27 |
| BR-13, BR-35, BR-42, BR-49, BR-56 | US-06 | AC-28…AC-31 |

## Quy tắc chưa được phủ trực tiếp

BR-01, BR-02, BR-06, BR-27…BR-32 và BR-40…BR-41 không có AC độc lập trong bản nháp này: chúng là phạm vi/công nghệ, nguyên tắc thực thi/dữ liệu hoặc hiển thị; phân loại và cách kiểm chứng dự kiến nằm trong traceability. Fixture SLA vẫn không thay thế test API/backend.
