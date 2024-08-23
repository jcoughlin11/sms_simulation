import argparse
import multiprocessing as mp
from typing import Dict
from typing import List

from sms_simulation.producer.producer import SmsProducer
from sms_simulation.sender.sender import SmsSender


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

        self._msgQueue: mp.Queue = mp.Queue(maxsize=self._nMessages)
        self._responseQueue: mp.Queue = mp.Queue(maxsize=self._nMessages)

        self._smsProducer: SmsProducer = SmsProducer(self._nMessages, self._msgQueue)
        self._smsSenders: List[SmsSender] = [
            SmsSender(
                self._timeToSend[i],
                self._sendFailureRate[i],
                self._msgQueue,
                self._responseQueue,
            )
            for i in range(self._nSenders)
        ]

        self._state: Dict[str, float] = {
            "messagesSent": 0.0,
            "successfulSends": 0.0,
            "failedSends": 0.0,
            "avgTimeToSend": 0.0,
        }

    # -----
    # run
    # -----
    def run(self) -> int:
        self._smsProducer.start()

        for sender in self._smsSenders:
            sender.start()

        while self._state["messagesSent"] < self._nMessages:
            self._monitor()

        return 0

    # -----
    # _monitor
    # -----
    def _monitor(self) -> None:
        pass
