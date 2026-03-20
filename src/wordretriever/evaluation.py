from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .contracts import PipelineResult


@dataclass(slots=True)
class SampleEvaluation:
    sample_id: str
    document_id: str
    expected: dict[str, object]
    observed: dict[str, object]
    pass_fail: str
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EvaluationSummary:
    gold_set_ref: str
    samples_checked: int
    summary_counts: dict[str, int]
    extractor_version: str
    taxonomy_version: str
    results: list[SampleEvaluation]


def load_gold_set(path: str) -> dict[str, object]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def evaluate_sample(sample: dict[str, object], result: PipelineResult) -> SampleEvaluation:
    expected = sample["expected"]
    observed = pipeline_result_to_observed(result)
    notes = _collect_mismatch_notes(expected, observed)
    return SampleEvaluation(
        sample_id=str(sample["sample_id"]),
        document_id=result.source.document_id,
        expected=expected,
        observed=observed,
        pass_fail="PASS" if not notes else "FAIL",
        notes=notes,
    )


def summarize_evaluations(evaluations: list[SampleEvaluation], gold_set_ref: str) -> EvaluationSummary:
    sample_count = len(evaluations)
    pass_count = sum(1 for evaluation in evaluations if evaluation.pass_fail == "PASS")
    fail_count = sample_count - pass_count
    extractor_version = evaluations[0].observed["extractor_version"] if evaluations else "unknown"
    taxonomy_version = evaluations[0].observed["taxonomy_version"] if evaluations else "unknown"
    return EvaluationSummary(
        gold_set_ref=gold_set_ref,
        samples_checked=sample_count,
        summary_counts={"PASS": pass_count, "FAIL": fail_count},
        extractor_version=str(extractor_version),
        taxonomy_version=str(taxonomy_version),
        results=evaluations,
    )


def write_evaluation_summary(summary: EvaluationSummary, output_path: str) -> None:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(asdict(summary), indent=2, ensure_ascii=True), encoding="utf-8")


def pipeline_result_to_observed(result: PipelineResult) -> dict[str, object]:
    return {
        "facts": result.extraction.facts,
        "inferences": result.extraction.inferences,
        "extractor_version": result.extraction.extractor_version,
        "taxonomy_version": result.extraction.taxonomy_version,
    }


def _collect_mismatch_notes(expected: dict[str, object], observed: dict[str, object]) -> list[str]:
    notes: list[str] = []
    expected_facts = expected.get("facts", {})
    observed_facts = observed.get("facts", {})
    for fact_group, expected_value in expected_facts.items():
        observed_value = observed_facts.get(fact_group, [])
        if observed_value != expected_value:
            notes.append(
                f"facts.{fact_group} expected {expected_value!r} but observed {observed_value!r}"
            )

    expected_inferences = expected.get("inferences", {})
    observed_inferences = observed.get("inferences", {})
    for inference_key, expected_value in expected_inferences.items():
        observed_value = observed_inferences.get(inference_key)
        if observed_value != expected_value:
            notes.append(
                f"inferences.{inference_key} expected {expected_value!r} but observed {observed_value!r}"
            )

    return notes