from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .contracts import InputFormat, PipelineResult
from .extract import extract_signals
from .loader import load_source_document
from .normalize import normalize_document


def run_single_document_pipeline(input_path: str, input_format: InputFormat) -> PipelineResult:
    source = load_source_document(input_path=input_path, input_format=input_format)
    normalized = normalize_document(source)
    extraction = extract_signals(source, normalized)
    return PipelineResult(source=source, normalized=normalized, extraction=extraction)


def write_pipeline_result(result: PipelineResult, output_path: str) -> None:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": asdict(result.source),
        "normalized": asdict(result.normalized),
        "extraction": asdict(result.extraction),
    }
    destination.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")