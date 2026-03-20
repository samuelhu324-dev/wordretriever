from __future__ import annotations

import argparse

from .review import review_batch_outputs, write_batch_review_summary, write_intake_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Review a batch run and produce sample decisions plus an intake report.")
    parser.add_argument("batch_summary_path", help="Path to a batch-summary.json file.")
    parser.add_argument(
        "--review-output-path",
        default="artifacts/_tmp_review/latest_review_summary.json",
        help="Where to write the batch review summary JSON.",
    )
    parser.add_argument(
        "--report-output-path",
        default="artifacts/_tmp_reports/latest_intake_report.md",
        help="Where to write the human-readable intake report markdown.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    summary = review_batch_outputs(args.batch_summary_path)
    write_batch_review_summary(summary, args.review_output_path)
    write_intake_report(summary, args.report_output_path)
    print(f"Review summary written to {args.review_output_path}")
    print(f"Intake report written to {args.report_output_path}")
    print(f"Reviewed {summary.reviewed_count} sample(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())