# runbook-S1B-formal-usage-v1

---

**id**: `runbook-S1B-formal-usage-v1`
**kind**: `runbook`
**title**: `formal usage workflow for JD analysis v1`
**status**: `stable`
**scope**: `S1`
**tags**: `RUNBOOK, jd-analysis, guardrails, reporting, epic/S1, sub/S1B`
**links**: ``
  **parent_log**: `logs/log-S1B-formal-usage-guardrails+reporting-spine.md`
  **reference_log_1**: `logs/log-S1A-JD-analysis-intelligence-MVP+contracts-first-spine.md`
  **reference_log_2**: `logs/log-S1B-1A-minimal-usage-guardrails+templates+drills-or-evidence.md`
**created**: `2026-03-20`
**updated**: `2026-03-20`

---

## Purpose

- 给正式使用 `wordretriever` 的批次一个固定顺序，避免样本 intake、report 总结和 GPT enrichment 混成一团。

## Formal usage order

1. 用 `templates/jd-sample-intake-v1.txt` 接收或整理新 JD 原文。
2. 将样本保存为本地 text file，优先放在受控目录下。
3. 运行单文档或 batch pipeline 生成 deterministic output。
4. 在准备正式报告前运行 `python -m wordretriever.guardrails_cli`。
5. 只有 guardrails PASS 的批次才进入 `templates/report-template-v1.md` 的报告层。
6. 如果需要 GPT 补充解释，按 `templates/gpt-enrichment-template-v1.json` 单独落 enrichment，不覆盖 deterministic output。

## Stable commands

### Single document

```powershell
d:/Project/wordretriever/.venv/Scripts/python.exe -m wordretriever.cli samples/manual/platform-engineer-002.txt --input-format text --output-path artifacts/_tmp_single_doc_pipeline/latest_output.json
```

### Batch run

```powershell
d:/Project/wordretriever/.venv/Scripts/python.exe -m wordretriever.batch_cli samples/gold --input-format text --output-dir artifacts/_tmp_batch_delivery/latest_run
```

### Guardrails run

```powershell
d:/Project/wordretriever/.venv/Scripts/python.exe -m wordretriever.guardrails_cli
```

## Rules for deterministic vs enrichment output

- `facts` 和 `inferences` 继续由现有 deterministic pipeline 维护。
- GPT enrichment 只能作为补充层，不能直接改写 deterministic output。
- 如果 GPT 发现新的候选字段，先作为 enrichment 存放，再决定是否进入后续 contract 演化。

## Rules for new samples

- intake 时尽量保留原始 wording，不提前把正文翻译成 taxonomy。
- 公司、地点缺失时保留 `unknown`，不要补猜测值。
- 不是每条样本都进入 gold set；gold set 只保留高质量、可稳定复核的样本。

## Rules for reports

- 每轮正式报告都应包含：
  - batch metadata
  - deterministic facts summary
  - inference summary
  - GPT enrichment summary
  - open questions
  - taxonomy / contract changes
- 报告必须引用 guardrails artifacts，而不是只保留自然语言结论。