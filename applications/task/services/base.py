from applications.task.models import Task
from applications.task.services.clock_task import delete_clock_task, create_clock_check_task, create_clock_cycle_task
from applications.task.utils import delete_cron_task, create_cron_check_task
from applications.task.services.cycle_task import delete_cycle_task


def delete_period_task(task_id):
    task = Task.objects.filter(id=task_id).first()
    if not task:
        return False
    run_type = task.run_type
    if run_type == "time":
        delete_clock_task(task_id)
    elif run_type == "cycle":
        delete_cycle_task(task_id)
    elif run_type == "cron":
        delete_cron_task(task_id)


def create_period_task(task_id):
    task = Task.objects.filter(id=task_id).first()
    if not task:
        return False
    run_type = task.run_type
    if run_type == "time":
        create_clock_check_task(task_id)
    elif run_type == "cycle":
        create_clock_cycle_task(task_id)
    elif run_type == "cron":
        create_cron_check_task(task_id)
