from sms_simulation.io.args import parse_args
from sms_simulation.monitor.monitor import SmsMonitor


# ============================================
#                    main
# ============================================
def main() -> int:
    args = parse_args()
    monitor = SmsMonitor(args)

    print(f"Sending: {args.nMessages} messages")
    print(f"Using: {args.nSenders} senders")

    print(f"Average time to send (s) for each sender:")
    for i in range(args.nSenders):
        if i == 5:
            print("\t* (showing only first five)")
            break
        print(f"\t* {args.timeToSend[i]}")

    print(f"Failure rate for each sender:")
    for i in range(args.nSenders):
        if i == 5:
            print("\t* (showing only first five)")
            break
        print(f"\t* {args.sendFailureRate[i]}")

    print("\n")

    return monitor.run()
