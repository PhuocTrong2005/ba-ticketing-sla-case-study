# Hòa giải SLA — việc 1, ngày 06/10/2026

**Kết quả: hoàn thành phần kiểm tra độc lập với gói nguồn; phần tham chiếu bị chặn do thiếu tệp. Chưa xác nhận mở gate SLA chính hoặc M-07.** Không thực hiện việc 2/3, không viết logic SLA hoặc tạo ca/đáp án mới.

## Trạng thái đầu vào và nguồn nhiệm vụ

Branch `main`, remote `origin` = `https://github.com/PhuocTrong2005/ba-ticketing-sla-case-study.git`; index ban đầu trống. Đã đọc trạng thái/diff trước sửa. [Baseline](sla-reconciliation-baseline.json) lưu HEAD, trạng thái Git, hash các file trước nhiệm vụ và hash nguồn chỉ dẫn.

Đã có thay đổi chưa commit ở README, TASKS, decision-log, open-questions, business-rules, scenario-coverage, traceability, fixture; thêm ba tài liệu stories/FR/NFR draft chưa tracked. Giữ những thay đổi này. Các tài liệu được sửa trong nhiệm vụ trùng các file đã dirty; không tách commit an toàn chỉ bằng stage cả file. Không commit, không stage, không push, không đổi branch/remote, không reset/clean.

Không tìm thấy file tên `Codex_Task_1_Reconcile_SLA.md`. Nguồn chỉ dẫn thực tế là tệp người dùng đính kèm `C:/Users/ASUS/.codex/attachments/8bb84ad0-083d-4752-ac35-2e3f6c47aba9/Pasted text.txt` chứa “NHIỆM VỤ: Tự động hòa giải gate và nguồn gốc bộ SLA”.

Đã tìm ZIP/script/task trong repo và thư mục `.codex/attachments`, Downloads, Documents, Desktop bằng `rg --files` cùng lọc tên. Không tìm thấy `SLA_Verification_Package.zip` hay `validate_sla_reference.py`; vì vậy chưa có fixture nguồn, báo cáo tham chiếu hoặc tài liệu provenance của gói. Tìm rộng ở thư mục gốc `C:/Users/ASUS` bị `Access is denied`; không khẳng định toàn bộ máy không có tệp. Không giải nén gói không tồn tại, không chạy prompt trong ZIP và không tạo lại checker.

## Kết quả thực thi thực tế

| Hoạt động | Kết quả |
|---|---|
| Parse JSON, ID | Mảng parse được, không trùng key; đủ đúng 69 ID SLA-01…SLA-69, không trùng ID |
| Audit cấu trúc | 69 PASS / 0 FAIL; 3.792 assertion cấu trúc; 0 lỗi tổng thể; exit code thực tế 0 |
| Checker tham chiếu SLA | **Chưa chạy**; PASS/FAIL, số so sánh, exit code: không có (`null`), không ghi là 0 FAIL |
| So fixture với nguồn ZIP | Chưa kiểm tra được; chưa kết luận khớp/khác nghiệp vụ |
| Backend/API/SQL/prototype/concurrency | Chưa chạy |

Audit chạy lúc **2026-10-06T11:04:39+07:00**, Python **3.13.3**, executable `C:\Program Files\Python313\python.exe`. Người thực thi: **trợ lý AI Codex chạy Python cục bộ thay chủ dự án**. Chủ dự án xác nhận fixture; không có bằng chứng chủ dự án tự chạy Python hoặc tự tính tay. Stdout, stderr, argv, exit code thực tế ở [run record](sla-fixture-audit-run.json); kết quả từng ca ở [JSON audit](sla-fixture-audit.json).

Lệnh chạy lại từ thư mục repo:

```powershell
python tests/sla/audit_fixture_structure.py tests/sla/sla-scenarios.json --report tests/evidence/sla-fixture-audit.json
```

[Script audit](../sla/audit_fixture_structure.py) chỉ đọc fixture, kiểm tra schema/metadata/thứ tự sự kiện và đối chiếu ID trong bảng coverage; không tính lịch làm việc, deadline, ngân sách, trạng thái SLA hoặc M-07. Timestamps, policy enum, thời lượng nguyên, cắt `at_raw`, thứ tự `seq`, các bước bị từ chối, review_status và nguồn xác nhận được kiểm tra trong phạm vi cấu trúc. Sự kiện sau `as_of` là hợp lệ và được liệt kê riêng; không tự bỏ chúng khỏi fixture. Enum SLA chữ thường trong fixture tương ứng nhãn mã chữ hoa ở codes; đây là mô tả schema hiện tại, chưa phải ánh xạ với gói nguồn.

Tính đúng nghiệp vụ của **mọi `expected_*`, `resolution_result_final` và kết quả bước bị từ chối đều chưa kiểm tra lại được**. Không tính chúng là PASS nghiệp vụ chỉ vì đúng kiểu dữ liệu. Chưa có adapter vì chưa đọc được schema nguồn; input thực tế là nguyên file repo `tests/sla/sla-scenarios.json`.

Lệnh tham chiếu dự kiến **chưa thực thi**, chỉ dùng sau khi nhận và kiểm tra script gốc/schema:

```powershell
python tests/sla/reference/validate_sla_reference.py tests/sla/sla-scenarios.json --report tests/evidence/sla-reference-results.json
```

Hai đường dẫn script/report tham chiếu trên chưa tồn tại; không đặt script audit vào tên checker nguồn.

## Hash và provenance

SHA-256 tính trên toàn bộ byte. [Manifest hiện hành](sla-reconciliation.sha256) lưu hash fixture, script thực sự chạy, các báo cáo và tài liệu nhiệm vụ. Báo cáo JSON tự ghi hash input/script/coverage; hash chính báo cáo nằm ở manifest ngoài để tránh tự tham chiếu.

| Artefact | SHA-256 / trạng thái |
|---|---|
| Fixture repo hiện hành; cũng là input thực tế | `4bcad90141b1d6b86a28804b93a961cea2862d84011c6b463439c370c17397b9` |
| Script audit thực tế chạy | `f780b258036de3bd0b9ccee560074efa1d426b6405cc9e34a93e10ce8a670127` |
| Fixture được báo trong lịch sử D-40/README | `91c3163a6dcb6707832e2e3c2f6ada4677a8f01e0e67ae6a8f0b5ad0af4c569f` — chưa có byte nguồn |
| Script tham chiếu được báo trong lịch sử | `764c284609d7074cbebc7c027576e9c8a16c9a8792456f8e4909ca221464f9ed` — chưa có script nguồn |
| ZIP, fixture nguồn, adapter, report tham chiếu mới | Không có; không cấp hash giả |

Kết quả **69/69 PASS, 1.243 so sánh** giữ như lịch sử do chủ dự án cung cấp, không gán cho lần chạy này. Fixture hiện tại khác hash lịch sử; **nguyên nhân chưa xác định**. Chưa phân loại được khác biệt nội dung nghiệp vụ, cấu trúc JSON, định dạng hay metadata nếu không có nguồn. Không dùng khác hash làm kết luận khác nghiệp vụ.

69 ca giữ `drafted_by = AI advisor`, `verified_by = project owner`, xác nhận lúc `2026-10-06T09:42:31+07:00`, `verification_basis = owner_confirmation`; `reviewed_by` và các giá trị `owner_results` vẫn null, các ghi chú tính tay chủ dự án vẫn rỗng. Metadata `verification_method`/`verification_evidence_status` còn ghi chưa cung cấp phương pháp/bằng chứng trong hội thoại; ghi nhận đây là trạng thái metadata ban đầu, không nâng thành bằng chứng đã tái lập. D-40 bổ sung lời báo cáo lịch sử của chủ dự án về công cụ do AI chạy. Báo cáo này phân biệt hai nguồn đó và việc thiếu artefact gốc. Không sửa bất kỳ byte fixture nào để làm chúng trông nhất quán hơn.

## Nhóm → mã verified

Giữ xác nhận có sẵn, không tự chuyển review_status. Các liên kết bổ sung ngoài `coverage_groups` được giải thích tại [scenario coverage](../../docs/spec/scenario-coverage.md); audit kiểm tra cả nhóm trong fixture và bảng tài liệu.

| Nhóm | Mã verified trong bảng hiện hành |
|---:|---|
| 1 | SLA-01…SLA-05 |
| 2 | SLA-14…SLA-18 |
| 3 | SLA-19…SLA-21 |
| 4 | SLA-06…SLA-13 |
| 5 | SLA-27…SLA-30 |
| 6 | SLA-22…SLA-26; SLA-38; SLA-40; SLA-46…SLA-47; SLA-55 |
| 7 | SLA-31…SLA-35 |
| 8 | SLA-36…SLA-39; SLA-60…SLA-64 |
| 9 | SLA-40…SLA-45; SLA-67…SLA-69 |
| 10 | SLA-46…SLA-48; SLA-61; SLA-64 |
| 11 | SLA-49…SLA-57 |
| 12 | SLA-58…SLA-69 |

Không còn nhóm trống, nhưng **có mã đại diện không đồng nghĩa đủ nhánh**. Rà chuỗi sự kiện của 69 ca thấy còn thiếu:

- Nhóm 2: Agent nhận ngoài giờ; nhóm 3: tạo Chủ nhật.
- Nhóm 6: vào/ra Waiting ngoài giờ, tiếp tục trước 08:00 cùng ngày làm việc; nhóm 9: từ chối lúc hết ngân sách trước 08:00 cùng ngày làm việc.
- Nhóm 11: đồng hồ giải quyết đang chạy còn đúng 3.600 hoặc 900 giây. Inventory tự động không tìm thấy ca nào; SLA-56/57 có 3.599/899.
- Nhóm 12: lần từ chối thứ 5 (chuỗi hiện có tối đa 4); Manager ghi phương án lúc Waiting (SLA-63 hoàn thành lúc 13:00, sau Customer trả lời 12:30); Resolved bị chặn sau khi Customer trả lời nhưng review còn mở; hai lỗi Manager `INVALID_TICKET_STATE`/`TICKET_CLOSED` (danh sách bước bị từ chối hiện chỉ có `REVIEW_REQUIRED` ở SLA-61).

Đây là khoảng thiếu đối với văn bản hiện hành, không đề xuất thêm ca/expected và không ghi bug backend. Không khẳng định danh sách này là kiểm toán đầy đủ mọi nhánh nghiệp vụ khi checker nguồn còn thiếu.

## Gate và blocker

| Gate / tiêu chí | Kết luận thực tế |
|---|---|
| Logic SLA chính | Chưa xác nhận mở: điều kiện mã verified nhóm 1–11 đạt; điều kiện nhánh có kết quả khác nhau có ca riêng và bằng chứng phép tính độc lập chưa được chứng minh đầy đủ |
| Logic bối cảnh M-07 | Chưa xác nhận mở: nhóm 12 có mã verified; còn nhánh thiếu và chưa truy xuất/chạy lại được artefact tham chiếu |
| Workflow review | Không bị gate verified này chặn theo AGENTS/D-33; không triển khai trong việc 1 |
| Hoàn thành v1.0 | Chưa đạt: ngoài coverage còn thiếu prototype/API, kiểm tra quyền backend, hai ca concurrency, dựng lại dữ liệu, SQL và README chạy từ thư mục mới |

AGENTS và D-33 tách nhóm 1–11/12 như trên. Phần “Điều kiện hoàn tất” của scenario coverage còn yêu cầu phép tính độc lập và chủ dự án tự kiểm tra/xác nhận. Không bỏ điều kiện đó. D-40 nêu rõ AI chạy thay, chủ dự án xác nhận và không bỏ gate; không suy ra chủ dự án tự tính tay/tự chạy. Không cần xác nhận lại 69 ca hoặc OQ-20/OQ-21 đã đóng.

Để tiếp tục phần phụ thuộc: cần ZIP gốc/đường dẫn đọc được chứa fixture, checker và báo cáo/provenance; sau đó mới so cấu trúc và nghiệp vụ, lập adapter nếu cần, chạy checker, giải thích hash. Coverage nhánh còn thiếu cần ca verified phù hợp; không mở rộng bộ ca trong nhiệm vụ này. [Open questions](../../docs/open-questions.md) đã ghi blocker mà không mở lại quyết định đã đóng.

Fixture/reference check **chưa chứng minh backend/API/SQL/prototype/concurrency đã chạy đúng**. Không tạo bug, issue hoặc bằng chứng implementation từ dữ liệu này; stories/FR/NFR vẫn draft.

## File của nhiệm vụ và kiểm tra cuối

Sửa: `README.md`, `TASKS.md`, `docs/spec/scenario-coverage.md`, `docs/decision-log.md`, `docs/open-questions.md`, `docs/traceability.md`.

Thêm: `tests/sla/audit_fixture_structure.py`, `tests/evidence/sla-reconciliation-baseline.json`, `tests/evidence/sla-fixture-audit.json`, `tests/evidence/sla-fixture-audit-run.json`, `tests/evidence/sla-reconciliation.md`, `tests/evidence/sla-reconciliation-checks.json`, `tests/evidence/sla-reconciliation.sha256`.

[Kiểm tra cuối](sla-reconciliation-checks.json) lưu đối chiếu hash fixture/tài liệu không thuộc phần sửa với baseline, liên kết file Markdown, hash input/script của audit và `git diff --check`. Fixture nguyên byte nên mọi `expected_*`, bước bị từ chối, review_status và metadata nguyên vẹn. File fixture và business-rules vẫn dirty do thay đổi có trước, không phải do nhiệm vụ này.

Khi chạy lại audit, timestamp/report hash sẽ đổi; cần cập nhật run record và manifest tương ứng, không coi manifest lần này là hash của lần chạy khác. Có thể xác minh từng hash bằng `Get-FileHash -Algorithm SHA256 <đường-dẫn-file>`.

Không có commit mới vì thay đổi nhiệm vụ chồng lên các file đã sửa trước đó; giữ working tree để chủ dự án review. **Chưa push.**
