import argparse
from .utils import load_csv
from .detector import detect_drift
from .report import generate_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline")
    parser.add_argument("current")
    args = parser.parse_args()

    df1 = load_csv(args.baseline)
    df2 = load_csv(args.current)

    results = detect_drift(df1, df2)
    report = generate_report(results, df1, df2)

    # -------- TERMINAL OUTPUT (same as before) --------
    print(f"\nOverall Drift: {report['overall_label']} ({report['overall_score']})")
    print(f"Recommendation: {report['recommendation']}\n")

    sorted_cols = sorted(results.items(), key=lambda x: x[1]["score"], reverse=True)

    print("Top Risk Columns:")
    for col, r in sorted_cols[:3]:
        print(f"  {col} ({r['label']})")
    print()

    for col, r in sorted_cols:
        print(f"{col} → {r['label']} ({r['score']})")
        for e in r["explanation"]:
            print(f"  - {e}")
        print()

    # -------- FILE OUTPUT --------
    print("Reports generated:")
    print("  report.json")
    print("  report.html\n")


if __name__ == "__main__":
    main()