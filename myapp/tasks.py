from celery.task.schedules import crontab
from celery.decorators import periodic_task
from myapp import notifications,models

@periodic_task(run_every=(crontab()), name="some_task", ignore_result=True)
def some_task():
    newNotification = notifications.Notifications('SNAP')
    newNotification.check_stock_price()