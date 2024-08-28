from sms_simulation.io.args import parse_args
from sms_simulation.monitor.monitor import SmsMonitor


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
        0 if success.
    """
    args = parse_args()
    monitor = SmsMonitor(args)

    return monitor.run()
