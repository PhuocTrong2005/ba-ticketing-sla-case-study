# Báo cáo đối chiếu 69 kịch bản SLA

**Kết quả: 69/69 ca khớp; 0 ca lệch; 1.243 phép so sánh trường dữ liệu.**

## Vai trò và nguồn gốc

- Chủ dự án: người yêu cầu, quyết định chính sách và xác nhận toàn bộ 69 ca thành verified qua hội thoại lúc 2026-10-06T09:42:31+07:00.
- Đáp án nháp và công cụ tham chiếu: được soạn với hỗ trợ AI.
- Thực thi lần kiểm tra trong báo cáo này: trợ lý AI chạy công cụ Python thay chủ dự án.
- Cách mô tả đúng: **Chủ dự án xác nhận kết quả kiểm chứng, có hỗ trợ AI và công cụ tự động.**
- Không ghi chủ dự án tự tính tay, tự viết bảng tính hoặc tự chạy công cụ khi chưa có bằng chứng về hoạt động đó.

## Cách tính và đối chiếu

Công cụ độc lập với backend: không import code dự án, không gọi API. Nó dựng lịch bằng danh sách từng giây làm việc hợp lệ, dùng tìm kiếm nhị phân để đếm khoảng [start, end) và tìm deadline, sau đó replay sự kiện gốc. Đây là cách khác với phép cộng từng đoạn trong bản nháp.

Calendar: thứ Hai–thứ Sáu 08:00–17:00 UTC+7, 32.400 giây/ngày, không nghỉ trưa và chưa xử lý ngày lễ. High: P/G = 3.600/28.800; Normal: 7.200/57.600. Còn lại kẹp 0; consumed giữ giá trị thật. So timestamp với deadline riêng để bắt vi phạm ngoài giờ và đúng mốc 17:00:01.

Mỗi ca được tính lại và so các trường: deadline P/G; consumed P/G; remaining P/G; status P/G; warning P/G; snapshot P/G lúc nhận; khoảng chạy G; trạng thái ticket; số lần từ chối; review đang mở; toàn bộ kết quả từng review; cờ kết quả cuối. SLA-61 kiểm tra thêm điều kiện từ chối Resolved với REVIEW_REQUIRED ở mức fixture nghiệp vụ, không phải gọi HTTP thật.

M-07 tính lại thời gian chờ lịch, phần giao với các khoảng G thực sự chạy trong giờ làm việc và bối cảnh vi phạm; giữ riêng R1/R2. Sự kiện sau as_of được bỏ qua; thứ tự cùng giây dùng seq. at_raw được đối chiếu với at đã cắt dưới giây.

## Kiểm tra khả năng phát hiện sai

Đã tạo bản sao tạm, cố ý làm sai năm ca: SLA-13 remaining, SLA-21 deadline, SLA-22 deadline, SLA-45 snapshot, SLA-64 thời gian trùng review. Công cụ phát hiện **5/5 ca bị sửa**, trả exit code 1. Đây là lỗi đưa vào để kiểm tra công cụ; không phải bug thực của backend hay lỗi mới trong bộ dữ liệu gốc. Bản sao tạm không làm thay đổi nguồn.

## Chạy lại

Đặt script và JSON trong cùng thư mục rồi chạy:

```bash
python validate_sla_reference.py sla_draft_data.json --report sla_validation_results.json
```

Không cần cài thư viện ngoài Python. Exit code 0 nghĩa là bộ kỳ vọng khớp công cụ tham chiếu; exit code 1 nghĩa là có chênh lệch. File JSON báo cáo có reference và mismatches của từng ca.

## Dấu vết lần chạy

- Thời điểm công cụ ghi: `2026-10-06T10:00:20+07:00`.
- SHA-256 dữ liệu nguồn: `91c3163a6dcb6707832e2e3c2f6ada4677a8f01e0e67ae6a8f0b5ad0af4c569f`.
- SHA-256 script: `764c284609d7074cbebc7c027576e9c8a16c9a8792456f8e4909ca221464f9ed`.
- Khi sửa nguồn hoặc script, phải chạy lại; báo cáo này chỉ có hiệu lực cho đúng hai hash nêu trên.

## Giới hạn và điều kiện chốt

**Có thể chốt:** tính toán/đối chiếu bộ 69 ca, xác nhận của chủ dự án, bằng chứng chạy công cụ tham chiếu và khả năng phát hiện các lỗi đã thử.

**Chưa được tuyên bố:** backend thực thi đúng, API/phân quyền/đồng thời đúng, truy vấn SQL/prototype đạt hoặc doanh nghiệp thật có cải thiện. Fixtures không có đầy đủ actor và nội dung bắt buộc; cần các ca API riêng.

Cả đáp án và công cụ có hỗ trợ từ cùng trợ lý AI. Hai cách tính khác nhau giúp bắt sai lệch nhưng không bảo đảm không có sai sót chung trong cách hiểu spec. Coverage trong repo chưa được truy cập trực tiếp nên chưa chứng minh mọi điều kiện phủ nhóm.

Nếu D-39/AGENTS vẫn yêu cầu chủ dự án tự tính tay hoặc kiểm chứng bằng bảng tính độc lập trước khi mở khóa code SLA chính, báo cáo tự động này không tự sửa điều kiện đó. Ghi đúng bằng chứng hiện có và tiếp tục phần tài liệu độc lập; không đổi quy định âm thầm.

## Kết quả từng ca

| Ca | Phép so sánh trường | Kết quả |
|---|---:|---|
| SLA-01 | 18 | PASS |
| SLA-02 | 18 | PASS |
| SLA-03 | 18 | PASS |
| SLA-04 | 18 | PASS |
| SLA-05 | 18 | PASS |
| SLA-06 | 18 | PASS |
| SLA-07 | 18 | PASS |
| SLA-08 | 18 | PASS |
| SLA-09 | 18 | PASS |
| SLA-10 | 18 | PASS |
| SLA-11 | 18 | PASS |
| SLA-12 | 18 | PASS |
| SLA-13 | 18 | PASS |
| SLA-14 | 18 | PASS |
| SLA-15 | 18 | PASS |
| SLA-16 | 18 | PASS |
| SLA-17 | 18 | PASS |
| SLA-18 | 18 | PASS |
| SLA-19 | 18 | PASS |
| SLA-20 | 18 | PASS |
| SLA-21 | 18 | PASS |
| SLA-22 | 18 | PASS |
| SLA-23 | 18 | PASS |
| SLA-24 | 18 | PASS |
| SLA-25 | 18 | PASS |
| SLA-26 | 18 | PASS |
| SLA-27 | 18 | PASS |
| SLA-28 | 18 | PASS |
| SLA-29 | 18 | PASS |
| SLA-30 | 18 | PASS |
| SLA-31 | 18 | PASS |
| SLA-32 | 18 | PASS |
| SLA-33 | 18 | PASS |
| SLA-34 | 18 | PASS |
| SLA-35 | 18 | PASS |
| SLA-36 | 18 | PASS |
| SLA-37 | 18 | PASS |
| SLA-38 | 18 | PASS |
| SLA-39 | 18 | PASS |
| SLA-40 | 18 | PASS |
| SLA-41 | 18 | PASS |
| SLA-42 | 18 | PASS |
| SLA-43 | 18 | PASS |
| SLA-44 | 18 | PASS |
| SLA-45 | 18 | PASS |
| SLA-46 | 18 | PASS |
| SLA-47 | 18 | PASS |
| SLA-48 | 18 | PASS |
| SLA-49 | 18 | PASS |
| SLA-50 | 18 | PASS |
| SLA-51 | 18 | PASS |
| SLA-52 | 18 | PASS |
| SLA-53 | 18 | PASS |
| SLA-54 | 18 | PASS |
| SLA-55 | 18 | PASS |
| SLA-56 | 18 | PASS |
| SLA-57 | 18 | PASS |
| SLA-58 | 18 | PASS |
| SLA-59 | 18 | PASS |
| SLA-60 | 18 | PASS |
| SLA-61 | 19 | PASS |
| SLA-62 | 18 | PASS |
| SLA-63 | 18 | PASS |
| SLA-64 | 18 | PASS |
| SLA-65 | 18 | PASS |
| SLA-66 | 18 | PASS |
| SLA-67 | 18 | PASS |
| SLA-68 | 18 | PASS |
| SLA-69 | 18 | PASS |