import json

from django_celery_beat.models import PeriodicTask, CrontabSchedule

from applications.task.models import Task


def create_cron_check_task(task_id):
    """启动cron周期任务"""
    task_obj = Task.objects.get(id=task_id)
    cron_time = task_obj.cron_time  # cron字符串  */5 * 1-6/7 * *
    cron_interval = CronTaskUtils.cron_schedule(*cron_time.split(" "))
    task_args = json.dumps([task_id])
    task_func = "applications.task.tasks.run_by_task_in_celery"
    task = CronTaskUtils(f"job_task.{task_id}", cron_interval, task_func, task_args)
    task.start_task()


def delete_cron_task(task_id):
    CronTaskUtils.del_task(task_id)


class CronTaskUtils:
    """cron周期任务"""

    def __init__(self, task_name, cron_schedule, task, task_args, **kwargs):
        self.periodic_task = PeriodicTask.objects.create(
            name=task_name,
            task=task,
            crontab=cron_schedule,
            args=task_args,
            kwargs=kwargs,
        )

    @staticmethod
    def cron_schedule(minute="30", hour="*", day_of_week="*", day_of_month="*", month_of_year="*"):
        interval = CrontabSchedule.objects.create(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
        )
        return interval

    def start_task(self):
        """
        启动任务
        """
        self.periodic_task.enabled = True
        self.periodic_task.save()

    def stop_task(self):
        """
        停止任务
        """
        self.periodic_task.enabled = False
        self.periodic_task.save()

    @staticmethod
    def del_task(check_task_id):
        """
        删除任务
        """
        PeriodicTask.objects.filter(name=f"job_task.{check_task_id}").update(enabled=False)
        PeriodicTask.objects.filter(name=f"job_task.{check_task_id}").delete()
