# log-S2A (Sample Intake and Corpus Operations Spine)

---

**id**: `S2A`
**kind**: `log`
**title**: `sample intake and corpus operations spine v1`
**status**: `stable`
**scope**: `S2`
**tags**: `EVOLUTION, jd-analysis, sample-ops, corpus, epic/S2, sub/S2A`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: `logs/runbook-S2A-sample-operations-v1.md`
  **roadmap**: ``
  **reference_log_1**: `logs/log-S1B-formal-usage-guardrails+reporting-spine.md`
  **reference_log_2**: `logs/log-S1A-JD-analysis-intelligence-MVP+contracts-first-spine.md`
  **phase_log_1**: `logs/log-S2A-1A-sample-intake-review-and-batch-manifest-baseline+drills-or-evidence.md`
  **phase_log_2**: `TBD`
  **phase_log_3**: `TBD`
**created**: `2026-03-20`
**updated**: `2026-03-20`

---

## Decision / Outcome（结论区）

**Decision**:

- `S2A` 的目标是把样本运营从“零散追加”变成“分阶段管理的 corpus workflow”。
- v1 先建立四层样本阶段：`intake -> reviewed -> gold_candidates -> gold`。
- 样本批次必须通过 manifest 记录，后续 review、promotion 与报告都以 batch 为单位推进。

**Default choices（默认基线 / v1）**:

- 默认 intake stage：`samples/intake/`
- 默认 reviewed stage：`samples/reviewed/`
- 默认 gold candidate stage：`samples/gold_candidates/`
- 默认 sample batch manifest 入口：`python -m wordretriever.sample_ops_cli`
- 默认 review record template：`templates/sample-review-record-v1.json`

**Non-goals（不做什么）**:

- 不在 `S2A` 一开始就扩大 deterministic extractor 能力。
- 不在 `S2A` 一开始就把大量新样本并入 gold set。
- 不在 `S2A` 处理网页抓取来源治理或自动同步来源。

## Background（背景）

- `S1A` 解决了 MVP 能力，`S1B` 解决了正式使用护栏。
- 下一步真正会持续增长的是样本数量，而不是工具入口本身。
- 如果样本没有 stage 和 batch 纪律，后续 taxonomy 扩张、gold candidate 判断和报告对比都会失去可追溯性。

## Constraints（约束）

- 样本进入 repo 时必须优先保留原文。
- 不是每条样本都进入 gold；promotion 必须审慎。
- 样本阶段迁移应尽量以 batch 为单位记录，而不是随手挪动。
- 样本运营不能破坏 `S1B` 已冻结的 formal usage order。

## Scope（本 log 范围）

- 本 log 负责：
  - 固定样本 stage 结构与批次 manifest 纪律。
  - 为后续 review / promotion / corpus expansion 提供稳定起点。
  - 记录 `S2A-1A` 的 baseline implementation 与 drill。
- 本 log 不负责：
  - 新 taxonomy 的最终并入策略。
  - gold set 扩容规则的最终闭环。
  - 复杂统计报告自动化。

## Success Criteria（DoD）

- repo 中存在明确的样本 stage 目录。
- 存在一个统一入口可为样本批次生成 manifest。
- 至少一轮 sample-ops drill 在 committed head 上完成并落盘。
- 运行者可以按固定 runbook 接收新样本，而不需要临时决定放到哪里。

## Phases（切片）

- `S2A-1A`（Phase 1）：建立样本 stage、batch manifest 与 review baseline。
  - 详见：`logs/log-S2A-1A-sample-intake-review-and-batch-manifest-baseline+drills-or-evidence.md`
- `S2A-2A`（Phase 2）：review-to-gold-candidate promotion baseline。
  - 详见：`TBD`
- `S2A-3A`（Phase 3）：corpus expansion summary 与 taxonomy impact review。
  - 详见：`TBD`

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：冻结样本 stage 结构、manifest 纪律与 review record 口径。
- [x] `P1`：补齐 sample ops CLI、stage directories 与模板文件。
- [x] `P2`：在 committed head 上生成一轮正式 sample batch manifest。
- [x] `P3`：收口 runbook、phase log 与 sample-intake guidance。

## Current Status（进展摘要）

- `S2A` baseline 已完成，当前 repo 已具备稳定的样本 intake 与批次记录框架。
- 你现在可以开始持续把样本发来，我可以按固定阶段把它们整理进 corpus。
- 下一步更自然的方向是 `S2A-2A`，也就是 review 后如何提升为 gold candidate 的规则和证据链。

## Notes（落地原则，可选）

- 样本先求稳定 intake，再求高质量 review，再决定是否晋升。
- manifest 是 batch 的事实来源，report 只是阅读层。
- 如果一条样本不够干净，可以长期停留在 intake，不必强行推进。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - 样本 stage 结构、manifest 入口与 runbook 已冻结。
  - 新样本可以按统一流程持续进入系统。
  - 至少一轮 committed-head sample-ops drill 已完成并留痕。

## Recent changes（for traceability，可选）

- 2026-03-20：完成 `S2A-1A`，新增 sample ops CLI、样本 stage 目录、batch manifest 与 review record 模板，并通过 committed-head drill 将 `S2A` baseline 标记为 stable。