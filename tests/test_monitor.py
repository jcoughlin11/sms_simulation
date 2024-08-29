import argparse
from typing import List

from hypothesis import given
from hypothesis import settings
import hypothesis.strategies as st

from sms_simulation.args import _get_parser
from sms_simulation.args import _validate_args
from sms_simulation.constants import TIMEOUT_BUFFER
from sms_simulation.monitor import SmsMonitor


# ============================================
#                test_monitor
# ============================================
@settings(deadline=None)
@given(
    st.integers(min_value=1, max_value=5),
    st.integers(min_value=1, max_value=5),
    st.lists(
        st.floats(min_value=0.1, max_value=0.5, allow_infinity=False, allow_nan=False)
    ),
    st.lists(
        st.floats(min_value=0.0, max_value=1.0, allow_infinity=False, allow_nan=False)
    ),
    st.floats(min_value=0.1, max_value=0.5, allow_infinity=False, allow_nan=False),
)
def test_monitor(
    nMessages: int,
    nSenders: int,
    timeToSend: List[float],
    sendFailureRate: List[float],
    progUpdateTime: float,
) -> None:
    args: argparse.Namespace = argparse.Namespace()

    args.nMessages = nMessages
    args.nSenders = nSenders
    args.timeToSend = timeToSend
    args.sendFailureRate = sendFailureRate
    args.progUpdateTime = progUpdateTime

    parser = _get_parser()
    args = _validate_args(args, parser)

    monitor: SmsMonitor = SmsMonitor(args)

    timeout: float = args.nMessages * max(args.timeToSend) + TIMEOUT_BUFFER
    returnValue: int = monitor.run(timeout)

    assert returnValue == 0
