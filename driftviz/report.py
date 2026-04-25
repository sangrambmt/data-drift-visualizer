import json
import os
import matplotlib.pyplot as plt


def recommendation(score):
    if score < 0.3:
        return "No action needed"
    elif score < 0.7:
        return "Monitor closely"
    return "Retraining recommended"


# -------- CHARTS --------
def plot_histograms(df1, df2):
    os.makedirs("reports/images", exist_ok=True)

    image_paths = {}

    for col in df1.columns:
        if col not in df2.columns:
            continue

        try:
            plt.figure()

            plt.hist(df1[col].dropna(), alpha=0.5, label="baseline")
            plt.hist(df2[col].dropna(), alpha=0.5, label="current")

            plt.title(col)
            plt.legend()

            # save full path
            full_path = f"reports/images/{col}.png"
            plt.savefig(full_path)
            plt.close()

            # store RELATIVE path (important fix)
            image_paths[col] = f"images/{col}.png"

        except Exception as e:
            continue

    return image_paths


# -------- HTML --------
def generate_html(report, image_paths, path):
    rows = ""

    sorted_cols = sorted(
        report["columns"].items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )

    for col, r in sorted_cols:
        explanation = ", ".join(r["explanation"]) or "No issue"
        img = image_paths.get(col, "")

        img_tag = f'<img src="{img}" width="300">' if img else ""

        rows += f"""
        <tr>
            <td>{col}</td>
            <td>{r["type"]}</td>
            <td>{r["score"]}</td>
            <td class="{r["label"].lower()}">{r["label"]}</td>
            <td>{explanation}</td>
            <td>{img_tag}</td>
        </tr>
        """

    html = f"""
<html>
<head>
<style>
body {{ font-family: Arial; background:#f5f5f5; padding:20px; }}
.card {{ background:white; padding:20px; border-radius:10px; margin-bottom:20px; }}
.low {{ color:green; font-weight:bold; }}
.medium {{ color:orange; font-weight:bold; }}
.high {{ color:red; font-weight:bold; }}
table {{ width:100%; border-collapse: collapse; }}
td, th {{ padding:10px; border-bottom:1px solid #ddd; }}
img {{ border-radius:6px; }}
</style>
</head>

<body>

<div class="card">
<h2>Overall Drift: <span class="{report["overall_label"].lower()}">
{report["overall_label"]} ({report["overall_score"]})
</span></h2>

<p><b>Recommendation:</b> {report["recommendation"]}</p>
</div>

<div class="card">
<table>
<tr>
<th>Column</th>
<th>Type</th>
<th>Score</th>
<th>Risk</th>
<th>Explanation</th>
<th>Chart</th>
</tr>
{rows}
</table>
</div>

</body>
</html>
"""

    with open(path, "w") as f:
        f.write(html)


# -------- MAIN REPORT --------
def generate_report(results, df1, df2):
    os.makedirs("reports", exist_ok=True)

    scores = [r["score"] for r in results.values()]
    overall_score = sum(scores) / len(scores)

    if overall_score < 0.3:
        label = "LOW"
    elif overall_score < 0.7:
        label = "MEDIUM"
    else:
        label = "HIGH"

    report = {
        "overall_score": round(overall_score, 3),
        "overall_label": label,
        "recommendation": recommendation(overall_score),
        "columns": results
    }

    json_path = "reports/report.json"
    html_path = "reports/report.html"

    # save JSON
    with open(json_path, "w") as f:
        json.dump(report, f, indent=2)

    # generate charts
    image_paths = plot_histograms(df1, df2)

    # generate HTML
    generate_html(report, image_paths, html_path)

    return report