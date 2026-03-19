# log-S1A-1A-analysis-first-MVP-contracts+taxonomy+drills/evidence

---

**id**: `S1A-1A`
**kind**: `log`
**title**: `analysis-first MVP contracts + taxonomy + drills/evidence`
**status**: `draft`
**scope**: `S1`
**tags**: `EVOLUTION, jd-analysis, Drills, Evidence, epic/S1, sub/S1A-1A`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **parent_log**: `logs/log-S1A-JD-analysis-intelligence-MVP+contracts-first-spine.md`
  **previous_log**: ``
  **reference_log_1**: `logs/_plan.md`
**created**: `2026-03-19`
**updated**: `2026-03-19`

---

## Decision / Outcome

**Decision**:

- 本 phase 先冻结 analysis-first MVP 的 contract、taxonomy 与 evidence 口径。
- v1 只定义稳定输入输出边界，不在本 phase 实现网页抓取或复杂模型能力。
- phase 完成后，后续实现必须建立在统一的 source / normalized / extraction schema 上。

**Default choices (phase defaults / v1)**:

- 先支持 manual text / JSON / CSV 作为输入来源。
- schema 以“原文保留、标准化另存、推断可追证”为默认语义。
- taxonomy 先做小而稳定的 canonical set，不追求全覆盖。
- evidence 默认记录文本片段，不强求首轮记录精确字符 offset。
- 生成工件不提交原始抓取 dumps；如需样本，仅保留可控测试输入。

## Definitions (optional)

- `source object`: 统一输入文档对象，供分析层消费。
- `normalized object`: 对 source 做清洗与字段标准化后的中间对象。
- `facts`: 可直接由文本命中的事实性提取结果。
- `inferences`: 对岗位角色、seniority 等进行的判断性结果。
- `evidence span`: 支撑某项提取或判断的原文片段。
- `taxonomy`: 稳定的 canonical labels 与 alias 映射集合。

## Constraints

- 原始文本必须保留，不允许被清洗结果覆盖。
- `facts` 与 `inferences` 必须分开建模。
- 每个核心判断应尽量保留 evidence。
- taxonomy 命名一旦进入 v1，不轻易改 canonical name。
- 本 phase 产出应足够具体，使下个 phase 可以直接实现，而不需要重新解释语义。

## Scope

- `P0`: contract（MVP 边界、source/normalized/extraction/evidence/taxonomy contract）
- `P1`: 文档化 contract 清单与样例对象草案
- `P2`: contract review drill 与样例 walkthrough
- `P3`: evidence 口径检查与 phase 收口

## Success Criteria (DoD)

- 明确写出 MVP v1 的输入边界、输出边界与非目标。
- 明确 source contract 的字段、命名与语义。
- 明确 normalized contract 的字段与“不覆盖原文”原则。
- 明确 extraction contract 的 `facts / inferences / evidence` 结构。
- 明确 taxonomy v1 的 canonical labels 与首轮覆盖范围。
- 明确 evidence JSON 的最低必填字段。
- 至少完成一次针对样例 JD 的人工 walkthrough，验证 schema 能承载真实文本。

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0` 的 contract、命名、默认语义、evidence 口径已明确且无关键歧义。
  - `P1-P3` 至少完成一轮样例 walkthrough 与 contract review。
  - The Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## P0 (Contract | v1)

### P0-C1-S1 (Freeze MVP boundary | v1)

- 明确 v1 的目标是“把 JD 文本转成结构化分析结果”，不是“稳定抓取招聘网站”。
- 明确 v1 的支持岗位族：Platform Engineer、DevOps Engineer、SRE。
- 明确 v1 的输入来源：manual text、JSON import、CSV import。
- 明确 v1 的输出类型：structured JSON、CSV export、最小汇总视图。
- 明确 v1 的非目标：抓取适配器、复杂前端、生产级服务化。

### P0-C1-S2 (Source contract | v1)

- source object 至少包含：
  - `document_id`
  - `source`
  - `source_type`
  - `source_url`
  - `captured_at`
  - `title`
  - `company`
  - `location`
  - `posted_at`
  - `content_text`
  - `raw_payload_ref`
- 语义要求：分析层只依赖 source contract，不依赖 DOM、selector 或平台页面结构。

### P0-C1-S3 (Normalized contract | v1)

- normalized object 至少包含：
  - `title_normalized`
  - `company_normalized`
  - `location_normalized`
  - `employment_type`
  - `description_cleaned`
- 语义要求：
  - 清洗结果与原文分开存储。
  - 清洗只做最小必要标准化，不做解释性改写。

### P0-C1-S4 (Extraction contract | v1)

- extraction object 至少包含：
  - `facts.cloud_platforms`
  - `facts.containers`
  - `facts.iac_tools`
  - `facts.observability_tools`
  - `facts.programming_languages`
  - `inferences.role_family`
  - `inferences.seniority`
  - `evidence`
  - `extractor_version`
  - `taxonomy_version`
- 语义要求：
  - `facts` 仅承载文本直接支持的命中。
  - `inferences` 承载角色归类与 seniority 判断。
  - 每项核心提取尽量附带可复核 evidence。

### P0-C1-S5 (Taxonomy contract | v1)

- role family canonical labels：
  - `platform_engineering`
  - `devops`
  - `sre`
  - `cloud_infra`
- seniority canonical labels：
  - `junior`
  - `mid`
  - `senior`
  - `staff`
  - `principal`
- 首轮 skills/tooling canonical labels：
  - `aws`
  - `azure`
  - `gcp`
  - `kubernetes`
  - `docker`
  - `terraform`
  - `datadog`
  - `prometheus`
  - `grafana`
  - `python`
  - `go`
  - `java`

### P0-C1-S6 (Evidence contract | v1)

- Evidence JSON must include:
  - `logId`
  - `phaseId`
  - `headSha`
  - `inputSampleId`
  - `extractorVersion`
  - `taxonomyVersion`
  - `artifactPaths`
  - `passFail`
  - `observedSummary`
- 语义要求：
  - 至少能追溯某次 walkthrough / regression 用了哪条样本、哪版 schema、哪版 extractor。

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S1A-1A` 相关文档与实现默认落在 `S1A-*` 分支上，保证 scope、log、commit、artifacts 可追溯。
- 若后续同时推进 `S1A-2A` 实现与其他实验，优先拆分成独立 PR，避免 phase 边界混淆。

**Commit discipline (recommended)**:

- 完成一个清晰的 contract 单元后就提交，例如：
  - `S1A-1A/P0-C1-S1S2: freeze MVP boundary and source contract`
- 不建议把 P0 contract、P1 样例、P2 walkthrough 混在同一大提交里。

## Plan (draft)

### P1 (Contract examples / schema walkthrough)

- `P1-C1-S1`: 为 source / normalized / extraction contract 各写 1 个最小样例对象。
- `P1-C1-S2`: 用 1 条真实风格 JD 文本做字段映射 walkthrough，检查 schema 是否缺字段。

## P1-C1-S1 Deliverable (Minimal example objects | v1)

### Example 1: Source object

```json
{
  "document_id": "manual:platform-engineer:001",
  "source": "manual",
  "source_type": "job_posting",
  "source_url": null,
  "captured_at": "2026-03-19T10:00:00Z",
  "title": "Senior Platform Engineer",
  "company": "Example Cloud Pty Ltd",
  "location": "Sydney, NSW",
  "posted_at": "2026-03-12",
  "content_text": "We are hiring a Senior Platform Engineer to build AWS-based internal platforms. You will work with Kubernetes, Terraform, Datadog, and Python to improve developer productivity and platform reliability.",
  "raw_payload_ref": "samples/manual/platform-engineer-001.txt"
}
```

### Example 2: Normalized object

```json
{
  "document_id": "manual:platform-engineer:001",
  "title_normalized": "platform engineer",
  "company_normalized": "example cloud pty ltd",
  "location_normalized": "sydney_nsw_au",
  "employment_type": "full_time",
  "description_cleaned": "We are hiring a Senior Platform Engineer to build AWS-based internal platforms. You will work with Kubernetes, Terraform, Datadog, and Python to improve developer productivity and platform reliability."
}
```

### Example 3: Extraction object

```json
{
  "document_id": "manual:platform-engineer:001",
  "facts": {
    "cloud_platforms": ["aws"],
    "containers": ["kubernetes"],
    "iac_tools": ["terraform"],
    "observability_tools": ["datadog"],
    "programming_languages": ["python"]
  },
  "inferences": {
    "role_family": "platform_engineering",
    "seniority": "senior"
  },
  "evidence": {
    "cloud_platforms": ["AWS-based internal platforms"],
    "containers": ["work with Kubernetes"],
    "iac_tools": ["Terraform"],
    "observability_tools": ["Datadog"],
    "programming_languages": ["Python"],
    "role_family": ["Platform Engineer", "internal platforms", "developer productivity"],
    "seniority": ["Senior Platform Engineer"]
  },
  "extractor_version": "v1-rules-baseline",
  "taxonomy_version": "v1"
}
```

### Notes for P1-C1-S1

- 这 3 个对象共享同一个 `document_id`，用于说明 source、normalized、extraction 的链路关联方式。
- source object 保留原始标题、公司、地点与正文，不做解释性改写。
- normalized object 只负责清洗和标准化，不引入 role / seniority 判断。
- extraction object 严格区分 `facts` 和 `inferences`，并为核心命中保留 evidence。
- 该样例优先服务于 `Platform Engineer / DevOps / SRE` 邻近岗位的 MVP 验证，不代表通用 schema 已覆盖所有岗位族。

## P1-C1-S2 Deliverable (Sample JD walkthrough | v1)

### Input sample (realistic JD style excerpt)

```text
Senior Platform Engineer
Location: Sydney, NSW
Company: Northstar Cloud

We are looking for a Senior Platform Engineer to help build and operate our internal developer platform on AWS. You will design reusable Kubernetes-based infrastructure, manage Terraform modules, and improve observability with Datadog and Prometheus. The role works closely with software teams to improve CI/CD workflows and developer experience. Strong Python or Go skills are preferred. Experience supporting production systems and mentoring engineers is highly regarded.
```

### Walkthrough Step 1: Source mapping

- `document_id`: `manual:platform-engineer:002`
- `source`: `manual`
- `source_type`: `job_posting`
- `source_url`: `null`
- `captured_at`: `2026-03-19T11:00:00Z`
- `title`: `Senior Platform Engineer`
- `company`: `Northstar Cloud`
- `location`: `Sydney, NSW`
- `posted_at`: `null`
- `content_text`: full JD excerpt above
- `raw_payload_ref`: `samples/manual/platform-engineer-002.txt`

结论：source contract 可以完整承接这条 JD，且不需要依赖网页结构信息。

### Walkthrough Step 2: Normalized mapping

- `title_normalized`: `platform engineer`
- `company_normalized`: `northstar cloud`
- `location_normalized`: `sydney_nsw_au`
- `employment_type`: `unknown`
- `description_cleaned`: 保留正文语义，仅移除多余换行和标题噪音

结论：normalized contract 可以完成最小清洗，但 `employment_type` 在原文未出现时需要允许 `unknown` 或 `null`。

### Walkthrough Step 3: Facts extraction

- `facts.cloud_platforms`: `aws`
  - evidence: `internal developer platform on AWS`
- `facts.containers`: `kubernetes`
  - evidence: `Kubernetes-based infrastructure`
- `facts.iac_tools`: `terraform`
  - evidence: `manage Terraform modules`
- `facts.observability_tools`: `datadog`, `prometheus`
  - evidence: `improve observability with Datadog and Prometheus`
- `facts.programming_languages`: `python`, `go`
  - evidence: `Strong Python or Go skills are preferred`

结论：facts contract 足以承载首轮核心技术栈提取，且证据片段可直接回看。

### Walkthrough Step 4: Inference mapping

- `inferences.role_family`: `platform_engineering`
  - evidence:
    - `Senior Platform Engineer`
    - `internal developer platform`
    - `improve CI/CD workflows and developer experience`
- `inferences.seniority`: `senior`
  - evidence:
    - `Senior Platform Engineer`
    - `mentoring engineers is highly regarded`

结论：`role_family` 与 `seniority` 依然属于判断性字段，应保留在 `inferences` 而不是 `normalized`。

### Walkthrough Step 5: Schema gap check

- 当前 schema 足以覆盖该样本的核心分析目标。
- `posted_at`、`source_url`、`employment_type` 在缺失时需要允许空值，不应强制伪造。
- JD 中出现了 `CI/CD workflows` 与 `developer experience`，这类信号暂未进入 v1 facts 字段；首轮可保留在 evidence 中，后续再决定是否增加 `delivery_practices` 或 `focus_areas`。
- `mentoring engineers` 对 seniority 有辅助价值，但不应单独决定 seniority；需要与 title signal 联合判断。

### P1-C1-S2 Outcome

- source、normalized、extraction 三层对象可以承接一条真实风格 JD。
- 当前 schema 没有出现关键断裂字段。
- v1 后续实现时需要明确“允许空值字段”和“多证据联合判断”的规则。
- 下一步应进入 `P2-C1-S1`，把 `facts` 与 `inferences` 的 review 规则写清，避免实现阶段语义漂移。

### P2 (Drill / Verify)

- `P2-C1-S1`: 进行一次 contract review，确认 `facts` 与 `inferences` 无语义重叠。
- `P2-C1-S2`: 进行一次 taxonomy review，确认 canonical labels 足以覆盖首轮 MVP。

## P2-C1-S1 Deliverable (Facts vs inferences review rules | v1)

### Review objective

- 防止实现阶段把“文本直接命中”与“分析判断”混写到同一层。
- 保证 extraction output 对下游统计、回归和人工复核都保持稳定语义。
- 降低因为 prompt、规则或实现习惯不同而导致的 schema 漂移。

### Rule group A: What belongs to facts

- `facts` 只记录可以被原文直接支持的命中项，不记录岗位语义解释。
- 进入 `facts` 的字段必须满足以下条件之一：
  - 原文出现明确技术名词或工具名。
  - 原文出现可稳定映射到 taxonomy 的平台、语言、工具、组件名。
  - 对应 evidence 可以直接截取原文短语，不依赖推理链补全。
- v1 中适合进入 `facts` 的内容包括：
  - `cloud_platforms`
  - `containers`
  - `iac_tools`
  - `observability_tools`
  - `programming_languages`

### Rule group B: What belongs to inferences

- `inferences` 只记录需要语义判断、上下文归纳或多证据联合判断的字段。
- 进入 `inferences` 的字段通常满足以下特征：
  - 不能仅依靠单一工具名直接得出。
  - 结论依赖标题、职责描述、协作模式、语气强弱或多处线索合并。
  - 不同样本中同一结论可能由不同证据组合支持。
- v1 中必须保留在 `inferences` 的内容包括：
  - `role_family`
  - `seniority`

### Rule group C: Evidence threshold

- 每个 `facts` 字段至少应有 1 条原文 evidence。
- 每个 `inferences` 字段应尽量有 2 类证据中的至少 1 类：
  - 强信号：标题、明确角色命名、明确 seniority 命名。
  - 辅助信号：职责描述、协作对象、交付目标、 mentoring / ownership / scope 等语义线索。
- 若 inference 只有弱信号，没有明确主信号，应允许输出 `unknown`、留空或降低置信度，而不是强行归类。

### Rule group D: Anti-patterns

- 不要把 `Platform Engineer`、`DevOps Engineer`、`SRE` 这类岗位归类直接写进 `facts`。
- 不要因为出现 `AWS`、`Kubernetes`、`Terraform` 就自动判定 `role_family=platform_engineering`。
- 不要因为出现 `mentoring`、`ownership`、`production systems` 就单独判定 `seniority=senior`。
- 不要把 `CI/CD`、`developer experience`、`reliability` 这类尚未进入 v1 taxonomy 的信号硬塞进已有 facts 字段。
- 不要为了满足完整性而伪造 `posted_at`、`source_url`、`employment_type`。

### Rule group E: Review checklist for implementation

- 检查每个 `facts` 值是否都能用原文短语直接回指。
- 检查每个 `inferences` 值是否都依赖了至少一个可解释证据，而不是默认猜测。
- 检查 normalized 层是否混入了 role、seniority、focus 等判断性字段。
- 检查 evidence 是否与字段类型一致：
  - 技术命中对应事实 evidence。
  - 岗位归类对应判断 evidence。
- 检查未知值处理是否稳定：缺失信息时优先 `null` / `unknown`，不做伪确定性输出。

### Rule group F: Decision examples

- 示例 1：原文出现 `Terraform`。
  - 正确：写入 `facts.iac_tools`。
  - 错误：直接因此推断 `role_family=platform_engineering`。
- 示例 2：标题是 `Senior Platform Engineer`。
  - 正确：作为 `inferences.role_family` 与 `inferences.seniority` 的强信号 evidence。
  - 错误：把 `Senior` 或 `Platform Engineer` 当成 facts。
- 示例 3：原文出现 `improve developer experience`。
  - 正确：先保留为 inference evidence 或 future-extension signal。
  - 错误：硬写入现有 facts schema。

### P2-C1-S1 Outcome

- `facts` 与 `inferences` 的边界已经被明确到实现可执行程度。
- v1 实现阶段应按“先 facts、后 inferences、最后 evidence 校验”的顺序落地。
- 当前剩余的 review 工作应转向 `P2-C1-S2`，检查 taxonomy 是否足够覆盖首轮 MVP 样本。

## P2-C1-S2 Deliverable (Taxonomy coverage review | v1)

### Review objective

- 检查当前 taxonomy 的 canonical labels 是否足以覆盖首轮 MVP 的目标岗位族与样本信号。
- 明确哪些信号已经有稳定落点，哪些信号暂时只保留为 evidence 或 future extension。
- 避免实现阶段为了覆盖零散样本而临时扩张 taxonomy，导致 v1 失控。

### Coverage group A: Role family coverage

- 当前 canonical labels：
  - `platform_engineering`
  - `devops`
  - `sre`
  - `cloud_infra`
- 覆盖判断：
  - 足以覆盖首轮 MVP 目标岗位族：Platform Engineer、DevOps Engineer、SRE。
  - `cloud_infra` 作为邻近兜底分类是合理的，但首轮不应把它当成默认回收站。
- 结论：role family taxonomy 对首轮 MVP 是够用的，不需要在 v1 新增更多岗位大类。

### Coverage group B: Seniority coverage

- 当前 canonical labels：
  - `junior`
  - `mid`
  - `senior`
  - `staff`
  - `principal`
- 覆盖判断：
  - 足以承接首轮常见标题和职责语气。
  - `lead`、`manager`、`architect` 这类词在首轮不强行吸收到 seniority taxonomy 中。
  - 若标题和职责信号不足，应允许 `unknown` 或空值，而不是强行落到 `mid` / `senior`。
- 结论：seniority taxonomy 对首轮 MVP 是够用的，但需要通过 inference rules 保持克制。

### Coverage group C: Skills and tooling coverage

- 当前 canonical labels：
  - cloud: `aws`, `azure`, `gcp`
  - containers: `kubernetes`, `docker`
  - IaC: `terraform`
  - observability: `datadog`, `prometheus`, `grafana`
  - languages: `python`, `go`, `java`
- 覆盖判断：
  - 能覆盖首轮 walkthrough 样本中的核心技术词。
  - 能覆盖 Platform / DevOps / SRE 邻近岗位中最常见的一层基础信号。
  - 对首轮 MVP 来说，优先保证这些高频标签稳定，不急于增加长尾工具。
- 结论：skills/tooling taxonomy 对首轮 MVP 核心样本是够用的。

### Coverage group D: Known gaps kept out of v1 taxonomy

- 下列信号当前经常出现，但暂不纳入 v1 canonical taxonomy：
  - `CI/CD`
  - `developer experience`
  - `reliability`
  - `internal developer platform`
  - `mentoring`
  - `ownership`
- 处理原则：
  - 首轮先保留为 evidence 或 inference supporting signals。
  - 不为了单个样本临时新增 `focus_areas`、`delivery_practices`、`responsibility_tags`。
  - 只有在多个样本反复出现且确实影响下游分析时，才在后续 phase 正式扩张 taxonomy。

### Coverage group E: Admission rules for future taxonomy expansion

- 新 canonical label 进入 taxonomy 前，应同时满足：
  - 在多个样本中反复出现，而不是单次偶发。
  - 对下游分析、对比或聚类结果有明显增益。
  - 能稳定定义边界，不容易与已有 label 混淆。
  - 能配套 alias / evidence / review 规则，而不是只加名字。
- 若不满足以上条件，优先保留为 evidence，不进入 v1 taxonomy。

### P2-C1-S2 Outcome

- 当前 taxonomy 已足够覆盖首轮 MVP 的目标岗位族、seniority 层级与核心技术标签。
- 已识别的高频但未收编信号应先保留在 evidence / inference supporting signals 中。
- 下一步应进入 `P3-C1-S1`，把 walkthrough 与 review 的结果写成第一条 evidence JSON 口径说明。

### P3 (Evidence / closure)

- `P3-C1-S1`: 记录 walkthrough evidence，包含样本 id、headSha、artifact path、PASS/FAIL。
- `P3-C1-S2`: 输出 phase closure note，明确进入 `S1A-2A` 前的冻结项与开放项。

## P3-C1-S1 Deliverable (Evidence JSON template and example | v1)

### Evidence objective

- 为本 phase 已完成的 walkthrough 与 review 提供统一、可追溯、可机器读取的 evidence 记录口径。
- 保证后续每次 contract review、taxonomy review 或 sample walkthrough 都能用相同结构落证据。
- 让后续 phase 在读取 evidence 时，不需要重新解释字段含义。

### Evidence JSON template | v1

```json
{
  "logId": "S1A-1A",
  "phaseId": "P3-C1-S1",
  "headSha": "<git-sha>",
  "inputSampleId": "<sample-id>",
  "extractorVersion": "<extractor-version>",
  "taxonomyVersion": "<taxonomy-version>",
  "artifactPaths": [
    "<artifact-path-1>",
    "<artifact-path-2>"
  ],
  "passFail": "PASS",
  "observedSummary": [
    "<observation-1>",
    "<observation-2>"
  ]
}
```

### Evidence field semantics

- `logId`: 对应 phase log 的稳定标识，例如 `S1A-1A`。
- `phaseId`: 对应本次 evidence 属于哪一个 `P*-C*-S*` 单元。
- `headSha`: 记录生成该 evidence 时的 git head，用于代码与文档回溯。
- `inputSampleId`: 记录 walkthrough 或 review 绑定的输入样本。
- `extractorVersion`: 若是纯 contract review 也保留字段，首轮可记录 `v1-rules-baseline`。
- `taxonomyVersion`: 记录 review 所基于的 taxonomy 版本。
- `artifactPaths`: 记录证据文件、样例文件、导出文件等路径。
- `passFail`: 只允许 `PASS` 或 `FAIL`，避免自由文本污染统计。
- `observedSummary`: 用于记录本次 run 的关键观察结论，优先写成短句列表。

### Example evidence JSON for this phase

```json
{
  "logId": "S1A-1A",
  "phaseId": "P3-C1-S1",
  "headSha": "<git-sha>",
  "inputSampleId": "manual:platform-engineer:002",
  "extractorVersion": "v1-rules-baseline",
  "taxonomyVersion": "v1",
  "artifactPaths": [
    "samples/manual/platform-engineer-002.txt",
    "artifacts/_tmp_jd_analysis_contracts/drills_<ts>.json"
  ],
  "passFail": "PASS",
  "observedSummary": [
    "Source, normalized, and extraction contracts can carry one realistic Platform Engineer JD sample.",
    "Facts and inferences remain semantically distinct under the current review rules.",
    "Current taxonomy is sufficient for the first MVP scope.",
    "CI/CD and developer experience signals remain outside v1 canonical labels and stay in evidence."
  ]
}
```

### Evidence recording rules

- 每个 `P*-C*-S*` 最少应有 1 条 evidence JSON 记录。
- evidence 必须绑定具体样本或 review 对象，不能写成无输入上下文的抽象结论。
- `artifactPaths` 应优先记录工作区相对路径，保持迁移和回溯简单。
- 若本次检查失败，`passFail` 必须写 `FAIL`，并在 `observedSummary` 中写出阻断原因。
- evidence 是 phase 级别的事实记录，不承担解释业务语义的职责。

### P3-C1-S1 Outcome

- 本 phase 的 evidence 记录格式已经稳定，可供后续 contract review 和 implementation drill 复用。
- 下一步应进入 `P3-C1-S2`，把本 phase 的冻结项、开放项和 handoff 边界写成 closure note。

## P3-C1-S2 Deliverable (Phase closure note and handoff boundary | v1)

### Closure objective

- 正式收口 `S1A-1A` 的 phase 产出，避免后续实现阶段继续回头修改基础定义。
- 明确哪些内容在 v1 中视为冻结项，哪些内容仍是开放项或后续扩展点。
- 为 `S1A-2A` 提供直接可执行的 handoff 边界，减少实现前的解释成本。

### Frozen outputs for handoff to S1A-2A

- 以下内容视为 `S1A-1A` 的冻结交付：
  - source contract 字段边界
  - normalized contract 字段边界
  - extraction contract 中 `facts / inferences / evidence` 的分层语义
  - role family 与 seniority 的 v1 canonical labels
  - 首轮 skills/tooling canonical labels
  - facts vs inferences review rules
  - evidence JSON v1 模板与字段语义
- `S1A-2A` 可以直接基于以上冻结项进入实现，不应重新发明输入输出结构。

### Open items intentionally deferred after S1A-1A

- 以下内容明确不在本 phase 收口，保留为后续开放项：
  - `CI/CD`、`developer experience`、`reliability` 等新 taxonomy 维度是否入表
  - 更细粒度的 `focus_areas` / `delivery_practices` / `responsibility_tags`
  - 采集适配器、网页来源接入与平台差异处理
  - 复杂的 confidence scoring 与 ranking 机制
  - 大规模 gold set 与系统化回归基线

### Implementation boundary for S1A-2A

- `S1A-2A` 的实现起点应限定为：
  - 接收 manual text / JSON / CSV 输入
  - 生成 source object
  - 执行最小 normalized mapping
  - 产出 rules-first extraction JSON
  - 绑定 evidence spans
- `S1A-2A` 不应做的事情：
  - 回退修改 `S1A-1A` 已冻结的 schema 语义
  - 临时扩张 taxonomy 去追单个样本
  - 在未新增 phase contract 的前提下引入新的输出层级

### Exit criteria for closing S1A-1A

- `P1-C1-S1` 已完成：最小 example objects 已提供。
- `P1-C1-S2` 已完成：真实风格 JD walkthrough 已提供。
- `P2-C1-S1` 已完成：facts vs inferences 边界规则已明确。
- `P2-C1-S2` 已完成：taxonomy coverage 已确认足以支持首轮 MVP。
- `P3-C1-S1` 已完成：evidence JSON 模板与示例已建立。
- 当前剩余工作不再属于 contract baseline，而属于下一 phase 的实现工作。

### P3-C1-S2 Outcome

- `S1A-1A` 已形成可交接给实现 phase 的 contract baseline。
- `S1A-2A` 可以开始实现单文档 analysis pipeline，而不需要再回头定义 schema。
- 若后续实现发现结构性缺口，应通过新 phase 或新 cycle 回写，而不是直接破坏当前冻结面。

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: Freeze MVP boundary | v1
- [ ] `P0-C1-S2`: Source contract | v1
- [ ] `P0-C1-S3`: Normalized contract | v1
- [ ] `P0-C1-S4`: Extraction contract | v1
- [ ] `P0-C1-S5`: Taxonomy contract | v1
- [ ] `P0-C1-S6`: Evidence contract | v1

### P1 (Contract examples / schema walkthrough)

- [x] `P1-C1-S1`: Draft minimal example objects
- [x] `P1-C1-S2`: Walk through one sample JD against the contracts

### P2 (Drill / Verify)

- [x] `P2-C1-S1`: Review facts vs inferences boundaries
- [x] `P2-C1-S2`: Review taxonomy coverage for MVP

### P3 (Evidence / closure)

- [x] `P3-C1-S1`: Record walkthrough evidence JSON
- [x] `P3-C1-S2`: Freeze phase outputs and handoff to implementation phase

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).

### <Pn-Cx-Sy> (Contract walkthrough | 2026-03-19)

- headSha: `<git sha>`
- artifacts: `artifacts/_tmp_jd_analysis_contracts/drills_<ts>.json`
- env (example, optional):
  - `MVP_SCOPE=platform_devops_sre`
  - `TAXONOMY_VERSION=v1`
- expected:
  - Source, normalized, extraction, evidence fields are sufficient for one sample JD.
  - Facts and inferences remain semantically distinct.
- observed:
  - Completed one document-level walkthrough using a realistic Platform Engineer JD excerpt.
  - No blocking schema gap found for source, normalized, or extraction v1.
  - Optional future extension identified for delivery-practice or focus-area style signals.
  - Added explicit review rules that separate direct textual facts from judgment-based inferences.
  - Confirmed current taxonomy is sufficient for the first MVP scope and identified deferred signal groups that remain outside v1 canonical labels.

### P3-C1-S1 (Evidence JSON contract | 2026-03-19)

- headSha: `<git sha>`
- artifacts:
  - `samples/manual/platform-engineer-002.txt`
  - `artifacts/_tmp_jd_analysis_contracts/drills_<ts>.json`
- env:
  - `EXTRACTOR_VERSION=v1-rules-baseline`
  - `TAXONOMY_VERSION=v1`
- expected:
  - Evidence JSON has a stable shape for future phase runs.
  - Required fields are sufficient for traceability and simple machine checks.
- observed:
  - Added a reusable evidence JSON template and a phase-specific example record.
  - Required fields now cover log identity, sample identity, versions, artifacts, and PASS/FAIL status.
  - Evidence format is ready to be reused by later drills and implementation runs.

### P3-C1-S2 (Phase closure and handoff | 2026-03-19)

- headSha: `<git sha>`
- artifacts:
  - `logs/log-S1A-1A-analysis-first-MVP-contracts+taxonomy+drills-or-evidence.md`
- env:
  - `PHASE_ID=S1A-1A`
  - `NEXT_PHASE=S1A-2A`
- expected:
  - Frozen outputs and deferred items are explicitly separated.
  - The implementation phase has a stable handoff boundary.
- observed:
  - Recorded the frozen v1 outputs that S1A-2A must consume unchanged.
  - Recorded deferred items that must not be expanded ad hoc during implementation.
  - Declared S1A-2A as the next phase for single-document analysis pipeline implementation.

## Recent changes (for traceability, optional)

- 2026-03-19: 完成 `P3-C1-S2`，收口 phase closure note，明确冻结项、开放项和 `S1A-2A` 的 handoff 边界。
- 2026-03-19: 完成 `P3-C1-S1`，补充 evidence JSON 模板、字段语义、phase 示例以及记录规则。
- 2026-03-19: 完成 `P2-C1-S2`，确认首轮 taxonomy coverage 够用，并记录暂不纳入 v1 的信号类型与扩张准入规则。
- 2026-03-19: 完成 `P2-C1-S1`，补充 facts 与 inferences 的 review 规则、证据门槛与反例约束。
- 2026-03-19: 完成 `P1-C1-S2`，新增 1 条真实风格 JD 的 walkthrough，并记录 schema gap 检查结论。
- 2026-03-19: 完成 `P1-C1-S1`，补充 source / normalized / extraction 的 3 个最小样例对象，并修正 parent log 链接。
- 2026-03-19: 创建 `log-S1A-1A`，把 analysis-first MVP 的第一阶段固定为 contracts、taxonomy 与 evidence 基线收口。