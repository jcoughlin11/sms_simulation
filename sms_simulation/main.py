from sms_simulation.io.args import parse_args
from sms_simulation.monitor.monitor import SmsMonitor


# ============================================
#                    main
# ============================================
def main() -> int:
    args = parse_args()
    monitor = SmsMonitor(args)

    print(f"\nSending: {args.nMessages} messages")
    print(f"Using: {args.nSenders} senders")

    print(f"\nAverage time to send (s) for each sender:")
    for i in range(args.nSenders):
        if i == 5:
            print("\t* (showing only first five)")
            break
        print(f"\t* {args.timeToSend[i]}")

    print(f"\nFailure rate for each sender:")
    for i in range(args.nSenders):
        if i == 5:
            print("\t* (showing only first five)")
            break
        print(f"\t* {args.sendFailureRate[i] * 100}%")

    print(f"\nUpdating progress every: {args.progUpdateTime:.2f}s\n")

    return monitor.run()
