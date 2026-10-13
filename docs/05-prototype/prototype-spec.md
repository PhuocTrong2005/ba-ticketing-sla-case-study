# Đặc tả prototype tĩnh v1.0

Nguồn nghiệp vụ: main commit `eb8d483d8e3af914b487c1728b22b4108fa1397f`, BR-01…BR-64, codes, stories/AC đã duyệt và API contract. Chủ dự án đồng ý bốn màn hình, sáu nhóm kịch bản và điều khiển demo trong hội thoại ngày 12/10/2026. Tài liệu này cụ thể hóa cách trình bày/triển khai, không đổi nghiệp vụ. Chưa có giao diện hoặc kết quả kiểm thử prototype.

## 1. Mục tiêu và nền tảng

Các câu “chưa có giao diện/kết quả” và trạng thái planned trong phần gốc ghi nhận mốc lập spec 12/10. Kết quả thực thi sau đó ở [report gốc](../../tests/evidence/prototype-report-20261012.md); UX hiện hành theo mục 9/D-45 và [bàn giao UX](../../tests/evidence/prototype-ux-report-20261013.md). Không sửa kết quả lịch sử thành bằng chứng của lần chạy mới.

Người xem thực hiện được các quyết định Customer/Agent/Manager và thấy ảnh hưởng tới trạng thái, SLA, tải, review, báo cáo. HTML/CSS/JavaScript thuần; không backend Node, framework, đăng nhập hoặc API thật. Prototype độc lập với FastAPI/SQLite. Không thêm chuyển Agent, trạng thái thứ sáu, tự phân công, tự đóng, mở lại Closed hoặc thông báo thật.

Có thể dùng một index.html với bốn view điều hướng bằng hash; bốn view không bắt buộc bốn file HTML. Asset dùng đường dẫn tương đối để chạy dưới GitHub Pages project subpath. Chạy cục bộ qua static HTTP server; việc server phục vụ file không biến prototype thành hệ thống gọi API. GitHub Pages triển khai sau kiểm tra local, không tự deploy trong nhiệm vụ dựng giao diện.

Dòng cố định: **“Demo mô phỏng — dữ liệu trong trình duyệt, không gọi API.”** Bộ chọn danh tính nằm ở vùng “Điều khiển demo”, không là màn hình đăng nhập. Footer dẫn README/nguồn dự án và giải thích backend có bộ kiểm thử riêng.

## 2. Bố cục bốn màn hình

| View | Bố cục và trường | Hành động |
|---|---|---|
| Customer | Form tạo: title, description, priority. Danh sách của Customer đang chọn: mã, tiêu đề, ưu tiên, trạng thái, thời điểm tạo. Empty state có lời hướng dẫn. | Tạo và mở chi tiết. Không SLA, cảnh báo, ghi chú, review hoặc chỉ số nội bộ. |
| Chi tiết ticket | Header mã/tiêu đề/ưu tiên/trạng thái; mô tả; hội thoại công khai; vùng thao tác theo vai trò. Agent/Manager có SLA và thông tin nội bộ đúng quyền. | Bảng quyền ở mục 3. Mở trực tiếp bằng hash vẫn kiểm tra quyền; không chỉ ẩn nút. |
| Agent | Tải của Agent đang chọn với nhãn dưới giới hạn / đạt giới hạn / quá tải. Hai vùng: hàng đợi New và ticket phụ trách. | Nhận New; mở chi tiết ticket của mình. Queue đúng năm trường: mã, tiêu đề, ưu tiên, hạn phản hồi, thời điểm tạo; nút nhận là control, không thêm trường dữ liệu nội bộ. Gợi ý High → hạn phản hồi → tạo sớm, không ép thứ tự nhận. |
| Manager | Danh sách tất cả ticket; review mở; tải ba Agent; báo cáo M-01…M-07 trong các tab/section cùng view. | Mở chi tiết, xem ghi chú, ghi phương án cho review mở. Không xử lý ticket thay Agent. |

Bố cục desktop dễ đọc, co giãn trên mobile; bảng dài cuộn ngang có nhãn. Trạng thái/cảnh báo có chữ, không chỉ dựa màu. Form có label; button có focus; nội dung khách nhập render dưới dạng text, không chèn HTML. Ưu tiên luồng nghiệp vụ hơn animation hoặc trang trí.

## 3. Ma trận thao tác ở chi tiết

| Actor | New | In Progress | Waiting for Customer | Resolved | Closed |
|---|---|---|---|---|---|
| Customer của ticket | Nhắn công khai | Nhắn công khai, không đổi trạng thái | Nhắn công khai, tự về In Progress | Xác nhận; từ chối có reason | Chỉ xem |
| Agent phụ trách | Không có người phụ trách; chỉ xem queue | Nhắn, note, Waiting sau phản hồi đầu; Resolved nếu không review mở | Nhắn/note không tiếp tục SLA | Chỉ xem | Chỉ xem |
| Manager | Xem | Xem; hoàn tất review nếu có | Xem; hoàn tất review nếu có, không đổi trạng thái | Xem | Xem |

Agent đọc chi tiết chỉ khi được giao; Customer khác 404, Agent khác hoặc Agent mở New 403 theo controller mô phỏng. Customer không có block review/notes/SLA trong view-model hoặc DOM; dữ liệu toàn bộ demo vẫn có thể đọc bằng DevTools, không tuyên bố bảo mật production. Manager-only review resource không cấp cho Agent; Agent đọc phương án trong chi tiết của mình.

Ẩn hành động không thuộc vai trò, vô hiệu hóa hành động bị điều kiện nghiệp vụ chặn và ghi lý do ngắn. Controller phải kiểm tra lại dù gọi trực tiếp không qua nút. Gửi thiếu nội dung đúng kiểu trả lỗi nội dung; thứ tự nghiệp vụ theo BR-33. Frontend không giả lập validator FastAPI sai cấu trúc thành một kiểm tra HTTP thực.

### Form và phản hồi

- title/description, content, resolution_summary, reason: không trắng theo contract.
- handling_plan: unresolved_reason, next_action không trắng; needs_expert_input boolean; expert_note tùy chọn. Không phát thông báo hoặc phân công khi bật cờ.
- Lỗi hiển thị bằng lời rõ: “Ticket đã đóng”, “Agent đã đạt giới hạn nhận”, “Cần Manager hoàn tất review”…; không đưa chi tiết triển khai vào luồng người dùng.
- Customer từ chối chỉ thấy kết quả công khai và trạng thái, không thấy thông báo tiết lộ review vừa tạo.

## 4. SLA và trình bày nội bộ

Dùng đúng calendar T2–T6 08:00–17:00 UTC+7, không nghỉ trưa/ngày lễ; HIGH 3600/28800, NORMAL 7200/57600 giây. Phản hồi đầu chỉ một lần; Waiting tạm dừng giải quyết; Resolved dừng lượt; từ chối không reset/nhân đôi, giữ breach. Manager review không tự tạm dừng SLA.

Chi tiết Agent/Manager hiển thị hai đồng hồ: consumed_seconds, remaining_seconds, deadline đang áp dụng, trạng thái và mức cảnh báo. Waiting ghi “Tạm dừng”, không đưa deadline cũ như hạn đang chạy. Resolved ghi kết quả tạm thời, Closed kết quả cuối. Vi phạm đã có không biến mất khi Waiting/Resolved hoặc từ chối.

Thứ tự cảnh báo theo BR-39/61: breached trước; met hoặc paused chưa breached → none; đúng deadline đang chạy → due; trước deadline còn 0…899 → emphasized, 900…3599 → soft, từ 3600 → none. Ngân sách 0 ngoài giờ và trước deadline phiên kế tiếp vẫn là pending/emphasized. Sau deadline một giây breached, dù thời gian ngoài giờ không cộng consumed.

Bộ đếm giây chỉ trong chi tiết. Danh sách không đưa live countdown giây; dùng phút/giờ, dưới một phút ghi “Dưới 1 phút”. Không tự phát âm thanh, nhấp nháy hoặc toast cảnh báo SLA lặp. Không thêm công thức “trễ” chưa được BR định nghĩa; hiển thị timestamp deadline/hoàn tất và nhãn breached để người xem hiểu biên.

## 5. Điều khiển demo và lưu dữ liệu

Danh tính đúng backend: Customer 1/2, Agent 3/4/5, Manager 6. Chọn danh tính đổi view phù hợp; không tự tạo event hoặc tiến thời gian. Khi đang mở ticket không thuộc quyền mới, quay về dashboard phù hợp và bỏ nội dung chi tiết khỏi DOM.

Clock mô phỏng **đứng yên mặc định**, hiển thị rõ giờ/phút/giây và UTC+7. Controls: +1 giây, +15 phút, +1 giờ, tới bắt đầu phiên làm việc kế tiếp; thêm ô “Tiến tới thời điểm” UTC+7 có giây để tới chính xác mốc kịch bản, chỉ chấp nhận thời điểm không trước clock hiện hành. Không có nút lùi giờ trong cùng bộ dữ liệu; muốn về đầu dùng khôi phục hoặc tải kịch bản. Nhảy tới phiên kế tiếp phải tính ngày làm việc kế tiếp đúng lịch, không luôn cộng 24 giờ. Controls không cấp thêm ngân sách hoặc tự tạo phản hồi/resolution.

Lưu dataset hiện hành vào localStorage với namespace và schema_version: seed scenario đang chọn, clock, events, danh tính demo. Source là các events + policy; trạng thái/interval/report dựng lại, không sửa riêng cache. Prototype dùng demo_event_seq tăng cục bộ cho thứ tự cùng giây, **không tuyên bố đây là event_id do database cấp**. Database event_id và atomicity vẫn được chứng minh trong backend. Không sửa fixture để phù hợp browser sequence.

Đổi kịch bản tải lại bộ mẫu xác định của kịch bản đó; nút khôi phục quay lại seed/clock gốc. Vùng control ghi rõ thao tác thay thế dữ liệu demo hiện hành; không âm thầm reset khi đổi vai trò. Nếu storage lỗi, tiếp tục trong memory và ghi rõ không lưu được; schema không tương thích thì báo cần khôi phục, không diễn giải dữ liệu hỏng như dữ liệu hợp lệ. Không thêm nút xóa dữ liệu backend vì prototype không kết nối backend.

## 6. Sáu kịch bản và kết quả mong đợi

Mã DEMO chỉ là tình huống UI, không tạo SLA-84 hoặc thay expected của 83 fixture. Seed có prehistory phải dựng bằng sự kiện và được gắn nhãn “Dữ liệu mẫu dựng sẵn”, không phải log vận hành thật. Kỳ vọng bên dưới suy từ BR đã chốt; trạng thái test là planned.

| Mã | Đầu vào / cách thao tác | Kết quả nghiệp vụ cần kiểm tra |
|---|---|---|
| DEMO-01 Thành công | Clock T2 05/10/2026 09:00; tạo High. Agent nhận 09:05, phản hồi 09:10, Resolved 09:30, Customer xác nhận 09:35. | P consumed 600/met; G 1800/met; Closed. SLA nội bộ không hiện ở Customer. |
| DEMO-02 Waiting | High tạo T2 09:00; nhận 09:05, phản hồi 09:10, Waiting 10:00; Agent nhắn/note 10:15; Customer trả lời 11:00; Resolved 11:30. | Waiting giữ G 3600 giây; Agent message/note không resume. G cuối 5400/met, remaining 23400; deadline sau resume T3 09:00 vì 7h từ 11:00 vượt 17:00, còn 1h sang ngày kế tiếp. |
| DEMO-03 Từ chối | High tạo T2 08:00, Agent nhận 08:05, phản hồi 08:10; Resolved 14:00 (6h); từ chối 15:00. | G đã dùng 21600, còn 7200; deadline 17:00 cùng ngày. Không reset/nhân đôi; P đã hoàn tất không chạy lại. Resolve đúng 17:00 đạt nếu chưa có breach trước đó; dùng bản khôi phục riêng để thử 17:00:01. |
| DEMO-04 Review | Dựng cùng chuỗi SLA-61: tạo 08:00, nhận 08:05, phản hồi 08:10, Resolved 09:00/10:00/11:00; reject 09:10/10:10/11:10. | Review R1 mở lúc reject thứ 3; Resolved bị chặn, không tạo event. Agent Waiting 11:30 được phép; Manager ghi phương án 12:00 giữ Waiting; Customer trả lời 12:30 mới resume. Agent đọc phương án, Customer không thấy. |
| DEMO-05 Tải | Seed Agent 3 có ba In Progress và một ticket Resolved khác cùng Agent; thêm New. | Không nhận mới ở tải 3. Customer từ chối ticket Resolved → tải 4 hợp lệ. New vẫn không nhận. Đưa một ticket In Progress sang Waiting hợp lệ → tải 3; phải xuống 2 mới nhận mới. Không tuyên bố demo này kiểm thử race. |
| DEMO-06 Biên SLA/quyền | Có các biến thể chọn trong cùng nhóm: High tạo T2 16:00; High tạo T6 16:59; dùng nguồn SLA-83 cho resume Waiting 0 ngoài giờ. | T2 deadline P 17:00; phản hồi đúng hạn met, sau một giây breached ở bản chạy riêng. T6 16:59 → P T2 08:59. SLA-83 resume 18:00 sau Waiting đúng 17:00, G deadline hôm sau 08:00:00; tại 08:00 pending/due, 08:00:01 breached. Customer không thấy nội bộ; đổi Agent khác không thấy chi tiết. |

Seed DEMO-05 phải dựng prehistory hợp lệ: nhận/Resolved ticket đầu để giải phóng tải trước khi nhận ba ticket In Progress; những ticket sẽ dùng Waiting đã có phản hồi đầu. Không tạo lịch sử nhận mới khi đã đầy tải để đạt dataset mong muốn.

Các thời điểm hành động được người xem điều khiển; hướng dẫn từng bước trên demo chỉ gợi ý, không tự thực hiện nghiệp vụ. Cần bổ sung biến thể cảnh báo tại remaining 3600/3599/900/899 theo fixture verified, và sticky breach khi Waiting theo SLA-40. Dùng lại đầu vào hiện có, không tự xác nhận fixture mới.

Kiểm tra chéo DEMO-02: đã dùng 3600 trước Waiting, resume còn 25200; 11:00→17:00 = 21600, còn 3600 từ T3 08:00→09:00. Hạn đúng T3 09:00.

## 7. Báo cáo Manager

Báo cáo tính từ cùng dataset/clock, không hardcode tỷ lệ mẫu. M-01…03 chọn ngày từ/đến; UI ngày đến inclusive chuyển API-equivalent thành 00:00 ngày kế tiếp, [from,to). Priority/Agent filter theo BR-63. M-06 chỉ filter Agent, tải luôn qua tất cả ưu tiên.

M-01 met/(met+breached), pending riêng; M-02 Closed giải quyết met/Closed trong kỳ; M-03 Closed từng bị từ chối/Closed trong kỳ. Mẫu số 0 ghi “không có dữ liệu”. M-02/03 có N chưa Closed tại as_of cùng filter, không giới hạn ngày tạo và không gọi là phần bù mẫu số. M-04 hiện hai cờ breach trên ticket chưa Closed, đặt cạnh các tỷ lệ. M-05 thời gian chờ từ Resolved gần nhất theo giờ lịch; M-06 nhãn tải; M-07 từng review, giờ lịch chờ, giây chồng SLA trong giờ làm việc, before_request/during_wait/none. Không tự quy lỗi/ranking.

Clock chỉ tiến trong một dataset nên màn hình Manager mặc định báo cáo tại clock hiện hành; không thêm bộ chọn as_of quá khứ tùy ý trong UI. Engine vẫn phải bỏ event tương lai khi chạy fixture có as_of cũ. Kỳ/filter không ảnh hưởng snapshot admission của Agent.

## 8. Cấu trúc file và kiểm chứng

Cấu trúc đề xuất (Codex được tách file để dễ đọc, không đổi contract):

- prototype/index.html, styles.css: shell và bốn view.
- prototype/app.js: navigation/control/render; không fetch FastAPI.
- prototype/domain.js: controller, quyền, transitions và replay nghiệp vụ.
- prototype/sla.js: calendar/seconds/deadline/warnings.
- prototype/seeds.js: sáu nhóm tình huống xác định, không expected giả làm logic.
- prototype/README.md: chạy static, giới hạn và controls.
- tests/prototype/: kiểm thử engine/controller và kịch bản UI.
- tests/evidence/prototype-*: kết quả thực và ảnh sau khi chạy, không tạo trước.

JavaScript cần tính SLA để demo tương tác, không dùng expected_* như lookup runtime. Python backend giữ nguyên. Test harness có thể đọc fixture gốc từ tests/sla/sla-scenarios.json trên static server cục bộ và đối chiếu JS; không copy/sửa expected hoặc đóng gói các fixture như dữ liệu demo runtime. Nếu dùng Node để chạy test JS thì chỉ là công cụ dev, không backend hoặc điều kiện để xem GitHub Pages.

| Kiểm tra dự kiến | AC / BR | Bằng chứng cần có |
|---|---|---|
| JS replay khớp 83 fixture và các biên cảnh báo | AC-17…22; BR-17…26,38,39,46…48,59…61 | Output chạy JS thực, hash fixture; không thay bằng checker Python |
| Role/ownership, controller lỗi không mutate | AC-01…16,27,33,34; BR-62/64 | Test controller thực + kiểm tra DOM quyền |
| Sáu nhóm demo hoàn thành theo bước | AC tương ứng từng nhóm | Ảnh trạng thái trước/sau và log thao tác thực |
| Hiển thị/keyboard/mobile, không countdown danh sách | AC-32; BR-40/41/49 | Review UI thực, ảnh; không suy từ unit test |
| Reports khớp dataset và filter | AC-28…31; BR-35/63 | So kết quả UI/model với dữ liệu tính xác định |
| Không gọi API, tải/reset/switch không hỏng dữ liệu | BR-02/06 | Network inspection/local smoke và persistence test |

Hai ca đồng thời chỉ dẫn bằng chứng backend, không gán PASS prototype cho atomicity SQLite. Chưa có kết quả test prototype trong tài liệu này. Không có cơ sở tuyên bố v1.0 hoàn thành.

## 9. UX đã duyệt — 13/10/2026

Nguồn: yêu cầu chủ dự án trong hội thoại ngày 13/10/2026, D-45. Chỉ đổi trình bày, hướng dẫn và điều hướng; giữ BR, backend/dependencies, 83 fixture, seeds và công thức hiện hành.

- Controls dùng details/summary mở ở lần xem đầu; thu gọn vẫn hiện danh tính, mã nhóm/biến thể và clock UTC+7. Mở/thu gọn không ghi dữ liệu hoặc tiến clock. Banner mô phỏng luôn hiện.
- Nội dung/hướng dẫn 14–16px, nhãn chữ cho SLA/cảnh báo, focus-visible và bảng cuộn riêng ở mobile 390px; giữ màu/bố cục, không animation/âm thanh/cảnh báo lặp.
- Hướng dẫn sáu nhóm nằm gần nội dung, theo vai trò và biến thể seed. Customer chỉ thấy thao tác Customer/thông tin công khai. Hướng dẫn không thực hiện hành động, không xác nhận hoàn thành hoặc kết quả test.
- Nhãn: Đến hết ngày; Chưa có kết quả phản hồi đầu; Vi phạm SLA / Đạt SLA / Chưa có kết quả, giữ chữ Đang chạy/Tạm dừng và vi phạm sticky. M-02: Ticket đã đóng đạt SLA giải quyết; M-03: Ticket đã đóng từng bị khách từ chối. N: Ticket chưa đóng tại thời điểm xem, cùng bộ lọc, không giới hạn ngày tạo. Giải thích kỹ thuật N ở details mở rộng. M-06: Tải thực — tính tất cả mức ưu tiên. M-07 diễn đạt trước yêu cầu review / trong thời gian chờ / chưa ghi nhận vi phạm trong bối cảnh này; không quy lỗi cá nhân.
- Manager có liên kết nhảy Review mở / Báo cáo / Tải Agent / Tất cả ticket, heading đích nhận focus; giữ M-04 cạnh M-01…03. Nhảy không reset filter/clock/dữ liệu; giữ inclusive thành [from,to), as_of và mọi bộ lọc.
- Chạy lại harness prototype và bổ sung kiểm tra UX/keyboard/mobile; ảnh mới từ thao tác thật, không ghi đè evidence. Backend 181 test không chạy lại khi backend/dependencies giữ nguyên. Không commit/push/deploy, Postman hoặc video.

## 10. Thứ tự triển khai

1. Ghi nguồn phê duyệt cấu trúc prototype vào decision log, thêm traceability planned cho AC-32 và các UI cases; không đổi BR hoặc gán PASS.
2. Dựng domain/time/seeds; đối chiếu 83 fixture và controller trước khi kết nối render.
3. Dựng bốn view và controls; kiểm tra sáu nhóm kịch bản/quyền/persistence.
4. Ghi bằng chứng thực, cập nhật README/TASKS đúng phạm vi; không chạy lại backend 181 test nếu backend/dependencies không đổi.
5. Chủ dự án xem giao diện/kết quả, rồi cập nhật GitHub và triển khai Pages. Postman và video ở bước kế tiếp.


## 10. Xuất bản Pages được duyệt — 13/10/2026

Chủ dự án phê duyệt yêu cầu/kịch bản và các chỉnh UX, chấp nhận kết quả và ảnh bằng chứng từ kiểm thử tự động; cho phép commit, push main thường và triển khai GitHub Pages trong nhiệm vụ này. Không ghi rằng chủ dự án tự thao tác mọi kịch bản hoặc chạy công cụ. GitHub Actions chỉ đóng gói runtime prototype ở gốc project subpath, không đưa backend/SQLite/tests/fixture kiểm thử/log/secrets vào site. Prototype tiếp tục độc lập; giữ banner mô phỏng, hướng dẫn theo vai trò và khôi phục bộ mẫu. Sửa link nguồn ở footer để dùng được khi Pages chỉ chứa runtime. Kiểm tra công khai phải ghi riêng phạm vi smoke với sáu nhóm kiểm thử đầy đủ ở local. Giữ bằng chứng cũ, không đổi expected/verified, không xác nhận hoàn thành v1.0; Postman/video ngoài nhiệm vụ.
