# log-S1A-JD-analysis-intelligence-MVP+contracts-first-spine

---

**id**: `S1A`
**kind**: `log`
**title**: `JD analysis intelligence MVP + contracts-first spine v1`
**status**: `draft`
**scope**: `S1`
**tags**: `EVOLUTION, jd-analysis, intelligence, epic/S1, sub/mvp`
**links**: ``
  **issue**: ``
  **pr**: ``
  **adr**: ``
  **runbook**: ``
  **roadmap**: ``
  **reference_log_1**: `logs/_plan.md`
  **reference_log_2**: `logs/_template-log-phase-drills-evidence.md`
  **phase_log_1**: `logs/log-S1A-1A-analysis-first-MVP-contracts+taxonomy+drills-or-evidence.md`
  **phase_log_2**: `logs/log-S1A-2A-single-document-analysis-pipeline-MVP+drills-or-evidence.md`
  **phase_log_3**: `logs/log-S1A-3A-minimal-evaluation-batch-import-export+delivery-surface.md`
**created**: `2026-03-19`
**updated**: `2026-03-20`

---

## Decision / Outcome（结论区）

**Decision**:

- 本轮先做 `analysis-first` 的 JD intelligence MVP，不以网页抓取为主路径。
- MVP 的核心交付是稳定的 `document contract -> normalization -> extraction -> evidence -> export` 闭环。
- v1 输入先采用可控来源：manual text、JSON/CSV import；网页采集适配器不作为首轮前置条件。
- v1 提取策略采用 `rules-first`，LLM 仅作为后续可选增强，不进入首轮稳定面。

**Default choices（默认基线 / v1）**:

- 默认输入：单条 JD 文本或本地 JSON/CSV 导入。
- 默认存储：本地文件工件 + 轻量结构化输出；如需落库，优先 SQLite。
- 默认输出：结构化 JSON 为主，CSV 为辅。
- 默认可解释性：关键字段提取应尽量附带 evidence spans。
- 默认质量门槛：先建立小样本 gold set 回归，不追求大规模覆盖。

**Non-goals（不做什么）**:

- 不在本轮优先解决 Seek / LinkedIn 抓取稳定性。
- 不在本轮引入登录态、代理、频控、反爬绕过等采集能力。
- 不在本轮构建生产级服务、复杂前端、复杂权限体系。
- 不在本轮覆盖广泛岗位族；首轮聚焦 Platform / DevOps / SRE 邻近岗位。

## Background（背景）

- 以网页为核心的方案受页面结构变化影响大，系统稳定性被采集层绑架。
- 真正长期可维护的资产是 schema、taxonomy、extractor、evaluation，而不是 selector。
- 因此本 epic 先把分析系统的稳定边界立住，再决定是否接入额外来源。

## Constraints（约束）

- 先收口 contract 和 taxonomy，再扩展工程化实现。
- 原始文本必须保留，清洗结果不得覆盖原文。
- `facts` 与 `inferences` 必须分开，避免把判断伪装成事实。
- 提取结果应尽量保留 evidence，便于人工复核与回归。
- 任何 extractor / taxonomy 变更都应能通过小样本回归验证。

## Scope（本 log 范围）

- 本 log 负责：
  - 定义 MVP 边界、默认基线、phase 切片与执行顺序。
  - 规定首轮 contract、taxonomy、evidence、evaluation 的优先级。
  - 为后续 phase log 提供稳定索引入口。
- 本 log 不负责：
  - 具体实现细节与脚本代码。
  - drill evidence 的逐条记录与工件路径。
  - 后续多来源采集器的实现方案。

## Success Criteria（DoD）

- 结构层面：
  - 读者可在 30 秒内理解本项目首轮到底交付什么、不交付什么。
  - `phase_log_1` 已明确且可导航到首个执行切片。
- 工程层面：
  - 系统可接收至少一种可控输入并转换为统一 source object。
  - 系统可对单条 JD 输出稳定的 extraction JSON。
  - 输出至少覆盖 role family、seniority、核心技能与 evidence。
  - 系统可导出 JSON/CSV 供后续分析。
- 证据层面：
  - 每个已执行 phase 至少有 1 条带 `headSha + artifact path` 的可追溯 evidence。

## Phases（切片）

- `S1A-1A`（Phase 1）：收口 contracts、taxonomy 与 evidence 口径。
  - 详见：`logs/log-S1A-1A-analysis-first-MVP-contracts+taxonomy+drills-or-evidence.md`
- `S1A-2A`（Phase 2）：实现单文档分析管线 MVP。
  - 详见：`logs/log-S1A-2A-single-document-analysis-pipeline-MVP+drills-or-evidence.md`
- `S1A-3A`（Phase 3）：建立最小 evaluation、批量导入导出与 MVP 交付面。
  - 详见：`logs/log-S1A-3A-minimal-evaluation-batch-import-export+delivery-surface.md`

## Execution Checklist（当前骨架里程碑汇总）

- [x] `P0`：冻结 MVP 边界、核心 schema、taxonomy 与 evidence contract。
- [x] `P1`：跑通单条 JD 的输入、清洗、提取、结构化输出。
- [ ] `P2`：建立最小 gold set、回归检查与 evidence 纪律。
- [ ] `P3`：补齐批量 import/export 与最小使用入口。

## Current Status（进展摘要）

- 当前仍处于 `draft`，但 `S1A-1A` 与 `S1A-2A` 都已完成并形成 evidence 链，`S1A-3A` 也已创建并冻结 P0 默认边界。
- `S1A-3A` 当前处于 phase log 已建立、实现尚未开始的状态；执行重心已正式切换到 evaluation 与 batch delivery。
- 当前主要风险是 phase 3 可能同时展开 gold set、batch CLI、export 三条线，导致实现顺序失控；因此需严格按 `P1 -> P2 -> P3` 推进。

## Notes（落地原则，可选）

- 先分析、后采集；采集适配器是输入源，不是系统中心。
- 先做单文档，再做批量；先做规则，再加模型；先做可解释，再谈复杂度。
- evidence 要能支持回看“为什么判成这个 role / skill”。

## Stability（stable 口径）

- 本 log 标记为 `stable` 表示：
  - MVP 边界、默认基线、phase 拆分与 evidence 口径已经稳定。
  - 至少一个稳定入口可把 JD 文本跑成结构化输出。
  - Phase 1 到 Phase 3 的最小闭环已被实际执行并有证据链。

## Numbering & Commit Naming（编号与提交命名）

- 编号约定：`P<n>` 表示 Phase，`C<n>` 表示 Cycle，`S<n>` 表示 Step。
- Commit / PR 命名：
  - 基础形式：`<ID>/P<phase>-C<cycle>-S<steps>: <summary>`；
  - `<steps>` 可以是单个 step（`1`，即 `...-S1`），也可以是在同一 phase / cycle 下连续的多个 step 合并（如 `1S2`，即 `...-S1S2`）。
  - Multi-step 规则：只允许在 **同一 Phase + 同一 Cycle** 下合并多个 step；一旦跨 Phase 或跨 Cycle，必须拆成多次 commit。

**Branch 约定（建议）**:

- `S1A` 相关改动默认落在 `S1A-*` 前缀工作分支上，便于回溯 `scope -> branch -> commits -> artifacts`。
- 若后续把 import/export、evaluation、采集适配器拆分为不同 scope，优先保持 parent spine 对单一 scope 的聚焦，不在一条 PR 混入多条演进主线。

**Commit 纪律（建议）**:

- 完成每个关键 `P*-C*-S*` 单元后，尽量及时提交，避免 contracts、taxonomy、scripts 与 evidence 混在同一大提交中。
- 推荐节奏：先在 `S1A-*` 分支上按 `P*-C*-S*` 粒度积累清晰 commit，再定期向 `main` 发起聚焦 PR。

## Recent changes（for traceability，可选）

- 2026-03-20：创建 `S1A-3A` phase log，并冻结 phase 3 的默认边界、计划与执行顺序。
- 2026-03-20：`S1A-2A` 完成 phase closure，单文档 pipeline MVP 已形成稳定入口、artifact 与 evidence 链，整体工作进入 `S1A-3A` 准备阶段。
- 2026-03-19：新增 `S1A-2A` phase 索引，明确 Phase 2 进入单文档 analysis pipeline MVP 实现准备。
- 2026-03-19：创建 `log-S1A`，确定本项目首轮为 analysis-first 的 MVP 主 spine，并把首个执行切片固定为 `S1A-1A`。