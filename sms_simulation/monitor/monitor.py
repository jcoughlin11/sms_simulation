import argparse
import multiprocessing as mp
import time
from typing import Dict
from typing import List

from sms_simulation.constants import SENTINEL
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

        self._startTime: float = 0.0

        self._msgQueue: mp.Queue = mp.Queue(maxsize=self._nMessages + self._nSenders)
        self._responseQueue: mp.Queue = mp.Queue(
            maxsize=self._nMessages + self._nSenders
        )

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
            "failedSends": 0.0,
            "avgTimeToSend": 0.0,
        }

    # -----
    # run
    # -----
    def run(self) -> int:
        self._startTime = time.time()

        self._smsProducer.start()

        for sender in self._smsSenders:
            sender.start()

        while self._state["messagesSent"] < self._nMessages:
            try:
                response: Dict[str, float | bool] = self._responseQueue.get_nowait()
            except mp.queues.Empty:
                pass
            else:
                self._state["messagesSent"] += 1.0
                self._state["failedSends"] += 1 if not response["successful"] else 0
                self._state["avgTimeToSend"] += response["timeToSend"]

            currentTime: float = time.time()

            if (currentTime - self._startTime) >= self._progUpdateTime:
                self._display()
                self._startTime = currentTime

        self._smsProducer.join()

        for _ in range(self._nSenders):
            self._msgQueue.put(SENTINEL)

        for sender in self._smsSenders:
            sender.join()

        self._display()

        return 0

    # -----
    # _display
    # -----
    def _display(self) -> None:
        print(
            "Number of messages sent: "
            f"{self._state['messagesSent']} / {self._nMessages}\n"
            f"Number of messages failed: {self._state['failedSends']}\n"
            "Average time per message: "
            f"{self._state['avgTimeToSend'] / self._state['messagesSent']}s",
            end="\r",
        )
