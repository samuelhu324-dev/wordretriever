from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass(slots=True)
class SampleReviewDecision:
    sample_id: str
    source_path: str
    output_path: str
    title: str | None
    company: str | None
    role_family: str | None
    seniority: str | None
    work_arrangement: str | None
    decision: str
    gold_candidate_eligible: bool
    facts_present: list[str]
    taxonomy_gaps: list[str] = field(default_factory=list)
    review_notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class BatchReviewSummary:
    batch_summary_ref: str
    reviewed_at: str
    reviewed_count: int
    decision_counts: dict[str, int]
    role_family_counts: dict[str, int]
    top_skill_counts: dict[str, int]
    combination_signatures: list[str]
    critical_taxonomy_gaps: list[str]
    items: list[SampleReviewDecision]


FACT_GROUP_PRIORITY: tuple[str, ...] = (
    "cloud_platforms",
    "cloud_services",
    "containers",
    "iac_tools",
    "observability_tools",
    "datastores",
    "data_and_messaging",
    "backend_frameworks",
    "ci_cd_tools",
    "scripting_tools",
    "api_and_architecture",
    "programming_languages",
    "employment_conditions",
)

GAP_PATTERNS: dict[str, tuple[str, str, str]] = {
    "full_stack_role_family": ("full stack", "role_family", "full_stack_engineering"),
    "cloud_engineering_role_family": ("cloud engineer", "role_family", "cloud_engineering"),
    "nodejs_framework": ("node.js", "backend_frameworks", "nodejs"),
    "cloudformation_iac": ("cloudformation", "iac_tools", "cloudformation"),
    "ansible_iac": ("ansible", "iac_tools", "ansible"),
    "azure_devops_ci_cd": ("azure devops", "ci_cd_tools", "azure_devops"),
    "github_actions_ci_cd": ("github actions", "ci_cd_tools", "github_actions"),
    "gitlab_ci_ci_cd": ("gitlab ci", "ci_cd_tools", "gitlab_ci"),
    "jenkins_ci_cd": ("jenkins", "ci_cd_tools", "jenkins"),
    "powershell_scripting": ("powershell", "scripting_tools", "powershell"),
    "bash_scripting": ("bash", "scripting_tools", "bash"),
    "function_apps_service": ("function apps", "cloud_services", "function_apps"),
    "web_apps_service": ("web apps", "cloud_services", "web_apps"),
    "rest_api_architecture": ("rest api", "api_and_architecture", "rest_api"),
    "microservices_architecture": ("microservices", "api_and_architecture", "microservices"),
    "baseline_clearance_condition": (
        "baseline clearance required",
        "employment_conditions",
        "baseline_clearance_required",
    ),
    "citizenship_or_pr_condition": (
        "permanent resident",
        "employment_conditions",
        "citizenship_or_pr_required",
    ),
}


def review_batch_outputs(batch_summary_path: str) -> BatchReviewSummary:
    batch_summary = json.loads(Path(batch_summary_path).read_text(encoding="utf-8"))
    items: list[SampleReviewDecision] = []
    decision_counter: Counter[str] = Counter()
    role_counter: Counter[str] = Counter()
    skill_counter: Counter[str] = Counter()
    signature_counter: Counter[str] = Counter()
    gap_counter: Counter[str] = Counter()

    for item in batch_summary["items"]:
        payload = json.loads(Path(item["output_path"]).read_text(encoding="utf-8"))
        review = review_sample_output(
            sample_id=item["document_id"],
            source_path=item["input_path"],
            output_path=item["output_path"],
            payload=payload,
        )
        items.append(review)
        decision_counter.update([review.decision])
        if review.role_family:
            role_counter.update([review.role_family])
        skill_counter.update(review.facts_present)
        if review.taxonomy_gaps:
            gap_counter.update(review.taxonomy_gaps)
        signature_counter.update([_build_combination_signature(payload)])

    return BatchReviewSummary(
        batch_summary_ref=batch_summary_path,
        reviewed_at=_iso_utc_now(),
        reviewed_count=len(items),
        decision_counts=dict(decision_counter),
        role_family_counts=dict(role_counter),
        top_skill_counts=dict(skill_counter.most_common(15)),
        combination_signatures=[signature for signature, _ in signature_counter.most_common(10)],
        critical_taxonomy_gaps=[gap for gap, _ in gap_counter.most_common(12)],
        items=items,
    )


def review_sample_output(
    sample_id: str,
    source_path: str,
    output_path: str,
    payload: dict[str, object],
) -> SampleReviewDecision:
    source = payload["source"]
    extraction = payload["extraction"]
    facts = extraction["facts"]
    inferences = extraction["inferences"]
    content_text = str(source["content_text"])
    title = _optional_string(source.get("title"))
    role_family = _optional_string(inferences.get("role_family"))
    seniority = _optional_string(inferences.get("seniority"))
    work_arrangement = _optional_string(inferences.get("work_arrangement"))
    facts_present = _flatten_fact_labels(facts)
    taxonomy_gaps = _detect_taxonomy_gaps(content_text, title, role_family, facts)
    review_notes = _build_review_notes(source, role_family, seniority, taxonomy_gaps, content_text)

    if _detect_multi_role_sample(content_text):
        decision = "split_multi_role"
    elif not role_family or len(facts_present) < 2:
        decision = "keep_in_intake"
    else:
        decision = "promote_to_reviewed"

    gold_candidate_eligible = (
        decision == "promote_to_reviewed"
        and not taxonomy_gaps
        and len(facts_present) >= 4
        and seniority is not None
        and not _detect_multi_role_sample(content_text)
    )

    return SampleReviewDecision(
        sample_id=sample_id,
        source_path=source_path,
        output_path=output_path,
        title=title,
        company=_optional_string(source.get("company")),
        role_family=role_family,
        seniority=seniority,
        work_arrangement=work_arrangement,
        decision=decision,
        gold_candidate_eligible=gold_candidate_eligible,
        facts_present=facts_present,
        taxonomy_gaps=taxonomy_gaps,
        review_notes=review_notes,
    )


def write_batch_review_summary(summary: BatchReviewSummary, output_path: str) -> None:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(asdict(summary), indent=2, ensure_ascii=True), encoding="utf-8")


def write_intake_report(summary: BatchReviewSummary, output_path: str) -> None:
    lines = [
        "# Intake Analysis Report",
        "",
        "## Batch metadata",
        "",
        f"- batch_summary_ref: `{summary.batch_summary_ref}`",
        f"- reviewed_at: `{summary.reviewed_at}`",
        f"- reviewed_count: `{summary.reviewed_count}`",
        "",
        "## Decision summary",
        "",
    ]
    for decision, count in sorted(summary.decision_counts.items()):
        lines.append(f"- {decision}: {count}")

    lines.extend(["", "## Role family distribution", ""])
    for role_family, count in sorted(summary.role_family_counts.items()):
        lines.append(f"- {role_family}: {count}")

    lines.extend(["", "## Top skills", ""])
    for skill, count in summary.top_skill_counts.items():
        lines.append(f"- {skill}: {count}")

    lines.extend(["", "## Combination signatures", ""])
    for signature in summary.combination_signatures:
        lines.append(f"- {signature}")

    lines.extend(["", "## Critical taxonomy gaps", ""])
    for gap in summary.critical_taxonomy_gaps:
        lines.append(f"- {gap}")

    lines.extend(["", "## Sample decisions", ""])
    for item in summary.items:
        facts_text = ", ".join(item.facts_present[:8]) if item.facts_present else "none"
        gaps_text = ", ".join(item.taxonomy_gaps) if item.taxonomy_gaps else "none"
        lines.append(
            f"- {item.sample_id}: decision={item.decision}; role_family={item.role_family or 'unknown'}; seniority={item.seniority or 'unknown'}; facts={facts_text}; gaps={gaps_text}"
        )

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _flatten_fact_labels(facts: dict[str, object]) -> list[str]:
    labels: list[str] = []
    for group in FACT_GROUP_PRIORITY:
        group_values = facts.get(group, [])
        if isinstance(group_values, list):
            labels.extend(str(value) for value in group_values)
    return labels


def _detect_taxonomy_gaps(
    content_text: str,
    title: str | None,
    role_family: str | None,
    facts: dict[str, object],
) -> list[str]:
    lowered = f" {(title or '').lower()} {content_text.lower()} "
    gaps: list[str] = []
    for gap_name, (pattern, target_group, expected_label) in GAP_PATTERNS.items():
        if pattern not in lowered:
            continue
        if target_group == "role_family":
            if role_family != expected_label:
                gaps.append(gap_name)
            continue
        observed_values = facts.get(target_group, [])
        if isinstance(observed_values, list) and expected_label not in observed_values:
            gaps.append(gap_name)
    return gaps


def _build_review_notes(
    source: dict[str, object],
    role_family: str | None,
    seniority: str | None,
    taxonomy_gaps: list[str],
    content_text: str,
) -> list[str]:
    notes: list[str] = []
    employer_questions = source.get("employer_questions", [])
    if isinstance(employer_questions, list) and employer_questions:
        notes.append("Employer questions preserved in source metadata.")
    if source.get("salary_text"):
        notes.append("Salary text captured in source metadata.")
    if _detect_multi_role_sample(content_text):
        notes.append("Multi-role advertisement detected; review should treat this source as split-capable.")
    if role_family == "software_engineering" and "full_stack_role_family" in taxonomy_gaps:
        notes.append("Full stack signals are present but the role family is still too generic.")
    if seniority is None and re.search(r"(?<!\w)mid-level(?!\w)|(?<!\w)mid level(?!\w)", content_text.lower()):
        notes.append("Mid-level seniority signal exists but was not stabilized in inference.")
    return notes


def _detect_multi_role_sample(content_text: str) -> bool:
    lowered = content_text.lower()
    return (
        "role 1" in lowered and "role 2" in lowered
    ) or "one or both roles" in lowered


def _build_combination_signature(payload: dict[str, object]) -> str:
    extraction = payload["extraction"]
    inferences = extraction["inferences"]
    facts = extraction["facts"]
    signature_parts: list[str] = []
    role_family = _optional_string(inferences.get("role_family"))
    if role_family:
        signature_parts.append(role_family)
    for group in (
        "cloud_platforms",
        "containers",
        "iac_tools",
        "ci_cd_tools",
        "backend_frameworks",
        "programming_languages",
        "data_and_messaging",
    ):
        values = facts.get(group, [])
        if isinstance(values, list) and values:
            signature_parts.append(str(values[0]))
        if len(signature_parts) >= 5:
            break
    return " + ".join(signature_parts) if signature_parts else "unknown"


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")