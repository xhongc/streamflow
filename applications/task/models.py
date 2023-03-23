from datetime import datetime

from django.db import models

from applications.flow.models import ProcessRun, Process
from django_mysql.models import JSONField


class Task(models.Model):
    TypeChoices = (
        ("hand", "手动"),
        ("now", "立即"),
        ("time", "定时"),
        ("cycle", "周期"),
        ("cron", "cron表达式"),
    )
    CycleChoices = (
        ("min", "分钟"),
        ("hour", "小时"),
        ("day", "天"),
    )
    name = models.CharField("任务名称", max_length=255, blank=False, null=False)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, db_constraint=False, related_name="base_tasks",
                                null=True)
    process_run = models.ForeignKey(ProcessRun, on_delete=models.SET_NULL, null=True, db_constraint=False,
                                    related_name="tasks")
    run_type = models.CharField("执行方式", choices=TypeChoices, max_length=64)
    when_start = models.CharField(max_length=100, verbose_name="执行时间", null=True)
    cycle_time = models.CharField(max_length=20, null=True, verbose_name="周期时间")
    cycle_type = models.CharField(max_length=20, null=True, verbose_name="周期间隔(min,hour,day)", choices=CycleChoices)
    cron_time = models.TextField(default="", verbose_name="cron表达式", null=True)

    celery_task_id = models.CharField(max_length=64, null=True, verbose_name="celery的任务ID")

    var_table = JSONField("运行时变量", default=dict)

    success_count = models.IntegerField("成功执行次数", default=0)
    fail_count = models.IntegerField("失败执行次数", default=0)
    log_converge = models.BooleanField("记录收敛", default=False)


class VarTable(models.Model):
    name = models.CharField("变量表名称", max_length=255, blank=False, null=False, unique=True)
    description = models.CharField("变量表描述", max_length=255)
    create_time = models.DateTimeField("创建时间", default=datetime.now)
    update_time = models.DateTimeField("修改时间", auto_now=True)
    data = JSONField("变量", default=list)
