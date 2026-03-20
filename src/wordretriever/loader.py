from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .contracts import InputFormat, SourceDocument


def load_source_document(input_path: str, input_format: InputFormat) -> SourceDocument:
    path = Path(input_path)
    if input_format == "text":
        return _load_from_text(path)
    if input_format == "json":
        return _load_from_json(path)
    if input_format == "csv":
        return _load_from_csv(path)
    raise ValueError(f"Unsupported input format: {input_format}")


def source_to_dict(source: SourceDocument) -> dict[str, object]:
    return asdict(source)


def _load_from_text(path: Path) -> SourceDocument:
    content_text = path.read_text(encoding="utf-8").strip()
    title = _first_non_empty_line(content_text)
    metadata = _extract_text_metadata(content_text)
    document_id = f"manual:{path.stem}"
    return SourceDocument(
        document_id=document_id,
        source="manual",
        source_type="job_posting",
        source_url=None,
        captured_at=_utc_timestamp(),
        title=title,
        company=metadata.get("company"),
        location=metadata.get("location"),
        posted_at=None,
        content_text=content_text,
        raw_payload_ref=str(path.relative_to(path.parent.parent.parent)),
    )


def _load_from_json(path: Path) -> SourceDocument:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return SourceDocument(
        document_id=str(payload["document_id"]),
        source=str(payload.get("source", "manual")),
        source_type=str(payload.get("source_type", "job_posting")),
        source_url=_optional_string(payload.get("source_url")),
        captured_at=str(payload.get("captured_at", _utc_timestamp())),
        title=_optional_string(payload.get("title")),
        company=_optional_string(payload.get("company")),
        location=_optional_string(payload.get("location")),
        posted_at=_optional_string(payload.get("posted_at")),
        content_text=str(payload["content_text"]).strip(),
        raw_payload_ref=_optional_string(payload.get("raw_payload_ref", str(path))),
    )


def _load_from_csv(path: Path) -> SourceDocument:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        try:
            row = next(reader)
        except StopIteration as exc:
            raise ValueError("CSV input must contain at least one row") from exc

    return SourceDocument(
        document_id=str(row.get("document_id") or f"csv:{path.stem}:1"),
        source=str(row.get("source") or "manual"),
        source_type=str(row.get("source_type") or "job_posting"),
        source_url=_optional_string(row.get("source_url")),
        captured_at=str(row.get("captured_at") or _utc_timestamp()),
        title=_optional_string(row.get("title")),
        company=_optional_string(row.get("company")),
        location=_optional_string(row.get("location")),
        posted_at=_optional_string(row.get("posted_at")),
        content_text=str(row.get("content_text") or "").strip(),
        raw_payload_ref=_optional_string(row.get("raw_payload_ref") or str(path)),
    )


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _first_non_empty_line(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return None


def _extract_text_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines()[:6]:
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        normalized_key = key.strip().lower()
        normalized_value = value.strip()
        if normalized_key in {"company", "location"} and normalized_value:
            metadata[normalized_key] = normalized_value
    return metadata


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")