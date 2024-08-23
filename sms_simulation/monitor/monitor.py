import argparse
from typing import List


# ============================================
#                 SmsMonitor
# ============================================
class SmsMonitor:
    # -----
    # constructor
    # -----
    def __init__(self, args: argparse.Namespace) -> None:
        self._nMessages: int = args.nMessages
        self._nSenders: int = args.nSenders
        self._timeToSend: List[float] = args.timeToSend
        self._sendFailureRate: List[float] = args.sendFailureRate
        self._progUpdateTime: float = args.progUpdateTime

    # -----
    # run
    # -----
    def run(self) -> int:
        return 0
