# run_scheduler.py
import os
import django
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from user_system.alert_scheduler.alertScheduler import check_and_send_alerts

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disaster_management.settings')
django.setup()

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', hours=10)
def scheduled_job():
    check_and_send_alerts()

print("Scheduler started...")
scheduler.start()
