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

## P0 Deliverable (Implementation defaults frozen | v1)

### P0 outcome summary

- 本 phase 的默认实现语言冻结为 Python。
- 单文档 pipeline 的最小工程布局冻结为：
  - `src/wordretriever/`
  - `samples/manual/`
  - `artifacts/_tmp_single_doc_pipeline/`
- 输入路径、样本路径、artifacts 路径彼此分离，避免 phase 2 的实现工件与受控样本混在一起。
- 本 phase 继续复用 `S1A-1A` 的 source / normalized / extraction / evidence contract，不新增并行 schema。

### P0 frozen defaults for implementation

- 入口语言：Python
- 入口风格：CLI-first
- 受控样本位置：`samples/manual/`
- phase 2 临时工件位置：`artifacts/_tmp_single_doc_pipeline/`
- 实现包根位置：`src/wordretriever/`

### P0 outcome

- `P0-C1-S1`、`P0-C1-S2`、`P0-C1-S3` 视为已冻结，可直接交给 `P1` 开始落实现骨架。

## P1-C1-S1 Deliverable (Minimal directory and artifact layout | v1)

### Created layout

- `src/wordretriever/`
- `samples/manual/`
- `artifacts/_tmp_single_doc_pipeline/`

### Layout rationale

- `src/wordretriever/`：存放 phase 2 后续的 loader、mapper、extractor 和 CLI 入口。
- `samples/manual/`：存放受控手工样本，作为单文档 drill 的输入源。
- `artifacts/_tmp_single_doc_pipeline/`：存放 phase 2 drill 产生的 JSON 工件，避免和 logs 或 source samples 混放。

### P1-C1-S1 outcome

- phase 2 的最小目录布局已经落盘，可直接承接下一步 CLI 入口和 pipeline skeleton。
- 后续实现应继续在上述目录内推进，不临时新开平行目录结构。

## P1-C1-S2 Deliverable (Python CLI entrypoint fixed | v1)

### CLI entrypoint

- 本 phase 的单文档 pipeline 入口固定为：`wordretriever.cli`
- CLI 输入参数：
  - `input_path`
  - `--input-format`，支持 `text` / `json` / `csv`
  - `--output-path`，默认写入 `artifacts/_tmp_single_doc_pipeline/latest_output.json`

### CLI usage contract

- 入口职责：
  - 接收单条输入文件路径
  - 调用 pipeline 运行 source -> normalized -> extraction
  - 把结果写成 JSON artifact
- 默认受控样本：`samples/manual/platform-engineer-002.txt`
- 当前实现约定：先支持单条输入，不在 CLI 层做批量调度。

### P1-C1-S2 outcome

- Python CLI 入口已经固定，后续实现与 drill 都应围绕该入口推进。
- phase 2 后续无需再讨论入口形式，直接在 `wordretriever.cli` 上迭代。

## P1-C1-S3 Deliverable (Pipeline skeleton | v1)

### Implemented skeleton modules

- `src/wordretriever/contracts.py`
- `src/wordretriever/loader.py`
- `src/wordretriever/normalize.py`
- `src/wordretriever/extract.py`
- `src/wordretriever/pipeline.py`
- `src/wordretriever/cli.py`
- `samples/manual/platform-engineer-002.txt`

### Skeleton responsibilities

- `contracts.py`：定义 source、normalized、extraction、pipeline result 的最小数据结构。
- `loader.py`：支持从 `text` / `json` / `csv` 加载单条 source document。
- `normalize.py`：执行最小 title/company/location 清洗与 employment type 推断。
- `extract.py`：按 rules-first 方式抽取 facts，并做 role family / seniority 的最小 inference。
- `pipeline.py`：串联 loader、mapper、extractor，并提供 JSON 输出写入函数。
- `cli.py`：固定单文档 pipeline 的运行入口。

### P1-C1-S3 outcome

- 单文档 pipeline 的最小实现骨架已经存在，可直接进入受控样本 drill。
- 下一步应进入 `P2-C1-S1`，用 `samples/manual/platform-engineer-002.txt` 跑出第一份 extraction artifact。

## P2-C1-S1 Deliverable (Single-document drill run | v1)

### Drill input

- 输入样本：`samples/manual/platform-engineer-002.txt`
- CLI 入口：`wordretriever.cli`
- 输入格式：`text`
- 输出工件：`artifacts/_tmp_single_doc_pipeline/platform-engineer-002.output.json`

### Drill result summary

- pipeline 已成功跑通 source -> normalized -> extraction 三段链路。
- 已生成第一份单文档 extraction artifact。
- artifact 包含：
  - `source`
  - `normalized`
  - `extraction`
- extraction 结果已包含：
  - `facts.cloud_platforms = ["aws"]`
  - `facts.containers = ["kubernetes"]`
  - `facts.iac_tools = ["terraform"]`
  - `facts.observability_tools = ["datadog", "prometheus"]`
  - `facts.programming_languages = ["python", "go"]`
  - `inferences.role_family = "platform_engineering"`
  - `inferences.seniority = "senior"`

### Drill observations

- 当前受控样本使用 `text` loader 路径，title 能被捕获，但 `company` 与 `location` 仍为 `null`。
- 这说明 CLI 和 pipeline 已可执行，但 text loader 还没有从正文前几行里提取 `Location:` / `Company:` 元信息。
- 对 `P2-C1-S1` 来说，这不是阻断项，因为单文档 pipeline 已经真正跑通；但它会成为 `P2-C1-S2` review 的重点之一。

### P2-C1-S1 outcome

- `S1A-2A` 的第一条单文档 drill 已完成。
- phase 2 已从“只有骨架”进入“可运行并产出 artifact”的状态。
- 下一步应进入 `P2-C1-S2`，对照 `S1A-1A` 的 frozen contracts 检查输出是否需要修正。

### P2 (Drill / Verify)

- `P2-C1-S1`: 用 1 条受控样本跑通 pipeline 并生成 extraction JSON。
- `P2-C1-S2`: 核对输出是否符合 `S1A-1A` 的 contract 与 review rules。

### P3 (Evidence / closure)

- `P3-C1-S1`: 记录单文档 pipeline 的第一条 evidence JSON。
- `P3-C1-S2`: 收口 phase 2 的最小实现边界与后续批量化 handoff。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: Implementation entrypoint and layout | v1
- [x] `P0-C1-S2`: Input and output contract binding | v1
- [x] `P0-C1-S3`: Evidence contract reuse | v1

### P1 (Implementation)

- [x] `P1-C1-S1`: Define minimal directory and artifact layout
- [x] `P1-C1-S2`: Fix Python CLI as pipeline entrypoint
- [x] `P1-C1-S3`: Draft pipeline skeleton for loader, mapper, and extractor

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: Run one controlled sample through the pipeline
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
  - Ran `wordretriever.cli` against `samples/manual/platform-engineer-002.txt` and produced `artifacts/_tmp_single_doc_pipeline/platform-engineer-002.output.json`.
  - Output retained document_id, extractor_version, taxonomy_version, and evidence fields.
  - Text loader baseline did not yet lift company/location metadata into source fields, which will be reviewed in `P2-C1-S2`.

## Recent changes (for traceability, optional)

- 2026-03-20: 完成 `S1A-2A/P2-C1-S1`，跑通第一条单文档 drill 并生成 extraction artifact。
- 2026-03-20: 完成 `S1A-2A/P1-C1-S2` 与 `P1-C1-S3`，固定 Python CLI 入口并落下单文档 pipeline skeleton。
- 2026-03-19: 完成 `S1A-2A/P0-C1-S1S3` 与 `P1-C1-S1`，冻结 phase 2 默认实现布局并创建最小目录结构。
- 2026-03-19: 创建 `log-S1A-2A`，把第二阶段固定为单文档 analysis pipeline MVP 的实现准备与 drill/evidence 记录。