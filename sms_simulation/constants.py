# Value sent from the monitor process to each worker process to
# indicate that the message queue has been emptied
SENTINEL = None

# The time (in seconds) each worker process takes to send its current
# sms is drawn from a normal distribution whose mean is specified as a
# command-line argument (or uses the default value) and whose standard
# deviation is given by SEND_SIGMA
SEND_SIGMA: float = 0.1

# Extra time to account for overhead and deviations in the send time
TIMEOUT_BUFFER = 5 * SEND_SIGMA
