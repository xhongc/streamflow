from applications.flow.utils import build_and_create_process
from applications.task.services.cycle_task import create_cycle_task
from bamboo_engine import api
from dj_flow.celery_app import app
from pipeline.eri.runtime import BambooDjangoRuntime


def run_by_task(task_id):
    try:
        pipeline = build_and_create_process(task_id)
        # 执行
        runtime = BambooDjangoRuntime()
        api.run_pipeline(runtime=runtime, pipeline=pipeline)
        return True, "success"
    except Exception as e:
        return False, str(e)


@app.task
def run_by_task_in_celery(task_id):
    run_by_task(task_id)


@app.task
def cycle_run_by_task_in_celery(task_id):
    create_cycle_task(task_id)
