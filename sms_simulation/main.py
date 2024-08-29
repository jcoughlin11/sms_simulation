import argparse

from sms_simulation.constants import TIMEOUT_BUFFER
from sms_simulation.args import parse_args
from sms_simulation.monitor import SmsMonitor


# ============================================
#                    main
# ============================================
def main() -> int:
    """
    Entry point.

    Oversees parsing the command-line arguments, setting up the
    simualation, and then running the simulation.

    Returns
    -------
    int
        0 if success, -1 otherwise.
    """
    args: argparse.Namespace = parse_args()
    monitor: SmsMonitor = SmsMonitor(args)

    timeout: float = args.nMessages * max(args.timeToSend) + TIMEOUT_BUFFER
    return monitor.run(timeout)
