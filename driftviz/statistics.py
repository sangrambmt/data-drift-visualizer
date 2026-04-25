import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, chi2_contingency


# NUMERICAL DRIFT
def ks_test(a, b):
    stat, p = ks_2samp(a.dropna(), b.dropna())
    return {"ks_stat": stat, "p_value": p}


def psi(expected, actual, bins=10):
    expected = expected.dropna()
    actual = actual.dropna()

    breakpoints = np.linspace(0, 100, bins + 1)
    breakpoints = np.percentile(expected, breakpoints)

    e_counts, _ = np.histogram(expected, bins=breakpoints)
    a_counts, _ = np.histogram(actual, bins=breakpoints)

    e_perc = e_counts / len(expected)
    a_perc = a_counts / len(actual)

    e_perc = np.where(e_perc == 0, 0.0001, e_perc)
    a_perc = np.where(a_perc == 0, 0.0001, a_perc)

    return np.sum((a_perc - e_perc) * np.log(a_perc / e_perc))


# CATEGORICAL DRIFT
def chi_square(a, b):
    a_counts = a.value_counts()
    b_counts = b.value_counts()

    all_cats = set(a_counts.index).union(set(b_counts.index))
    a_vals = [a_counts.get(cat, 0) for cat in all_cats]
    b_vals = [b_counts.get(cat, 0) for cat in all_cats]

    chi2, p, _, _ = chi2_contingency([a_vals, b_vals])
    return {"chi2": chi2, "p_value": p}