from __future__ import annotations

import argparse
from pathlib import Path

from .guardrails import run_guardrails


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run wordretriever usage guardrails and regression checks.")
    parser.add_argument(
        "--gold-set-path",
        default="samples/gold/gold-set-v1.json",
        help="Path to the gold set JSON used for evaluation.",
    )
    parser.add_argument(
        "--batch-input-path",
        default="samples/gold",
        help="Path to a folder or file used for the batch smoke run.",
    )
    parser.add_argument(
        "--batch-input-format",
        choices=("text", "json", "csv"),
        default="text",
        help="Format of the batch smoke inputs. Defaults to text.",
    )
    parser.add_argument(
        "--output-root",
        default="artifacts/_tmp_guardrails",
        help="Directory where guardrail run artifacts will be written.",
    )
    parser.add_argument(
        "--report-template-path",
        default="templates/report-template-v1.md",
        help="Path to the report template that formal usage should follow.",
    )
    parser.add_argument(
        "--intake-template-path",
        default="templates/jd-sample-intake-v1.txt",
        help="Path to the intake template for new JD samples.",
    )
    parser.add_argument(
        "--enrichment-template-path",
        default="templates/gpt-enrichment-template-v1.json",
        help="Path to the GPT enrichment contract template.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    summary = run_guardrails(
        gold_set_path=args.gold_set_path,
        batch_input_path=args.batch_input_path,
        batch_input_format=args.batch_input_format,
        output_root=args.output_root,
        report_template_path=args.report_template_path,
        intake_template_path=args.intake_template_path,
        enrichment_template_path=args.enrichment_template_path,
    )
    print(f"Guardrail run written under {Path(args.output_root) / f'run_{summary.run_id}'}")
    print(f"PASS/FAIL: {summary.pass_fail}")
    print(f"Evaluation summary: {summary.evaluation_summary_path}")
    print(f"Batch summary JSON: {summary.batch_summary_json_path}")
    print(f"Batch summary CSV: {summary.batch_summary_csv_path}")
    return 0 if summary.pass_fail == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())