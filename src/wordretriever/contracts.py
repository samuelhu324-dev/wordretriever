from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


FactList = list[str]
EvidenceMap = dict[str, FactList]


@dataclass(slots=True)
class SourceDocument:
    document_id: str
    source: str
    source_type: str
    source_url: str | None
    captured_at: str
    title: str | None
    company: str | None
    location: str | None
    posted_at: str | None
    content_text: str
    raw_payload_ref: str | None


@dataclass(slots=True)
class NormalizedDocument:
    document_id: str
    title_normalized: str | None
    company_normalized: str | None
    location_normalized: str | None
    employment_type: str | None
    description_cleaned: str


@dataclass(slots=True)
class ExtractionResult:
    document_id: str
    facts: dict[str, FactList]
    inferences: dict[str, str | None]
    evidence: EvidenceMap = field(default_factory=dict)
    extractor_version: str = "v1-rules-baseline"
    taxonomy_version: str = "v1"


@dataclass(slots=True)
class PipelineResult:
    source: SourceDocument
    normalized: NormalizedDocument
    extraction: ExtractionResult


InputFormat = Literal["text", "json", "csv"]