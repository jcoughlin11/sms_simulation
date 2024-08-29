import argparse
from typing import List

from hypothesis import assume
from hypothesis import given
import hypothesis.strategies as st
import pytest

from sms_simulation.io.args import _positive_int
from sms_simulation.io.args import _time_float
from sms_simulation.io.args import _failure_float
from sms_simulation.io.args import _squeeze_list


# ============================================
#      test_positive_int_numeric_input
# ============================================
@given(st.text().filter(lambda x: x.isnumeric()))
def test_positive_int_numeric_input(s: str) -> None:
    if int(s) > 0:
        assert int(s) == _positive_int(s)
    else:
        with pytest.raises(argparse.ArgumentTypeError):
            _positive_int(s)


# ============================================
#       test_positive_int_alpha_input
# ============================================
@given(st.text().filter(lambda x: x.isalpha()))
def test_positive_int_alpha_input(s: str) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        _positive_int(s)


# ============================================
#        test_time_float_numeric_input
# ============================================
@given(st.text().filter(lambda x: x.isnumeric()))
def test_time_float_numeric_input(s: str) -> None:
    if float(s) > 0:
        assert float(s) == _time_float(s)
    else:
        with pytest.raises(argparse.ArgumentTypeError):
            _time_float(s)


# ============================================
#        test_time_float_alpha_input
# ============================================
@given(st.text().filter(lambda x: x.isalpha()))
def test_time_float_alpha_input(s: str) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        _time_float(s)


# ============================================
#      test_failure_float_numeric_input
# ============================================
@given(st.text().filter(lambda x: x.isnumeric()))
def test_failure_float_numeric_input(s: str) -> None:
    if float(s) > 0:
        assert float(s) == _failure_float(s)
    else:
        with pytest.raises(argparse.ArgumentTypeError):
            _failure_float(s)


# ============================================
#        test_failure_float_alpha_input
# ============================================
@given(st.text().filter(lambda x: x.isalpha()))
def test_failure_float_alpha_input(s: str) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        _failure_float(s)


# ============================================
#             test_squeeze_list
# ============================================
@given(st.lists(st.floats()), st.integers(), st.floats())
def test_squeeze_list(lst: List[float], length: int, fill: float) -> None:
    # The failure_float and time_float checks should prevent an invalid length
    assume(length > 0)
    assert len(_squeeze_list(lst, length, fill)) == length
