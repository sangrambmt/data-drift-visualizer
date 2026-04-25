import pandas as pd
from driftviz.statistics import psi


def test_psi_no_drift():
    a = pd.Series([1,2,3,4,5])
    b = pd.Series([1,2,3,4,5])
    assert psi(a, b) < 0.1