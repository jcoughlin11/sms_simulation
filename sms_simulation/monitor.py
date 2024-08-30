import argparse
import multiprocessing as mp
import queue
import time
from typing import Dict
from typing import List

from progress.spinner import Spinner  # type: ignore

from sms_simulation.constants import SENTINEL
from sms_simulation.producer import SmsProducer
from sms_simulation.sender import SmsSender


# ============================================
#                 SmsMonitor
# ============================================
class SmsMonitor:
    """
    Oversees the sms producer and sender processes as well as displays
    progress information to the user via stdout.

    Parameters
    ----------
    args : argparse.Namespace
        The parsed command-line arguments passed to the tool.
    """

    # -----
    # constructor
    # -----
    def __init__(self, args: argparse.Namespace) -> None:
        self._nMessages: int = args.nMessages
        self._progUpdateTime: float = args.progUpdateTime

        self._processManager: mp.managers.SyncManager = mp.Manager()
        self._msgQueue: queue.Queue = self._processManager.Queue(
            maxsize=self._nMessages + args.nSenders
        )
        self._responseQueue: queue.Queue = self._processManager.Queue(
            maxsize=self._nMessages + args.nSenders
        )

        self._smsProducer: SmsProducer = SmsProducer(
            self._nMessages, self._msgQueue, "producer"
        )
        self._smsSenders: List[SmsSender] = [
            SmsSender(
                args.timeToSend[i],
                args.sendFailureRate[i],
                self._msgQueue,
                self._responseQueue,
                f"sender_{i}",
            )
            for i in range(args.nSenders)
        ]

        self._state: Dict[str, float] = {
            "messagesSent": 0.0,
            "failedSends": 0.0,
            "totalSendTime": 0.0,
        }

    # -----
    # run
    # -----
    def run(self, timeout: float) -> int:
        """
        Main loop.

        Starts the producer and sender processes and then keeps tabs on
        the progress.

        Returns
        -------
        int
            0 on success, a negative value otherwise.
        """
        self._start_processes()
        monitorReturnValue: int = self._monitor(timeout)
        cleanupReturnValue: int = self._cleanup()
        if monitorReturnValue + cleanupReturnValue == 0:
            self._display()

        print("Done.")
        return monitorReturnValue + cleanupReturnValue

    # -----
    # _start_processes
    # -----
    def _start_processes(self) -> None:
        self._smsProducer.start()

        for sender in self._smsSenders:
            sender.start()

    # -----
    # _monitor
    # -----
    def _monitor(self, timeout: float) -> int:
        print(f"Running with timeout: {timeout:.2f}s\n")

        returnValue: int = 0
        spinner: Spinner = Spinner()

        startTime: float = time.time()
        prevUpdateTime: float = time.time()

        while self._state["messagesSent"] < self._nMessages:
            try:
                response: Dict[str, float | bool] = self._responseQueue.get_nowait()
            except queue.Empty:
                pass
            else:
                self._state["messagesSent"] += 1.0
                self._state["failedSends"] += 1 if not response["successful"] else 0
                self._state["totalSendTime"] += response["timeToSend"]

            currentTime: float = time.time()

            if (currentTime - prevUpdateTime) >= self._progUpdateTime:
                self._display(spinner)
                self._move_cursor_up(3)
                prevUpdateTime = currentTime

            if currentTime - startTime > timeout:
                self._move_cursor_down(4)
                print("Error: timeout processing messages.")
                returnValue = -1
                break

        return returnValue

    # -----
    # _display
    # -----
    def _display(self, spinner: Spinner | None = None) -> None:
        """
        Displays progress to stdout.
        """
        # Avoid division by zero errors
        avgTime: float | str = "N/A"

        if self._state["messagesSent"] > 0:
            avgTime = round(
                self._state["totalSendTime"] / self._state["messagesSent"], 2
            )

        print(
            "Number of messages sent: "
            f"{int(self._state['messagesSent'])} / {self._nMessages}\n"
            f"Number of messages failed: {int(self._state['failedSends'])}\n"
            f"Average time per message: {avgTime}"
        )
        if spinner:
            spinner.next()

    # -----
    # _cleanup
    # -----
    def _cleanup(self) -> int:
        returnValue: int = self._stop_process(self._smsProducer)

        for _ in range(len(self._smsSenders)):
            self._msgQueue.put_nowait(SENTINEL)

        for proc in self._smsSenders:
            returnValue += self._stop_process(proc)

        return returnValue

    # -----
    # _stop_process
    # -----
    def _stop_process(self, proc: mp.Process) -> int:
        returnValue: int = 0

        proc.join(timeout=1)

        exitCode: int | None = proc.exitcode

        if exitCode is None:
            print(f"Error: process {proc.name} not done: terminating.")
            proc.terminate()
            proc.join(timeout=1)
            if proc.exitcode is None:
                proc.kill()
                proc.join(timeout=1)
            returnValue = -1

        elif exitCode != 0:
            print(f"Error: process {proc.name} failed with exit code: {exitCode}")
            returnValue = -1

        return returnValue

    # -----
    # _move_cursor_up
    # -----
    def _move_cursor_up(self, nLines: int) -> None:
        """
        Keeps the updated display "in-place" by using the ascii code
        to move the cursor up the desired number of lines.

        Parameters
        ----------
        nLines : int
            The number of lines by which to move up the cursor.
        """
        for _ in range(nLines):
            print("\033[F", end="")

    # -----
    # _move_cursor_down
    # -----
    def _move_cursor_down(self, nLines: int) -> None:
        """
        Shifts below the progress display by using the ascii code
        to move the cursor down the desired number of lines.

        Parameters
        ----------
        nLines : int
            The number of lines by which to move down the cursor.
        """
        for _ in range(nLines):
            print("\033[B", end="")
        print("\033[K", end="")
