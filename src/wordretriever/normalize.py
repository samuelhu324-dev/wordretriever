from __future__ import annotations

import re
from dataclasses import asdict

from .contracts import NormalizedDocument, SourceDocument


def normalize_document(source: SourceDocument) -> NormalizedDocument:
    return NormalizedDocument(
        document_id=source.document_id,
        title_normalized=_normalize_title(source.title),
        company_normalized=_normalize_name(source.company),
        location_normalized=_normalize_location(source.location),
        employment_type=_infer_employment_type(source.content_text),
        description_cleaned=_clean_description(source.content_text),
    )


def normalized_to_dict(normalized: NormalizedDocument) -> dict[str, object]:
    return asdict(normalized)


def _normalize_title(title: str | None) -> str | None:
    if not title:
        return None
    text = re.sub(r"\s+", " ", title.strip().lower())
    for seniority_prefix in ("senior ", "junior ", "staff ", "principal ", "lead ", "mid "):
        if text.startswith(seniority_prefix):
            return text[len(seniority_prefix) :].strip()
    return text


def _normalize_name(value: str | None) -> str | None:
    if not value:
        return None
    return re.sub(r"\s+", " ", value.strip().lower())


def _normalize_location(location: str | None) -> str | None:
    if not location:
        return None
    normalized = re.sub(r"[^a-z0-9]+", "_", location.strip().lower())
    return normalized.strip("_")


def _infer_employment_type(content_text: str) -> str | None:
    lowered = content_text.lower()
    if "full-time" in lowered or "full time" in lowered:
        return "full_time"
    if "part-time" in lowered or "part time" in lowered:
        return "part_time"
    if "contract" in lowered:
        return "contract"
    return "unknown"


def _clean_description(content_text: str) -> str:
    lines = [line.strip() for line in content_text.splitlines() if line.strip()]
    return re.sub(r"\s+", " ", "\n".join(lines)).strip()