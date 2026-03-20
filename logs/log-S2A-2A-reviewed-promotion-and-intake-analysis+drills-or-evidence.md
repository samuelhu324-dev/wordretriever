# log-S2A-2A (Phase 2: Reviewed Promotion Baseline and Intake Analysis)

---

**id**: `S2A-2A`
**kind**: `log`
**title**: `reviewed promotion baseline + intake analysis + drills/evidence + v1`
**status**: `stable`
**scope**: `S2`
**tags**: `EVOLUTION, jd-analysis, sample-ops, review, Drills, Evidence, epic/S2, sub/S2A-2A`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `logs/runbook-S2A-sample-operations-v1.md`
  **parent_log**: `logs/log-S2A-sample-intake-and-corpus-operations-spine.md`
  **previous_log**: `logs/log-S2A-1A-sample-intake-review-and-batch-manifest-baseline+drills-or-evidence.md`
  **reference_log_1**: `logs/log-S1B-formal-usage-guardrails+reporting-spine.md`
**created**: `2026-03-20`
**updated**: `2026-03-20`

---

## Decision / Outcome

**Decision**:

- `S2A-2A` 的核心不是继续 intake，而是把 intake batch 变成 reviewed decisions 与第一版 corpus reading。
- v1 的 review outcome 允许三类主决策：`keep_in_intake`、`promote_to_reviewed`、`split_multi_role`。
- 同一批样本 review 完成后，系统应能给出 role family 分布、top skills、combination signatures 与 taxonomy gap 观察。

**Default choices (phase defaults / v1)**:

- 默认 review 入口：`python -m wordretriever.review_cli`
- 默认 review artifacts：
  - `artifacts/_tmp_review/`
  - `artifacts/_tmp_reports/`
- 默认 promoted baseline：先生成 decisions，不强制自动搬运文件。

## Definitions (optional)

- `review decision`: 对 intake 样本是否进入 reviewed 的判断。
- `combination signature`: 以 role family + 代表性技能信号拼接出的样本组合特征。
- `split_multi_role`: 一条源 JD 同时包含多个明确角色时的特殊处理决策。

## Constraints

- review decision 不应偷偷修改原始 intake 文本。
- 多角色广告不得直接混入单角色 gold candidate 路径。
- skills / combo report 是阅读层，不替代 per-sample review summary。

## Scope

- `P0`: 冻结 review decision categories、promotion baseline 与 report 输出边界
- `P1`: 补 review CLI、title-first inference fixes 与 taxonomy gap coverage
- `P2`: 跑一轮正式 intake review drill，生成 review summary 与 markdown report
- `P3`: 收口 phase log、runbook 与推荐下一步

## Success Criteria (DoD)

- 存在一个统一命令可从 batch-summary.json 生成 review summary。
- review summary 能给出每条样本的 decision、facts、taxonomy gaps 和 review notes。
- 同一批次能生成一份可读的 intake analysis report。
- 当前 8 条 intake 样本至少能稳定区分 reviewed promotion 与 multi-role split。

## Stability (what stable means)

- This log can be marked `stable` when:
  - review CLI 和 report generation 都已跑通。
  - title-first role/seniority inference 已覆盖本轮样本中的关键误差。
  - 至少一轮 intake review drill 已经落盘并形成 evidence。

## P0 (Contract | v1)

### P0-C1-S1 (Review decision contract | v1)

- `decision` 当前固定为以下集合之一：
  - `keep_in_intake`
  - `promote_to_reviewed`
  - `split_multi_role`

### P0-C1-S2 (Review record expansion | v1)

- review record 现在额外固定包含：
  - `decision`
  - `taxonomy_gaps`
  - `gold_candidate_eligible`
  - `next_action`

### P0-C1-S3 (Intake analysis report boundary | v1)

- batch review 完成后，报告至少包含：
  - decision summary
  - role family distribution
  - top skills
  - combination signatures
  - critical taxonomy gaps

## P1-C1-S1 Deliverable (Review CLI and review summary generation | v1)

### Added assets

- `src/wordretriever/review.py`
- `src/wordretriever/review_cli.py`

### Outcome

- intake batch 现在可以生成 machine-readable review summary，而不只是 batch outputs。
- 每条样本都能拿到 `decision`、`facts_present`、`taxonomy_gaps` 与 `review_notes`。

## P1-C1-S2 Deliverable (Title-first inference and taxonomy expansion | v1)

### Key implementation outcome

- seniority 现在优先以 title 判定，`mid-level` 不再被正文中的 `lead` 噪音覆盖。
- role family 现在补齐：
  - `full_stack_engineering`
  - `cloud_engineering`
  - `backend_engineering`
- 新增 facts groups 以覆盖本轮样本中的常见组合：
  - `ci_cd_tools`
  - `scripting_tools`
  - `api_and_architecture`
- `employment_conditions` 扩展到 `baseline_clearance_required` 与 `citizenship_or_pr_required`。

## P2-C1-S1 Deliverable (Formal intake review drill | v1)

### Drill artifacts

- head_sha：`81ed81f1db57dc8fd3ec3fef6a670fc856bacf4f`
- batch outputs：`artifacts/_tmp_batch_delivery/intake_20260320T074500Z/`
- review summary：`artifacts/_tmp_review/intake-review-summary-20260320T074500Z.json`
- intake report：`artifacts/_tmp_reports/intake-analysis-report-20260320T074500Z.md`

### Drill outcome

- reviewed_count = `8`
- decision_counts =
  - `promote_to_reviewed = 7`
  - `split_multi_role = 1`
- role_family_counts =
  - `backend_engineering = 2`
  - `software_engineering = 1`
  - `full_stack_engineering = 1`
  - `devops = 3`
  - `cloud_engineering = 1`
- top_skill_counts（top 7） =
  - `docker = 4`
  - `work_rights_required = 4`
  - `azure = 4`
  - `terraform = 4`
  - `aws = 3`
  - `typescript = 3`
  - `kubernetes = 3`

### Promotion observations

- `Ethos ... Full Stack Engineer` 与 `Milestone ... Mid-Level DevOps Engineer` 在当前 v1 review 下已经可稳定进入 `promote_to_reviewed`。
- `PRA ... AWS Cloud Engineer` 因一条源文本中同时出现 `Role 1` / `Role 2`，被稳定判为 `split_multi_role`。
- 当前 `critical_taxonomy_gaps = []`，说明这批样本已基本落入 v2 deterministic taxonomy 的可读范围内。

## P3-C1-S1 Deliverable (Phase closure and next-step guidance | v1)

### Closure outcome

- `S2A-2A` 已把 intake 变成可判断、可报告、可继续推进的 reviewed baseline。
- 现在系统不仅能接样本，还能先读出“要求技能”和“组合特征”。
- 下一步不再需要盲目继续扩样本；可以先基于这批 reviewed decisions 做一次有目的的读取与总结，再决定要补哪些样本。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: Freeze review decision categories
- [x] `P0-C1-S2`: Expand review record contract
- [x] `P0-C1-S3`: Freeze intake analysis report boundary

### P1 (Implementation)

- [x] `P1-C1-S1`: Add review CLI and review summary generation
- [x] `P1-C1-S2`: Tighten title-first inference and taxonomy coverage

### P2 (Drill)

- [x] `P2-C1-S1`: Run one formal intake review drill

### P3 (Closure)

- [x] `P3-C1-S1`: Close phase with report-ready guidance

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths.

### P2-C1-S1 (Formal intake review drill | 2026-03-20)

- artifacts:
  - `artifacts/_tmp_batch_delivery/intake_20260320T074500Z/batch-summary.json`
  - `artifacts/_tmp_review/intake-review-summary-20260320T074500Z.json`
  - `artifacts/_tmp_reports/intake-analysis-report-20260320T074500Z.md`
- head_sha:
  - `81ed81f1db57dc8fd3ec3fef6a670fc856bacf4f`
- expected:
  - One batch run should yield both machine-readable review decisions and a readable intake report.
  - Multi-role advertisements should be separated from ordinary reviewed promotion decisions.
- observed:
  - The batch processed `8` intake samples and the review summary recorded `7 promote_to_reviewed` plus `1 split_multi_role`.
  - The report surfaced stable role-family distribution, top skills, and combination signatures for the current intake corpus.
  - No critical taxonomy gaps were emitted in the review summary.

## Recent changes (for traceability, optional)

- 2026-03-20: 完成 `S2A-2A`，新增 review CLI、review summary、intake analysis report，并将 reviewed promotion baseline 标记为 stable。