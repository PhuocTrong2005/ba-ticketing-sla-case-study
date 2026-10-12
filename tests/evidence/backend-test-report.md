# Backend implementation — kết quả thực thi

Baseline: `9688b7889df0d91b1bb9d26d3626b283945d9d5e`. Chủ dự án duyệt yêu cầu, thiết kế và backend trong hội thoại 12/10/2026. Thời điểm runtime, platform, hash và lệnh ở [run record](backend-run.json). Kết quả do trợ lý AI chạy, không phải chủ dự án tự thực thi.

## Kết quả

| Nhóm | Đạt | Phạm vi |
|---|---:|---|
| Engine SLA | 85 | 83 fixture, biên lịch, fallback tzdata |
| HTTP API | 87 | 83 fixture qua FastAPI/SQLite; quyền, validation, review, overload |
| Dữ liệu/đồng thời | 5 | Hai race nhận, rollback review, append-only/rebuild, giây thô/khoảng 0 |
| Báo cáo | 4 | M-01…07; cohort, filter, as_of quá khứ, mẫu số 0 |
| **Tổng** | **181** | **0 failure, 0 error** |

Lệnh: `python -m pytest -q --junitxml=tests/evidence/backend-junit.xml`. [JUnit](backend-junit.xml) ghi từng case. [Môi trường mới](backend-clean-start.json) và [JUnit riêng](backend-clean-junit.xml): 181 test đạt sau pip install trong virtualenv mới; Uvicorn chạy thật với /docs, /tickets, /openapi.json qua HTTP. Không suy đây là kiểm tra Windows hoặc production.

## Điều đã chứng minh

- Toàn bộ 83 fixture, expected và review_status giữ nguyên byte so với baseline. Engine mới dùng giao khoảng ngày làm việc, không import checker tham chiếu.
- Các ca HTTP fixture dùng ASGI TestClient gọi đầy đủ FastAPI handler/SQLite; kiểm tra socket Uvicorn được ghi riêng. Adapter thêm Customer 1, Agent 3, Manager 6 và nội dung xác định vì fixture không có actor/payload. Thử resolved_attempt thật trả 409 REVIEW_REQUIRED, không tạo event. A1/A2 được gọi API thật.
- SQL kiểm tra interval và snapshot đã lưu. Ảnh quá khứ đối chiếu bằng replay đến as_of; không nhầm cache hiện tại với lịch sử. Mỗi Resolved có snapshot ngân sách so với prefix đến đúng event_id.
- Hai race dùng threads, barrier, connection riêng và cùng file SQLite, kiểm tra response và database cuối. Không phải chạy tuần tự giả đồng thời.
- Fault injection có chủ đích kiểm tra rollback mọi bảng khi tạo review, không được ghi là bug nghiệp vụ thật. Event/policy có trigger chống sửa/xóa; projection bị làm hỏng trong test được dựng lại đúng.
- SQL tổng hợp trên TEMP snapshot theo as_of; M-07 tính giao khoảng bằng engine, không tuyên bố SQL thuần. Không có xếp hạng/quy lỗi cá nhân.

## Lỗi phát hiện và xử lý trong quá trình phát triển

1. WAL khởi tạo trong transaction gây SQLite error: chuyển setup WAL/schema ra ngoài transaction nghiệp vụ; test khởi tạo sau sửa đạt.
2. Clock inject lùi trước event gần nhất gây ValueError: chặn trước replay, trả 422 và giữ dữ liệu; test clock/rollback sau sửa đạt.
3. Lỗi test đã sửa: đọc cờ nội bộ từ response Customer (response phải không chứa); so cache hiện tại với as_of cũ có event tương lai. Sửa cách kiểm tra, không thay fixture hoặc nới chính sách.

Có một cảnh báo deprecation từ Starlette/AnyIO trong runtime, không có test failure và không phải cảnh báo nghiệp vụ sản phẩm.

## Giới hạn và việc tiếp

Demo identity không phải đăng nhập. Không có benchmark hiệu năng/uptime. Linux/Python 3.12 đã chạy; requirements có tzdata và test fallback không có IANA hệ thống, nhưng Windows chưa chạy thật. Prototype AC-32 planned; Postman/Newman, video và deploy chưa làm. Không đánh dấu hoàn thành toàn bộ v1.0.

Tiếp: áp dụng bản thay đổi vào repo trên máy chủ dự án, chạy lại Windows; sau đó prototype tĩnh bốn màn hình, Postman và demo, bám cùng BR.

Kiểm tra tài liệu mới/sửa: liên kết local và ID BR/AC/D hợp lệ. Bản evidence lịch sử được giữ nguyên byte, có tám link theo vị trí cũ; [chỉ mục lịch sử](history/README.md) cung cấp đường đọc đúng, không sửa nguồn lịch sử.
