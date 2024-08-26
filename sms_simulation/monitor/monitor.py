import argparse
import multiprocessing as mp
from queue import Empty
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
        self._progUpdateTime: float = args.progUpdateTime

        self._msgQueue: mp.Queue = mp.Queue(maxsize=self._nMessages + args.nSenders)
        self._responseQueue: mp.Queue = mp.Queue(
            maxsize=self._nMessages + args.nSenders
        )

        self._smsProducer: SmsProducer = SmsProducer(self._nMessages, self._msgQueue)
        self._smsSenders: List[SmsSender] = [
            SmsSender(
                args.timeToSend[i],
                args.sendFailureRate[i],
                self._msgQueue,
                self._responseQueue,
            )
            for i in range(args.nSenders)
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
        startTime = time.time()

        self._smsProducer.start()

        for sender in self._smsSenders:
            sender.start()

        while self._state["messagesSent"] < self._nMessages:
            try:
                response: Dict[str, float | bool] = self._responseQueue.get_nowait()
            except Empty:
                pass
            else:
                self._state["messagesSent"] += 1.0
                self._state["failedSends"] += 1 if not response["successful"] else 0
                self._state["avgTimeToSend"] += response["timeToSend"]

            currentTime: float = time.time()

            if (currentTime - startTime) >= self._progUpdateTime:
                self.display()
                self._move_cursor_up(3)
                startTime = currentTime

        self._smsProducer.join()

        for _ in range(len(self._smsSenders)):
            self._msgQueue.put(SENTINEL)

        for sender in self._smsSenders:
            sender.join()

        self.display()

        return 0

    # -----
    # display
    # -----
    def display(self) -> None:
        avgTime: float | str = "N/A"

        if self._state["messagesSent"] > 0:
            avgTime = round(
                self._state["avgTimeToSend"] / self._state["messagesSent"], 2
            )

        print(
            "Number of messages sent: "
            f"{int(self._state['messagesSent'])} / {self._nMessages}\n"
            f"Number of messages failed: {int(self._state['failedSends'])}\n"
            f"Average time per message: {avgTime}"
        )

    # -----
    # _move_cursor_up
    # -----
    def _move_cursor_up(self, nLines: int) -> None:
        for _ in range(nLines):
            print("\033[F", end="")
