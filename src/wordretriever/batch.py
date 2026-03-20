from __future__ import annotations

import csv
import json
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path

from .contracts import InputFormat
from .pipeline import run_single_document_pipeline, write_pipeline_result


FILE_PATTERNS: dict[InputFormat, str] = {
    "text": "*.txt",
    "json": "*.json",
    "csv": "*.csv",
}


@dataclass(slots=True)
class BatchRunItem:
    input_path: str
    output_path: str
    document_id: str
    title: str | None
    extractor_version: str
    taxonomy_version: str


@dataclass(slots=True)
class BatchRunSummary:
    input_batch_ref: str
    input_format: str
    processed_count: int
    extractor_version: str
    taxonomy_version: str
    output_dir: str
    items: list[BatchRunItem]


def collect_batch_input_paths(input_path: str, input_format: InputFormat) -> list[Path]:
    path = Path(input_path)
    if path.is_file():
        return [path]
    if not path.is_dir():
        raise ValueError(f"Batch input path does not exist: {path}")

    matched_paths = sorted(path.glob(FILE_PATTERNS[input_format]))
    if not matched_paths:
        raise ValueError(f"No {input_format} inputs found under {path}")
    return matched_paths


def run_batch_pipeline(input_path: str, input_format: InputFormat, output_dir: str) -> BatchRunSummary:
    source_paths = collect_batch_input_paths(input_path=input_path, input_format=input_format)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    items: list[BatchRunItem] = []
    for source_path in source_paths:
        result = run_single_document_pipeline(input_path=str(source_path), input_format=input_format)
        output_path = destination / f"{source_path.stem}.output.json"
        write_pipeline_result(result, str(output_path))
        items.append(
            BatchRunItem(
                input_path=str(source_path),
                output_path=str(output_path),
                document_id=result.source.document_id,
                title=result.source.title,
                extractor_version=result.extraction.extractor_version,
                taxonomy_version=result.extraction.taxonomy_version,
            )
        )

    extractor_version = items[0].extractor_version if items else "unknown"
    taxonomy_version = items[0].taxonomy_version if items else "unknown"
    return BatchRunSummary(
        input_batch_ref=input_path,
        input_format=input_format,
        processed_count=len(items),
        extractor_version=extractor_version,
        taxonomy_version=taxonomy_version,
        output_dir=str(destination),
        items=items,
    )


def write_batch_summary_json(summary: BatchRunSummary, output_path: str) -> None:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(asdict(summary), indent=2, ensure_ascii=True), encoding="utf-8")


def write_batch_summary_csv(summary: BatchRunSummary, output_path: str) -> None:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "document_id",
                "title",
                "input_path",
                "output_path",
                "extractor_version",
                "taxonomy_version",
            ],
        )
        writer.writeheader()
        for item in summary.items:
            writer.writerow(
                {
                    "document_id": item.document_id,
                    "title": item.title or "",
                    "input_path": item.input_path,
                    "output_path": item.output_path,
                    "extractor_version": item.extractor_version,
                    "taxonomy_version": item.taxonomy_version,
                }
            )