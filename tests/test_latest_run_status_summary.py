from tools.check_latest_run_status import parse_report


def test_parse_report_uses_final_pytest_summary_not_earlier_small_summary():
    text = """
    tests/test_one.py::test_a PASSED
    ========================= 1 passed in 0.01s =========================
    other output
    ========================= 346 passed, 3 warnings in 31.0s =========================
    """

    passed, failed, state = parse_report(text)

    assert passed == 346
    assert failed == 0
    assert state == "OK"
