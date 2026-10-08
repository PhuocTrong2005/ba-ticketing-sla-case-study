# Phạm vi kịch bản SLA

Tài liệu này quy định phạm vi, định dạng và ánh xạ kịch bản SLA. Đóng OQ-08 không có nghĩa các ca đã verified.

## Quy ước file kịch bản SLA

Mỗi ca phải có ID, mô tả, `policy_id`, `created_at`, `as_of`, và `events` ở JSON cố định. Mỗi sự kiện có `seq`, `type`, `at` ở ISO 8601 `+07:00` đến giây, và có `at_raw` khi đầu vào có phần dưới giây. Quy ước sự kiện SLA gồm `agent_assigned`, `agent_public_reply`, `resolved`, `status_waiting`, `customer_public_message`, `customer_confirm`, `customer_reject`, `internal_note`, `resolved_attempt` và `review_completed`. Mỗi ca có các trường `expected_*`: deadline, giây đã tiêu/còn lại, trạng thái, mức cảnh báo, snapshot lúc nhận, `expected_resolution_intervals`, `expected_reviews`, `expected_rejected_actions`, trạng thái ticket, số lần từ chối và review đang mở. `resolution_due_at` là `null` khi Waiting; tại Resolved/Closed giữ deadline dùng để đánh giá lượt giải quyết đó. Hai trường `expected_*_warning_level` dùng `none`, `soft`, `emphasized`, `due`, `breached`; `resolution_result_final` chỉ `true` sau Closed. `review_status` ghi nhận xác nhận của chủ dự án; `verification_basis`, `verification_evidence_status` và `verification_method` mô tả riêng nguồn/bằng chứng. Xác nhận hoặc đối chiếu fixture không tự là bằng chứng backend/API. Mọi tính toán theo giây nguyên.

## Ca đã soạn và xác nhận

Các mã dưới đây đã được chủ dự án xác nhận `verified` ngày 06/10/2026. Bằng chứng được ghi là đối chiếu fixture bằng công cụ tham chiếu, không phải kết quả chạy backend/API; điều kiện mở khóa code giữ nguyên cho đến khi tiêu chí bằng chứng của dự án được thỏa mãn độc lập.

SLA-17 và SLA-18 minh họa BR-59. Bộ SLA-01…SLA-69 được chủ dự án xác nhận ngày 06/10/2026 và báo cáo đối chiếu tham chiếu ghi 69/69 PASS; điều này không chứng minh backend/API/SQL/prototype.

| Nhóm | Mã ca verified (phân nhóm chính khi soạn) |
|---:|---|
| 1 | SLA-01…SLA-05 |
| 2 | SLA-14…SLA-18 |
| 3 | SLA-19…SLA-21 |
| 4 | SLA-06…SLA-13 |
| 5 | SLA-27…SLA-30 |
| 6 | SLA-22…SLA-26 |
| 7 | SLA-31…SLA-35 |
| 8 | SLA-36…SLA-39; SLA-60…SLA-64 |
| 9 | SLA-40…SLA-45 |
| 10 | SLA-46…SLA-48 |
| 11 | SLA-49…SLA-57 |
| 12 | SLA-58…SLA-69 |

## Mười hai nhóm kịch bản tối thiểu

| Nhóm | Phạm vi | Mã kịch bản verified |
|---:|---|---|
| 1 | Luồng cơ bản: High và Normal; tính riêng SLA phản hồi đầu và giải quyết; cả hai bắt đầu từ lúc tạo. | SLA-01…SLA-05 |
| 2 | Ngoài giờ: tạo trước 08:00, sau 17:00; Agent nhận, phản hồi hoặc Resolved ngoài giờ; không cộng thời gian ngoài lịch; thời điểm trước 08:00 của một ngày làm việc (phiên bắt đầu cùng ngày). | SLA-14…SLA-18; SLA-70 |
| 3 | Qua ngày và cuối tuần: chạy qua đêm, từ Thứ Sáu sang Thứ Hai; tạo ticket vào Thứ Bảy/Chủ nhật. | SLA-19…SLA-21; SLA-70 |
| 4 | Mốc biên và độ chính xác: tạo đúng 08:00/17:00; hoàn thành trước deadline 1 giây, đúng deadline, sau 1 giây; deadline đúng 17:00 không bị đẩy sang hôm sau; ghi nhận timestamp có phần dưới giây bị cắt bỏ (ví dụ `17:00:00.900` → `17:00:00`). | SLA-06…SLA-13 |
| 5 | Phản hồi đầu: tin nhắn khách và ghi chú nội bộ không tính; chỉ phản hồi công khai đầu tiên của Agent; nội dung Resolved có thể là phản hồi đầu; khách từ chối không đổi kết quả này. | SLA-27…SLA-30; SLA-76 |
| 6 | Waiting for Customer: một hoặc nhiều lần; vào/ra ngoài giờ hoặc qua cuối tuần; không cộng thời gian chờ; tiếp tục đúng ngân sách còn lại; thời điểm trước 08:00 của một ngày làm việc (phiên bắt đầu cùng ngày). | SLA-22…SLA-26; SLA-38; SLA-40; SLA-46…SLA-47; SLA-55; SLA-71…SLA-75; SLA-80…SLA-81 |
| 7 | Resolved và Closed: Resolved đúng hạn/trễ; khách xác nhận muộn hoặc chưa xác nhận; thời gian ở Resolved không cộng SLA; kết quả chỉ xác nhận cuối khi Closed. | SLA-31…SLA-35 |
| 8 | Từ chối kết quả: một hoặc nhiều lần, gồm từ chối lần thứ 3 trở đi; ngoài giờ; xen kẽ Waiting; giữ ngân sách còn lại, không reset hoặc nhân đôi. | SLA-36…SLA-39; SLA-60…SLA-64; SLA-76; SLA-79; SLA-81 |
| 9 | Vi phạm và hết ngân sách: đã vi phạm trước Waiting, Resolved hoặc lúc nhận; vi phạm không bị xóa. Từ chối với 0 giây còn lại: TRONG giờ → deadline bằng thời điểm ticket quay lại In Progress (BR-46); NGOÀI giờ → deadline bằng bắt đầu phiên làm việc kế tiếp: 08:00:00 cùng ngày nếu thời điểm đó trước 08:00 của một ngày làm việc; ngược lại 08:00:00 của ngày làm việc kế tiếp (BR-38). | SLA-40…SLA-45; SLA-67…SLA-69; SLA-73…SLA-76 |
| 10 | Thời điểm đánh giá và dữ liệu: đánh giá tại `as_of` khi đang chạy, Waiting, Resolved; snapshot lúc nhận; hai đồng hồ có kết quả khác nhau; lưu khoảng chạy 0 giây; sự kiện cùng giây theo `event_id`. | SLA-46…SLA-48; SLA-61; SLA-64; SLA-70; SLA-73; SLA-75…SLA-76 |
| 11 | Ngưỡng cảnh báo áp dụng cho cả hai đồng hồ SLA đang chạy: còn đúng 3.600 giây chưa cảnh báo; 3.599 cảnh báo nhẹ; đúng 900 vẫn nhẹ; 899 nhấn mạnh; đúng deadline “đến hạn”; sau 1 giây vi phạm; tạm dừng/hoàn tất không cảnh báo. Có ca High phản hồi đầu tại thời điểm tạo (còn đúng 3.600 giây → chưa cảnh báo) và sau 1 giây (3.599 → cảnh báo nhẹ). | SLA-49…SLA-57; SLA-77…SLA-78 |
| 12 | Escalation: từ chối lần 1, 2 không tạo review; lần 3 tạo review; lần 4, 5 tạo review mới; Agent báo Resolved khi review mở (`REVIEW_REQUIRED`); báo Resolved sau khi Manager ghi phương án; Agent chuyển Waiting khi review mở; Manager ghi phương án khi ticket ở Waiting; Customer trả lời làm ticket về In Progress, review vẫn mở và Resolved vẫn bị chặn; Manager ghi phương án khi không có review mở (`INVALID_TICKET_STATE`) và khi ticket Closed (`TICKET_CLOSED`); chờ Manager theo giờ lịch và phần trùng SLA đang chạy trong giờ làm việc; SLA vi phạm trước yêu cầu review và vi phạm trong lúc chờ; review chưa hoàn thành tính đến `as_of`; review hoàn thành sau `as_of` vẫn mở tại `as_of`; SLA không đổi do chờ Manager. | SLA-58…SLA-69; SLA-79…SLA-81 |

## Điều kiện hoàn tất

- Mỗi nhóm có ca đại diện; nhánh có kết quả khác nhau phải có ca riêng.
- Một ca có thể phủ nhiều nhóm.
- Mỗi ca ghi đầu vào, chuỗi sự kiện, `as_of`, `expected_*` và phép tính độc lập.
- Chủ dự án tự kiểm tra và xác nhận `verified`; Codex không tự xác nhận.
- Nhóm 1 đến 11 chặn logic tính SLA chính; nhóm 12 chặn logic tính bối cảnh M-07 (giây chờ theo giờ lịch, giây trùng SLA đang chạy, vi phạm trước/trong lúc chờ). Workflow review không bị chặn bởi các ca verified.
- Điều kiện hoàn thành v1.0 cần đủ 12 nhóm có ca `verified`; không bắt buộc số ca cố định.

## Nhập S1–S12 ngày 08/10/2026 — draft, chưa mở gate

**Lịch sử tại thời điểm nhập nháp; trạng thái hiện hành ở phần “Đối soát sau xác nhận” cuối tài liệu.** Nguồn: đặc tả S1–S12 do chủ dự án cung cấp trong nhiệm vụ nhập nháp. Giữ nguyên SLA-01…SLA-69 verified; mã mới liên tục SLA-70…SLA-81. Tại thời điểm này các ca mới là `draft` và chưa được thêm vào bảng verified. [Báo cáo nhập và kiểm tra](../../tests/evidence/sla-draft-import.md) giữ nguyên bằng chứng lịch sử.

| Ca nguồn | Mã chính thức | coverage_groups | Nhánh minh họa bằng draft |
|---|---|---|---|
| S1 | SLA-70 | 2, 3, 10 | Tạo Chủ nhật, nhận ngoài giờ; snapshot pending/pending tại lúc nhận |
| S2 | SLA-71 | 6 | Resume Waiting sau 17:00, còn ngân sách |
| S3 | SLA-72 | 6 | Resume Waiting trước 08:00, dùng phiên cùng ngày |
| S4 | SLA-73 | 6, 9, 10 | Resume Waiting còn 0 trong giờ, đúng hạn; khoảng mở 0 giây tại as_of |
| S5 | SLA-74 | 6, 9 | Resume Waiting còn 0 sau giờ làm, deadline phiên kế tiếp; giữ breach cũ |
| S6 | SLA-75 | 6, 9, 10 | Resume Waiting còn 0 trước 08:00; khoảng mở 0 giây tại as_of |
| S7 | SLA-76 | 5, 8, 9, 10 | Từ chối còn 0 trước 08:00; P giữ met; khoảng mở 0 giây |
| S8 | SLA-77 | 11 | G đang chạy còn đúng 3.600 giây, none |
| S9 | SLA-78 | 11 | G đang chạy còn đúng 900 giây, soft |
| S10 | SLA-79 | 8, 12 | Lần từ chối 5 mở R3 riêng; giữ R1/R2 và bối cảnh M-07 |
| S11 | SLA-80 | 6, 12 | Manager hoàn tất R1 trong Waiting; ticket vẫn Waiting theo BR-08/57 |
| S12 | SLA-81 | 6, 8, 12 | Resume Waiting khi R1 mở; refusal ở expected_rejected_actions; G due 2026-10-06T08:30:00+07:00 |

Đối với 16 dòng thiếu của lần đối soát dưới đây: 14 dòng có minh họa draft (S1 phủ hai dòng, S5 phủ hai dòng); **chưa dòng nào được đóng bằng ca verified mới**. Nhánh resume Waiting sau 17:00 có S2/S5; biến thể Customer trả lời ngay trong cuối tuần vẫn chưa có (SLA-25 trả lời Thứ Hai 08:00). S5 chứng minh trường hợp đã breached, không chứng minh trường hợp còn 0 nhưng chưa breached rồi resume sau 17:00/cuối tuần. Các biến thể này tiếp tục mở; không tự thêm ca/đáp án ngoài S1–S12. S4 chỉ đánh giá đúng deadline, không chứng minh ảnh chụp sau deadline một giây của cùng đầu vào.

Hai dòng còn lại là workflow/API: **A1** Manager ghi phương án khi không có review mở → 409 `INVALID_TICKET_STATE`; **A2** khi Closed → 409 `TICKET_CLOSED`, ưu tiên lỗi Closed. Giữ trong backlog API, không đưa vào đối chiếu SLA. S12 chỉ ghi đáp án refusal; HTTP thật, quyền, payload hợp lệ và không ghi ticket_event/đóng interval còn chờ API test. S1 cũng chưa kiểm tra quyền nhận ngoài giờ.

Fixture toán học hiện chỉ lưu `seq/type/at` (và `at_raw` khi cần), không lưu actor/nội dung. Không tự thêm field cho kết quả công khai, lý do từ chối hoặc phương án Manager. Khi chuyển S7/S10–S12 thành API test phải có nội dung bắt buộc theo contract; contract payload chưa có, xem [open questions](../open-questions.md). Snapshot fixture dùng hai trường trạng thái tại assignment, thời điểm từ `agent_assigned.at`; chưa có field lưu số giây snapshot.

Checker gốc khóa đúng 69 ID; audit lịch sử cũng chỉ nhận verified. Không sửa hai công cụ đó để xác nhận draft. Gate SLA chính và M-07 **vẫn chưa được xác nhận mở** theo D-33.

## Đối soát việc 1 — 06/10/2026

Bảng verified trên có mã cho đủ 12 nhóm, nhưng chưa chứng minh mọi nhánh trong phạm vi nhóm đã có ca riêng. `coverage_groups` trong fixture ghi nhóm gốc; các liên kết bổ sung trong bảng dựa trên nội dung: nhóm 6 có SLA-38/40/46/47/55 (Waiting), nhóm 9 có SLA-67…69 (vi phạm trước/trong review), nhóm 10 có SLA-61/64 (đánh giá tại `as_of`). Không sửa metadata hay đáp án fixture để điền bảng. Bảng phân nhóm chính phía trên không còn mang nhãn draft.

Lần tiếp tục ngày 06/10/2026 đã đọc gói nguồn tại `D:\Download\SLA_Verification_Package.zip`: 69 scenario khớp toàn bộ với repo; checker gốc chạy trực tiếp trên fixture repo đạt **69 PASS, 0 FAIL, 1.243 so sánh, exit code 0**. [Kết quả tham chiếu](../../tests/evidence/sla-reference-results.json) khác với [audit cấu trúc lịch sử](../../tests/evidence/sla-fixture-audit.json) gồm 3.792 assertion; giữ nguyên audit đó, không chạy lại hoặc đổi tên loại kiểm tra.

Rà lại coverage sửa nhận định trước: **SLA-40 đã phủ vào Waiting ngoài giờ** lúc 17:30 với SLA breached. Không còn liệt kê toàn bộ nhánh “vào/ra ngoài giờ” là thiếu. Những phần còn thiếu dưới đây là yêu cầu có sẵn, không phải ca/đáp án mới. Các liên kết ca là đối chứng gần nhất, không gán chúng thành ca phủ nhánh còn thiếu.

| Nhóm / yêu cầu hiện hành | Ca hiện có và bằng chứng | Phần chưa được kiểm chứng bằng ca riêng |
|---|---|---|
| 2; BR-16/59 — nhận ngoài giờ | SLA-16 nhận 08:10; SLA-17 nhận 16:40 rồi phản hồi 18:00; mọi `agent_assigned` đều trong giờ | Nhận ngoài giờ và snapshot SLA tại chính thời điểm nhận đó |
| 3; BR-17 — tạo cuối tuần | SLA-19/21 bắt đầu Thứ Sáu; SLA-20 tạo Thứ Bảy 10/10 | Tạo Chủ nhật rồi tính phiên Thứ Hai |
| 6; BR-17/20 — tiếp tục từ Waiting ngoài giờ | SLA-40 vào Waiting 17:30 nhưng không ra; SLA-24 ra 08:30; SLA-25 ra Thứ Hai 08:00 | Customer trả lời sau 17:00 hoặc cuối tuần khi đang Waiting, chờ phiên kế tiếp mà không cộng giây ngoài lịch |
| 6; BR-17/20 — phiên cùng ngày trước 08:00 | SLA-14 tạo 07:30 (không phải resume); SLA-24/25 resume 08:30/08:00 | Customer trả lời trước 08:00 ngày làm việc để resume Waiting, dùng phiên cùng ngày |
| 6/9; BR-48 — resume Waiting còn 0 giây trong giờ | SLA-24 còn 1.800 giây tại resume 08:30, chỉ về 0 tại `as_of` 09:00; SLA-40 hết ngân sách nhưng không resume | Resume từ Waiting khi ngân sách đã bằng 0, deadline bằng thời điểm quay lại |
| 6/9; BR-48 — resume Waiting còn 0 giây ngoài giờ, phiên ngày kế tiếp | SLA-43/44 resume sau **từ chối**, không phải Waiting | Customer trả lời Waiting khi còn 0 sau giờ làm/cuối tuần và dùng 08:00 ngày làm việc kế tiếp |
| 6/9; BR-48 — resume Waiting còn 0 giây trước 08:00 | SLA-43/44 từ chối lúc 18:00; không có resume Waiting trước 08:00 | Resume Waiting với 0 giây trước 08:00, deadline bằng 08:00 cùng ngày |
| 6/9; BR-23/48/61 — giữ breached sau Waiting | SLA-40 giữ breached khi Waiting nhưng chưa có Customer trả lời | Giữ breached qua bước tiếp tục, không chỉ trong ảnh chụp lúc đang Waiting |
| 9; BR-38 — từ chối còn 0 trước 08:00 | SLA-41/42 từ chối trong giờ; SLA-43/44 từ chối 18:00, đánh giá 08:00/08:00:01 hôm sau | Từ chối trước 08:00 ngày làm việc, deadline 08:00 cùng ngày |
| 11; BR-39 — G còn đúng 3.600 giây khi chạy | SLA-49 kiểm tra P=3.600; SLA-56 G=3.599; SLA-31 G=3.600 nhưng đã Resolved | G đang chạy tại đúng ngưỡng 3.600, chưa cảnh báo |
| 11; BR-39 — G còn đúng 900 giây khi chạy | SLA-51 kiểm tra P=900; SLA-57 G=899 | G đang chạy tại đúng ngưỡng 900, cảnh báo nhẹ |
| 12; BR-52 — từ chối lần 5 | SLA-60 lần 3 tạo R1; SLA-64 lần 4 tạo R2; tối đa hiện có là 4 | Lần 5 tạo review mới riêng sau khi review trước hoàn tất |
| 12; BR-54/57 — Manager ghi phương án lúc Waiting | SLA-63 Waiting 11:30–12:30, review hoàn tất 13:00 | Hoàn tất review ngay trong Waiting và bối cảnh M-07 lúc đó |
| 12; BR-53/57 — chặn Resolved sau Customer trả lời khi review mở | SLA-63 trả lời 12:30, review đóng 13:00 nhưng không thử Resolved ở khoảng giữa; SLA-61 thử Resolved mà chưa qua Waiting | `REVIEW_REQUIRED` sau resume Waiting trước khi review đóng |
| 12; BR-58 — Manager ghi phương án không có review mở | SLA-58/59 chưa có review; SLA-62 có review đã hoàn tất, không thử ghi phương án lại | Bước bị từ chối `INVALID_TICKET_STATE` khi không có review mở |
| 12; BR-58 — Manager ghi phương án khi Closed | SLA-33…35 có Closed, không có bước Manager ghi phương án | Bước bị từ chối `TICKET_CLOSED` và ưu tiên lỗi Closed |

Checker chỉ hỗ trợ đối chiếu bước từ chối `resolved_attempt`/`REVIEW_REQUIRED` hiện có ở SLA-61; chưa kiểm tra được hai mã lỗi Manager trên. Actor, nội dung bắt buộc, HTTP thật, quyền và tính nguyên tử cần test API riêng; không tính vào PASS của bộ fixture. Không tạo bug backend từ các khoảng thiếu này.

Gate logic SLA chính **chưa được xác nhận mở**: nhóm 1–11 có mã verified và đã có bằng chứng tham chiếu, nhưng các nhánh còn thiếu nêu trên chưa thỏa điều kiện “nhánh có kết quả khác nhau phải có ca riêng”. Gate tính bối cảnh M-07 **chưa được xác nhận mở**: nhóm 12 có mã verified và phép tính M-07 hiện có khớp checker; chưa có ca Manager hoàn tất review trong Waiting, cùng các nhánh nhóm 12 còn thiếu. Các nhánh lỗi/quyền thuần workflow không trở thành điều kiện mới chặn viết workflow: workflow review vẫn không bị gate này chặn theo AGENTS/D-33. Không sửa tiêu chí gate hoặc triển khai logic trong nhiệm vụ này.

Giữ điều kiện phép tính độc lập và xác nhận chủ dự án ở trên. D-40 ghi chủ dự án xác nhận, AI chạy thay; checker độc lập với backend nhưng cả fixture/checker có hỗ trợ AI, không chứng minh chủ dự án tự tính tay/tự chạy Python. Hướng dẫn trong gói là tài liệu nguồn, không thay thế AGENTS/D-33 hoặc yêu cầu mới nhất của chủ dự án. Không hỏi lại xác nhận 69 ca/OQ-20/OQ-21. Blocker thiếu ZIP và chưa giải thích hash đã được xử lý; còn coverage và tiêu chí implementation/test v1.0 tại TASKS. Chi tiết ở [báo cáo hòa giải](../../tests/evidence/sla-reconciliation.md).

## Đối soát sau xác nhận S1–S12 — 08/10/2026

Chủ dự án xác nhận “tôi đã verify bộ SLA đó” cho đúng SLA-70…SLA-81 và cho phép ghi `verified`. Không có giờ xác nhận đến giây hoặc mô tả phương pháp chủ dự án kiểm tra; `verified_at` của 12 ca mới là `null`, còn ngày và lời xác nhận nằm trong metadata. SLA-01…SLA-69 giữ nguyên. Bảng nhóm verified phía trên đã bổ sung các ID mới theo `coverage_groups` thực tế. [Báo cáo hiện hành](../../tests/evidence/sla-verification-81.md) và [đối chiếu tham chiếu 81 ca](../../tests/evidence/sla-reference-81-results.json) ghi phương pháp, kết quả và giới hạn; [báo cáo nhập nháp](../../tests/evidence/sla-draft-import.md) vẫn phản ánh đúng thời điểm trước xác nhận.

| Nhánh trong bảng thiếu lịch sử | Ca verified hiện có | Phần còn thiếu hoặc giới hạn |
|---|---|---|
| Nhận ngoài giờ/snapshot; tạo Chủ nhật | SLA-70 | Quyền nhận ngoài giờ chờ API test. |
| Resume Waiting sau 17:00, trước 08:00 | SLA-71, SLA-72 | Customer trả lời **ngay trong cuối tuần** khi đang Waiting chưa có ca riêng. |
| Resume Waiting còn 0 trong giờ/trước 08:00 | SLA-73, SLA-75 | Hai ca đánh giá đúng deadline; ảnh chụp sau deadline một giây của chính nhánh Waiting còn 0 chưa có. Nhóm 11 đã có ca vi phạm sau deadline cho các nhánh khác. |
| Resume Waiting còn 0 sau 17:00; giữ breach cũ | SLA-74 | SLA-74 đã breached trước Waiting. Chưa có ca còn 0 nhưng **chưa từng breached**, resume sau 17:00/cuối tuần và giữ pending tại deadline mới. |
| Từ chối còn 0 trước 08:00; P không đổi | SLA-76 | HTTP/nội dung bắt buộc chờ API test. |
| G đang chạy tại đúng 3.600/900 giây còn lại | SLA-77, SLA-78 | Hai ngưỡng có ca riêng và khớp checker tham chiếu. |
| Từ chối lần 5/R3; Manager hoàn tất review trong Waiting; refusal sau resume Waiting | SLA-79, SLA-80, SLA-81 | Context của M-07 có ca verified; HTTP `REVIEW_REQUIRED` và payload/quyền vẫn chờ API test. |
| Manager ghi phương án khi không có review mở / ticket Closed | Chưa có fixture SLA; A1/A2 trong API-02 | Cần API test `INVALID_TICKET_STATE` / `TICKET_CLOSED` và thứ tự lỗi Closed. Không tính vào đối chiếu SLA/M-07. |

**Gate logic SLA chính: chưa mở.** Dù nhóm 1–11 đều có mã verified và 81/81 ca khớp tham chiếu, hai biến thể Waiting có kết quả khác nhau còn thiếu: Customer trả lời ngay trong cuối tuần; và resume ngoài giờ với ngân sách 0 khi chưa từng breached. Ca sau deadline một giây của chính đường resume Waiting còn 0 cũng cần được cân nhắc theo điều kiện nhánh biên nhóm 6/9/11 trước khi xác nhận gate. Không tạo hoặc tự verified ca mới trong lần đối soát này.

**Gate tính bối cảnh M-07: đủ điều kiện mở cho việc viết logic tính M-07 theo AGENTS/D-33.** Nhóm 12 có ca verified cho R1/R2/R3 và lần từ chối thứ 5 (SLA-60/64/79), review trong Waiting (SLA-80), phần chờ trùng và không trùng G (SLA-63/80/81), review mở/đóng và hoàn tất sau `as_of` (SLA-60/62/65/79), cùng bối cảnh breach trước/trong lúc chờ (SLA-67…SLA-69). Checker 81 ca khớp các trường review. Đây là đánh giá điều kiện viết logic, chưa phải kết quả chạy M-07 trong backend. A1/A2 và HTTP `REVIEW_REQUIRED` là workflow/API riêng; D-33 không dùng chúng để chặn phép tính M-07.

Chỉ chủ dự án xác nhận ca verified; Codex ghi lại xác nhận và chạy checker. Không suy chủ dự án tự tính tay, tự chạy Python hoặc đã kiểm tra backend/API/SQL/prototype. Bảng thiếu của lần đối soát 06/10 ở trên là lịch sử, không phải kết luận coverage hiện hành.
