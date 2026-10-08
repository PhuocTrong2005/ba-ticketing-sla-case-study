# Đối chiếu fixture SLA-01…SLA-81 — 08/10/2026

Chủ dự án nói “tôi đã verify bộ SLA đó” ngày 08/10/2026, xác nhận phạm vi S1–S12 = SLA-70…SLA-81 và hạn G của SLA-81 `2026-10-06T08:30:00+07:00`. Codex ghi 12 ca thành `verified` và thực thi công cụ cục bộ. Không có thời điểm xác nhận đến giây, phương pháp tính của chủ dự án hay bằng chứng chủ dự án tự chạy Python; `verified_at=null` trong 12 ca mới. SLA-01…SLA-69 giữ nguyên object và byte. Mọi `expected_*`, events, calculation_note, coverage_groups của 12 ca mới khớp bản draft đã commit trước đó; SLA-81 vẫn để `resolved_attempt` trong `expected_rejected_actions`, ngoài events thành công.

## Kết quả thực thi

| Công cụ / dữ liệu | Ca cũ | Ca mới | Tổng / so sánh | Exit |
|---|---:|---:|---:|---:|
| [Checker gốc 69 ca](../sla/reference/validate_sla_reference.py) trên [fixture nguồn 69](../sla/reference/source/sla_draft_data.json), [report chạy lại](sla-reference-69-rerun.json) | 69 PASS / 0 FAIL | Không áp dụng | 1.243 phép so sánh | 0 |
| [Checker 81 ca](../sla/reference/validate_sla_reference_81.py) trên [fixture hiện hành](../sla/sla-scenarios.json), [report từng ca](sla-reference-81-results.json) | 69 PASS / 0 FAIL; 1.243 | 12 PASS / 0 FAIL; 217 | **81 PASS / 0 FAIL; 1.460 phép so sánh** | 0 |
| [Audit cấu trúc hiện hành](../sla/audit_fixture_current.py), [report](sla-fixture-current-audit.json) | 69 PASS / 0 FAIL; 3.792 assertion | 12 PASS / 0 FAIL; 946 assertion | 0 phép tính SLA | 0 |

Checker mới dùng nguyên các hàm `Calendar`, `ts`, `calculate` từ checker gốc, không import backend. Nó chỉ thay điều kiện CLI từ đúng 69 ID thành đúng 81 ID, giữ 18 trường so sánh/ca và một phép kiểm tra ngữ cảnh refusal cho mỗi `expected_rejected_actions`. Các trường intervals, snapshots và reviews được so cấu trúc sâu với kết quả replay. Không chép `expected_*` thành phép tính. Checker gốc và các báo cáo 69 ca lịch sử không thay đổi.

| Ca mới | Kết quả | Phép so sánh |
|---|---|---:|
| SLA-70 / S1 | PASS | 18 |
| SLA-71 / S2 | PASS | 18 |
| SLA-72 / S3 | PASS | 18 |
| SLA-73 / S4 | PASS | 18 |
| SLA-74 / S5 | PASS | 18 |
| SLA-75 / S6 | PASS | 18 |
| SLA-76 / S7 | PASS | 18 |
| SLA-77 / S8 | PASS | 18 |
| SLA-78 / S9 | PASS | 18 |
| SLA-79 / S10 | PASS | 18 |
| SLA-80 / S11 | PASS | 18 |
| SLA-81 / S12 | PASS | 19, gồm một kiểm tra ngữ cảnh refusal |

Lệnh chạy thật từ root repo:

```powershell
python -B tests/sla/reference/validate_sla_reference.py tests/sla/reference/source/sla_draft_data.json --report tests/evidence/sla-reference-69-rerun.json
python -B tests/sla/reference/validate_sla_reference_81.py tests/sla/sla-scenarios.json --report tests/evidence/sla-reference-81-results.json
python -B tests/sla/audit_fixture_current.py tests/sla/sla-scenarios.json --report tests/evidence/sla-fixture-current-audit.json
```

Checker 81 chạy lại lần cuối lúc `2026-10-08T16:43:13+07:00` bởi Codex. SHA-256 fixture 81: `d4198ce6201ecaffc0444d9af50e5a505e7fcceecd81f96cc8d97da8c2ea005c`; checker 81: `d0284a0c4bf9524f1149c623637431aa65b3d0c337b0d9bc19262d801f04d81f`; checker gốc/engine: `764c284609d7074cbebc7c027576e9c8a16c9a8792456f8e4909ca221464f9ed`. Report JSON lưu argv/command, giờ, hash, exit code, 81 kết quả riêng và các giá trị tham chiếu. Checker gốc chạy lại lúc `2026-10-08T16:39:02+07:00` trên nguồn 69 ca SHA-256 `91c3163a6dcb6707832e2e3c2f6ada4677a8f01e0e67ae6a8f0b5ad0af4c569f`; không dùng kết quả này cho 12 ca mới.

Audit hiện hành chạy lại lần cuối lúc `2026-10-08T16:43:13+07:00` (SHA-256 script `6136ea7fdc2bf51c6899b0c3ce48368a40d61b7b61be57e28082128d2a247e19`). Nó kiểm tra schema, trạng thái/provenance, ID, liên kết coverage, byte 69 object đầu, tính nguyên vẹn checker gốc, thứ tự sự kiện và shape interval/review/refusal; không tính SLA. [Audit nhập nháp cũ](sla-draft-import-structure.json) và [báo cáo nhập](sla-draft-import.md) được giữ nguyên, đúng trạng thái 12 draft tại thời điểm đó.

[Kiểm tra cuối](sla-verification-81-checks.json) xác nhận JSON/ID, 69 object cũ nguyên byte, 12 ca mới không đổi input/`expected_*`, hash fixture/checker/audit khớp report, 67 liên kết tài liệu hợp lệ và `git diff --check` exit 0. Hai JSON lịch sử có byte worktree khác blob Git do chuẩn hóa dòng; `git diff` và nội dung JSON xác nhận chúng không đổi. Không thay báo cáo kiểm tra lịch sử.

## Gate và phần chưa kiểm tra

Gate logic SLA chính **chưa mở**: thiếu ca Customer trả lời ngay trong cuối tuần để resume Waiting; thiếu resume Waiting ngoài giờ khi G còn đúng 0 nhưng chưa từng breached. Ảnh chụp một giây sau deadline của nhánh Waiting còn 0 chưa có, cần cân nhắc theo tiêu chí nhánh biên nhóm 6/9/11 trước khi xác nhận gate. Không tự tạo hoặc verified ca tiếp theo.

Gate tính bối cảnh M-07 **đủ điều kiện mở cho việc viết logic** theo AGENTS/D-33: nhóm 12 có ca verified cho lần từ chối 5/R3, hoàn tất review trong Waiting, overlap G, review mở/đóng/sau `as_of`, và bối cảnh vi phạm trước/trong chờ; checker khớp các trường review. Không có implementation/backend M-07 được chạy trong lần này. [Bảng nhánh hiện hành](../../docs/spec/scenario-coverage.md#đối-soát-sau-xác-nhận-s1s12--08102026) nêu đối chứng từng phần.

Checker chỉ đối chiếu fixture bằng phương pháp tham chiếu AI độc lập với backend; cả fixture và checker có hỗ trợ AI. Một phép refusal của SLA-81 chứng minh ngữ cảnh In Progress/review mở và đáp án kỳ vọng trong fixture, **không phải HTTP 409 thực tế**. A1/A2, HTTP `REVIEW_REQUIRED`, payload/nội dung bắt buộc, quyền, tính nguyên tử, backend, API, SQL, prototype và concurrency vẫn chưa được kiểm thử. Chủ dự án xác nhận fixture qua hội thoại; không suy ra phương pháp kiểm tra của chủ dự án.
