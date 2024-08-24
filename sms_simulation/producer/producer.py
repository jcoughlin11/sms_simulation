import multiprocessing as mp
import random
import string
from typing import Dict


# ============================================
#                 SmsProducer
# ============================================
class SmsProducer:
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
        phoneNumber: str = "-".join(
            str(random.randint(0, 999)).zfill(3) for _ in range(3)
        )
        return phoneNumber + str(random.randint(0, 9))

    # -----
    # _generate_message
    # -----
    def _generate_message(self) -> str:
        msgLen: int = random.randint(1, self._maxMsgLen)
        return "".join(random.choice(string.ascii_lowercase) for _ in range(msgLen))

    # -----
    # _produce_sms
    # -----
    def _produce_sms(self, nMessages: int, msgQueue: mp.Queue) -> None:
        for _ in range(nMessages):
            sms: Dict[str, str] = {
                self._generate_phone_number(): self._generate_message()
            }

            msgQueue.put(sms)

    # -----
    # start
    # -----
    def start(self) -> None:
        self._producerProcess.start()

    # -----
    # join
    # -----
    def join(self) -> None:
        self._producerProcess.join()
