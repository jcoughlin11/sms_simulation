import argparse
import math
from typing import List

from hypothesis import assume
from hypothesis import given
import hypothesis.strategies as st
import pytest

from sms_simulation.args import _positive_int
from sms_simulation.args import _time_float
from sms_simulation.args import _failure_float
from sms_simulation.args import _squeeze_list


# ============================================
#      test_positive_int_numeric_input
# ============================================
@given(st.integers().map(str))
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
    with pytest.raises(ValueError):
        _positive_int(s)


# ============================================
#        test_time_float_numeric_input
# ============================================
@given(st.floats().map(str))
def test_time_float_numeric_input(s: str) -> None:
    if float(s) > 0 and math.isfinite(float(s)):
        assert float(s) == _time_float(s)
    else:
        with pytest.raises(argparse.ArgumentTypeError):
            _time_float(s)


# ============================================
#        test_time_float_alpha_input
# ============================================
@given(st.text().filter(lambda x: x.isalpha()))
def test_time_float_alpha_input(s: str) -> None:
    with pytest.raises(ValueError):
        _time_float(s)


# ============================================
#      test_failure_float_numeric_input
# ============================================
@given(st.floats().map(str))
def test_failure_float_numeric_input(s: str) -> None:
    if float(s) >= 0.0 and float(s) <= 1.0 and math.isfinite(float(s)):
        assert float(s) == _failure_float(s)
    else:
        with pytest.raises(argparse.ArgumentTypeError):
            _failure_float(s)


# ============================================
#        test_failure_float_alpha_input
# ============================================
@given(st.text().filter(lambda x: x.isalpha()))
def test_failure_float_alpha_input(s: str) -> None:
    with pytest.raises(ValueError):
        _failure_float(s)


# ============================================
#             test_squeeze_list
# ============================================
@given(
    st.lists(st.floats(min_value=42, max_value=42), max_size=10),
    st.integers(min_value=1, max_value=100),
)
def test_squeeze_list(lst: List[float], length: int) -> None:
    # The failure_float and time_float checks should prevent an invalid length
    assert len(_squeeze_list(lst, length, 42)) == length
