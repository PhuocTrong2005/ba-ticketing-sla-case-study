# Prototype ticketing / SLA

HTML/CSS/JavaScript thuần, bốn view trong một shell. Không cần Node để xem, không gọi FastAPI/database. Danh tính demo cố định Customer 1/2, Agent 3/4/5, Manager 6; selector không là đăng nhập thật. Nguồn phê duyệt: [spec](../docs/05-prototype/prototype-spec.md), D-44; nguồn nghiệp vụ BR/codes/decision log hiện hành.

## Mở cục bộ

Từ thư mục repository, dùng Python đã có trong môi trường:

```powershell
& .\.venv\Scripts\python.exe -m http.server 8765 --bind 127.0.0.1
```

Mở <http://127.0.0.1:8765/prototype/>. Dừng server bằng Ctrl+C. Không mở bằng `file://`: ES modules cần HTTP. Mọi asset là relative. Pages xuất bản nội dung `prototype/` tại gốc project subpath: [mở demo](https://phuoctrong2005.github.io/ba-ticketing-sla-case-study/), không thêm `/prototype/`. Kết quả triển khai và kiểm tra công khai ghi riêng trong [báo cáo Pages](../tests/evidence/pages-report-20261013.md).

Clock đứng yên, UTC+7 có giây. Đổi danh tính không tiến clock hoặc thay dataset. Nút tiến / ô giờ chỉ đi về phía trước; “Phiên làm việc kế tiếp” tới 08:00 ngày làm việc phù hợp. Để thử một nhánh khác từ đầu, dùng **Khôi phục bộ mẫu** trong **Điều khiển demo**. Tải kịch bản / đổi biến thể / khôi phục thay thế dữ liệu hiện hành, đã ghi rõ trên UI. localStorage của Pages độc lập với localhost; không cần chạy backend để mở demo.

UX được chủ dự án duyệt ngày 13/10/2026 (D-45): controls mở mặc định; bấm tiêu đề hoặc dùng Tab rồi Enter/Space để mở/thu gọn. Khi thu gọn vẫn thấy danh tính, nhóm/biến thể và clock UTC+7; thao tác này không ghi event, đổi clock hoặc danh tính. Hướng dẫn gần nội dung vẫn hiện, bám sáu nhóm/biến thể và vai trò đang chọn; Customer chỉ nhận hướng dẫn công khai. Hướng dẫn không tự thao tác hay xác nhận hoàn thành.

Nội dung/ghi chú 14–16px, chữ phụ có tương phản cao hơn, bảng cuộn trong vùng riêng ở 390px. SLA hiển thị Đạt SLA / Vi phạm SLA / Chưa có kết quả cùng Đang chạy/Tạm dừng, giữ vi phạm khi Waiting. Nhãn báo cáo giữ mã M-01…M-07; dòng N có giải thích ngắn và mục mở rộng. Manager dùng Review mở / Báo cáo / Tải Agent / Tất cả ticket để nhảy và đưa focus tới heading, giữ bộ lọc/dữ liệu/clock. M-04 vẫn cạnh các tỷ lệ; M-06 ghi rõ tải qua tất cả ưu tiên, M-07 mô tả bối cảnh bằng lời, không quy lỗi.

Lưu trong localStorage namespace `ba-ticketing.prototype.v1`, `schema_version=1`: metadata ticket, clock, events và danh tính. Không lưu projection/report/cache SLA. Đọc lại xác minh sự kiện qua controller; dữ liệu hỏng hoặc schema khác cần khôi phục. Storage không khả dụng/quota thì tiếp tục trong memory và có nhãn thông báo. Sequence cục bộ `demo_event_seq` không là database `event_id`.

## Thử sáu nhóm demo

Mỗi dòng là hướng dẫn thao tác bằng tay, không tự thực hiện theo clock. Thời điểm đều UTC+7 ngày 05/10/2026, trừ nơi ghi ngày khác. Sau đổi danh tính, mở lại ticket từ danh sách.

| Nhóm | Bước thao tác |
|---|---|
| DEMO-01 | Customer 1 tạo High 09:00 → Agent 3 nhận 09:05, nhắn 09:10, Resolved 09:30 → Customer 1 xác nhận 09:35. Agent/Manager thấy P 600, G 1800 giây, met; Customer chỉ thấy công khai/Closed. |
| DEMO-02 | Ticket New mẫu 09:00 → Agent nhận 09:05, nhắn 09:10, Waiting 10:00, nhắn và note 10:15 (giữ Waiting) → Customer nhắn 11:00 → Agent thấy hạn 06/10 09:00, Resolved 11:30 (G 5400, còn 23400). |
| DEMO-03 | Ticket 08:00 → Agent nhận 08:05, nhắn 08:10, Resolved 14:00 → Customer từ chối 15:00 → Agent thấy G còn 7200, hạn 17:00; Resolved đúng hạn met. Khôi phục và làm lại để thử 17:00:01 breached. |
| DEMO-04 | Prehistory SLA-61 tới từ chối lần 3, 11:10 → Agent thấy Resolved bị chặn; Waiting 11:30 → Manager ghi nguyên nhân/hướng xử lý 12:00, trạng thái vẫn Waiting → Customer nhắn 12:30 mới resume. Agent đọc phương án trên chi tiết; Customer không có dữ liệu nội bộ. |
| DEMO-05 | Agent 3 tải 3 và New #5 bị chặn → Customer từ chối #1 đưa tải 4 → Agent chuyển #2 Waiting (tải 3, vẫn chặn), #3 Waiting (tải 2), nhận #5. Prehistory nhận/Resolved #1 trước ba ticket In Progress. |
| DEMO-06 | Biến thể T2 16:00: thử phản hồi 17:00 / khôi phục để thử 17:00:01. T6 09/10 16:59: hạn P T2 12/10 08:59. SLA-83: tới 06/10 08:00 due, +1 giây breached. Ngưỡng: từ 09:00 còn 3600 none; +1 giây 3599 soft; tới 09:45 còn 900 soft; +1 giây 899 emphasized. SLA-40: Waiting giữ breach và không cộng G. |

Manager dùng cùng dataset/clock. M-01…03 chọn ngày inclusive ở UI, chuyển thành kỳ [from, ngày sau ngày đến 00:00). M-04…07 chỉ snapshot; bộ lọc ưu tiên/Agent theo BR-63; M-06 chỉ Agent, tải tất cả ưu tiên. Không có as_of quá khứ trong UI. Engine/test vẫn bỏ sự kiện tương lai.

## Cấu trúc và kiểm chứng

- `sla.js`: lịch giây nguyên, deadline, warning, replay và bối cảnh M-07.
- `domain.js`: controller kiểm tra danh tính/quyền/state/content trước ghi event; lỗi không mutate.
- `seeds.js`: tình huống xác định, prehistory được dựng qua controller, không fixture expected.
- `reports.js`, `storage.js`: báo cáo từ replay, lưu/khôi phục và kiểm tra nguồn.
- `app.js`, `index.html`, `styles.css`: shell, hash navigation, forms, render text và responsive.

Harness test-only đọc fixture gốc qua static server, chạy JavaScript trong Edge; không dùng Python SLA/backend/checker làm kết quả thay thế. Adapter bổ sung actor/nội dung hợp lệ cho fixture toán học và thực thi rejected attempts riêng; không sửa fixture. Python chỉ phục vụ HTTP, điều khiển CDP, ghi kết quả/ảnh và hashes.

```powershell
& .\.venv\Scripts\python.exe tests/prototype/run_browser.py
```

Runner cần Edge ở vị trí cài mặc định Windows. Dùng profile tạm riêng, headless và `--no-sandbox` để renderer chạy được trong môi trường thực thi hạn chế; chỉ mở source cục bộ. Runner tự dừng browser/server của nó. Không thay dependencies hoặc backend. Test harness standalone tại `/tests/prototype/` cần runner để đáp ứng các checkpoint chụp ảnh.

Kết quả và ảnh thật: [báo cáo prototype](../tests/evidence/prototype-report-20261012.md), [clean-start từ clone mới](../tests/evidence/portfolio-clean-start-report-20261013.md). Kiểm tra browser là tự động/headless, không thay xác nhận UX của chủ dự án, thiết bị vật lý hoặc cross-browser. Các trạng thái chưa commit/Pages/Postman trong report cũ là lịch sử; Pages/Postman đã có bằng chứng riêng, video Chưa có và v1.0 chưa hoàn tất. Atomicity SQLite/hai race xem [backend report](../tests/evidence/backend-test-report.md), không gán PASS từ demo.

Bàn giao UX: [báo cáo và sáu ảnh](../tests/evidence/prototype-ux-report-20261013.md). Runner giữ 106 ca cũ và bổ sung UX-01…04; keyboard CDP thực, desktop 1280/1440px và mobile 390px. Tên run/ảnh chứa timestamp UTC; ngày bàn giao theo UTC+7.

**Checkout mới:** chạy `tests/prototype/run_browser.py` như trên là kiểm chứng runtime; không cần baseline/file local từ repo tác giả. `tests/prototype/audit_ux.py` là auditor của nhiệm vụ UX lịch sử, dùng `ux-baseline-20261013.json` gồm virtualenv/backup/thư mục thử và file local của mốc đó. Nó không là bước nghiệm thu clone mới và sẽ báo lỗi với các file không nên sao chép. Không tạo/sao chép các file đó để làm auditor đạt. Giữ nguyên auditor và record lịch sử; việc bảo toàn clean-start đối chiếu manifest source của chính clone mới, hash run, link/diff và file gốc. [DOC-CS-01 và evidence trước/sau sửa](../tests/evidence/portfolio-clean-start-report-20261013.md) phân biệt lỗi hướng dẫn với test UI.

Customer view-model/khối nội dung ticket không có SLA/notes/review. Các controls và hướng dẫn mô phỏng không là quyền production; mọi dữ liệu vẫn đọc được bằng DevTools. Manager chỉ ghi phương án; cờ chuyên môn không phát thông báo, phân công hoặc chuyển Agent.
