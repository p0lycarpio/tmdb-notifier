from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import os
import time

import tmdb

discord_url = os.getenv("DISCORD_WEBHOOK")
cron = os.getenv("CRON", "0 20 * * *")


# if discord_url is None:
#     print("La variable 'DISCORD_WEBHOOK' n'est pas valorisée"), exit()

if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone="Europe/Paris")
    scheduler.add_job(tmdb.main(), CronTrigger.from_crontab(cron), misfire_grace_time=60)

    scheduler.print_jobs()
    scheduler.start()

    try:
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
