from pathlib import Path
from subprocess import run

import pytest


def assert_makefile_valid(ex: Path):
    make = ex / "Makefile"
    assert make.exists()
    assert run(["make", "-C", str(ex), "clean"]).returncode == 0
    assert run(["make", "-C", str(ex)]).returncode == 0


def assert_no_forbidden_cfuncs(obj: Path):
    FORBIDDENS = ["alloc", "printf", "free"]

    def find_forbidden_cfuncs(symbols: str):
        for line in symbols.splitlines():
            if line.startswith("__") or line.startswith("___"):
                continue
            for forbidden in FORBIDDENS:
                assert forbidden not in line

    result = run(["nm", "-u", obj], capture_output=True)
    assert result.returncode == 0
    find_forbidden_cfuncs(result.stdout.decode())


def assert_no_forbidden_text(text: str):
    FORBIDDENS = ["friend", "using namespace"]


def assert_no_algorithm(text: str):
    assert "<algorithm>" not in text


module00 = [("ex00", False), ("ex01", False), ("ex02", True)]


@pytest.mark.parametrize(("exstr", "algorithm_allowed"), module00)
def test_ex_valid(exstr: str, algorithm_allowed: bool):
    ex = Path(exstr)
    assert_makefile_valid(ex)

    glob_len = lambda p, ext: len(list(p.glob(f"*.{ext}")))

    assert glob_len(ex, "c") == 0
    assert glob_len(ex, "h") == 0

    for cppfile in ex.glob("*.cpp"):
        text = cppfile.read_text()
        assert_no_forbidden_text(text)
        if not algorithm_allowed:
            assert_no_algorithm(text)

    for obj in ex.glob("*.o"):
        assert_no_forbidden_cfuncs(obj)
