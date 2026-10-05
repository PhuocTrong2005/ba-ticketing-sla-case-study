# Business rules v1.0

Nguồn sự thật nghiệp vụ của case study hệ thống quản lý ticket hỗ trợ khách hàng và SLA cho doanh nghiệp phần mềm B2B giả định. Đây là giải pháp mẫu (prototype và backend mô phỏng), không phải sản phẩm vận hành. Các vấn đề chưa chốt nằm ở [open-questions.md](../open-questions.md) và không phải quy tắc có hiệu lực.

## Mục lục

1. [Phạm vi và công nghệ](#phạm-vi-và-công-nghệ)
2. [Vai trò và quyền](#vai-trò-và-quyền)
3. [Vòng đời ticket](#vòng-đời-ticket)
4. [Tin nhắn](#tin-nhắn)
5. [Nhận ticket và tải](#nhận-ticket-và-tải)
6. [SLA (BR-17…BR-59)](#sla)
7. [Dữ liệu và khả năng dựng lại](#dữ-liệu-và-khả-năng-dựng-lại)
8. [Hiển thị](#hiển-thị)
9. [API, quyền và lỗi](#api-quyền-và-lỗi)
10. [Báo cáo](#báo-cáo)
11. [Escalation sau nhiều lần Customer từ chối (BR-52…BR-58)](#escalation-sau-nhiều-lần-customer-từ-chối)

## Phạm vi và công nghệ

**BR-01 — Phạm vi case study.** Mọi số liệu, chính sách và quy mô là giả định; không tuyên bố cải thiện hiệu quả của doanh nghiệp thực.

**BR-02 — Công nghệ đã chốt.** Prototype HTML/CSS/JS tĩnh, dữ liệu trong trình duyệt và GitHub Pages, không gọi API thật. Backend dùng Python FastAPI và SQLite; dùng pytest và Postman. Không dùng backend Node.

## Vai trò và quyền

**BR-03 — Customer.** Customer chỉ tạo và xem ticket của chính mình; gửi tin nhắn công khai; xác nhận hoặc từ chối kết quả. Customer không xem ghi chú nội bộ.

**BR-04 — Agent.** Ba Agent trong dữ liệu demo xem hàng đợi New chỉ với mã, tiêu đề, ưu tiên, hạn phản hồi và thời điểm tạo. Agent tự nhận ticket, xử lý ticket mình phụ trách, phản hồi công khai và ghi chú nội bộ. Agent chỉ xem chi tiết ticket mình phụ trách.

**BR-05 — Manager.** Một Manager xem toàn bộ ticket, tin nhắn công khai, ghi chú nội bộ và báo cáo; ghi nhận phương án xử lý cho lượt review đang mở (BR-54). Manager không nhắn công khai, không nhận ticket, không bấm Resolved.

**BR-06 — Thực thi quyền.** Backend kiểm tra quyền; không dựa vào việc ẩn nút giao diện. Danh tính demo là cố định, không phải hệ thống đăng nhập.

## Vòng đời ticket

**BR-07 — Trạng thái hợp lệ.** Ticket có đúng năm trạng thái: New, In Progress, Waiting for Customer, Resolved và Closed.

**BR-08 — Chuyển trạng thái.** Chỉ các chuyển trạng thái sau được phép:

| Từ | Sang | Chủ thể | Điều kiện |
|---|---|---|---|
| New | In Progress | Agent | Chưa có người nhận; Agent có dưới 3 ticket In Progress. |
| In Progress | Waiting for Customer | Agent phụ trách | Đã có phản hồi công khai đầu tiên của Agent. |
| Waiting for Customer | In Progress | Customer | Customer gửi tin nhắn công khai; hệ thống tự chuyển. |
| In Progress | Resolved | Agent phụ trách | Có nội dung kết quả hiển thị cho Customer. Nếu có lượt review chưa hoàn thành (BR-52), bị chặn; xem BR-53. |
| Resolved | Closed | Customer | Customer xác nhận đã giải quyết. |
| Resolved | In Progress | Customer | Customer từ chối, bắt buộc có lý do; lưu công khai và ghi lịch sử. |
| Closed | — | — | Closed là trạng thái cuối, không mở lại. |

**BR-09 — Chờ xác nhận.** Ticket Resolved mà Customer không phản hồi giữ nguyên và không tự đóng. Manager thấy ticket này trong danh sách chờ xác nhận.

**BR-36 — Ưu tiên và policy khi tạo.** Customer tạo ticket và chọn mức ưu tiên High hoặc Normal. Mức ưu tiên và `policy_id` được cố định từ lúc tạo và không đổi sau đó.

## Tin nhắn

**BR-10 — Quy tắc theo trạng thái.**

| Trạng thái | Customer | Agent phụ trách | Ảnh hưởng trạng thái |
|---|---|---|---|
| New | Được nhắn công khai. | Chưa có Agent phụ trách. | Tin nhắn Customer không đổi trạng thái. |
| In Progress | Được nhắn công khai. | Được phản hồi công khai hoặc ghi chú nội bộ. | Không đổi trạng thái. |
| Waiting for Customer | Nhắn công khai được và tự chuyển sang In Progress. | Được nhắn công khai hoặc ghi chú nội bộ. | Hành động Agent không đổi trạng thái và không tiếp tục đồng hồ giải quyết. |
| Resolved | Chỉ xác nhận hoặc từ chối. | Không gửi thêm tin nhắn hoặc ghi chú. | Xem BR-08. |
| Closed | Không gửi được. | Không gửi được. | Không có. |

**BR-11 — Kết quả Resolved và phản hồi đầu.** Nội dung khi chuyển Resolved được lưu là phản hồi công khai. Nếu trước đó chưa có phản hồi công khai nào của Agent, nội dung này cũng hoàn tất SLA phản hồi đầu. Tin nhắn Customer và ghi chú nội bộ không phải phản hồi đầu.

## Nhận ticket và tải

**BR-12 — Tự nhận và gợi ý.** Agent tự nhận từ hàng đợi chung. Thứ tự High trước Normal, hạn phản hồi sớm trước và tạo sớm trước chỉ là gợi ý, không bắt buộc.

**BR-13 — Cách tính tải.** Chỉ ticket In Progress tính vào tải: dưới 3 được nhận; bằng 3 đạt giới hạn; trên 3 quá tải. Từ 3 trở lên không nhận ticket mới. Waiting for Customer và Resolved không tính tải.

**BR-14 — Quay lại In Progress.** Ticket quay lại In Progress do Customer trả lời hoặc từ chối vẫn được phép, kể cả khi Agent vượt 3. Không chuyển Agent; mỗi ticket chỉ được nhận một lần và chỉ có một người phụ trách.

**BR-15 — Đồng thời và tính nguyên tử.** Khi hai Agent nhận cùng một ticket, chỉ một thao tác thành công. Khi Agent đang có 2 ticket In Progress nhận đồng thời 2 ticket, chỉ một thành công và tổng dừng ở 3. Kiểm tra điều kiện, gán phụ trách, chuyển trạng thái, ghi lịch sử và lưu snapshot SLA phải nằm trong cùng một giao dịch.

**BR-16 — Snapshot khi nhận.** Lúc nhận lưu `assigned_at`, `first_response_sla_status_at_assignment` và `resolution_sla_status_at_assignment`. Snapshot tính tại `as_of = assigned_at`; chỉ có giá trị pending hoặc breached.

## SLA

**BR-17 — Lịch nghiệp vụ.** Lịch là Thứ Hai–Thứ Sáu, 08:00–17:00, múi giờ Asia/Ho_Chi_Minh (UTC+7), không nghỉ trưa. Phiên bản 1.0 không xử lý ngày lễ; ngày lễ vào Thứ Hai–Thứ Sáu vẫn tính 08:00–17:00 bình thường. 08:00 thuộc giờ làm việc, 17:00 không thuộc; deadline được phép đúng 17:00 và không đẩy sang 08:00 hôm sau. Chỉ thời gian trong giờ làm việc được cộng vào SLA. Đồng hồ bắt đầu tại thời điểm tạo ticket; nếu thời điểm đó ngoài giờ làm việc (trước 08:00, từ 17:00 trở đi, hoặc cuối tuần), khoảng thời gian làm việc đầu tiên được tính từ bắt đầu phiên làm việc kế tiếp: 08:00:00 cùng ngày nếu thời điểm đó trước 08:00 của một ngày làm việc; ngược lại 08:00:00 của ngày làm việc kế tiếp.

**BR-18 — Chính sách.** High: phản hồi 3.600 giây làm việc, giải quyết 28.800 giây làm việc. Normal: phản hồi 7.200 giây làm việc, giải quyết 57.600 giây làm việc. `policy_id` xác định policy dùng để tính và dựng lại dữ liệu.

**BR-19 — Đồng hồ phản hồi đầu.** Bắt đầu khi ticket được tạo, dừng ở phản hồi công khai đầu tiên của Agent, chỉ đo một lần và không thay đổi khi Customer từ chối.

**BR-20 — Đồng hồ giải quyết.** Bắt đầu khi ticket được tạo, không chờ Agent nhận; chạy tại New và In Progress; tạm dừng tại Waiting for Customer; dừng tại Resolved. Thời gian ở Waiting for Customer và Resolved không được cộng.

**BR-21 — Từ chối.** Khi Customer từ chối, SLA giải quyết tiếp tục với ngân sách còn lại: không nhân đôi, không reset, không tự cấp thêm thời gian. Vi phạm đã xảy ra không bị xóa. Việc chờ Manager review (BR-52) không tạm dừng, không reset và không cấp thêm thời gian.

**BR-22 — Đúng hạn và quá hạn.** Khi hoàn thành, `completed_at <= deadline` là met; `completed_at > deadline`, kể cả sau deadline 1 giây, là breached.

**BR-23 — Trạng thái SLA giải quyết.** Khi đồng hồ chạy và chưa hoàn thành, `as_of <= deadline` là pending, `as_of > deadline` là breached. Khi Waiting for Customer, giữ breached nếu đã vi phạm trước đó; nếu chưa thì giữ pending, không so sánh deadline cũ. Tại Resolved, đánh giá kết quả lượt giải quyết vừa kết thúc; met chỉ tạm thời đến khi Customer xác nhận, breached không bị xóa; chỉ Closed là kết quả cuối. Khi tiếp tục sau Waiting hoặc từ chối, tính deadline mới từ lúc tiếp tục theo lịch nghiệp vụ và ngân sách còn lại. Khi Customer từ chối, kết quả met tạm thời của lượt trước không còn hiệu lực; kết quả được đánh giá lại là pending hoặc breached theo tổng giây đã tiêu và deadline mới. Với đồng hồ phản hồi đầu: chưa hoàn thành và `as_of <= deadline` là pending; `as_of > deadline` là breached. Tổng số giây đã tiêu cộng dồn qua mọi khoảng chạy dùng để xác định ngân sách còn lại và tính deadline; không tính riêng từng lượt xử lý. Khi đồng hồ đang chạy, đánh giá bằng cách so `as_of` với deadline hiện hành; khi hoàn tất, so thời điểm hoàn tất với deadline áp dụng tại thời điểm đó (BR-22). Khi Waiting for Customer, giữ trạng thái vi phạm đã có, hoặc pending nếu chưa vi phạm; không so với deadline cũ. Khi Resolved hoặc Closed, giữ kết quả đã xác định, trừ trường hợp Customer từ chối và đồng hồ giải quyết tiếp tục theo quy tắc hiện hành. Vi phạm đã xảy ra không bị xóa.

**BR-24 — Hiển thị khi tạm dừng.** Khi đồng hồ giải quyết tạm dừng, giữ số giây đã tiêu và ngân sách còn lại, hiển thị thời gian còn lại; không hiển thị deadline cũ như hạn đang chạy. Deadline trước tạm dừng chỉ là thông tin lịch sử, không kết luận vi phạm khi đang tạm dừng.

**BR-25 — Độ chính xác giây.** Timestamp sự kiện lưu theo ISO 8601 với offset `+07:00`, gồm giờ-phút-giây; phần dưới giây bị cắt bỏ khi ghi, không làm tròn. Đầu vào thô có phần dưới giây được lưu riêng khỏi giá trị ghi nhận; giá trị ghi nhận là phần giây nguyên sau khi cắt, không làm tròn. Thời lượng là giây nguyên, hậu tố `_seconds`. Sự kiện cùng giây được sắp theo `event_id` do database cấp; client không gửi `event_id`.

**BR-26 — Ví dụ kiểm tra.** Ticket High tạo 16:00:00 Thứ Hai có hạn phản hồi 17:00:00 Thứ Hai: phản hồi 17:00:00 đạt, 17:00:01 trễ. Hạn giải quyết là 15:00:00 Thứ Ba: dùng 3.600 giây Thứ Hai và còn 25.200 giây từ 08:00:00 Thứ Ba.

**BR-38 — Tiếp tục sau từ chối ngoài giờ.** Khi Customer từ chối và ticket quay về In Progress ngoài giờ làm việc, deadline giải quyết mới = (bắt đầu phiên làm việc kế tiếp: 08:00:00 cùng ngày nếu thời điểm đó trước 08:00 của một ngày làm việc; ngược lại 08:00:00 của ngày làm việc kế tiếp) + ngân sách còn lại. Với ngân sách còn lại bằng 0 giây, deadline bằng đúng bắt đầu phiên làm việc kế tiếp: 08:00:00 cùng ngày nếu thời điểm đó trước 08:00 của một ngày làm việc; ngược lại 08:00:00 của ngày làm việc kế tiếp. Ticket là breached khi `as_of` > deadline; hoàn thành đúng deadline vẫn đạt. Nếu đã breached trước đó thì giữ breached. Không cấp thêm thời gian.

**BR-39 — Ngưỡng cảnh báo SLA.** Ngưỡng áp dụng cho cả hai đồng hồ SLA khi đang chạy; mỗi đồng hồ tính theo số giây làm việc còn lại của chính nó. Khi đồng hồ SLA đang chạy, còn dưới 3.600 giây làm việc thì cảnh báo nhẹ; còn dưới 900 giây thì nhấn mạnh. Đúng 3.600 giây chưa cảnh báo; 3.599 giây cảnh báo nhẹ; đúng 900 giây vẫn cảnh báo nhẹ; 899 giây nhấn mạnh; đúng deadline hiển thị “đến hạn”; sau deadline 1 giây hiển thị “vi phạm”. Đồng hồ tạm dừng không phát cảnh báo sắp đến hạn; đồng hồ hoàn tất đạt (met) không phát cảnh báo. Mức `breached` cũng hiển thị cho đồng hồ đã hoàn tất trễ. Mức cảnh báo tính theo số giây làm việc còn lại, không phụ thuộc `as_of` nằm trong hay ngoài giờ làm việc. Khi đồng hồ tạm dừng, thời gian còn lại vẫn được hiển thị theo BR-24; chỉ mức cảnh báo bị tắt.

**BR-59 — Thao tác ngoài giờ.** Thao tác của Agent hoặc Customer ngoài giờ làm việc vẫn được ghi nhận với timestamp thực (BR-27); không giây ngoài giờ nào được cộng vào SLA (BR-17). Kết quả đạt hoặc trễ vẫn xác định theo BR-22: thao tác có thời điểm không sau deadline là met; thao tác sau deadline vẫn được ghi nhận nhưng là breached.

**BR-46 — Từ chối trong giờ với ngân sách 0 giây.** Khi Customer từ chối trong giờ làm việc và ngân sách còn lại bằng 0 giây, deadline bằng đúng thời điểm ticket quay lại In Progress; ticket là breached khi `as_of` > deadline. Ngoài giờ áp dụng BR-38, gồm quy tắc bắt đầu phiên làm việc kế tiếp.

**BR-48 — Tiếp tục sau Waiting với ngân sách 0 giây.** Khi Customer trả lời và ticket quay về In Progress từ Waiting for Customer với ngân sách giải quyết còn 0 giây: trong giờ làm việc, deadline bằng đúng thời điểm quay lại như BR-46; ngoài giờ, deadline bằng bắt đầu phiên làm việc kế tiếp như BR-38. Nếu đã breached trước đó thì giữ breached. Không cấp thêm thời gian.

## Dữ liệu và khả năng dựng lại

**BR-27 — Dữ liệu gốc.** `ticket_events` là lịch sử sự kiện gốc gồm `event_id`, ticket, thời điểm, actor, loại, trạng thái trước/sau, nội dung và `policy_id`. Chỉ ghi bổ sung; không sửa hoặc xóa để thay đổi kết quả SLA.

**BR-28 — Dữ liệu dẫn xuất.** Các khoảng đồng hồ chạy (`started_at`, `ended_at`, `business_seconds`, loại SLA), tổng giây đã tiêu, deadline và trạng thái SLA là dữ liệu dẫn xuất, có thể lưu để SQL nhưng không được sửa độc lập. Phải có test dựng lại từ sự kiện gốc.

**BR-29 — Khoảng đang chạy.** Khoảng đang chạy có `ended_at = null`; thời lượng tính tại `as_of`, không lưu giá trị giây thay đổi liên tục. Chỉ khoảng đã kết thúc lưu `business_seconds` cố định.

**BR-30 — Phân biệt khái niệm.** Waiting kết thúc một khoảng chạy. Resolved kết thúc một lượt xử lý. Từ chối mở lượt mới nhưng giữ ngân sách còn lại.

**BR-31 — Bảng dự kiến.** `users`, `tickets`, `messages`, `ticket_events`, `ticket_reviews`, `sla_policies`, `sla_intervals`, `ticket_sla`, `assignment_snapshots`.

**BR-47 — Khoảng chạy 0 giây và thứ tự sự kiện.** Khoảng chạy dài 0 giây vẫn được lưu. Sự kiện cùng giây được xếp theo `event_id` do database cấp.

## Hiển thị

**BR-40 — Hiển thị quá hạn.** Quá hạn chỉ hiện nhãn rõ ràng; không nhấp nháy, không âm thanh và không thông báo lặp lại.

**BR-41 — Hiển thị bộ đếm thời gian.** Bộ đếm giây chỉ hiển thị trong chi tiết ticket; danh sách hiển thị phút/giờ; trễ chưa đủ một phút ghi “Dưới 1 phút”. Thời gian còn lại dưới một phút hiển thị “Dưới 1 phút”.

**BR-49 — Hiển thị mức cảnh báo SLA.** Mức cảnh báo SLA là thông tin nội bộ. Agent thấy mức cảnh báo trên ticket mình phụ trách. Manager thấy mức cảnh báo trên mọi màn hình ticket và thấy ticket vi phạm qua M-04. Customer không thấy mức cảnh báo SLA, chỉ thấy trạng thái ticket; phản hồi API dành cho Customer không chứa mức cảnh báo. Không có thông báo đẩy. Cờ escalation và phương án xử lý là thông tin nội bộ; Agent thấy trên ticket mình phụ trách, Manager thấy trên mọi màn hình ticket; Customer không thấy, API Customer không chứa.

## API, quyền và lỗi

**BR-32 — Kết quả lỗi.** 401 cho thiếu/sai danh tính demo; 403 cho sai vai trò hoặc Agent không phải phụ trách; 404 cho ticket không tồn tại hoặc Customer truy cập ticket người khác, kể cả cập nhật; 409 cho sai trạng thái/đã nhận/đạt giới hạn/Closed; 422 cho dữ liệu sai hoặc thiếu nội dung/lý do bắt buộc. Mã 409 riêng: `INVALID_TICKET_STATE`, `TICKET_ALREADY_ASSIGNED`, `AGENT_CAPACITY_REACHED`, `TICKET_CLOSED`, `REVIEW_REQUIRED`.

**BR-33 — Thứ tự kiểm tra.** Danh tính → vai trò → tìm ticket và quyền truy cập → người phụ trách → trạng thái/điều kiện nhận/giới hạn tải → nội dung bắt buộc. Điều kiện review được kiểm tra cùng bước trạng thái, sau khi xác nhận ticket đang In Progress. Ngoại lệ: tài nguyên review nội bộ, Customer luôn nhận 404 (BR-54). Ngoại lệ: FastAPI có thể trả 422 vì cấu trúc payload sai trước handler. Ngoại lệ: thao tác nhận ticket không đi qua bước kiểm tra người phụ trách; xem BR-37.

**BR-34 — Che sự tồn tại và hàng đợi.** Customer truy cập ticket không thuộc mình nhận 404. Agent truy cập hoặc thao tác ticket do Agent khác phụ trách nhận 403, không phụ thuộc việc Agent từng thấy ticket ở hàng đợi. Agent chỉ xem tóm tắt ticket New và chi tiết ticket mình phụ trách. Thao tác nhận ticket được quy định riêng tại BR-37.

**BR-37 — Nhận ticket đã có người nhận.** Thao tác nhận không đi qua bước kiểm tra người phụ trách. Ticket đã có Agent nhận trả 409 `TICKET_ALREADY_ASSIGNED`. Các thao tác khác (nhắn, ghi chú, chuyển trạng thái, xem chi tiết) của Agent không phải người phụ trách trả 403. Thứ tự kiểm tra khi nhận: ticket Closed trả 409 `TICKET_CLOSED` (BR-51); ticket đã có người nhận trả 409 `TICKET_ALREADY_ASSIGNED`; Agent đạt giới hạn tải trả 409 `AGENT_CAPACITY_REACHED`.

**BR-43 — Tin nhắn và ghi chú của Agent ở New.** Agent nhắn hoặc ghi chú khi ticket New trả 403.

**BR-44 — Tin nhắn và ghi chú của Agent ở Resolved hoặc Closed.** Agent nhắn hoặc ghi chú khi ticket Resolved trả 409 `INVALID_TICKET_STATE`; khi ticket Closed trả 409 `TICKET_CLOSED`.

**BR-45 — Nhận ticket đã được nhận khi đầy tải.** Khi nhận ticket đã có Agent nhận và Agent đang đạt giới hạn tải, trả 409 `TICKET_ALREADY_ASSIGNED`; điều kiện cấp ticket được kiểm tra trước, ngoại trừ ticket Closed, xem BR-51.

**BR-50 — Lỗi thao tác Customer và xem chi tiết Agent.** Customer nhắn khi ticket Resolved trả 409 `INVALID_TICKET_STATE`; khi Closed trả 409 `TICKET_CLOSED`. Customer xác nhận hoặc từ chối khi ticket không ở Resolved trả 409 `INVALID_TICKET_STATE`; khi Closed trả `TICKET_CLOSED`. Customer truy cập ticket không thuộc mình vẫn là 404, kiểm tra trước trạng thái theo BR-33. Agent xem chi tiết ticket New chưa nhận hoặc ticket do Agent khác phụ trách trả 403.

**BR-51 — Lỗi nhận ticket Closed.** Agent nhận ticket đã Closed trả 409 `TICKET_CLOSED`; kiểm tra trạng thái Closed trước `TICKET_ALREADY_ASSIGNED` và `AGENT_CAPACITY_REACHED`. Giao diện vô hiệu hóa nút nhận với ticket đã được nhận hoặc đã Closed; đây chỉ là hành vi giao diện, backend vẫn phải trả lỗi như trên theo BR-06.

## Báo cáo

**BR-35 — Nguyên tắc báo cáo.** Mỗi chỉ số phải ghi kỳ, bộ lọc, tử số và mẫu số. Mẫu số bằng 0 hiển thị “không có dữ liệu”. M-02 và M-03 luôn có dòng “Còn N ticket chưa Closed, chưa tính vào các tỷ lệ này”. M-04 hiển thị cạnh các tỷ lệ. Không có điểm tổng hợp hoặc xếp hạng Agent. M-07 là ảnh chụp tại `as_of`, danh sách các lượt review, không có mẫu số.

| Mã | Chỉ số | Công thức/quy tắc cơ bản |
|---|---|---|
| M-01 | Tỷ lệ phản hồi đầu đúng SLA | Chọn theo ngày tạo; ticket met / ticket met hoặc breached tại `as_of`; pending báo riêng. |
| M-02 | Tỷ lệ Closed đạt SLA giải quyết | Chọn theo ngày Closed; Closed có kết quả met / ticket Closed trong kỳ. |
| M-03 | Ticket từng bị từ chối | Chọn theo ngày Closed; ticket Closed trong kỳ có ≥1 lần từ chối / ticket Closed trong kỳ. |
| M-04 | Ticket chưa Closed vi phạm SLA | Ảnh chụp tại `as_of`, không có mẫu số. Danh sách ticket chưa Closed có ít nhất một đồng hồ breached, gồm hai cột cờ `first_response_breached` và `resolution_breached`; có thể gồm ticket Resolved giải quyết trễ; ticket vi phạm phản hồi đầu vẫn nằm trong danh sách đến khi Closed. |
| M-05 | Resolved chờ xác nhận | Ảnh chụp tại `as_of`, không có mẫu số: số ticket đang Resolved và thời gian chờ theo giờ lịch từ lần vào Resolved gần nhất đến `as_of`. |
| M-06 | Tải Agent | Ảnh chụp tại `as_of`, không có mẫu số: số ticket theo trạng thái và mức tải: <3, =3, >3. |
| M-07 | Chờ Manager review | Ảnh chụp tại `as_of`, danh sách các lượt có `review_requested_at <= as_of`, không có mẫu số. Thời gian chờ Manager theo giờ lịch tính đến thời điểm sớm hơn giữa `review_completed_at` và `as_of`; review hoàn thành sau `as_of` vẫn mở tại `as_of`. Hiển thị phần chờ trùng với khoảng SLA giải quyết đang chạy trong giờ làm việc (giây làm việc), SLA giải quyết đã breached trước khi yêu cầu review hay vượt hạn trong lúc chờ. |

**BR-42 — Đánh giá Agent và đọc báo cáo.** Đánh giá Agent xem mức độ trễ, chất lượng giải quyết và bối cảnh; không tự quy lỗi khi ticket đã trễ lúc nhận hoặc Customer từ chối khi hết ngân sách. Báo cáo đọc kết quả SLA cùng tỷ lệ Customer từ chối; không có điểm tổng hợp hoặc xếp hạng Agent. M-07 cung cấp bối cảnh chờ Manager; không tự quy lỗi hoặc miễn trách nhiệm cho cá nhân nào chỉ từ các khoảng thời gian này.

## Escalation sau nhiều lần Customer từ chối

**BR-52 — Vòng đời escalation.** `rejection_count` là số lần Customer từ chối ở Resolved, cộng dồn suốt vòng đời ticket; tin nhắn thông thường không tính và giá trị này dẫn xuất từ `ticket_events` (BR-28). Từ lần từ chối thứ 3 trở đi, mỗi lần từ chối tạo một lượt review mới; ngưỡng 3 là cấu hình demo. Ticket vẫn về In Progress theo BR-08, Agent hiện tại tiếp tục phụ trách và ticket gắn cờ “Cần Manager can thiệp”; hai lần từ chối đầu xử lý bình thường. Ghi nhận từ chối, chuyển về In Progress và tạo lượt review phải nằm trong cùng một giao dịch. Mỗi lượt xử lý có tối đa một review; mỗi ticket có tối đa một review đang mở.

**BR-53 — Chặn Resolved khi review mở.** Khi còn review chưa hoàn thành (`review_completed_at` rỗng), Agent không được chuyển Resolved và nhận 409 `REVIEW_REQUIRED`. Chỉ được báo Resolved lại sau khi Manager ghi phương án hợp lệ. Nếu Customer lại từ chối, cần review mới. Ticket không tự đóng; chỉ Customer xác nhận mới Closed. Xem BR-57.

**BR-54 — Quyền review của Manager.** Manager được ghi `handling_plan` cho review đang mở. Manager không nhắn công khai, không nhận ticket, không bấm Resolved. Agent ghi phương án nhận 403. Với tài nguyên review nội bộ, Customer luôn nhận 404, kể cả ticket thuộc mình; không trả dữ liệu cho phép suy ra review tồn tại. Xem BR-58.

**BR-55 — Dữ liệu review.** Mỗi lượt review là một bản ghi riêng trong `ticket_reviews`: `review_requested_at` (bắt đầu yêu cầu, đồng thời chặn Resolved), `review_completed_at` (Manager ghi phương án hợp lệ và gỡ chặn), `reviewed_by`, `handling_plan`, `resolution_cycle_id`. `handling_plan` gồm nguyên nhân chưa giải quyết được và hướng xử lý tiếp theo (đều bắt buộc), `needs_expert_input` (boolean) và ghi chú ý kiến chuyên môn (tùy chọn); thiếu trường bắt buộc trả 422. Đây là thông tin nội bộ. `needs_expert_input` chỉ là cờ và ghi chú nội bộ, không tạo yêu cầu, thông báo, phân công nhóm kỹ thuật hoặc chuyển Agent; phối hợp thực tế diễn ra ngoài hệ thống, không mô phỏng trong v1.0. Sự kiện review được ghi bổ sung vào `ticket_events`.

**BR-56 — SLA và review.** Chờ Manager review không tạm dừng, không reset, không cấp thêm thời gian SLA. Lưu thời điểm yêu cầu và hoàn thành review để báo cáo M-07, tách bối cảnh chờ Manager khỏi kết quả SLA.

**BR-57 — Waiting khi review mở.** Khi review đang mở, Agent phụ trách được chủ động chuyển ticket In Progress sang Waiting for Customer nếu thỏa điều kiện BR-08; chỉ Resolved bị chặn theo BR-53. Khi Customer trả lời, ticket về In Progress và review vẫn mở. Manager được ghi phương án cho review đang mở ở cả In Progress và Waiting for Customer. Đồng hồ giải quyết tạm dừng ở Waiting for Customer theo BR-20 như thường lệ; thời gian chờ Manager trong M-07 vẫn tính theo giờ lịch.

**BR-58 — Lỗi ghi phương án khi không có review mở.** Manager ghi phương án khi ticket không có review mở trả 409 `INVALID_TICKET_STATE`; ticket Closed trả 409 `TICKET_CLOSED`. Review đã hoàn thành không còn là review mở. Thứ tự kiểm tra: danh tính, vai trò, truy cập (Customer luôn 404 với tài nguyên review, Agent 403), rồi trạng thái, rồi nội dung (422), theo BR-33 và BR-54.
