# log-S1A-3A (Phase 3: Minimal Evaluation, Batch Import/Export, and MVP Delivery Surface)

---

**id**: `S1A-3A`
**kind**: `log`
**title**: `minimal evaluation + batch import/export + MVP delivery surface + drills/evidence + v1`
**status**: `draft`
**scope**: `S1`
**tags**: `EVOLUTION, jd-analysis, Drills, Evidence, epic/S1, sub/S1A-3A`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `logs/log-S1A-JD-analysis-intelligence-MVP+contracts-first-spine.md`
  **previous_log**: `logs/log-S1A-2A-single-document-analysis-pipeline-MVP+drills-or-evidence.md`
  **reference_log_1**: `logs/log-S1A-1A-analysis-first-MVP-contracts+taxonomy+drills-or-evidence.md`
**created**: `2026-03-20`
**updated**: `2026-03-20`

---

## Decision / Outcome

**Decision**:

- 本 phase 目标是在 `S1A-2A` 已稳定的单文档 pipeline 之上，补齐最小 evaluation、批量 import/export 与 MVP 交付入口。
- v1 继续保持 `analysis-first` 路线，不引入网页抓取器、服务化部署或复杂前端。
- phase 3 的核心任务不是重写 extractor，而是让现有 pipeline 进入“可批量运行、可最小评估、可最小交付”的状态。

**Default choices (phase defaults / v1)**:

- 默认 evaluation 形式：小样本 gold set + 规则化 review summary。
- 默认批量范围：本地 folder / JSON / CSV 输入，不接外部数据源。
- 默认交付入口：Python CLI-first，优先单命令批量运行方式。
- 默认导出物：批量 JSON 结果、最小 CSV 摘要、evaluation summary JSON。
- 默认证据纪律：每次 batch/eval drill 都记录输入集、输出工件、headSha 和 PASS/FAIL。

## Definitions (optional)

- `gold set`: 一组受控、可人工复核的 JD 样本及其期望标签/判断。
- `batch run`: 对多条输入样本连续执行单文档 pipeline，并收集统一输出的运行方式。
- `evaluation summary`: 对 gold set 的命中情况、偏差点和通过状态做的结构化汇总。
- `delivery surface`: 面向使用者的最小入口，例如批量 CLI、导出目录和说明性输出。

## Constraints

- 不回退 `S1A-1A` 已冻结的 contracts / taxonomy / evidence 口径。
- 不回退 `S1A-2A` 已冻结的单文档 pipeline 边界。
- 不在本 phase 临时扩张岗位 taxonomy 去追单条异常样本。
- 不把抓取适配器、数据库服务化、前端界面混入 phase 3。

## Scope

- `P0`: phase 3 defaults（evaluation、batch import/export、delivery surface、evidence contract）
- `P1`: 最小 gold set 与 evaluation 骨架
- `P2`: batch import/export 与 delivery 入口
- `P3`: drills、evidence 与 phase closure

## Success Criteria (DoD)

- 至少有 1 组最小 gold set 能用于复核关键 extraction 输出。
- 用户可以通过一个明确的批量入口对多条本地样本运行 pipeline。
- 系统能导出批量 JSON 结果与最小 CSV 摘要。
- evaluation 与 batch drill 都能生成可追溯 evidence。
- phase 3 完成后，MVP 达到“可批量输入、可最小评估、可最小交付”的状态。

## Stability (what stable means)

- This log can be marked `stable` when:
  - phase 3 的 evaluation、batch import/export 与 delivery 入口都已实际跑通。
  - 至少有 1 条 evaluation evidence 与 1 条 batch delivery evidence 可追溯。
  - `S1A-2A` 的稳定边界没有被 phase 3 回头破坏。

## P0 (Contract | v1)

### P0-C1-S1 (Evaluation contract | v1)

- 最小 gold set 应覆盖：
  - `role_family`
  - `seniority`
  - 至少 3 组核心 facts 类别
- evaluation 输出至少包含：
  - `sample_id`
  - `expected`
  - `observed`
  - `pass_fail`
  - `notes`
- v1 不追求复杂评分体系，先以 PASS/FAIL + 偏差说明为主。

### P0-C1-S2 (Batch import/export contract | v1)

- batch 输入支持：
  - 本地目录下的 text files
  - 本地 JSON 文件
  - 本地 CSV 文件
- batch 输出至少包含：
  - 每条文档的结构化 JSON 结果
  - 一份可读的 CSV 摘要
  - 一份批量运行 summary JSON
- 文档级输出仍复用 `S1A-2A` 的 source / normalized / extraction contract。

### P0-C1-S3 (MVP delivery surface contract | v1)

- phase 3 默认交付入口固定为批量 Python CLI。
- v1 目标是“给用户一个可以直接跑本地样本集的命令”，而不是服务端 API。
- 交付面至少应明确：
  - 输入参数
  - 输出目录
  - summary 输出位置

### P0-C1-S4 (Evidence contract reuse and extension | v1)

- Evidence JSON must include:
  - `inputBatchRef`
  - `artifactPaths`
  - `extractorVersion`
  - `taxonomyVersion`
  - `passFail`
- 对 evaluation drill 还应补充：
  - `goldSetRef`
  - `samplesChecked`
  - `summaryCounts`

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S1A-3A` 相关改动继续落在当前 `S1A-*` 分支上，与 parent spine 和 phase 1 / 2 的证据链保持连续。
- phase 3 若同时推进 evaluation 与 batch delivery，仍优先按 `P*-C*-S*` 小提交切开，不在一条提交里混入过多责任。

**Commit discipline (recommended)**:

- 推荐节奏：
  - `P0` 先冻结 phase 3 默认边界
  - `P1` 先落 gold set / evaluation skeleton
  - `P2` 再落 batch import/export 与交付入口
  - `P3` 最后做 drills / evidence / closure

## Plan (draft)

### P1 (Evaluation)

- `P1-C1-S1`: 定义最小 gold set 样本与期望字段格式。
- `P1-C1-S2`: 落 evaluation summary skeleton，先支持 PASS/FAIL 与偏差说明。

### P2 (Batch import/export and delivery)

- `P2-C1-S1`: 固定 batch CLI 入口与输入输出目录约定。
- `P2-C1-S2`: 输出批量 JSON 结果、CSV 摘要与 batch summary。

### P3 (Drill / Evidence / closure)

- `P3-C1-S1`: 用最小 gold set 跑一轮 evaluation drill。
- `P3-C1-S2`: 用最小 batch 输入跑一轮 delivery drill，并收口 phase 3。

## P0 Deliverable (Phase 3 defaults frozen | v1)

### P0 outcome summary

- phase 3 的默认目标冻结为：evaluation + batch import/export + MVP delivery surface。
- phase 3 的默认实现路径冻结为：先 gold set/eval，再 batch CLI/export，最后 drill/evidence。
- phase 3 继续以 CLI-first、本地样本、本地工件为主，不引入外部依赖面的范围扩张。

### P0 frozen defaults for implementation

- gold set 建议位置：`samples/gold/`
- phase 3 evaluation 工件建议位置：`artifacts/_tmp_eval/`
- phase 3 batch delivery 工件建议位置：`artifacts/_tmp_batch_delivery/`
- batch 入口风格：Python CLI-first

### P0 outcome

- `P0-C1-S1`、`P0-C1-S2`、`P0-C1-S3`、`P0-C1-S4` 视为已冻结，可直接进入 `P1`。

## P1-C1-S1 Deliverable (Minimal gold set samples and expected fields | v1)

### Created gold set assets

- `samples/gold/platform-engineer-002.txt`
- `samples/gold/devops-engineer-001.txt`
- `samples/gold/sre-001.txt`
- `samples/gold/gold-set-v1.json`

### Gold set coverage

- 当前最小 gold set 覆盖 3 条受控样本：
  - `platform_engineering`
  - `devops`
  - `sre`
- 每条样本都至少声明：
  - `sample_id`
  - `input_path`
  - `input_format`
  - `document_id`
  - `expected.facts`
  - `expected.inferences`
  - `notes`

### Expected field format frozen for v1

- `expected.facts` 当前按 category -> canonical labels list 记录。
- `expected.inferences` 当前至少包含：
  - `role_family`
  - `seniority`
- v1 仍不引入复杂分数或权重，只保留后续 evaluation 所需的最小 PASS/FAIL 对照面。

### P1-C1-S1 outcome

- phase 3 已拥有一套可直接被后续 evaluation skeleton 消费的最小 gold set。
- 已用当前 `S1A-2A` pipeline 对 3 条 gold 样本做快速兼容性检查，结果为 `3/3 passed`。
- 下一步应进入 `P1-C1-S2`，把 `expected / observed / pass_fail / notes` 的 evaluation summary 骨架固定下来。

## P1-C1-S2 Deliverable (Evaluation summary skeleton | v1)

### Added evaluation skeleton assets

- `src/wordretriever/evaluation.py`
- `artifacts/_tmp_eval/evaluation-summary-v1.template.json`

### Evaluation summary shape

- summary 顶层当前固定包含：
  - `gold_set_ref`
  - `samples_checked`
  - `summary_counts`
  - `extractor_version`
  - `taxonomy_version`
  - `results`
- `results[]` 中每条 sample summary 当前固定包含：
  - `sample_id`
  - `document_id`
  - `expected`
  - `observed`
  - `pass_fail`
  - `notes`

### Skeleton responsibilities

- `load_gold_set(...)`：加载 gold set JSON。
- `pipeline_result_to_observed(...)`：把 pipeline result 折叠成 evaluation 可消费的 observed 结构。
- `evaluate_sample(...)`：生成单条样本的 `expected / observed / pass_fail / notes` 结果。
- `summarize_evaluations(...)`：汇总 PASS/FAIL 计数与版本字段。
- `write_evaluation_summary(...)`：把 evaluation summary 写出到 JSON 工件。

### P1-C1-S2 outcome

- phase 3 现在不仅有 gold set，还有一套可直接承接 drill 的 evaluation summary 骨架。
- 已用当前 gold set 与 `S1A-2A` pipeline 做最小 summary 生成验证，结果为 `samples_checked=3`、`PASS=3`、`FAIL=0`。
- 后续 `P3-C1-S1` 可以直接复用这套 skeleton 跑最小 evaluation drill，而不需要再定义输出结构。
- 下一步应进入 `P2-C1-S1` 或先做一次轻量级 skeleton 验证；按当前 phase 计划，建议继续 `P2-C1-S1` 固定 batch CLI 入口与目录约定。

## P2-C1-S1 Deliverable (Batch CLI entrypoint and I/O layout | v1)

### Added batch delivery assets

- `src/wordretriever/batch.py`
- `src/wordretriever/batch_cli.py`
- `artifacts/_tmp_batch_delivery/.gitkeep`

### Batch entrypoint fixed

- phase 3 的 batch 入口当前固定为：`wordretriever.batch_cli`
- CLI 输入参数：
  - `input_path`
  - `--input-format`，支持 `text` / `json` / `csv`
  - `--output-dir`，默认写入 `artifacts/_tmp_batch_delivery/latest_run`

### Batch I/O layout frozen for v1

- 输入形态：
  - 单个文件，或
  - 指向同一格式文件集合的本地目录
- 默认输出形态：
  - 每条输入生成 1 个 `*.output.json`
  - 全部输出落在同一个 batch run 目录下
- v1 当前只固定“逐文档 JSON 输出目录”这层布局；CSV summary 与 batch run summary 留给 `P2-C1-S2`。

### P2-C1-S1 outcome

- phase 3 现在已有明确的 batch CLI 入口和默认输出目录约定。
- 已用 `samples/gold/` 做最小 smoke run，`wordretriever.batch_cli` 成功处理 `3` 条 text 输入并写出逐文档 JSON 输出。
- 后续 `P2-C1-S2` 可以在这个固定入口上补齐 CSV summary 与 batch run summary，而不需要再改入口语义。
- 下一步应进入 `P2-C1-S2`，补全 batch JSON export、CSV 摘要与 batch summary 输出。

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: Freeze evaluation contract | v1
- [x] `P0-C1-S2`: Freeze batch import/export contract | v1
- [x] `P0-C1-S3`: Freeze MVP delivery surface contract | v1
- [x] `P0-C1-S4`: Reuse and extend evidence contract | v1

### P1 (Evaluation)

- [x] `P1-C1-S1`: Define minimal gold set samples and expected fields
- [x] `P1-C1-S2`: Add evaluation summary skeleton

### P2 (Batch import/export and delivery)

- [x] `P2-C1-S1`: Fix batch CLI entrypoint and I/O layout
- [ ] `P2-C1-S2`: Export batch JSON, CSV summary, and run summary

### P3 (Drill / Evidence / closure)

- [ ] `P3-C1-S1`: Run one minimal evaluation drill with gold samples
- [ ] `P3-C1-S2`: Run one minimal batch delivery drill and close phase 3

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

## Recent changes (for traceability, optional)

- 2026-03-20: 完成 `S1A-3A/P2-C1-S1`，新增 `batch.py` 与 `batch_cli.py`，固定 batch 入口为 `wordretriever.batch_cli` 并冻结默认输出目录布局。
- 2026-03-20: 完成 `S1A-3A/P1-C1-S2`，新增 `evaluation.py` 与 evaluation summary template，冻结 phase 3 的 summary 输出骨架。
- 2026-03-20: 完成 `S1A-3A/P1-C1-S1`，新增最小 gold set 样本与 `gold-set-v1.json`，冻结 phase 3 evaluation 的 expected 字段格式。
- 2026-03-20: 创建 `log-S1A-3A`，冻结 phase 3 的 evaluation、batch import/export 与 MVP delivery surface 默认边界。
