# Project brief

## 1. Tổng quan
Dự án cá nhân trong portfolio Business Analyst: phân tích, thiết kế và kiểm chứng một hệ thống quản lý ticket hỗ trợ khách hàng và SLA cho một doanh nghiệp phần mềm B2B giả định. Sản phẩm là giải pháp mẫu (prototype và backend mô phỏng), không phải hệ thống vận hành (BR-01).

## 2. Bối cảnh giả định (As-Is)
> Mô tả dưới đây là quy trình giả định phục vụ case study, không phải kết quả khảo sát hay số liệu của một doanh nghiệp thật.

Doanh nghiệp giả định cung cấp phần mềm cho khách hàng doanh nghiệp. Yêu cầu hỗ trợ đến qua email và tin nhắn, được nhân viên chuyển tay nhau và theo dõi bằng trí nhớ hoặc bảng tính riêng. Không có định nghĩa chung về "đã phản hồi" hay "đã giải quyết".

## 3. Vấn đề (giả định, định tính)
1. Yêu cầu bị bỏ sót hoặc không rõ ai chịu trách nhiệm.
2. Khách hàng khó biết tiến độ xử lý.
3. Nhân viên không biết nên ưu tiên yêu cầu nào.
4. Không có quy tắc thống nhất để đo thời gian phản hồi và giải quyết.
5. Một nhân viên có thể nhận quá nhiều việc trong khi người khác còn khả năng xử lý.
6. Nhân viên báo "đã giải quyết" nhưng khách chưa đồng ý.
7. Báo cáo dễ đánh đồng việc ticket trễ SLA với lỗi của nhân viên, kể cả khi ticket đã trễ từ trước lúc được nhận.
8. Khi khách từ chối kết quả nhiều lần, chỉ nhân viên phụ trách biết; không ai ở cấp quản lý xem xét lại cách giải quyết, nên cách xử lý cũ tiếp tục lặp lại.

## 4. Giải pháp đề xuất
Mỗi yêu cầu là một ticket có mã, người tạo, mức ưu tiên cố định, trạng thái và lịch sử sự kiện. Ticket chưa có người phụ trách khi ở New; sau khi được nhận, có đúng một Agent phụ trách trong suốt vòng đời (BR-14). Mỗi ticket có hai đồng hồ SLA (phản hồi đầu tiên, giải quyết). Hệ thống gồm:
- Quy trình năm trạng thái (BR-07, BR-08).
- Phân quyền Customer, Agent, Manager (BR-03 đến BR-06).
- Nhận ticket có giới hạn tải (BR-12 đến BR-16).
- Bước khách xác nhận hoặc từ chối kết quả (BR-08, BR-09).
- Escalation: từ lần từ chối thứ 3, Manager xem xét và ghi phương án trước khi Agent báo Resolved lại (BR-52 đến BR-58).
- Báo cáo có định nghĩa chỉ số (BR-35).

## 5. Mục tiêu và bằng chứng
Đây là tiêu chí của giải pháp mẫu, không phải tuyên bố cải thiện doanh nghiệp thực.

| Mã | Mục tiêu | Bằng chứng cần có |
|---|---|---|
| G-01 | Ticket luôn có đúng một người phụ trách sau khi nhận | BR-14, BR-15; hai ca nhận đồng thời đạt; lịch sử phân công |
| G-02 | Gợi ý thứ tự ưu tiên xử lý rõ ràng | BR-12, BR-36; màn hình hàng đợi |
| G-03 | SLA tính đúng theo lịch làm việc | BR-17 đến BR-26, BR-38, BR-46, BR-48; bộ kịch bản SLA nhóm 1 đến 11 có đáp án được chủ dự án xác nhận `verified`; kết quả kiểm thử thực tế của logic SLA khớp các đáp án này. Nhóm 12 kiểm chứng escalation và bối cảnh M-07 tại G-08 |
| G-04 | Bảo vệ thông tin khách hàng | BR-03, BR-06, BR-32 đến BR-34, BR-49; test API về 404, 403 và ghi chú nội bộ |
| G-05 | Kết quả giải quyết được khách xác nhận | BR-08, BR-09; ca Resolved được xác nhận và bị từ chối |
| G-06 | Cung cấp dữ liệu theo dõi Agent có bối cảnh | Snapshot SLA lúc nhận (BR-16); các truy vấn M-01 đến M-07 khớp dữ liệu mẫu (BR-35, BR-42); báo cáo thể hiện thời gian chờ Manager và không tự quy trách nhiệm cá nhân |
| G-07 | Dữ liệu SLA kiểm tra lại được | BR-27 đến BR-29, BR-47; test dựng lại khoảng chạy từ sự kiện gốc |
| G-08 | Từ chối lặp lại buộc Manager xem xét lại cách giải quyết | BR-52 đến BR-58; test `REVIEW_REQUIRED`, quyền ghi phương án, Agent chuyển Waiting khi review mở, lỗi khi không có review mở, tính nguyên tử của lần từ chối tạo review; nhóm 12 và M-07 |

## 6. Giả định
| Mã | Giả định |
|---|---|
| AS-01 | Doanh nghiệp, As-Is, khách hàng và dữ liệu đều giả định. |
| AS-02 | Ba Agent và một Manager trong dữ liệu demo chỉ để thể hiện chọn việc, phân bố tải và xử lý đồng thời, không phải kết luận về nhân sự thực. |
| AS-03 | Giới hạn 3 ticket In Progress là cấu hình demo. |
| AS-04 | Chính sách SLA (D-03) và lịch làm việc (D-02) là giả định của case study. |
| AS-05 | Danh tính demo cố định, không có đăng nhập thật (BR-06). |
| AS-06 | Các bên liên quan chưa được phỏng vấn; nhu cầu của họ là suy luận. |
| AS-07 | Dữ liệu mẫu được thiết kế theo kịch bản, không sinh ngẫu nhiên. |
| AS-08 | Ngưỡng 3 lần từ chối để kích hoạt review của Manager là cấu hình demo (BR-52). |
| AS-09 | Việc phối hợp hỗ trợ chuyên môn nếu có diễn ra ngoài hệ thống và không được mô phỏng (BR-55). |

## 7. Ràng buộc
| Mã | Ràng buộc |
|---|---|
| C-01 | Một người thực hiện, có Codex hỗ trợ theo quy tắc `AGENTS.md`. |
| C-02 | Công nghệ đã chốt (BR-02): prototype HTML/CSS/JS tĩnh, FastAPI + SQLite, pytest, Postman. |
| C-03 | Prototype và backend không kết nối với nhau. |
| C-04 | Không dùng dữ liệu hoặc quy trình của doanh nghiệp thật. |
| C-05 | Không viết logic SLA chính trước khi có ca `verified` bao phủ nhóm 1 đến 11; logic tính bối cảnh M-07 chờ nhóm 12 có ca `verified`; workflow review không bị chặn bởi điều kiện này (D-33). |
| C-06 | Chỉ có một Manager demo, không có người thay thế và không tự leo thang tiếp. |

## 8. Tài liệu liên quan
[Business rules](../spec/business-rules.md), [Decision log](../decision-log.md), [Open questions](../open-questions.md), [Scope](scope.md), [Stakeholders](stakeholders.md).
