# Áp dụng backend vào repo trên máy chủ dự án

Bản thay đổi dựa trên commit `9688b7889df0d91b1bb9d26d3626b283945d9d5e`. Patch chứa tài liệu đã duyệt, backend, SQL, test và bằng chứng; không chứa SQLite demo, virtualenv, secrets hoặc thay đổi fixture.

Đưa file patch cho Codex cùng nội dung:

```text
Áp dụng patch backend vào repo ba-ticketing-sla-case-study trên máy này.
1. Đọc AGENTS.md và kiểm tra git status. Giữ mọi thay đổi có sẵn.
2. Kiểm tra baseline và chạy git apply --check với đúng đường dẫn patch tôi cung cấp.
   Nếu patch xung đột, không dùng force/reset; báo file và điểm lệch, tiếp tục phần độc lập.
3. Nếu kiểm tra đạt, áp dụng patch; không thay đổi bất kỳ expected_* hoặc review_status trong 83 fixture.
4. Tạo/activate virtualenv Windows Python 3.12, pip install -r requirements.txt,
   chạy python -m pytest. Ghi bằng chứng Windows vào file mới; không ghi đè bằng chứng Linux.
5. Chạy python -m uvicorn backend.app:app --port 8000, kiểm tra /docs và /openapi.json.
   Header danh tính demo: Customer 1/2, Agent 3/4/5, Manager 6. Không giả lập đăng nhập thật.
6. Báo danh sách thay đổi, kết quả thực chạy và phần còn thiếu.
Không thêm feature, đổi SLA, tự tạo PASS hoặc tuyên bố v1.0 hoàn thành.
Nhiệm vụ này chưa yêu cầu commit/push; báo lại trước khi cập nhật remote.
```

Lệnh áp dụng (thay đường dẫn ví dụ bằng nơi lưu thực):

```bash
git apply --check path/to/Backend_SLA.patch
git apply path/to/Backend_SLA.patch
```

Có thể dùng ZIP toàn bộ source để xem/chạy riêng; không chép thư mục .git hoặc ghi đè repo có thay đổi chưa lưu. Bằng chứng Linux ở tests/evidence/backend-test-report.md; Windows chưa được chạy trong phiên triển khai này.
