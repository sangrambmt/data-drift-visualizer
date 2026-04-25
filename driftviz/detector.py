import pandas as pd
from .statistics import ks_test, psi, chi_square


def label_score(score):
    if score < 0.3:
        return "LOW"
    elif score < 0.7:
        return "MEDIUM"
    else:
        return "HIGH"


def detect_drift(df1, df2):
    results = {}

    for col in df1.columns:
        if col not in df2.columns:
            continue

        n1, n2 = len(df1[col]), len(df2[col])
        low_sample = n1 < 30 or n2 < 30

        if pd.api.types.is_numeric_dtype(df1[col]):

            ks = ks_test(df1[col], df2[col])
            psi_val = psi(df1[col], df2[col])

            ks_score = 1 - ks["p_value"]
            psi_score = min(psi_val / 0.25, 1.0)

            final_score = 0.5 * ks_score + 0.5 * psi_score
            label = label_score(final_score)

            explanation = []
            if psi_val > 0.25:
                explanation.append("distribution shifted (PSI high)")
            if ks["p_value"] < 0.05:
                explanation.append("statistically different (KS test)")
            if low_sample:
                explanation.append("low sample size")

            results[col] = {
                "type": "numerical",
                "score": round(final_score, 3),
                "label": label,
                "psi": round(psi_val, 3),
                "ks_p": round(ks["p_value"], 3),
                "explanation": explanation
            }

        else:
            chi = chi_square(df1[col], df2[col])

            chi_score = 1 - chi["p_value"]
            final_score = chi_score
            label = label_score(final_score)

            explanation = []
            if chi["p_value"] < 0.05:
                explanation.append("category distribution changed")
            if low_sample:
                explanation.append("low sample size")

            results[col] = {
                "type": "categorical",
                "score": round(final_score, 3),
                "label": label,
                "chi_p": round(chi["p_value"], 3),
                "explanation": explanation
            }

    return results