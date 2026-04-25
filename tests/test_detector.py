import pandas as pd
from driftviz.detector import detect_drift


def test_detect():
    df1 = pd.DataFrame({"a": [1,2,3]})
    df2 = pd.DataFrame({"a": [10,20,30]})

    res = detect_drift(df1, df2)
    assert "a" in res