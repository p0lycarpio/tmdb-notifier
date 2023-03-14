from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import time

import base as run

if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone="Europe/Paris")
    scheduler.add_job(run.main(), CronTrigger.from_crontab(cron), misfire_grace_time=60)

    scheduler.print_jobs()
    scheduler.start()

    try:
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
