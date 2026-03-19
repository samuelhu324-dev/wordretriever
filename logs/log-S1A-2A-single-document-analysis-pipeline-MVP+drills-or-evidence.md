# log-S1A-2A (Phase 2: Single-Document Analysis Pipeline MVP)

---

**id**: `S1A-2A`
**kind**: `log`
**title**: `single-document analysis pipeline MVP + drills/evidence + v1`
**status**: `draft`
**scope**: `S1`
**tags**: `EVOLUTION, jd-analysis, Drills, Evidence, epic/S1, sub/S1A-2A`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `logs/log-S1A-JD-analysis-intelligence-MVP+contracts-first-spine.md`
  **previous_log**: `logs/log-S1A-1A-analysis-first-MVP-contracts+taxonomy+drills-or-evidence.md`
  **reference_log_1**: `logs/_plan.md`
**created**: `2026-03-19`
**updated**: `2026-03-19`

---

## Decision / Outcome

**Decision**:

- 本 phase 目标是把 `S1A-1A` 已冻结的 contract baseline 落成一个可运行的单文档 analysis pipeline MVP。
- v1 实现优先支持 manual text / JSON / CSV 输入，不接入网页采集器。
- 提取策略继续采用 `rules-first`，确保 pipeline 先稳定跑通输入、清洗、提取、evidence 输出四段链路。

**Default choices (phase defaults / v1)**:

- 默认入口：Python CLI。
- 默认范围：单文档输入先跑通，再考虑批量。
- 默认实现顺序：source loader -> normalized mapper -> rules extractor -> evidence output。
- 默认输出：结构化 JSON 工件；必要时附加控制台摘要。
- 默认工件纪律：样本、导出物和 drills evidence 分目录存放，不把抓取型原始数据混入本 phase。

## Definitions (optional)

- `single-document pipeline`: 从单条 JD 输入到 extraction JSON 输出的完整处理链路。
- `source loader`: 负责把 manual text / JSON / CSV 映射成 source object 的入口层。
- `normalized mapper`: 负责执行最小文本清洗和字段标准化。
- `rules extractor`: 负责按 taxonomy 与 review rules 生成 facts / inferences / evidence。
- `pipeline artifact`: pipeline 执行后产生的 JSON 输出或 drill evidence 文件。

## Constraints

- 不回退修改 `S1A-1A` 已冻结的 contract 语义。
- 不在本 phase 临时扩张 taxonomy 去追单个样本。
- 不把多文档批处理、统计聚合或 dashboard 混进单文档 pipeline phase。
- 不把网页抓取、登录态、远程 API 接入当作本 phase 的前置条件。

## Scope

- `P0`: implementation defaults（目录、入口、输入输出约定、artifact 纪律）
- `P1`: 单文档 pipeline 骨架实现
- `P2`: 单文档 drill / verify
- `P3`: evidence 与 phase closure

## Success Criteria (DoD)

- 单条 JD 文本可以被 loader 接收并映射为 source object。
- pipeline 能生成 normalized object 和 extraction object。
- extraction 输出符合 `S1A-1A` 中冻结的 facts / inferences / evidence contract。
- 至少有 1 条单文档 drill 证据记录 pipeline 跑通结果。
- 输出工件路径、输入样本 id、extractor/taxonomy 版本可追溯。

## Stability (what stable means)

- This log can be marked `stable` when:
  - 单文档 pipeline 的入口、输出格式、drill evidence 都已实际跑通。
  - `P0-P3` 的默认实现边界已经稳定，不需要再回头修改 phase contract。
  - The Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## P0 (Contract | v1)

### P0-C1-S1 (Implementation entrypoint and layout | v1)

- 默认实现语言：Python。
- 默认入口形式：CLI 脚本，例如 `python -m ...` 或单入口脚本。
- 建议最小目录：
  - `src/` 或等价实现目录
  - `samples/` 保存受控输入样本
  - `artifacts/` 保存 drill 输出
- 输入、输出和 evidence 文件应分开存放。

### P0-C1-S2 (Input and output contract binding | v1)

- 输入支持：manual text、JSON、CSV。
- 输出必须绑定到 `S1A-1A` 的 source / normalized / extraction contract。
- 缺失字段允许 `null` / `unknown`，不得伪造数据。
- 所有输出必须附带 `document_id`，保持链路可追溯。

### P0-C1-S3 (Evidence contract reuse | v1)

- Evidence JSON must include:
  - `inputSampleId`
  - `artifactPaths`
  - `extractorVersion`
  - `taxonomyVersion`
  - `passFail`
- 本 phase 直接复用 `S1A-1A` 的 evidence JSON 规则，不另起一套格式。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S1A-2A` 相关改动继续落在当前 `S1A-*` 分支上，保持与 parent spine 的 scope 一致。
- 当实现文件开始增加时，优先把 docs/log 与代码变更按 `P*-C*-S*` 拆成小提交，避免 phase 2 重新变成一条大杂烩提交。

**Commit discipline (recommended)**:

- 推荐先以 `P0` 和 `P1` 的 docs/骨架提交开路，再逐步提交实现文件。
- 示例：
  - `S1A-2A/P0-C1-S1S3: define pipeline entrypoint and artifact rules`
  - `S1A-2A/P1-C1-S1S2: add source loader and normalized mapper skeleton`

## Plan (draft)

### P1 (Implementation)

- `P1-C1-S1`: 约定最小目录结构、样本目录和 artifacts 目录。
- `P1-C1-S2`: 选定 Python CLI 作为单文档 pipeline 入口。
- `P1-C1-S3`: 设计 source loader、normalized mapper、rules extractor 的最小骨架。

### P2 (Drill / Verify)

- `P2-C1-S1`: 用 1 条受控样本跑通 pipeline 并生成 extraction JSON。
- `P2-C1-S2`: 核对输出是否符合 `S1A-1A` 的 contract 与 review rules。

### P3 (Evidence / closure)

- `P3-C1-S1`: 记录单文档 pipeline 的第一条 evidence JSON。
- `P3-C1-S2`: 收口 phase 2 的最小实现边界与后续批量化 handoff。

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: Implementation entrypoint and layout | v1
- [ ] `P0-C1-S2`: Input and output contract binding | v1
- [ ] `P0-C1-S3`: Evidence contract reuse | v1

### P1 (Implementation)

- [ ] `P1-C1-S1`: Define minimal directory and artifact layout
- [ ] `P1-C1-S2`: Fix Python CLI as pipeline entrypoint
- [ ] `P1-C1-S3`: Draft pipeline skeleton for loader, mapper, and extractor

### P2 (Drill / Verify)

- [ ] `P2-C1-S1`: Run one controlled sample through the pipeline
- [ ] `P2-C1-S2`: Review output against frozen contracts

### P3 (Evidence / closure)

- [ ] `P3-C1-S1`: Record single-document pipeline evidence JSON
- [ ] `P3-C1-S2`: Freeze phase outputs and handoff to batch-oriented phase

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### <Pn-Cx-Sy> (Single-document pipeline drill | 2026-03-19)

- headSha: `<git sha>`
- artifacts: `artifacts/_tmp_single_doc_pipeline/drills_<ts>.json`
- env (example, optional):
  - `PIPELINE_SCOPE=single_document`
  - `EXTRACTOR_VERSION=v1-rules-baseline`
- expected:
  - One controlled JD sample can reach extraction output without breaking the frozen contracts.
  - Output artifacts retain document_id, versions, and evidence fields.
- observed:
  - Pending first implementation drill.

## Recent changes (for traceability, optional)

- 2026-03-19: 创建 `log-S1A-2A`，把第二阶段固定为单文档 analysis pipeline MVP 的实现准备与 drill/evidence 记录。