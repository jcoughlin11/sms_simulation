import math
import multiprocessing as mp
import random
import time
from typing import Dict

from sms_simulation.constants import SEND_SIGMA
from sms_simulation.constants import SENTINEL


# ============================================
#                  SmsSender
# ============================================
class SmsSender:
    # -----
    # constructor
    # -----
    def __init__(
        self,
        timeToSend: float,
        sendFailureRate: float,
        msgQueue: mp.Queue,
        responseQueue: mp.Queue,
    ) -> None:
        self._timeToSend: float = timeToSend
        self._sendFailureRate: float = sendFailureRate
        self._msgQueue: mp.Queue = msgQueue
        self._responseQueue: mp.Queue = responseQueue

        self._senderProcess: mp.Process = mp.Process(
            target=self._send_sms, args=(self._msgQueue, self._responseQueue)
        )

    # -----
    # _send_sms
    # -----
    def _send_sms(self, msgQueue: mp.Queue, responseQueue: mp.Queue) -> None:
        while True:
            sms: Dict[str, str] = msgQueue.get()

            if sms == SENTINEL:
                break

            sendTime: float = math.fabs(
                random.normalvariate(mu=self._timeToSend, sigma=SEND_SIGMA)
            )
            time.sleep(sendTime)
            sendSuccessful: bool = random.uniform(0.0, 1.0) > self._sendFailureRate
            response: Dict[str, float | bool] = {
                "successful": sendSuccessful,
                "timeToSend": sendTime,
            }

            responseQueue.put(response)

    # -----
    # start
    # -----
    def start(self) -> None:
        self._senderProcess.start()

    # -----
    # join
    # -----
    def join(self) -> None:
        self._senderProcess.join()
