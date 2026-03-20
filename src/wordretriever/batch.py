from __future__ import annotations

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


def run_batch_pipeline(input_path: str, input_format: InputFormat, output_dir: str) -> list[BatchRunItem]:
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
            )
        )

    return items