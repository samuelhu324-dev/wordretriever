from __future__ import annotations

from dataclasses import asdict

from .contracts import ExtractionResult, NormalizedDocument, SourceDocument

KEYWORD_GROUPS: dict[str, dict[str, tuple[str, ...]]] = {
    "cloud_platforms": {
        "aws": ("aws",),
        "azure": ("azure",),
        "gcp": ("gcp", "google cloud"),
    },
    "containers": {
        "kubernetes": ("kubernetes", "eks"),
        "docker": ("docker",),
    },
    "iac_tools": {
        "terraform": ("terraform",),
    },
    "observability_tools": {
        "datadog": ("datadog",),
        "prometheus": ("prometheus",),
        "grafana": ("grafana",),
    },
    "programming_languages": {
        "python": ("python",),
        "go": (" go ", "golang"),
        "java": ("java",),
    },
}

ROLE_SIGNALS: dict[str, tuple[str, ...]] = {
    "platform_engineering": ("platform engineer", "internal developer platform", "developer experience"),
    "devops": ("devops", "ci/cd", "release"),
    "sre": ("site reliability", "sre", "slos", "slis", "reliability"),
    "cloud_infra": ("cloud infrastructure", "infra automation", "infrastructure"),
}

SENIORITY_SIGNALS: dict[str, tuple[str, ...]] = {
    "principal": ("principal",),
    "staff": ("staff",),
    "senior": ("senior",),
    "mid": ("mid",),
    "junior": ("junior",),
}


def extract_signals(source: SourceDocument, normalized: NormalizedDocument) -> ExtractionResult:
    text = f" {source.content_text.lower()} "
    facts: dict[str, list[str]] = {key: [] for key in KEYWORD_GROUPS}
    evidence: dict[str, list[str]] = {}

    for fact_group, aliases in KEYWORD_GROUPS.items():
        for canonical_label, patterns in aliases.items():
            matches = [pattern.strip() for pattern in patterns if pattern in text]
            if matches:
                facts[fact_group].append(canonical_label)
                evidence.setdefault(fact_group, []).append(matches[0])

    role_family = _infer_role_family(text, source.title)
    seniority = _infer_seniority(text, source.title)

    if role_family:
        evidence.setdefault("role_family", []).append(role_family)
    if seniority:
        evidence.setdefault("seniority", []).append(seniority)

    return ExtractionResult(
        document_id=source.document_id,
        facts=facts,
        inferences={
            "role_family": role_family,
            "seniority": seniority,
        },
        evidence=evidence,
    )


def extraction_to_dict(extraction: ExtractionResult) -> dict[str, object]:
    return asdict(extraction)


def _infer_role_family(text: str, title: str | None) -> str | None:
    ranked_text = f" {(title or '').lower()} {text} "
    for role_family, patterns in ROLE_SIGNALS.items():
        if any(pattern in ranked_text for pattern in patterns):
            return role_family
    return None


def _infer_seniority(text: str, title: str | None) -> str | None:
    ranked_text = f" {(title or '').lower()} {text} "
    for seniority, patterns in SENIORITY_SIGNALS.items():
        if any(pattern in ranked_text for pattern in patterns):
            return seniority
    return None