import json

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from applications.task.models import Task
from dj_flow.settings import SCHEDULE_TASK_POINT


def create_cycle_task(task_id):
    task_obj = Task.objects.get(id=task_id)

    cycle_type = task_obj.cycle_type
    cycle_time = int(task_obj.cycle_time)
    p = CycleTaskUtil()
    p.create_periodic_task(
        cycle_type=cycle_type,
        cycle_time=cycle_time,
        task_name=f"cycle_task.{task_id}",
        task=SCHEDULE_TASK_POINT,
        task_args=json.dumps([task_id]),
        kwargs={}
    )
    p.start_task()


def delete_cycle_task(task_id):
    CycleTaskUtil.del_task(task_id)


class CycleTaskUtil:
    def __init__(self):
        self.periodic_task = None

    def create_periodic_task(self, cycle_type, cycle_time, task_name, task, task_args, kwargs):
        if cycle_type == "min":
            schedule, _ = IntervalSchedule.objects.get_or_create(every=cycle_time, period="minutes")
        elif cycle_type == "hour":
            schedule, _ = IntervalSchedule.objects.get_or_create(every=cycle_time, period="hours")
        else:
            schedule, _ = IntervalSchedule.objects.get_or_create(every=cycle_time, period="days")

        self.periodic_task = PeriodicTask.objects.create(name=task_name,
                                                         task=task,
                                                         interval=schedule,
                                                         args=task_args,
                                                         kwargs=kwargs)

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
        PeriodicTask.objects.filter(name=f"cycle_task.{check_task_id}").update(enabled=False)
        PeriodicTask.objects.filter(name=f"cycle_task.{check_task_id}").delete()
