from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from .batch import run_batch_pipeline, write_batch_summary_csv, write_batch_summary_json
from .evaluation import evaluate_sample, load_gold_set, summarize_evaluations, write_evaluation_summary
from .pipeline import run_single_document_pipeline


@dataclass(slots=True)
class GuardrailRunSummary:
    run_id: str
    recorded_at: str
    gold_set_ref: str
    batch_input_ref: str
    batch_input_format: str
    evaluation_summary_path: str
    batch_output_dir: str
    batch_summary_json_path: str
    batch_summary_csv_path: str
    report_template_path: str
    intake_template_path: str
    enrichment_template_path: str
    samples_checked: int
    processed_count: int
    summary_counts: dict[str, int]
    pass_fail: str


def run_guardrails(
    gold_set_path: str,
    batch_input_path: str,
    batch_input_format: str,
    output_root: str,
    report_template_path: str,
    intake_template_path: str,
    enrichment_template_path: str,
) -> GuardrailRunSummary:
    run_id = _timestamp_slug()
    recorded_at = _iso_utc_now()
    destination = Path(output_root) / f"run_{run_id}"
    destination.mkdir(parents=True, exist_ok=True)

    evaluation_summary_path = destination / "evaluation-summary.json"
    batch_output_dir = destination / "batch"
    batch_summary_json_path = batch_output_dir / "batch-summary.json"
    batch_summary_csv_path = batch_output_dir / "batch-summary.csv"

    gold_set = load_gold_set(gold_set_path)
    evaluations = []
    for sample in gold_set["samples"]:
        result = run_single_document_pipeline(
            input_path=str(sample["input_path"]),
            input_format=str(sample.get("input_format", "text")),
        )
        evaluations.append(evaluate_sample(sample, result))

    evaluation_summary = summarize_evaluations(evaluations, gold_set_ref=gold_set_path)
    write_evaluation_summary(evaluation_summary, str(evaluation_summary_path))

    batch_summary = run_batch_pipeline(
        input_path=batch_input_path,
        input_format=batch_input_format,
        output_dir=str(batch_output_dir),
    )
    write_batch_summary_json(batch_summary, str(batch_summary_json_path))
    write_batch_summary_csv(batch_summary, str(batch_summary_csv_path))

    pass_fail = "PASS"
    if evaluation_summary.summary_counts.get("FAIL", 0) > 0:
        pass_fail = "FAIL"
    elif batch_summary.processed_count == 0:
        pass_fail = "FAIL"

    summary = GuardrailRunSummary(
        run_id=run_id,
        recorded_at=recorded_at,
        gold_set_ref=gold_set_path,
        batch_input_ref=batch_input_path,
        batch_input_format=batch_input_format,
        evaluation_summary_path=str(evaluation_summary_path),
        batch_output_dir=str(batch_output_dir),
        batch_summary_json_path=str(batch_summary_json_path),
        batch_summary_csv_path=str(batch_summary_csv_path),
        report_template_path=report_template_path,
        intake_template_path=intake_template_path,
        enrichment_template_path=enrichment_template_path,
        samples_checked=evaluation_summary.samples_checked,
        processed_count=batch_summary.processed_count,
        summary_counts=evaluation_summary.summary_counts,
        pass_fail=pass_fail,
    )
    write_guardrail_summary(summary, str(destination / "guardrails-summary.json"))
    return summary


def write_guardrail_summary(summary: GuardrailRunSummary, output_path: str) -> None:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(asdict(summary), indent=2, ensure_ascii=True), encoding="utf-8")


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _timestamp_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")