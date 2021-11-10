import datetime
import time

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


scheduler.add_job(func=print_date_time, trigger='cron', hour=1, minute=2, id=str('test'), timezone='Asia/Dubai')
scheduler.start()

scheduler.reschedule_job(job_id=str('test'), trigger='cron', hour=1, minute=12)
print(scheduler.get_jobs())

time.sleep(10000)
