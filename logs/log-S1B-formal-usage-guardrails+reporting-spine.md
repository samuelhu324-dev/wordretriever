# log-S1B (Formal Usage Guardrails and Reporting Spine)

---

**id**: `S1B`
**kind**: `log`
**title**: `formal usage guardrails + reporting spine v1`
**status**: `stable`
**scope**: `S1`
**tags**: `EVOLUTION, jd-analysis, guardrails, reporting, epic/S1, sub/S1B`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: `logs/runbook-S1B-formal-usage-v1.md`
  **roadmap**: ``
  **reference_log_1**: `logs/log-S1A-JD-analysis-intelligence-MVP+contracts-first-spine.md`
  **reference_log_2**: `logs/log-S1A-3A-minimal-evaluation-batch-import-export+delivery-surface.md`
  **phase_log_1**: `logs/log-S1B-1A-minimal-usage-guardrails+templates+drills-or-evidence.md`
  **phase_log_2**: `TBD`
  **phase_log_3**: `TBD`
**created**: `2026-03-20`
**updated**: `2026-03-20`

---

## Decision / Outcome（结论区）

**Decision**:

- `S1B` 的目标不是扩 taxonomy，而是把 `S1A` 的 MVP 变成一个可正式持续使用、但不容易失控的工作流。
- v1 正式使用护栏固定为四件事：统一 regression 入口、固定 report skeleton、固定 sample intake 格式、固定 GPT enrichment 边界。
- GPT 可以进入系统，但只能以 enrichment 形式接入，不得回写或污染 `S1A` 已冻结的 deterministic contracts。

**Default choices（默认基线 / v1）**:

- 默认 regression 入口：`python -m wordretriever.guardrails_cli`
- 默认 report template：`templates/report-template-v1.md`
- 默认 intake template：`templates/jd-sample-intake-v1.txt`
- 默认 enrichment contract：`templates/gpt-enrichment-template-v1.json`
- 默认正式使用节奏：先 intake，再 pipeline/batch，再 guardrails，再报告。

**Non-goals（不做什么）**:

- 不在 `S1B` 扩大 gold set 覆盖面。
- 不在 `S1B` 追求新的 extractor 能力或 taxonomy 扩展。
- 不在 `S1B` 引入 UI、数据库服务化或网页抓取。

## Background（背景）

- `S1A` 已经证明 analysis-first MVP 可以跑通，但缺少“正式使用时如何不越跑越乱”的护栏。
- 如果没有固定的 sample intake、report skeleton 与 GPT 边界，后续扩样本和出报告时很容易出现 contract drift。
- 因此 `S1B` 先把使用流程和回归入口冻结，再进入样本运营型的后续 scope。

## Constraints（约束）

- 不修改 `S1A` 已冻结的 source / normalized / facts / inferences / evidence contract 语义。
- GPT enrichment 必须和 deterministic 输出分层保存。
- 正式报告必须能回溯到 guardrail artifacts，而不是只保留自然语言总结。
- 新样本 intake 必须保留原始文本，不允许先手工“翻译成 taxonomy”。

## Scope（本 log 范围）

- 本 log 负责：
  - 固定正式使用顺序、模板与回归入口。
  - 为后续样本扩张提供稳定的 intake / report / enrichment 边界。
  - 记录 guardrails drill 的完成状态。
- 本 log 不负责：
  - 新 taxonomy 类别的扩展。
  - 新 gold 样本批次的持续积累。
  - GPT prompt 深度优化或多模型比较。

## Success Criteria（DoD）

- 存在一个统一命令可同时跑 evaluation 与 batch smoke。
- 正式使用者有固定的 sample intake 模板、report template 与 enrichment template。
- 至少一轮 guardrails drill 在 committed head 上通过，并形成可追溯 artifacts。
- `S1B` 完成后，用户可以在不改旧 contracts 语义的情况下开始持续加样本和写报告。

## Phases（切片）

- `S1B-1A`（Phase 1）：建立最小 usage guardrails、模板与 formal usage drill。
  - 详见：`logs/log-S1B-1A-minimal-usage-guardrails+templates+drills-or-evidence.md`

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：冻结正式使用顺序、模板边界与 enrichment 接口。
- [x] `P1`：补齐 guardrails CLI、report template、intake template、GPT enrichment template。
- [x] `P2`：在 committed head 上跑通 guardrails drill。
- [x] `P3`：收口 evidence、runbook 与 stable usage guidance。

## Current Status（进展摘要）

- `S1B` 已完成，当前已有可重复运行的 formal usage 护栏。
- 当前 `S1` 系列已经具备两层稳定面：`S1A` 负责 MVP 能力，`S1B` 负责正式使用护栏。
- 下一步最合理的演进方向不再是继续补护栏，而是进入样本扩张型 scope，例如 `S2A`。

## Notes（落地原则，可选）

- deterministic output 用于长期比较；GPT enrichment 用于解释和补充，不用于覆盖 deterministic 字段。
- 报告是 artifacts 的阅读层，不是事实来源本身。
- guardrails 应在每一批正式报告前至少执行一次。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - 正式使用顺序、模板与 guardrails 入口已经冻结。
  - `S1A` 的 MVP 可以在不破坏旧 contract 的前提下被持续使用。
  - 至少一轮 committed-head guardrails drill 已经通过并有证据链。

## Numbering & Commit Naming（编号与提交命名）

- 编号约定：`P<n>` 表示 Phase，`C<n>` 表示 Cycle，`S<n>` 表示 Step。
- Commit / PR 命名：
  - 基础形式：`<ID>/P<phase>-C<cycle>-S<steps>: <summary>`；
  - `<steps>` 可以是单个 step（`1`），也可以是在同一 phase / cycle 下连续的多个 step 合并（如 `1S2`）。

## Recent changes（for traceability，可选）

- 2026-03-20：完成 `S1B-1A`，新增 `guardrails_cli`、usage templates 与 formal usage runbook，并通过 committed-head drill 将 `S1B` 标记为 stable。