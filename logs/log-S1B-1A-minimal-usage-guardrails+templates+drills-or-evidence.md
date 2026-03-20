# log-S1B-1A (Phase 1: Minimal Usage Guardrails, Templates, and Formal Usage Drill)

---

**id**: `S1B-1A`
**kind**: `log`
**title**: `minimal usage guardrails + templates + formal usage drill + v1`
**status**: `stable`
**scope**: `S1`
**tags**: `EVOLUTION, jd-analysis, guardrails, Drills, Evidence, epic/S1, sub/S1B-1A`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `logs/runbook-S1B-formal-usage-v1.md`
  **parent_log**: `logs/log-S1B-formal-usage-guardrails+reporting-spine.md`
  **previous_log**: `logs/log-S1A-3A-minimal-evaluation-batch-import-export+delivery-surface.md`
  **reference_log_1**: `logs/log-S1A-JD-analysis-intelligence-MVP+contracts-first-spine.md`
**created**: `2026-03-20`
**updated**: `2026-03-20`

---

## Decision / Outcome

**Decision**:

- `S1B-1A` 交付的是一套最小但可正式使用的 guardrails，而不是新的 extractor 功能。
- 正式使用必须经过固定 intake 模板、固定 report template、固定 GPT enrichment contract 和统一 guardrails 命令。
- 本 phase 以 committed-head drill 证明这些护栏已经可执行，而不是只停留在说明层。

**Default choices (phase defaults / v1)**:

- 默认 guardrails 命令：`python -m wordretriever.guardrails_cli`
- 默认 guardrails 输出根目录：`artifacts/_tmp_guardrails/`
- 默认报告模板：`templates/report-template-v1.md`
- 默认样本 intake 模板：`templates/jd-sample-intake-v1.txt`
- 默认 GPT enrichment contract：`templates/gpt-enrichment-template-v1.json`

## Definitions (optional)

- `formal usage`: 一种受控工作流，要求 intake、analysis、guardrails、reporting 都遵守固定边界。
- `guardrails run`: 同时执行 evaluation smoke 与 batch smoke 的一次统一回归动作。
- `enrichment`: 位于 deterministic contracts 之外的 GPT 补充层，用于解释、摘要与额外信号整理。

## Constraints

- 不修改 `S1A` 已冻结 contracts 的字段语义。
- GPT enrichment 输出必须与 deterministic 输出分文件、分区块保存。
- 正式报告必须能回溯到 guardrail artifacts。
- 本 phase 不把新样本直接并入 gold set，除非后续单独进入样本运营 scope。

## Scope

- `P0`: 冻结 usage order、template boundaries 与 enrichment contract
- `P1`: 落 guardrails CLI 与三个模板文件
- `P2`: 跑 committed-head guardrails drill
- `P3`: 收口 runbook、evidence 与 phase closure

## Success Criteria (DoD)

- 用户能用一个命令完成 evaluation smoke 与 batch smoke。
- 新样本 intake 有固定模板，避免手工格式漂移。
- 正式报告有固定骨架，避免每轮总结越写越散。
- GPT enrichment 有明确 contract，可增量接入但不污染 deterministic 输出。
- 至少一轮 committed-head drill PASS，并记录 artifacts 与 headSha。

## Stability (what stable means)

- This log can be marked `stable` when:
  - guardrails CLI 与模板文件都已落地。
  - 一轮 committed-head drill 已完成并 PASS。
  - runbook 已明确正式使用顺序与边界。

## P0 (Contract | v1)

### P0-C1-S1 (Formal usage order | v1)

- 正式使用顺序固定为：
  - `intake`
  - `pipeline / batch`
  - `guardrails`
  - `reporting`
- 若 guardrails 未执行，则该批次不应视为正式报告输入。

### P0-C1-S2 (Template boundaries | v1)

- `templates/jd-sample-intake-v1.txt` 负责原始样本 intake。
- `templates/report-template-v1.md` 负责报告骨架。
- `templates/gpt-enrichment-template-v1.json` 负责 GPT enrichment 结构。

### P0-C1-S3 (Enrichment contract | v1)

- GPT enrichment 必须至少记录：
  - `document_id`
  - `enrichment_version`
  - `model`
  - `prompt_version`
  - `extracted_at`
  - `summary`
  - `must_haves`
  - `nice_to_haves`
  - `focus_areas`
  - `commentary`
  - `confidence`
  - `supporting_evidence`

### P0-C1-S4 (Guardrails evidence contract | v1)

- guardrails summary 必须至少记录：
  - `run_id`
  - `recorded_at`
  - `gold_set_ref`
  - `batch_input_ref`
  - `evaluation_summary_path`
  - `batch_summary_json_path`
  - `batch_summary_csv_path`
  - `samples_checked`
  - `processed_count`
  - `summary_counts`
  - `pass_fail`

## P1-C1-S1 Deliverable (Guardrails CLI | v1)

### Added CLI assets

- `src/wordretriever/guardrails.py`
- `src/wordretriever/guardrails_cli.py`

### Guardrails CLI responsibilities

- 同时执行一轮 gold-set evaluation。
- 同时执行一轮 batch smoke。
- 将 evaluation、batch 与 template references 汇总为一个 `guardrails-summary.json`。
- 用单个 PASS/FAIL 状态作为正式使用前的最小门槛。

## P1-C1-S2 Deliverable (Formal usage templates | v1)

### Added template assets

- `templates/jd-sample-intake-v1.txt`
- `templates/report-template-v1.md`
- `templates/gpt-enrichment-template-v1.json`

### Template outcome

- 新样本 intake 现在有固定的 copy-paste 格式。
- 正式报告现在有固定骨架，不需要每次临时决定章节。
- GPT enrichment 现在有固定 contract，可以逐步接入更多解释字段而不污染旧 schema。

## P2-C1-S1 Deliverable (Committed-head guardrails drill | v1)

### Drill summary

- headSha：`c09e2269e7e00471219897a9177d99947a7e970a`
- run_id：`20260320T051541Z`
- passFail：`PASS`
- `samples_checked = 3`
- `processed_count = 3`
- `summary_counts = { PASS: 3, FAIL: 0 }`

### Drill artifacts

- `artifacts/_tmp_guardrails/run_20260320T051541Z/guardrails-summary.json`
- `artifacts/_tmp_guardrails/run_20260320T051541Z/evaluation-summary.json`
- `artifacts/_tmp_guardrails/run_20260320T051541Z/batch/batch-summary.json`
- `artifacts/_tmp_guardrails/run_20260320T051541Z/batch/batch-summary.csv`

## P3-C1-S1 Deliverable (Formal usage runbook and phase closure | v1)

### Runbook outcome

- `logs/runbook-S1B-formal-usage-v1.md` 已固定正式使用顺序。
- runbook 明确区分 deterministic output、GPT enrichment 与 report layer。
- phase 结束后，用户已经可以按固定模板开始持续 intake 样本并输出不易失控的报告。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: Freeze formal usage order
- [x] `P0-C1-S2`: Freeze template boundaries
- [x] `P0-C1-S3`: Freeze GPT enrichment contract
- [x] `P0-C1-S4`: Freeze guardrails evidence contract

### P1 (Implementation)

- [x] `P1-C1-S1`: Add unified guardrails CLI
- [x] `P1-C1-S2`: Add intake, report, and GPT enrichment templates

### P2 (Drill)

- [x] `P2-C1-S1`: Run one committed-head guardrails drill

### P3 (Closure)

- [x] `P3-C1-S1`: Add formal usage runbook and close phase

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths.

### P2-C1-S1 (Committed-head guardrails drill | 2026-03-20)

- headSha: `c09e2269e7e00471219897a9177d99947a7e970a`
- artifacts:
  - `artifacts/_tmp_guardrails/run_20260320T051541Z/guardrails-summary.json`
  - `artifacts/_tmp_guardrails/run_20260320T051541Z/evaluation-summary.json`
  - `artifacts/_tmp_guardrails/run_20260320T051541Z/batch/batch-summary.json`
  - `artifacts/_tmp_guardrails/run_20260320T051541Z/batch/batch-summary.csv`
- expected:
  - One command should run the gold-set evaluation and the batch smoke against committed code.
  - The run should return machine-readable summary paths plus a single PASS/FAIL outcome.
- observed:
  - `wordretriever.guardrails_cli` completed successfully and returned `PASS`.
  - The run processed `3` gold samples in evaluation and `3` inputs in batch mode.
  - `guardrails-summary.json` captured all required references to templates and artifacts.

## Recent changes (for traceability, optional)

- 2026-03-20: 完成 `S1B-1A`，新增统一 guardrails CLI、三个 formal usage templates，并在 committed head 上通过一轮正式 guardrails drill。