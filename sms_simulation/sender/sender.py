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
    """
    Represents a worker process that takes sms messages off of the
    production queue and simulates sending them out.

    Parameters
    ----------
    timeToSend : float
        The mean number of seconds the worker should sleep for. Simulates how long
        it takes to physically send out the sms.

    sendFailureRate : float
        The percentage chance (as a decimal between 0.0 and 1.) that the current
        sms will fail to send.

    msgQueue : mp.Queue
        The production queue holding the generated sms messages that are ready
        to be sent out.

    responseQueue : mp.Queue
        After a worker sends (or fails to send) a message, it puts information
        about the sending into this queue to be aggregated by the monitor.
    """

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
        """
        The target function called by the worker process.

        In an infinite loop, checks for new messages ready to be sent, simulates
        sending them via a sleep, and then sends its response back to the monitor.
        If the worker process receives a sentinel value, it means that all of the
        messages have been handled, so we quit.

        Parameters
        ----------
        msgQueue : mp.Queue
            The production queue holding the generated sms messages that are ready
            to be sent out.

        responseQueue : mp.Queue
            After a worker sends (or fails to send) a message, it puts information
            about the sending into this queue to be aggregated by the monitor.
        """
        while True:
            sms: Dict[str, str] = msgQueue.get()

            if sms == SENTINEL:
                break

            # We take the absolute value here in order to avoid passing a
            # negative value to sleep
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
        """
        Wrapper around starting the worker process.
        """
        self._senderProcess.start()

    # -----
    # join
    # -----
    def join(self) -> None:
        """
        Wrapper around waiting for the worker process to finish.
        """
        self._senderProcess.join()
