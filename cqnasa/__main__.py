from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone
import sys

from .apod import send_apod
from .sdo import send_sdo

def main():
    args = sys.argv[1:]
    if args and args[0] == "test":
        send_apod()
        send_sdo()
        return
    sched = BlockingScheduler(timezone=timezone("Asia/Shanghai"))
    # every hour to ensure images delivered on time
    sched.add_job(send_apod, 'cron', minute=0)
    sched.add_job(send_sdo, 'cron', hour='0,6,12,18')
    sched.start()


if __name__ == "__main__":
    main()
