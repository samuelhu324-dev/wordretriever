from __future__ import annotations

import argparse
from pathlib import Path

from .sample_ops import build_sample_batch_manifest, write_sample_batch_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a sample batch manifest for JD curation work.")
    parser.add_argument("input_dir", help="Directory containing .txt JD samples for the batch.")
    parser.add_argument(
        "--stage",
        choices=("intake", "reviewed", "gold_candidate", "gold"),
        default="intake",
        help="Sample stage label for the batch. Defaults to intake.",
    )
    parser.add_argument(
        "--batch-id",
        default=None,
        help="Optional explicit batch identifier. Defaults to a UTC timestamp slug.",
    )
    parser.add_argument(
        "--output-path",
        default="artifacts/_tmp_sample_ops/latest_batch_manifest.json",
        help="Where to write the batch manifest JSON.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    manifest = build_sample_batch_manifest(
        input_dir=args.input_dir,
        stage=args.stage,
        batch_id=args.batch_id,
    )
    write_sample_batch_manifest(manifest, args.output_path)
    print(f"Sample batch manifest written to {Path(args.output_path)}")
    print(f"Batch id: {manifest.batch_id}")
    print(f"Stage: {manifest.stage}")
    print(f"Sample count: {manifest.sample_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())