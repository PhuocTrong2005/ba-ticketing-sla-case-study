# Stakeholder register

Các bên liên quan là giả định phục vụ case study và chưa được phỏng vấn. Nhu cầu và mức ảnh hưởng là suy luận của người phân tích (AS-06).

## 1. Người dùng hệ thống
| Bên | Vai trò | Nhu cầu | Ảnh hưởng | Cách tham gia trong v1.0 |
|---|---|---|---|---|
| Customer | Tạo và theo dõi ticket | Biết ticket có người phụ trách và tiến độ; xác nhận hoặc từ chối kết quả; không bị lộ dữ liệu cho người khác; khi từ chối nhiều lần có người xem xét lại | Cao | Persona demo và kịch bản UAT; xem thông tin ticket của mình, trạng thái và trao đổi công khai; không thấy cảnh báo, cờ escalation hoặc phương án nội bộ (BR-49) |
| Agent | Nhận và xử lý ticket | Biết ưu tiên việc nào; tải việc hợp lý; không bị tự động quy lỗi khi ticket đã trễ trước khi nhận hoặc đang chờ Manager; có hướng xử lý khi bị từ chối nhiều lần | Cao | Ba Agent demo; BR-13, BR-16, BR-42, BR-53 |
| Manager | Theo dõi tải, SLA, báo cáo; xem xét ticket bị từ chối nhiều lần | Thấy ticket vi phạm, Agent quá tải, ticket chờ xác nhận, ticket cần can thiệp; số liệu có cách xác định rõ, gồm tử số và mẫu số khi áp dụng; ghi phương án xử lý | Cao | Một Manager demo; màn hình báo cáo M-01 đến M-07; quyền ghi phương án (BR-54) |

## 2. Bên liên quan của doanh nghiệp giả định
Các bên dưới đây là stakeholder, không tự động trở thành vai trò ứng dụng. V1.0 chỉ có ba vai trò Customer, Agent, Manager.

| Bên | Quan tâm | Ảnh hưởng | Cách xử lý trong v1.0 |
|---|---|---|---|
| Người bảo trợ (trưởng bộ phận hỗ trợ/vận hành, giả định) | SLA đo được, báo cáo đáng tin, đánh giá Agent không bất công, vòng lặp từ chối được kiểm soát | Cao | Chính sách SLA và định nghĩa chỉ số trong decision log; không điểm tổng hợp hay xếp hạng (BR-42); escalation (D-26 đến D-30). Không có tài khoản riêng |
| Đội IT/bảo trì (giả định) | Hệ thống dễ chạy, dữ liệu dựng lại được, quyền rõ | Trung bình | Tài liệu dữ liệu và API; quyền kiểm tra ở backend; test dựng lại từ sự kiện gốc. Không có tài khoản riêng |
| Quản lý tài khoản khách hàng (giả định) | Cam kết SLA với khách; biết ticket nào đang trễ hoặc bị từ chối nhiều lần | Trung bình | Nhu cầu thông tin được ghi nhận trong phân tích. V1.0 không có tài khoản hoặc quyền riêng cho vai trò này; việc chia sẻ thông tin phù hợp qua Manager nằm ngoài hệ thống mô phỏng |
| Chuyên gia kỹ thuật/nhóm chuyên môn (giả định) | Được hỏi ý kiến khi ticket cần chuyên môn | Thấp trong v1.0 | Ngoài hệ thống: chỉ có cờ và ghi chú nội bộ, không thông báo hay phân công (BR-55, D-30). Không có tài khoản riêng |

## 3. Bên liên quan đến portfolio
Không phải stakeholder của doanh nghiệp giả định.

| Bên | Quan tâm | Cách xử lý |
|---|---|---|
| Nhà tuyển dụng, người đọc portfolio | Hiểu vấn đề, quyết định và bằng chứng kiểm chứng | README trung thực về phần chạy thật và phần mô phỏng |

## 4. Mối quan tâm có thể xung đột
| Xung đột | Cách xử lý |
|---|---|
| Manager muốn thấy ticket trễ, Agent không muốn bị quy lỗi | Snapshot SLA lúc nhận (BR-16); báo cáo đọc cùng bối cảnh (BR-42) |
| Customer muốn biết tiến độ, cảnh báo nội bộ có thể gây hiểu lầm | Customer không thấy cảnh báo nội bộ (BR-49) |
| Agent muốn có thời gian, khách muốn nhanh | Từ chối giữ ngân sách còn lại, không reset (BR-21) |
| Agent cần Manager ghi phương án mới được báo Resolved, nhưng SLA vẫn chạy trong lúc chờ | SLA không đổi (BR-56); M-07 ghi thời gian chờ làm bối cảnh, không tự quy lỗi hay miễn trách nhiệm cho ai (BR-42) |
| Chỉ có một Manager, review có thể chờ lâu | Chấp nhận là giới hạn v1.0 (C-06); không thêm cơ chế thay thế |
