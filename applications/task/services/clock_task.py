import json
from datetime import timedelta

from django_celery_beat.models import PeriodicTask, ClockedSchedule

from applications.task.models import Task
from applications.utils.timer import string_to_datetime
from dj_flow.settings import SCHEDULE_TASK_POINT


def create_clock_check_task(task_id):
    """创建一个定时任务"""
    task_obj = Task.objects.get(id=task_id)
    when_start = string_to_datetime(task_obj.when_start)
    when_start = when_start - timedelta(hours=8)
    p = PeriodicTaskUtil()
    p.create_periodic_task(
        when_start=when_start,
        task_name=f"job_task.{task_id}",
        task=SCHEDULE_TASK_POINT,
        task_args=json.dumps([task_id]),
        kwargs={}
    )
    p.start_task()


def create_clock_cycle_task(task_id):
    """定时创建一个周期任务"""
    task_obj = Task.objects.get(id=task_id)
    when_start = string_to_datetime(task_obj.when_start)
    when_start = when_start - timedelta(hours=8)
    task = "applications.task.tasks.cycle_run_by_task_in_celery"
    p = PeriodicTaskUtil()
    p.create_periodic_task(
        when_start=when_start,
        task_name=f"job_task.{task_id}",
        task=task,
        task_args=json.dumps([task_id]),
        kwargs={}
    )
    p.start_task()


def delete_clock_task(task_id):
    PeriodicTaskUtil.del_task(task_id)


class PeriodicTaskUtil:
    def __init__(self):
        self.periodic_task = None

    def create_periodic_task(self, when_start, task_name, task, task_args, kwargs):
        clock, _ = ClockedSchedule.objects.get_or_create(clocked_time=when_start)
        self.periodic_task = PeriodicTask.objects.create(name=task_name,
                                                         task=task,
                                                         clocked=clock,
                                                         one_off=True,
                                                         args=task_args,
                                                         kwargs=kwargs)

    def start_task(self):
        """
        启动任务
        """
        self.periodic_task.enabled = True
        self.periodic_task.save()

    @staticmethod
    def stop_task(check_task_id):
        """
        停止任务
        """
        PeriodicTask.objects.filter(name=f"job_task.{check_task_id}").update(enabled=False)

    @staticmethod
    def resume_task(check_task_id):
        """
        停止任务
        """
        PeriodicTask.objects.filter(name=f"job_task.{check_task_id}").update(enabled=True)

    @staticmethod
    def del_task(check_task_id):
        """
        删除任务
        """
        PeriodicTask.objects.filter(name=f"job_task.{check_task_id}").update(enabled=False)
        PeriodicTask.objects.filter(name=f"job_task.{check_task_id}").delete()
