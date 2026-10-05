# Hướng dẫn làm việc cho agent

- Nguồn sự thật: `docs/spec/business-rules.md`, `docs/spec/codes.md`, `docs/decision-log.md`.
- Không tự thêm tính năng, đổi phạm vi, hoặc đổi quy tắc SLA/múi giờ/định dạng thời gian nếu chưa cập nhật decision log.
- Ở nhiệm vụ sau, chỉ đề xuất kịch bản và `expected_*` ở trạng thái `draft` khi chủ dự án yêu cầu. Không đổi đáp án `verified`, không tự chuyển `review_status` sang `verified`, và không tự tạo kết quả kiểm thử, bug hay bằng chứng giả.
- Không viết logic tính SLA chính trước khi có kịch bản verified bao phủ các nhóm trong `docs/spec/scenario-coverage.md` và bảng nhóm → mã kịch bản không còn nhóm trống. Được tạo schema, parser, skeleton và cấu trúc test.
- Thời lượng là giây nguyên với hậu tố `_seconds`; phần dưới giây bị cắt khi ghi, không làm tròn; đồng hồ phải inject được.
- Dữ liệu mẫu phải theo kịch bản, có mã tình huống; không sinh ngẫu nhiên.
- Khi mâu thuẫn hoặc thiếu thông tin: cập nhật `docs/open-questions.md`, dừng phần phụ thuộc và tiếp tục phần độc lập.
- Thứ tự thay đổi: tài liệu gốc → decision log → code → test → traceability. Tiền tố commit: `docs:`, `feat:`, `test:`, `fix:`.
- Code chỉ phục vụ chứng minh yêu cầu trong phạm vi v1.0.
- `event_id` do database cấp; client không được gửi.
- Dữ liệu SLA dẫn xuất không được sửa độc lập và phải dựng lại được từ sự kiện gốc.
- Không triển khai hành vi thuộc điểm còn mở trong `docs/open-questions.md` cho đến khi chủ dự án chốt.
