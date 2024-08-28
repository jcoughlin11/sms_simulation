import multiprocessing as mp
import random
import string
from typing import Dict


# ============================================
#                 SmsProducer
# ============================================
class SmsProducer:
    """
    Generates the sms messages to be sent by the sender processes.

    Parameters
    ----------
    nMessages : int
        The number of sms messages to be generated.

    msgQueue : mp.Queue
        The production queue holding the generated sms messages that are ready
        to be sent out.
    """

    # -----
    # constructor
    # -----
    def __init__(self, nMessages: int, msgQueue: mp.Queue) -> None:
        self._nMessages: int = nMessages
        self._msgQueue: mp.Queue = msgQueue

        self._maxMsgLen: int = 100

        self._producerProcess: mp.Process = mp.Process(
            target=self._produce_sms, args=(self._nMessages, self._msgQueue)
        )

    # -----
    # _generate_phone_number
    # -----
    def _generate_phone_number(self) -> str:
        """
        Generates a random phone number of the form xxx-xxx-xxxx. No country code
        is applied, so we are implicitly assuming that these are all U.S. numbers.

        Returns
        -------
        str
            The randomly generated phone number that the sms will be sent to.
        """
        phoneNumber: str = "-".join(
            str(random.randint(0, 999)).zfill(3) for _ in range(3)
        )
        return phoneNumber + str(random.randint(0, 9))

    # -----
    # _generate_message
    # -----
    def _generate_message(self) -> str:
        """
        Generates a string of random characters up to self._maxMsgLen in length.
        These characters represent the body of the sms being sent.

        Returns
        -------
        str
            The random string of characters representing the body of the sms.
        """
        msgLen: int = random.randint(1, self._maxMsgLen)
        return "".join(random.choice(string.ascii_lowercase) for _ in range(msgLen))

    # -----
    # _produce_sms
    # -----
    def _produce_sms(self, nMessages: int, msgQueue: mp.Queue) -> None:
        """
        Generates a random sms message and random phone number the sms will be
        sent to. Currently, each number gets a different randomly generated
        message. This function serves as the target for the producer process.

        Parameters
        ----------
        nMessages : int
            The number of sms messages to be generated.

        msgQueue : mp.Queue
            The production queue holding the generated sms messages that are ready
            to be sent out.
        """
        for _ in range(nMessages):
            sms: Dict[str, str] = {
                self._generate_phone_number(): self._generate_message()
            }

            msgQueue.put(sms)

    # -----
    # start
    # -----
    def start(self) -> None:
        """
        Wrapper around starting the producer process.
        """
        self._producerProcess.start()

    # -----
    # join
    # -----
    def join(self) -> None:
        """
        Wrapper around waiting for the producer process to finish.
        """
        self._producerProcess.join()
