from __future__ import annotations

import argparse
from pathlib import Path

from .contracts import InputFormat
from .pipeline import run_single_document_pipeline, write_pipeline_result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the wordretriever single-document analysis pipeline.")
    parser.add_argument("input_path", help="Path to the manual text, JSON, or CSV input file.")
    parser.add_argument(
        "--input-format",
        choices=("text", "json", "csv"),
        default="text",
        help="Format of the input file. Defaults to text.",
    )
    parser.add_argument(
        "--output-path",
        default="artifacts/_tmp_single_doc_pipeline/latest_output.json",
        help="Where to write the pipeline JSON output.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    result = run_single_document_pipeline(
        input_path=args.input_path,
        input_format=args.input_format,  # type: ignore[arg-type]
    )
    write_pipeline_result(result, args.output_path)
    print(f"Pipeline output written to {Path(args.output_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())