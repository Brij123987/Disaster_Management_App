import os
from django.apps import AppConfig
# from apscheduler.schedulers.background import BackgroundScheduler
# from user_system.alert_scheduler.alertScheduler import check_and_send_alerts

# scheduler = BackgroundScheduler()

class UserSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_system'

    # def ready(self):
    #     # Prevent the scheduler from running twice in development
    #     if os.environ.get('RUN_MAIN') == 'true':
    #         self.schedule_job()

    # def schedule_job(self):
    #     # Check if job is already scheduled (optional if using global scheduler)
    #     if not scheduler.get_jobs():
    #         scheduler.add_job(check_and_send_alerts, 'interval', hours=1)
    #         scheduler.start()