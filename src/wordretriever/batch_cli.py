from __future__ import annotations

import argparse
from pathlib import Path

from .batch import run_batch_pipeline, write_batch_summary_csv, write_batch_summary_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the wordretriever batch analysis pipeline.")
    parser.add_argument("input_path", help="Path to a folder or file for batch processing.")
    parser.add_argument(
        "--input-format",
        choices=("text", "json", "csv"),
        default="text",
        help="Format of the batch inputs. Defaults to text.",
    )
    parser.add_argument(
        "--output-dir",
        default="artifacts/_tmp_batch_delivery/latest_run",
        help="Directory where per-document pipeline JSON outputs will be written.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    summary = run_batch_pipeline(
        input_path=args.input_path,
        input_format=args.input_format,
        output_dir=args.output_dir,
    )
    summary_json_path = Path(args.output_dir) / "batch-summary.json"
    summary_csv_path = Path(args.output_dir) / "batch-summary.csv"
    write_batch_summary_json(summary, str(summary_json_path))
    write_batch_summary_csv(summary, str(summary_csv_path))
    print(f"Batch outputs written to {Path(args.output_dir)}")
    print(f"Processed {summary.processed_count} input(s)")
    print(f"Batch summary JSON written to {summary_json_path}")
    print(f"Batch summary CSV written to {summary_csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())