import argparse
import multiprocessing as mp

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
    mp.set_start_method("spawn")

    args: argparse.Namespace = parse_args()
    monitor: SmsMonitor = SmsMonitor(args)

    timeout: float = args.nMessages
    return monitor.run(timeout)
