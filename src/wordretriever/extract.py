from __future__ import annotations

import re
from dataclasses import asdict

from .contracts import ExtractionResult, NormalizedDocument, SourceDocument

KEYWORD_GROUPS: dict[str, dict[str, tuple[str, ...]]] = {
    "cloud_platforms": {
        "aws": ("aws",),
        "azure": ("azure",),
        "gcp": ("gcp", "google cloud"),
    },
    "cloud_services": {
        "ec2": ("ec2",),
        "iot_core": ("iot core",),
        "rds": ("rds",),
        "s3": ("s3",),
        "cloudwatch": ("cloudwatch",),
        "ecs": ("ecs",),
        "function_apps": ("function apps", "function app"),
        "web_apps": ("web apps", "web app"),
    },
    "containers": {
        "kubernetes": ("kubernetes", "eks"),
        "docker": ("docker",),
        "podman": ("podman",),
    },
    "iac_tools": {
        "terraform": ("terraform",),
        "aws_cdk": ("aws cdk", "cdk"),
        "cloudformation": ("cloudformation",),
        "ansible": ("ansible",),
    },
    "observability_tools": {
        "datadog": ("datadog",),
        "prometheus": ("prometheus",),
        "grafana": ("grafana",),
        "elk": ("elk",),
    },
    "datastores": {
        "postgresql": ("postgres", "postgresql"),
        "redis": ("redis",),
        "azure_sql": ("azure sql", "sql managed instance"),
    },
    "data_and_messaging": {
        "kafka": ("kafka",),
        "mqtt": ("mqtt",),
        "etl": ("etl", "extracting, ingesting, transforming"),
    },
    "backend_frameworks": {
        "nestjs": ("nestjs",),
        "react": ("react",),
        "nodejs": ("node.js", "nodejs"),
    },
    "ci_cd_tools": {
        "azure_devops": ("azure devops",),
        "github_actions": ("github actions",),
        "gitlab_ci": ("gitlab ci",),
        "jenkins": ("jenkins",),
    },
    "scripting_tools": {
        "bash": ("bash",),
        "powershell": ("powershell",),
        "yaml": ("yaml",),
    },
    "api_and_architecture": {
        "rest_api": ("rest apis", "rest api"),
        "microservices": ("microservices", "microservice"),
        "distributed_architecture": ("distributed architecture",),
    },
    "programming_languages": {
        "python": ("python",),
        "go": ("go", "golang"),
        "java": ("java",),
        "typescript": ("typescript",),
        "kotlin": ("kotlin",),
        "javascript": ("javascript",),
    },
    "work_arrangements": {
        "hybrid": ("hybrid",),
        "remote": ("remote",),
        "on_site": ("on-site", "on site", "in the office"),
    },
    "employment_conditions": {
        "work_rights_required": ("right to work", "work rights", "legal rights to work"),
        "no_visa_sponsorship": ("unable to provide visa sponsorship", "no visa sponsorship", "without visa sponsorship"),
        "relocation_considered": ("planning to relocate", "relocate"),
        "baseline_clearance_required": ("baseline clearance required", "baseline/nv1 required", "baseline security clearance"),
        "citizenship_or_pr_required": ("australian citizen", "permanent resident"),
    },
}

ROLE_SIGNALS: dict[str, tuple[str, ...]] = {
    "full_stack_engineering": ("full stack engineer", "full stack role", "across the stack"),
    "cloud_engineering": ("cloud engineer", "cloud engineering", "aws cloud engineer"),
    "backend_engineering": ("backend engineer", "backend software engineer", "api development", "node.js"),
    "platform_engineering": ("platform engineer", "internal developer platform", "developer experience", "platform engineering"),
    "devops": ("devops", "ci/cd", "release", "devsecops"),
    "sre": ("site reliability", "sre", "slos", "slis", "reliability"),
    "data_engineering": ("data pipeline", "data pipelines", "etl", "ingestion", "event streaming"),
    "software_engineering": ("software engineer", "distributed architecture", "software construction"),
    "cloud_infra": ("cloud infrastructure", "infra automation", "infrastructure automation"),
}

SENIORITY_SIGNALS: dict[str, tuple[str, ...]] = {
    "principal": ("principal",),
    "staff": ("staff",),
    "lead": ("lead",),
    "senior": ("senior",),
    "mid": ("mid-level", "mid level", "mid"),
    "junior": ("junior",),
}

ROLE_PRIORITY: tuple[str, ...] = (
    "full_stack_engineering",
    "cloud_engineering",
    "backend_engineering",
    "platform_engineering",
    "devops",
    "sre",
    "data_engineering",
    "software_engineering",
    "cloud_infra",
)

TITLE_FIRST_ROLE_FAMILIES: frozenset[str] = frozenset(
    {
        "full_stack_engineering",
        "cloud_engineering",
        "backend_engineering",
        "platform_engineering",
        "devops",
        "sre",
        "software_engineering",
    }
)


def extract_signals(source: SourceDocument, normalized: NormalizedDocument) -> ExtractionResult:
    original_text = source.content_text
    text = f" {original_text.lower()} "
    facts: dict[str, list[str]] = {key: [] for key in KEYWORD_GROUPS}
    evidence: dict[str, list[str]] = {}

    for fact_group, aliases in KEYWORD_GROUPS.items():
        for canonical_label, patterns in aliases.items():
            matches = [pattern.strip() for pattern in patterns if _pattern_matches(pattern, text)]
            if matches:
                facts[fact_group].append(canonical_label)
                evidence.setdefault(fact_group, []).append(_find_evidence_snippet(original_text, patterns) or matches[0])

    role_family = _infer_role_family(text, source.title)
    seniority = _infer_seniority(text, source.title)

    if role_family:
        evidence.setdefault("role_family", []).append(
            _find_evidence_snippet(original_text, ROLE_SIGNALS[role_family]) or role_family
        )
    if seniority:
        evidence.setdefault("seniority", []).append(
            _find_evidence_snippet(original_text, SENIORITY_SIGNALS[seniority]) or (source.title or seniority)
        )

    return ExtractionResult(
        document_id=source.document_id,
        facts=facts,
        inferences={
            "role_family": role_family,
            "seniority": seniority,
            "work_arrangement": normalized.work_arrangement_normalized,
        },
        evidence=evidence,
    )


def extraction_to_dict(extraction: ExtractionResult) -> dict[str, object]:
    return asdict(extraction)


def _infer_role_family(text: str, title: str | None) -> str | None:
    title_text = f" {(title or '').lower()} "
    ranked_text = f" {text} "

    for role_family in ROLE_PRIORITY:
        if role_family not in TITLE_FIRST_ROLE_FAMILIES:
            continue
        patterns = ROLE_SIGNALS[role_family]
        if any(_pattern_matches(pattern, title_text) for pattern in patterns):
            return role_family

    for role_family in ROLE_PRIORITY:
        patterns = ROLE_SIGNALS[role_family]
        if any(_pattern_matches(pattern, ranked_text) for pattern in patterns):
            return role_family
    return None


def _infer_seniority(text: str, title: str | None) -> str | None:
    title_text = f" {(title or '').lower()} "
    ranked_text = f" {text} "
    for seniority, patterns in SENIORITY_SIGNALS.items():
        if any(_pattern_matches(pattern, title_text) for pattern in patterns):
            return seniority
    for seniority, patterns in SENIORITY_SIGNALS.items():
        if any(_pattern_matches(pattern, ranked_text) for pattern in patterns):
            return seniority
    return None


def _find_evidence_snippet(text: str, patterns: tuple[str, ...]) -> str | None:
    lowered_lines = [(line, line.lower()) for line in text.splitlines() if line.strip()]
    for pattern in patterns:
        for original_line, lowered_line in lowered_lines:
            if _pattern_matches(pattern, lowered_line):
                return original_line.strip()
    return None


def _pattern_matches(pattern: str, text: str) -> bool:
    expression = _compile_pattern(pattern)
    return bool(expression.search(text))


def _compile_pattern(pattern: str) -> re.Pattern[str]:
    escaped = re.escape(pattern.strip().lower())
    escaped = escaped.replace(r"\ ", r"\s+")
    return re.compile(rf"(?<!\w){escaped}(?!\w)")