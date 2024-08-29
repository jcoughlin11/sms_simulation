import argparse
import math
from typing import Dict
from typing import List

from sms_simulation.constants import SEND_SIGMA


# ============================================
#                 parse_args
# ============================================
def parse_args() -> argparse.Namespace:
    """
    Defines, reads-in, and error checks the command-line arguments.
    """
    parser: argparse.ArgumentParser = _get_parser()
    args: argparse.Namespace = _parse(parser)
    args = _validate_args(args, parser)

    print(f"\nSending: {args.nMessages} messages")
    print(f"Using: {args.nSenders} senders")

    messages: Dict[str, str] = {
        "Average time to send (s) for each sender:": "timeToSend",
        "Failure rate for each sender:": "sendFailureRate",
    }

    for msg, attr in messages.items():
        print(f"\n{msg}")
        for i in range(args.nSenders):
            if i == 5:
                print("\t* (showing only first five)")
                break
            info: str = ""
            if getattr(args, attr)[i] == parser.get_default(attr):
                info = "(default value)"
            print(f"\t* {getattr(args, attr)[i]} {info}")

    print(f"\nUpdating progress every: {args.progUpdateTime:.2f}s\n")

    return args


# ============================================
#               _get_parser
# ============================================
def _get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sms_simulation",
        description="Simulates sending out a large number of sms messages.",
    )

    parser.add_argument(
        "-n",
        "--n-messages",
        default=1000,
        type=_positive_int,
        dest="nMessages",
        help="The number of SMS messages to send.",
    )

    parser.add_argument(
        "-s",
        "--n-senders",
        default=1,
        type=_positive_int,
        dest="nSenders",
        help="The number of processes to use for sending messages.",
    )

    parser.add_argument(
        "-t",
        "--time-to-send",
        default=0.1,
        type=_time_float,
        dest="timeToSend",
        help="Each sender process takes a certain amount of time to physically send "
        "the message. That time is drawn from a normal distribution with standard "
        f"deviation = {SEND_SIGMA} and mean given by the value of this option "
        "(in seconds). This option can be specified multiple times, once for each "
        "sender instance. If fewer values of this option are given than there are "
        "senders, the default value will be used for the remaining senders. If more "
        "values of this option are specified than there are senders, only the first "
        "nSenders values will be used.",
        nargs="*",
    )

    parser.add_argument(
        "-f",
        "--failure-rate",
        default=0.1,
        type=_failure_float,
        dest="sendFailureRate",
        help="Specifies the probability, drawn from a uniform distribution, that a "
        "sender will fail to send any given sms. This option can be specified "
        "multiple times, once for each sender instance. If fewer values of this "
        "option are given than there are senders, the default value will be used for "
        "the remaining senders. If more values of this option are specified than "
        "there are senders, only the first nSenders values will be used.",
        nargs="*",
    )

    parser.add_argument(
        "-p",
        "--prog-update-time",
        default=1.0,
        type=_time_float,
        dest="progUpdateTime",
        help="The time, in seconds, between progress refreshes.",
    )

    return parser


# ============================================
#                   _parse
# ============================================
def _parse(parser: argparse.ArgumentParser) -> argparse.Namespace:
    return parser.parse_args()


# ============================================
#               _validate_args
# ============================================
def _validate_args(
    args: argparse.Namespace, parser: argparse.ArgumentParser
) -> argparse.Namespace:
    args.timeToSend = _squeeze_list(
        args.timeToSend, args.nSenders, parser.get_default("timeToSend")
    )

    args.sendFailureRate = _squeeze_list(
        args.sendFailureRate, args.nSenders, parser.get_default("sendFailureRate")
    )

    return args


# ============================================
#                _positive_int
# ============================================
def _positive_int(strValue: str) -> int:
    """
    Ensures that the given value can be converted to an integer and
    is > 0. Used by ArgumentParser.

    Parameters
    ----------
    strValue : str
        The value of the option/argument passed on the command-line.

    Returns
    -------
    value : int
        The verified, integer value of the given strValue.

    Raises
    ------
    argparse.ArgumentTypeError
        If the given value cannot be converted to an integer or is <= 0.
    """
    value: int = int(strValue)

    if value <= 0:
        raise argparse.ArgumentTypeError("Value must be > 0")

    return value


# ============================================
#                _time_float
# ============================================
def _time_float(strValue: str) -> float:
    """
    Ensures that the given value can be converted to a float and
    is > 0. Used by ArgumentParser.

    Parameters
    ----------
    strValue : str
        The value of the option/argument passed on the command-line.

    Returns
    -------
    value : float
        The verified, float value of the given strValue.

    Raises
    ------
    argparse.ArgumentTypeError
        If the given value cannot be converted to a float or is <= 0.
    """
    value: float = float(strValue)

    if not math.isfinite(value):
        raise argparse.ArgumentTypeError("Value must not be NaN or infinity.")

    # It is unphysical that something will take no time or negative time
    if value <= 0.0:
        raise argparse.ArgumentTypeError("Value must be > 0")

    return value


# ============================================
#               _failure_float
# ============================================
def _failure_float(strValue: str) -> float:
    """
    Ensures that the given value can be converted to a float and
    is (0, 1). Used by ArgumentParser.

    Parameters
    ----------
    strValue : str
        The value of the option/argument passed on the command-line.

    Returns
    -------
    value : float
        The verified, float value of the given strValue.

    Raises
    ------
    argparse.ArgumentTypeError
        If the given value cannot be converted to a float or is not in the valid range.
    """
    value: float = float(strValue)

    if not math.isfinite(value):
        raise argparse.ArgumentTypeError("Value must not be NaN or infinity.")

    if value < 0.0 or value > 1.0:
        raise argparse.ArgumentTypeError("Value must be > 0 and < 1")

    return value


# ============================================
#               _squeeze_list
# ============================================
def _squeeze_list(src: List[float] | float, length: int, fillVal: float) -> List[float]:
    """
    Ensures that the given list is equal to the desired length.

    The mean send times and failure rates can be given for only some of the worker
    processes. If there aren't enough values given, we pad the list with the default
    value. If too many are given, we keep only the first length values that were
    given.

    Parameters
    ----------
    src : List[float]
        The list to be squeezed.

    length : int
        The desired length of the list.

    fillVal : float
        The value to use in the case that not enough values were given on the
        command line.

    Returns
    -------
    squeezedList : List[float]
        The adjusted version of src that is the correct length.
    """
    squeezedList: List[float] = []

    # Just the default value is given. Means nothing was passed on the command line
    if isinstance(src, float):
        squeezedList = [fillVal] * length

    # Not enough values given on the command line
    elif isinstance(src, List) and len(src) <= length:
        squeezedList = src + [fillVal] * (length - len(src))

    # Too many values given on the command line
    elif isinstance(src, List) and len(src) > length:
        squeezedList = src[:length]
    else:
        raise argparse.ArgumentTypeError("Must be a float or List[float].")

    return squeezedList
