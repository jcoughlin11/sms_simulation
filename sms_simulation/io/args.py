import argparse
from typing import Dict
from typing import List

from sms_simulation.constants import SEND_SIGMA


# ============================================
#                 parse_args
# ============================================
def parse_args() -> argparse.Namespace:
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

    args = parser.parse_args()

    args.timeToSend = _squeeze_list(
        args.timeToSend, args.nSenders, parser.get_default("timeToSend")
    )

    args.sendFailureRate = _squeeze_list(
        args.sendFailureRate, args.nSenders, parser.get_default("sendFailureRate")
    )

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
            if args.__getattribute__(attr)[i] == parser.get_default(attr):
                info = "(default value)"
            print(f"\t* {args.__getattribute__(attr)[i]} {info}")

    print(f"\nUpdating progress every: {args.progUpdateTime:.2f}s\n")

    return args


# ============================================
#                _positive_int
# ============================================
def _positive_int(strValue: str) -> int:
    value: int = int(strValue)

    if value <= 0:
        raise argparse.ArgumentTypeError("Value must be > 0")

    return value


# ============================================
#                _time_float
# ============================================
def _time_float(strValue: str) -> float:
    value: float = float(strValue)

    if value <= 0.0:
        raise argparse.ArgumentTypeError("Value must be > 0")

    return value


# ============================================
#               _failure_float
# ============================================
def _failure_float(strValue: str) -> float:
    value: float = float(strValue)

    if value < 0.0 or value > 1.0:
        raise argparse.ArgumentTypeError("Value must be > 0 and < 1")

    return value


# ============================================
#               _squeeze_list
# ============================================
def _squeeze_list(src: List[float] | float, length: int, fillVal: float) -> List[float]:
    squeezedList: List[float] = []

    if isinstance(src, float):
        squeezedList = [fillVal] * length
    elif isinstance(src, List) and len(src) <= length:
        squeezedList = src + [fillVal] * (length - len(src))
    elif isinstance(src, List) and len(src) > length:
        squeezedList = src[:length]
    else:
        raise argparse.ArgumentTypeError("Must be a float or List[float].")

    return squeezedList
