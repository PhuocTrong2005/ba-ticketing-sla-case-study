# H?a gi?i SLA ? vi?c 1

**C?p nh?t 08/10/2026:** 69 scenario trong repo kh?p to?n b? scenario c?a g?i ngu?n. Checker g?c ?? ch?y tr?n fixture repo ng?y 06/10/2026: **69 PASS, 0 FAIL, 1.243 ph?p so s?nh, exit code 0**. Audit c?u tr?c c? 3.792 assertion l? b?ng ch?ng ri?ng. C? hai gate t?nh SLA ch?nh v? b?i c?nh M-07 **ch?a ???c x?c nh?n m?** v? coverage c?n c?c nh?nh thi?u theo t?i li?u hi?n h?nh.

## Ngu?n, vai tr? v? tr?ng th?i tr??c khi ti?p t?c

Ng??i d?ng n?u ???ng d?n trong repo nh?ng t?i th?i ?i?m ki?m tra file ?? **kh?ng t?n t?i**. ZIP th?c t? ng??i d?ng ??nh k?m/??c ???c l? `D:\Download\SLA_Verification_Package.zip`, SHA-256 `d445c012818d17007506206a8e0b089afbb46ce2fd3195c1eb6df2efa559d2a8`. G?i ???c gi?i n?n v?o th? m?c t?m sau khi ki?m tra t?n entry; m? checker ???c ??c tr??c khi ch?y. Kh?ng th?c thi `Codex_Import_SLA_Validation.md` hay ch? d?n kh?c trong g?i. B?n t?p d? li?u/t?i li?u ngu?n ???c gi? nguy?n byte t?i [source/](../sla/reference/source/); [checker g?c](../sla/reference/validate_sla_reference.py) ???c sao ch?p nguy?n byte. [README c?ng c?](../sla/reference/README.md) ghi c?ch ch?y v? gi?i h?n.

[Baseline ti?p t?c](sla-reference-baseline.json) ghi ZIP, hash m?i file trong worktree tr??c ph?n ti?p t?c, branch, remote, Git status, index. [Baseline vi?c 1 ban ??u](sla-reconciliation-baseline.json) v? [b?o c?o tr??c khi nh?n ZIP](history/sla-reconciliation-before-reference.md) ???c gi? l?m l?ch s?. Working tree ?? dirty tr??c khi l?m vi?c 1: fixture, business rules, README, TASKS, decision log, open questions, scenario coverage, traceability; ba b?n nh?p stories/FR/NFR ch?a tracked. Kh?ng thay ??i ??p ?n `expected_*`, `review_status`, metadata x?c nh?n ho?c c?c b?n nh?p ??.

Ch? d? ?n x?c nh?n c? 69 ca l?c `2026-10-06T09:42:31+07:00`. Fixture v? checker c? h? tr? AI; AI ch?y c?ng c? thay ch? d? ?n. Kh?ng c? b?ng ch?ng ch? d? ?n t? t?nh tay ho?c t? ch?y Python. L?ch s? ngu?n ghi thi?u chi ti?t ph??ng ph?p ki?m tra c?a ch? d? ?n, kh?ng suy th?m. OQ-20/OQ-21 ?? ??ng; kh?ng xin x?c nh?n l?i.

## ??i chi?u ngu?n v? hash

[So s?nh theo c?u tr?c JSON](sla-source-comparison.json) ??c ??ng hai input: `tests/sla/sla-scenarios.json` c?a repo v? `tests/sla/reference/source/sla_draft_data.json` c?a ZIP. Ngu?n c? root `{metadata, scenarios}`; repo c? root m?ng l? ??ng `scenarios`. **C? 69 object scenario kh?p s?u, c?ng th? t?**, g?m `created_at`, `as_of`, `policy_id`, `events`, to?n b? `expected_*`, `resolution_result_final`, `expected_rejected_actions`, `expected_reviews`, m? t? v? metadata x?c nh?n t?ng ca. K?t qu?: 0 kh?c bi?t nghi?p v?, 0 kh?c bi?t metadata/m? t? trong ca; 1.587 l??t so tr??ng nghi?p v? b?ng nhau trong ph?p so ngu?n, **kh?ng ph?i** 1.243 ph?p t?nh checker. ?nh x? tr??ng scenario l? identity, kh?ng ??i t?n, kh?ng c?n adapter. Metadata root c?a ZIP l? ph?n ri?ng, ???c l?u trong b?o c?o so ngu?n v? b?n ZIP nguy?n g?c.

| N?i dung | SHA-256 / ? ngh?a |
|---|---|
| ZIP ngu?n | `d445c012818d17007506206a8e0b089afbb46ce2fd3195c1eb6df2efa559d2a8` |
| Fixture repo, input l?n ch?y m?i | `4bcad90141b1d6b86a28804b93a961cea2862d84011c6b463439c370c17397b9` |
| Fixture ngu?n c? wrapper, hash l?ch s? D-40 | `91c3163a6dcb6707832e2e3c2f6ada4677a8f01e0e67ae6a8f0b5ad0af4c569f` |
| Checker sao nguy?n byte, hash l?ch s? D-40 | `764c284609d7074cbebc7c027576e9c8a16c9a8792456f8e4909ca221464f9ed` |
| Report checker m?i tr?n fixture repo | `47f71b63cad28ac0c5f56f1548a1198eec75b105ed38cdbf4d70813ae856b0a6` |

Hash fixture kh?c v? **root wrapper metadata v? ??nh d?ng**: repo 318.045 byte/6.462 d?ng, ngu?n 233.313 byte/5.955 d?ng. Canonical JSON c?a m?ng 69 scenario ? hai file c? c?ng SHA-256 `921fcbb3bbad04f29e833b357f04e2050e7d8ccff2c42d4b92bfc5afddad14e0`. Kh?ng c? kh?c bi?t ??p ?n nghi?p v?; kh?ng ch?nh fixture ?? ?p PASS. Hash ngu?n v? checker b?o trong [b?o c?o l?ch s?](../sla/reference/source/SLA_Validation_Report.md) kh?p byte ???c tr?ch t? ZIP. [Manifest SHA-256 hi?n h?nh](sla-reconciliation.sha256) li?t k? ??y ?? script, fixture, report, ngu?n b?o t?n v? t?i li?u; b?n manifest c? gi? ? [history](history/sla-reconciliation-before-reference.sha256).

## K?t qu? ch?y th?c t?

| Ki?m tra | PASS / FAIL | S? ph?p | Exit code | Vai tr? |
|---|---:|---:|---:|---|
| So scenario repo v?i ngu?n ZIP | 69 kh?p / 0 kh?c | 1.587 tr??ng nghi?p v? so b?ng nhau | 0 | So n?i dung/schema, kh?ng t?nh SLA |
| Checker tham chi?u g?c tr?n fixture repo | **69 PASS / 0 FAIL** | **1.243 so s?nh** | **0** | T?nh l?i deadline, gi?y, tr?ng th?i, c?nh b?o, intervals, reviews theo checker ??c l?p backend |
| Audit c?u tr?c tr??c khi nh?n ZIP | 69 PASS / 0 FAIL | 3.792 assertion c?u tr?c | 0 | Ki?m tra schema/metadata, kh?ng t?nh l?i SLA |

Checker th?c thi `2026-10-06T12:51:30+07:00`, Python 3.13.3 t?i `C:\Program Files\Python313\python.exe`, do AI Codex ch?y c?c b? thay ch? d? ?n. [Run record](sla-reference-run.json) l?u l?nh, stdout/stderr, exit code v? hash ba byte input/script/report; [JSON t?ng ca](sla-reference-results.json) c? s? ph?p, calculated reference, mismatch. B?o c?o ngu?n c? ghi `2026-10-06T10:00:20+07:00` v? 69/69 PASS, 1.243 so s?nh tr?n file ngu?n c? wrapper; ?? l? l?n l?ch s? ri?ng. [Run record audit c?u tr?c](sla-fixture-audit-run.json) v?n l? l?n 11:04:39, gi? nguy?n [report audit](sla-fixture-audit.json). Kh?ng c?ng ho?c g?i 3.792 assertion l? 1.243 ph?p checker.

L?nh ch?y l?i t? root repo n?u input/script ??i; **kh?ng ch?y l?i trong phi?n 08/10/2026** v? hash c?a fixture, checker v? report v?n kh?p run record:

```powershell
python tests/sla/reference/validate_sla_reference.py tests/sla/sla-scenarios.json --report tests/evidence/sla-reference-results.json
python tests/sla/reference/compare_sla_sources.py tests/sla/sla-scenarios.json tests/sla/reference/source/sla_draft_data.json --report tests/evidence/sla-source-comparison.json
```

Input checker l? m?ng repo, checker g?c h? tr? tr?c ti?p; report m?i c? `owner_confirmation: null` ? root v? wrapper kh?ng c? ? input. X?c nh?n v?n hi?n trong metadata t?ng ca v? b?n ngu?n b?o t?n. Checker c? 18 tr??ng k?t qu? c?p ca v? 1 b??c b? t? ch?i ? SLA-61. N? kh?ng ki?m ch?ng hai l?i Manager `INVALID_TICKET_STATE`/`TICKET_CLOSED`, kh?ng c? actor/n?i dung b?t bu?c ho?c HTTP th?c; c?ng kh?ng ch?ng minh backend/API/SQL/prototype/concurrency ??ng.

## Coverage v? gate

B?ng 12 nh?m v? [16 nh?nh c?n thi?u v?i BR, ca g?n nh?t, l? do ch?a ph?](../../docs/spec/scenario-coverage.md#??i-so?t-vi?c-1--06102026) l? ngu?n ??nh gi? hi?n h?nh. C? m? verified ? m?i nh?m; kh?ng t? chuy?n tr?ng th?i ho?c th?m ca. R? l?i ?? **s?a nh?n ??nh c?**: SLA-40 v?o Waiting ngo?i gi? l?c **17:30**, ? tr?ng th?i breached. N? kh?ng c? b??c Customer tr? l?i ?? ki?m ch?ng resume ngo?i gi? ho?c gi? breached sau resume. C?c kho?ng thi?u ch?nh:

- Nh?m 1?11: nh?n ngo?i gi? v? snapshot, t?o Ch? nh?t, resume Waiting ngo?i gi?/tr??c 08:00/h?t ng?n s?ch v? gi? breached, t? ch?i h?t ng?n s?ch tr??c 08:00, G ch?y t?i ??ng 3.600/900 gi?y. SLA-24, SLA-40, SLA-41?44, SLA-56?57 ch? ph? c?c nh?nh g?n nh?t ???c ghi ch?nh x?c trong b?ng coverage.
- Nh?m 12: l?n t? ch?i th? 5, Manager ho?n t?t review khi c?n Waiting, ch?n Resolved sau Customer tr? l?i khi review v?n m?, v? hai l?i Manager thi?u; SLA-60?64 v? SLA-63 ch? ph? nh?nh k? c?n. Checker hi?n t?i c?ng ch? hi?u `resolved_attempt`/`REVIEW_REQUIRED` trong SLA-61.

**Gate logic SLA ch?nh:** nh?m 1?11 c? ca verified v? ph?p t?nh tham chi?u ?? ch?y ??t, nh?ng ?i?u ki?n ?nh?nh c? k?t qu? kh?c nhau ph?i c? ca ri?ng? trong scenario coverage ch?a ??t; ch?a x?c nh?n m? gate. **Gate t?nh b?i c?nh M-07:** nh?m 12 c? ca verified v? c?c ph?p t?nh M-07 hi?n c? ??t checker, nh?ng thi?u nh?nh ho?n t?t review trong Waiting v? c?c nh?nh nh?m 12 kh?c; ch?a x?c nh?n m? gate. Workflow review kh?ng b? gate verified n?y ch?n theo AGENTS/D-33; kh?ng tri?n khai workflow ? vi?c 1. ?i?u ki?n ho?n th?nh v1.0 c?n c?n prototype/API, quy?n backend, concurrency, d?ng l?i d? li?u, SQL v? README ch?y t? th? m?c m?i. Kh?ng s?a quy t?c gate ho?c m? r?ng vi?c 2/3.

## Artefact v? ki?m tra cu?i

File s?a ti?p trong repo: `README.md`, `TASKS.md`, `docs/spec/scenario-coverage.md`, `docs/decision-log.md`, `docs/open-questions.md`, `docs/traceability.md`, b?o c?o n?y v? manifest. File ?? dirty tr??c nhi?m v? l? `docs/spec/business-rules.md` v? `tests/sla/sla-scenarios.json` v?n nguy?n byte so v?i baseline ti?p t?c. Files th?m ? l?n ti?p t?c: `tests/sla/reference/README.md`, `validate_sla_reference.py`, `compare_sla_sources.py`, `source/{sla_draft_data.json,sla_validation_results.json,SLA_Validation_Report.md,SLA_69_Draft_Verification.md}`, `tests/evidence/{sla-reference-baseline.json,sla-reference-results.json,sla-reference-run.json,sla-source-comparison.json,sla-reference-checks.json}`, v? hai b?n l?u `tests/evidence/history/`. C?c artefact vi?c 1 t? l?n ??u g?m `audit_fixture_structure.py`, audit JSON/run JSON v? reconciliation baseline/checks; kh?ng s?a l?i k?t qu? audit.

[Ki?m tra cu?i l?n ti?p t?c](sla-reference-checks.json) ??i chi?u hash fixture/checker/report v?i run record, hash ngu?n v?i ZIP/baseline, link Markdown, manifest, Git diff v? c?c file kh?ng thu?c nhi?m v?. Kh?ng stage ho?c commit v? c?c file t?i li?u ?? dirty v? thay ??i m?i ch?ng l?n thay ??i c?, kh?ng th? t?ch an to?n b?ng stage to?n file. Kh?ng push.
