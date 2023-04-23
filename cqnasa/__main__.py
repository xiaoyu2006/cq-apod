from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone
import argparse

from .common import load_config
from .apod import send_apod
from .sdo import send_sdo


def main():
    parser = argparse.ArgumentParser(
        prog="cqnasa",
        description="Send NASA images to QQ groups.",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Send images immediately.",
    )
    args = parser.parse_args()
    if args.test:
        send_apod()
        send_sdo()
        return
    config = load_config()
    sched = BlockingScheduler(timezone=timezone(config["TIMEZONE"]))
    # every hour to ensure images delivered on time
    sched.add_job(send_apod, "cron", minute=0)
    sched.add_job(send_sdo, "cron", hour="0,6,12,18")
    sched.start()


if __name__ == "__main__":
    main()
