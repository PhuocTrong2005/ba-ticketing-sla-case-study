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
| D-25 | Làm rõ BR-23: dùng tổng giây đã tiêu để xác định ngân sách còn lại và deadline, sau đó đánh giá theo deadline áp dụng. | So trực tiếp giây đã tiêu với ngân sách. | Phát hiện khi rà soát: deadline 17:00:00, hoàn thành 17:00:01 vẫn breached; chủ dự án chấp nhận sửa. Wording được chỉnh thêm để xử lý Waiting/Resolved. | Đã chốt |
| D-26 | Thêm escalation bằng lượt review của Manager và cờ, giữ năm trạng thái. | Thêm trạng thái thứ sáu; chuyển Agent, nhóm kỹ thuật hay phân công mới (ngoài phạm vi v1.0). | Chủ dự án (diễn đạt lại): lặp lại cách xử lý cũ sau nhiều lần bị từ chối không giải quyết được vấn đề của khách. | Đã chốt |
| D-27 | Kích hoạt từ lần từ chối thứ 3; mỗi lần từ đó tạo một review; ngưỡng 3 là cấu hình demo. | Chỉ kích hoạt từ lần thứ 4. | Cố vấn, chưa xác nhận: khách đã từ chối kết quả ba lần không nên chờ thêm một vòng. Chủ dự án chọn phương án này. | Đã chốt |
| D-28 | Quyền Manager từ chỉ đọc sang ghi phương án cho review đang mở (BR-05, BR-54). | Chưa ghi nhận. | Chủ dự án đề xuất. | Đã chốt |
| D-29 | SLA không đổi khi chờ Manager; báo cáo M-07 tách bối cảnh theo `as_of`. | Chưa ghi nhận. | Chủ dự án đề xuất; chi tiết M-07 do rà soát bổ sung. | Đã chốt |
| D-30 | Hỗ trợ chuyên môn chỉ là cờ và ghi chú nội bộ; phối hợp ngoài hệ thống. | Chưa ghi nhận. | Chủ dự án đề xuất. | Đã chốt |
| D-31 | Agent được chuyển Waiting khi review mở (BR-57). | Chặn mọi chuyển trạng thái khi review mở. | Chưa ghi nhận lý do của chủ dự án; chủ dự án chấp nhận đề xuất của cố vấn. | Đã chốt |
| D-32 | Mã lỗi Manager ghi phương án khi không có review mở theo BR-58. | Chưa ghi nhận. | Chủ dự án chấp nhận đề xuất của cố vấn. | Đã chốt |
| D-33 | Tách điều kiện chặn: nhóm 1 đến 11 chặn logic tính SLA chính; nhóm 12 chặn logic tính bối cảnh M-07; workflow review không bị chặn. Điều kiện hoàn thành v1.0 vẫn cần đủ 12 nhóm có ca verified. | Để 12 nhóm cùng chặn toàn bộ logic SLA. | Chủ dự án ủy quyền, cố vấn đề xuất: escalation không đổi cách tính SLA (BR-56); phần tính bối cảnh M-07 là phép tính mới cần đáp án riêng. | Đã chốt |
| D-34 | BR-39: hoàn tất trễ hiển thị `breached`. | `none` cho đồng hồ hoàn tất. | Chủ dự án chọn khi rà ca SLA-09. | Đã chốt |
| D-35 | BR-39: cảnh báo theo giây làm việc còn lại, không phụ thuộc `as_of` trong/ngoài giờ. | Chưa ghi nhận. | Chủ dự án chọn khi rà ca SLA-12. | Đã chốt |
| D-36 | BR-25: cắt phần dưới giây, không làm tròn; đầu vào thô lưu riêng. | Làm tròn. | Chủ dự án chọn khi rà ca SLA-13. | Đã chốt |
| D-37 | Định dạng file kịch bản là JSON (`tests/sla/sla-scenarios.json`), vì JSON lồng trong CSV dễ hỏng khi sửa bằng Excel. | Chưa ghi nhận. | Chủ dự án ủy quyền, cố vấn đề xuất. | Đã chốt |
| D-38 | BR-59: thao tác ngoài giờ vẫn được ghi nhận với timestamp thực; thao tác không sau deadline là met, thao tác sau deadline vẫn được ghi nhận nhưng breached. | Chưa ghi nhận. | Chủ dự án chốt khi rà SLA-17/SLA-18 ngày 06/10/2026; cách diễn đạt breached sau deadline nhất quán SLA-09/D-34. | Đã chốt |
| D-39 | Chốt OQ-20/OQ-21: số giây còn lại được kẹp về 0 khi vượt ngân sách; Waiting giữ `breached` nếu đã vi phạm, không cộng giây và không phát cảnh báo sắp đến hạn. | Số giây còn lại âm; hạ trạng thái vi phạm khi Waiting. | Chủ dự án chốt theo phương án đề xuất ngày 06/10/2026. | Đã chốt |
| D-40 | Ghi nhận nguồn gốc bộ 69 fixture: chủ dự án xác nhận; trợ lý AI chạy công cụ tham chiếu thay chủ dự án và báo cáo 69/69 PASS, 1.243 so sánh. | Coi xác nhận hoặc đối chiếu fixture là kết quả chạy backend/API/SQL/prototype, hoặc suy chủ dự án tự chạy công cụ. | Báo cáo đối chiếu do chủ dự án cung cấp ngày 06/10/2026; hash dữ liệu/script ghi tại README. Không bỏ gate hiện có và không khẳng định backend/API/SQL/prototype đúng. | Đã chốt |

Đề xuất mới không thuộc lịch sử quyết định này phải được ghi vào [open-questions.md](open-questions.md) đến khi chủ dự án chốt.

### Nhập nháp S1–S12 — 08/10/2026

Theo yêu cầu chủ dự án, nhập SLA-70…SLA-81 ở `draft`, giữ nguyên 69 ca verified. S12 dùng hạn G `2026-10-06T08:30:00+07:00` và `expected_rejected_actions` như SLA-61. Đây là ghi nhận phạm vi nhập liệu, không thay quy tắc nghiệp vụ/D-33, không xác nhận verified hoặc mở gate. Không suy phương pháp tính tay hay bằng chứng chủ dự án từ xác nhận con số. Checker gốc và audit lịch sử giữ nguyên; [báo cáo nhập](../tests/evidence/sla-draft-import.md) ghi giới hạn thực thi.

### Xác nhận SLA-70…SLA-81 — 08/10/2026

Chủ dự án nói “tôi đã verify bộ SLA đó” ngày 08/10/2026, chỉ rõ phạm vi 12 ca S1–S12 đã nhập thành SLA-70…SLA-81, gồm hạn G của SLA-81 là `2026-10-06T08:30:00+07:00`, và cho phép chuyển đúng 12 ca này sang `verified`. Codex ghi nhận xác nhận và chạy công cụ đối chiếu thay chủ dự án; không có thời điểm xác nhận chính xác đến giây hoặc mô tả phương pháp kiểm tra của chủ dự án. Đây là quyết định trạng thái fixture, không đổi quy tắc SLA/D-33 và không xác nhận backend/API/SQL/prototype. Đánh giá gate dựa trên nhánh coverage và kết quả đối chiếu thực tế, không suy từ tổng số ca verified.

### Bổ sung artefact cho D-40 — đối soát việc 1 ngày 06/10/2026

Giữ nguyên báo cáo lịch sử 69/69 PASS, 1.243 so sánh và vai trò chủ dự án xác nhận/trợ lý AI chạy thay. Lần đầu lúc 11:04:39 chỉ chạy [audit cấu trúc fixture](../tests/sla/audit_fixture_structure.py), 3.792 assertion; bằng chứng đó giữ nguyên. Sau khi nhận ZIP tại `D:\Download\SLA_Verification_Package.zip`, đã lưu [checker gốc](../tests/sla/reference/validate_sla_reference.py) và chạy trực tiếp trên fixture repo lúc `2026-10-06T12:51:30+07:00`: [69 PASS, 0 FAIL, 1.243 so sánh](../tests/evidence/sla-reference-results.json), exit code 0. Hash lịch sử fixture/script khớp byte trong gói; khác hash repo do wrapper metadata và định dạng, 69 scenario khớp toàn bộ. [Báo cáo hòa giải](../tests/evidence/sla-reconciliation.md) và [manifest SHA-256](../tests/evidence/sla-reconciliation.sha256) phân biệt các lần chạy và hash. Không thêm quyết định nghiệp vụ, không thay D-33, không coi fixture/reference check là bằng chứng backend/API/SQL/prototype/concurrency. Gate vẫn chưa được xác nhận mở do các nhánh coverage còn thiếu.

### Xác nhận SLA-82 và SLA-83 — 10/10/2026

Chủ dự án xác nhận và yêu cầu nhập đúng hai ca SLA-82/SLA-83 ở `verified`, giữ nguyên 81 ca cũ. Nguồn là nội dung hội thoại ngày 10/10/2026, không có giờ xác nhận đến giây, phương pháp tự tính hay bằng chứng chủ dự án chạy công cụ; `verified_at=null`. SLA-82 phủ resume Waiting ngay Chủ nhật; SLA-83 phủ hết ngân sách nhưng chưa breached, resume ngoài giờ, pending/due tại 08:00:00 và breached/breached tại `as_of=08:00:01`. Codex chỉ ghi nhận đáp án và chạy đối chiếu tham chiếu riêng. Không đổi chính sách, schema, quy tắc SLA hay tiêu chí gate D-33; kết luận gate phải dựa trên coverage và kết quả thực thi, không phải số lượng ca. Không xác nhận backend/API/SQL/prototype.

Sau đối chiếu thực tế 83/83 PASS và kiểm tra biên 08:00:00, gate logic SLA chính đủ điều kiện mở theo tiêu chí hiện hành; không thêm quyết định chính sách. Xem [coverage](spec/scenario-coverage.md) và [bằng chứng 83 ca](../tests/evidence/sla-verification-83.md). Kết luận chưa mở trong các bản đối soát trước là lịch sử.
