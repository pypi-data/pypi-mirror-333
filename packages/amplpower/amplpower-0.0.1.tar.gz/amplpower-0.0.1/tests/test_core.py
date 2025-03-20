from amplpower import compute, PowerSystem


def test_compute():
    assert compute(["a", "bc", "abc"]) == "abc"

def test_powersystem():
    ps = PowerSystem("case9")
    