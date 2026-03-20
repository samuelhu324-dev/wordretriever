# runbook-S2A-sample-operations-v1

---

**id**: `runbook-S2A-sample-operations-v1`
**kind**: `runbook`
**title**: `sample intake and curation workflow for JD analysis v1`
**status**: `stable`
**scope**: `S2`
**tags**: `RUNBOOK, jd-analysis, sample-ops, corpus, epic/S2, sub/S2A`
**links**: ``
  **parent_log**: `logs/log-S2A-sample-intake-and-corpus-operations-spine.md`
  **reference_log_1**: `logs/log-S1B-formal-usage-guardrails+reporting-spine.md`
  **reference_log_2**: `logs/log-S2A-1A-sample-intake-review-and-batch-manifest-baseline+drills-or-evidence.md`
**created**: `2026-03-20`
**updated**: `2026-03-20`

---

## Purpose

- 给新样本的 intake、review、gold candidate 判断提供固定路径，避免样本长期积累后失去层次。

## Stage layout

1. `samples/intake/`
   放原始 JD 文本，尽量保留原文。
2. `samples/reviewed/`
   放经过基础清理和人工确认后、可稳定运行 pipeline 的样本。
3. `samples/gold_candidates/`
   放已经较稳定、但尚未正式并入 gold set 的候选样本。
4. `samples/gold/`
   只放正式进入回归保护的样本。

## Recommended workflow

1. 你把 JD 原文直接发给我，或者按 `templates/jd-sample-intake-v1.txt` 的格式整理后给我。
2. 我先帮你归档到 `samples/intake/` 的标准文件形态。
3. 对值得继续保留的样本，我会整理到 `samples/reviewed/`，并补 review record。
4. 对表现稳定的样本，再判断是否移动到 `samples/gold_candidates/`。
5. 只有在重复验证稳定后，才会进入 `samples/gold/`。

## Stable command

```powershell
d:/Project/wordretriever/.venv/Scripts/python.exe -m wordretriever.sample_ops_cli samples/intake --stage intake --output-path artifacts/_tmp_sample_ops/latest_batch_manifest.json
```

## Rules

- 不是每条样本都值得进 gold。
- 新样本先求可复核，再求覆盖面。
- 如果一条 JD 太脏或缺字段，也可以先保留在 intake，不急着提升阶段。