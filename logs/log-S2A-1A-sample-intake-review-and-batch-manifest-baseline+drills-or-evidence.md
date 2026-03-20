# log-S2A-1A (Phase 1: Sample Intake, Review, and Batch Manifest Baseline)

---

**id**: `S2A-1A`
**kind**: `log`
**title**: `sample intake + review + batch manifest baseline + drills/evidence + v1`
**status**: `stable`
**scope**: `S2`
**tags**: `EVOLUTION, jd-analysis, sample-ops, Drills, Evidence, epic/S2, sub/S2A-1A`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `logs/runbook-S2A-sample-operations-v1.md`
  **parent_log**: `logs/log-S2A-sample-intake-and-corpus-operations-spine.md`
  **previous_log**: `logs/log-S1B-1A-minimal-usage-guardrails+templates+drills-or-evidence.md`
  **reference_log_1**: `logs/log-S1B-formal-usage-guardrails+reporting-spine.md`
**created**: `2026-03-20`
**updated**: `2026-03-20`

---

## Decision / Outcome

**Decision**:

- `S2A-1A` 交付的是样本阶段管理 baseline，而不是 taxonomy 扩张本身。
- 所有新样本先经过 `intake`，再视情况进入 `reviewed`、`gold_candidates`、`gold`。
- 样本批次必须先有 manifest，后续 review / promotion 才有可追溯入口。

**Default choices (phase defaults / v1)**:

- 默认 stage 目录：
  - `samples/intake/`
  - `samples/reviewed/`
  - `samples/gold_candidates/`
  - `samples/gold/`
- 默认 batch manifest template：`templates/sample-batch-manifest-v1.json`
- 默认 sample review template：`templates/sample-review-record-v1.json`
- 默认 manifest 命令：`python -m wordretriever.sample_ops_cli`

## Definitions (optional)

- `intake`: 原始样本入口层。
- `reviewed`: 已经过基础清理和人工确认的样本层。
- `gold_candidate`: 可能进入 gold set，但还未正式承诺稳定性的样本层。
- `batch manifest`: 一次样本批次的机器可读索引文件。

## Constraints

- 不提前把 intake 文本翻译成 taxonomy 结论。
- 不因为想补覆盖面就把不稳定样本推进到 gold。
- batch manifest 记录的是文件级索引，不替代 review judgment。

## Scope

- `P0`: 冻结样本 stage、manifest 字段与 review record 口径
- `P1`: 落 sample ops CLI、stage directories 与模板
- `P2`: 跑一轮 committed-head sample manifest drill
- `P3`: 收口 runbook 与 phase closure

## Success Criteria (DoD)

- 样本 stage 目录存在并被版本管理。
- 能通过一个命令为某个样本目录生成 batch manifest。
- 存在 review record template，便于后续逐条样本判断。
- 至少一轮 committed-head manifest drill 已落盘。

## Stability (what stable means)

- This log can be marked `stable` when:
  - sample ops CLI 与 stage directories 已落地。
  - manifest template 与 review template 已冻结。
  - committed-head drill 已完成并可回溯。

## P0 (Contract | v1)

### P0-C1-S1 (Sample stage contract | v1)

- 新样本先进入 `samples/intake/`。
- 经过基础整理后，才允许移动到 `samples/reviewed/`。
- 只有经过额外稳定性判断的样本，才允许进入 `samples/gold_candidates/`。

### P0-C1-S2 (Batch manifest contract | v1)

- manifest 至少包含：
  - `batch_id`
  - `created_at`
  - `stage`
  - `sample_count`
  - `input_dir`
  - `items[]`
- `items[]` 至少包含：
  - `sample_id`
  - `input_path`
  - `stage`
  - `source_type`
  - `notes`

### P0-C1-S3 (Review record contract | v1)

- review record 至少包含：
  - `sample_id`
  - `reviewed_at`
  - `review_status`
  - `source_path`
  - `normalized_destination`
  - `deterministic_summary`
  - `review_notes`
  - `gold_candidate`
  - `enrichment_recommended`

## P1-C1-S1 Deliverable (Sample ops CLI and stage directories | v1)

### Added assets

- `src/wordretriever/sample_ops.py`
- `src/wordretriever/sample_ops_cli.py`
- `samples/intake/.gitkeep`
- `samples/reviewed/.gitkeep`
- `samples/gold_candidates/.gitkeep`

### Outcome

- repo 现在已有清晰的样本 stage 目录。
- `wordretriever.sample_ops_cli` 可以把一个目录中的 `.txt` 样本整理成 batch manifest。

## P1-C1-S2 Deliverable (Manifest and review templates | v1)

### Added assets

- `templates/sample-batch-manifest-v1.json`
- `templates/sample-review-record-v1.json`

### Outcome

- 新样本批次现在有固定 manifest 结构。
- 后续逐条 review 时也有固定记录模板，不需要每次重想字段。

## P2-C1-S1 Deliverable (Committed-head sample manifest drill | v1)

### Drill summary

- headSha：`3db9de5ffc5ea92b9857661cb3ecea8912270119`
- artifact：`artifacts/_tmp_sample_ops/sample-batch-manifest-20260320T053200Z.json`
- batch_id：`gold-batch-20260320`
- stage：`gold`
- sample_count：`3`

### Drill outcome

- 已对 `samples/gold/` 成功生成正式 batch manifest。
- manifest 覆盖当前 `3` 条 gold 样本，可作为后续 corpus operations 的最小索引基线。

## P3-C1-S1 Deliverable (Runbook and phase closure | v1)

### Runbook outcome

- `logs/runbook-S2A-sample-operations-v1.md` 已固定样本运营顺序与 stage 含义。
- phase closure 后，你已经可以开始以批次方式把新样本交给我处理。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: Freeze sample stage contract
- [x] `P0-C1-S2`: Freeze batch manifest contract
- [x] `P0-C1-S3`: Freeze review record contract

### P1 (Implementation)

- [x] `P1-C1-S1`: Add sample ops CLI and stage directories
- [x] `P1-C1-S2`: Add batch manifest and review templates

### P2 (Drill)

- [x] `P2-C1-S1`: Run one committed-head sample manifest drill

### P3 (Closure)

- [x] `P3-C1-S1`: Add sample ops runbook and close phase

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths.

### P2-C1-S1 (Committed-head sample manifest drill | 2026-03-20)

- headSha: `3db9de5ffc5ea92b9857661cb3ecea8912270119`
- artifacts:
  - `artifacts/_tmp_sample_ops/sample-batch-manifest-20260320T053200Z.json`
- expected:
  - One command should produce a machine-readable manifest for a controlled sample directory.
  - The manifest should preserve stage, sample_count, and file paths for later review and promotion work.
- observed:
  - `wordretriever.sample_ops_cli` completed successfully for `samples/gold`.
  - The output manifest recorded `batch_id=gold-batch-20260320`, `stage=gold`, and `sample_count=3`.

## Recent changes (for traceability, optional)

- 2026-03-20: 完成 `S2A-1A`，新增 sample ops CLI、样本分层目录、manifest/review 模板，并通过 committed-head drill 将样本运营 baseline 标记为 stable。