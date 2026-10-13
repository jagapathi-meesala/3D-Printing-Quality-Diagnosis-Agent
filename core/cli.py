import argparse, json, sys
from pathlib import Path
from .diagnosis import build_diagnosis_report

def main() -> int:
    parser = argparse.ArgumentParser(description="Triage 3D-print quality symptoms.")
    parser.add_argument("input", help="JSON print-case file")
    args = parser.parse_args()
    try:
        case = json.loads(Path(args.input).read_text(encoding="utf-8"))
        report = build_diagnosis_report(case)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report.get("valid") else 1

if __name__ == "__main__":
    raise SystemExit(main())
