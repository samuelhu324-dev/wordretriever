from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(slots=True)
class SampleBatchItem:
    sample_id: str
    input_path: str
    stage: str
    source_type: str
    notes: list[str]


@dataclass(slots=True)
class SampleBatchManifest:
    batch_id: str
    created_at: str
    stage: str
    sample_count: int
    input_dir: str
    items: list[SampleBatchItem]


def build_sample_batch_manifest(input_dir: str, stage: str, batch_id: str | None = None) -> SampleBatchManifest:
    source_dir = Path(input_dir)
    if not source_dir.is_dir():
        raise ValueError(f"Sample input directory does not exist: {source_dir}")

    paths = sorted({*source_dir.glob("*.txt"), *source_dir.glob("*.md")})
    if not paths:
        raise ValueError(f"No text-like samples found under {source_dir}")

    resolved_batch_id = batch_id or _timestamp_slug()
    items = [
        SampleBatchItem(
            sample_id=f"{stage}:{path.stem}",
            input_path=str(path),
            stage=stage,
            source_type="job_posting",
            notes=[],
        )
        for path in paths
    ]
    return SampleBatchManifest(
        batch_id=resolved_batch_id,
        created_at=_iso_utc_now(),
        stage=stage,
        sample_count=len(items),
        input_dir=str(source_dir),
        items=items,
    )


def write_sample_batch_manifest(manifest: SampleBatchManifest, output_path: str) -> None:
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(asdict(manifest), indent=2, ensure_ascii=True), encoding="utf-8")


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _timestamp_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")