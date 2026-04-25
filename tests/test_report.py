from driftviz.report import generate_report


def test_report():
    res = {"a": {"psi": 0.3}}
    r = generate_report(res, "test.json")
    assert r["overall_drift"] == "HIGH"