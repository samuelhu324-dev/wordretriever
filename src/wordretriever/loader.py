from __future__ import annotations

import csv
import json
import re
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
        posted_at=metadata.get("posted_at"),
        salary_text=metadata.get("salary_text"),
        work_arrangement=metadata.get("work_arrangement"),
        employer_questions=metadata.get("employer_questions", []),
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
        salary_text=_optional_string(payload.get("salary_text")),
        work_arrangement=_optional_string(payload.get("work_arrangement")),
        employer_questions=_string_list(payload.get("employer_questions")),
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
        salary_text=_optional_string(row.get("salary_text")),
        work_arrangement=_optional_string(row.get("work_arrangement")),
        employer_questions=_split_questions(row.get("employer_questions")),
        content_text=str(row.get("content_text") or "").strip(),
        raw_payload_ref=_optional_string(row.get("raw_payload_ref") or str(path)),
    )


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _string_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return _split_questions(value)


def _split_questions(value: object) -> list[str]:
    if value is None:
        return []
    text = str(value).strip()
    if not text:
        return []
    return [part.strip() for part in text.split("||") if part.strip()]


def _first_non_empty_line(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return None


def _extract_text_metadata(text: str) -> dict[str, object]:
    metadata: dict[str, object] = {}
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in text.splitlines()[:10]:
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        normalized_key = key.strip().lower()
        normalized_value = value.strip()
        if normalized_key in {"company", "location"} and normalized_value:
            metadata[normalized_key] = normalized_value
        if normalized_key in {"salary range", "salary"} and normalized_value:
            metadata["salary_text"] = normalized_value

    top_lines = lines[:8]
    if "company" not in metadata:
        company = _extract_company_from_top_lines(top_lines)
        if company:
            metadata["company"] = company

    if "location" not in metadata:
        location = _extract_location_from_top_lines(top_lines)
        if location:
            metadata["location"] = location

    posted_at = _extract_posted_at(lines)
    if posted_at:
        metadata["posted_at"] = posted_at

    if "salary_text" not in metadata:
        salary_text = _extract_salary_text(lines)
        if salary_text:
            metadata["salary_text"] = salary_text

    work_arrangement = _infer_work_arrangement(text, metadata.get("location"))
    if work_arrangement:
        metadata["work_arrangement"] = work_arrangement

    metadata["employer_questions"] = _extract_employer_questions(lines)
    return metadata


def _extract_company_from_top_lines(lines: list[str]) -> str | None:
    if len(lines) < 2:
        return None
    candidate = lines[1].strip()
    lowered = candidate.lower()
    blocked_tokens = (
        "view all jobs",
        "full time",
        "part time",
        "contract",
        "posted ",
        "how you match",
        "salary",
    )
    if not candidate or any(token in lowered for token in blocked_tokens):
        return None
    if "$" in candidate:
        return None
    return candidate


def _extract_location_from_top_lines(lines: list[str]) -> str | None:
    state_tokens = (" vic", " nsw", " qld", " wa", " sa", " act", " tas")
    for line in lines:
        lowered = f" {line.lower()} "
        if any(token in lowered for token in state_tokens) or "hybrid" in lowered or "remote" in lowered:
            if "view all jobs" not in lowered:
                return line
    return None


def _extract_posted_at(lines: list[str]) -> str | None:
    for line in lines[:12]:
        if line.lower().startswith("posted "):
            return line
    return None


def _extract_salary_text(lines: list[str]) -> str | None:
    for line in lines[:16]:
        lowered = line.lower()
        if "$" in line or lowered.startswith("salary range"):
            return line
    return None


def _infer_work_arrangement(text: str, location: object) -> str | None:
    lowered = text.lower()
    location_text = str(location or "").lower()
    combined = f" {lowered} {location_text} "
    if re.search(r"(?<!\w)hybrid(?!\w)", combined):
        return "hybrid"
    if re.search(r"(?<!\w)remote(?!\w)", combined):
        return "remote"
    if (
        re.search(r"(?<!\w)on-site(?!\w)", combined)
        or re.search(r"(?<!\w)on site(?!\w)", combined)
        or re.search(r"(?<!\w)in the office(?!\w)", combined)
    ):
        return "on_site"
    return "unknown"


def _extract_employer_questions(lines: list[str]) -> list[str]:
    questions: list[str] = []
    capture = False
    for line in lines:
        lowered = line.lower()
        if lowered == "employer questions":
            capture = True
            continue
        if not capture:
            continue
        if line.endswith("?"):
            questions.append(line)
    return questions


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")