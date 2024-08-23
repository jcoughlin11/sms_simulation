from sms_simulation.io.args import parse_args
from sms_simulation.monitor.monitor import SmsMonitor


# ============================================
#                    main
# ============================================
def main() -> int:
    args = parse_args()
    monitor = SmsMonitor(args)
    return monitor.run()
