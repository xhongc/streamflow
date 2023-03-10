from datetime import datetime

from django.db import models
from django_mysql.models import JSONField, ListTextField

from applications.flow.constants import FAIL_OFFSET_UNIT_CHOICE, NodeTemplateType


class Category(models.Model):
    name = models.CharField("分类名称", max_length=255, blank=False, null=False)


class Process(models.Model):
    name = models.CharField("作业名称", max_length=255, blank=False, null=False)
    description = models.CharField("作业描述", max_length=255, blank=True, null=True)
    # category = models.ManyToManyField(Category)
    run_type = models.CharField("调度类型", max_length=32)
    total_run_count = models.PositiveIntegerField("执行次数", default=0)
    gateways = JSONField("网关信息", default=dict)
    constants = JSONField("内部变量信息", default=dict)
    dag = JSONField("DAG", default=dict)
    var_table = ListTextField(base_field=models.CharField(max_length=255), default=list)
    category = ListTextField(base_field=models.CharField(max_length=255), default=list)

    create_by = models.CharField("创建者", max_length=64, null=True)
    create_time = models.DateTimeField("创建时间", default=datetime.now)
    update_time = models.DateTimeField("修改时间", auto_now=True)
    update_by = models.CharField("修改人", max_length=64, null=True)

    @property
    def clone_data(self):
        return {
            "name": self.name,
            "description": self.description,
            "run_type": self.run_type,
            "gateways": self.gateways,
            "constants": self.constants,
            "dag": self.dag,
        }


class BaseNode(models.Model):
    START_NODE = 0
    END_NODE = 1
    JOB_NODE = 2
    SUB_PROCESS_NODE = 3
    CONDITION_NODE = 4
    CONVERGE_NODE = 5
    PARALLEL_NODE = 6
    CONDITION_PARALLEL_NODE = 7

    name = models.CharField("节点名称", max_length=255, blank=False, null=False)
    uuid = models.CharField("UUID", max_length=255, unique=True)
    description = models.CharField("节点描述", max_length=255, blank=True, null=True)

    show = models.BooleanField("是否显示", default=True)
    top = models.IntegerField(default=300)
    left = models.IntegerField(default=300)
    ico = models.CharField("icon", max_length=64, blank=True, null=True)

    fail_retry_count = models.IntegerField("失败重试次数", default=0)
    fail_offset = models.IntegerField("失败重试间隔", default=0)
    fail_offset_unit = models.CharField("重试间隔单位", choices=FAIL_OFFSET_UNIT_CHOICE, max_length=32)
    # 0：开始节点，1：结束节点，2：作业节点，3：子作业流 4：分支，5：汇聚.6:并行 7:条件并行
    node_type = models.IntegerField(default=2)
    component_code = models.CharField("插件名称", max_length=255, blank=False, null=False)
    is_skip_fail = models.BooleanField("忽略失败", default=False)
    is_timeout_alarm = models.BooleanField("超时告警", default=False)

    inputs = JSONField("输入参数", default=dict)
    outputs = JSONField("输出参数", default=dict)
    # 如为子流程content为process id， 如为 节点模板为node id
    content = models.IntegerField("模板id", default=0)

    class Meta:
        abstract = True

    @property
    def clone_data(self):
        return {
            "name": self.name,
            "show": self.show,
            "fail_retry_count": self.fail_retry_count,
            "fail_offset": self.fail_offset,
            "fail_offset_unit": self.fail_offset_unit,
            "is_skip_fail": self.is_skip_fail,
            "is_timeout_alarm": self.is_timeout_alarm,
            "outputs": self.outputs,
            "inputs": self.inputs,
            "content": self.content,
        }


class Node(BaseNode):
    process = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True, db_constraint=False,
                                related_name="nodes")
    inputs_component = JSONField("前端参数组件", default=list)


class ProcessRun(models.Model):
    # new
    process = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True, db_constraint=False,
                                related_name="run")
    task_id = models.IntegerField("任务ID", default=0)
    name = models.CharField("作业名称", max_length=255, blank=False, null=False)
    description = models.CharField("作业描述", max_length=255, blank=True, null=True)
    run_type = models.CharField("调度类型", max_length=32)
    gateways = JSONField("网关信息", default=dict)
    constants = JSONField("内部变量信息", default=dict)
    dag = JSONField("DAG", default=dict)

    create_by = models.CharField("创建者", max_length=64, null=True)
    create_time = models.DateTimeField("创建时间", default=datetime.now)
    update_time = models.DateTimeField("修改时间", auto_now=True)
    update_by = models.CharField("修改人", max_length=64, null=True)

    root_id = models.CharField("根节点uuid", max_length=255)
    state = models.CharField("作业流状态", max_length=32, default="")


class SubProcessRun(models.Model):
    process_run = models.ForeignKey(ProcessRun, on_delete=models.CASCADE, null=True, db_constraint=False,
                                    related_name="sub")
    process = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True, db_constraint=False,
                                related_name="sub_run")
    name = models.CharField("作业名称", max_length=255, blank=False, null=False)
    description = models.CharField("作业描述", max_length=255, blank=True, null=True)
    run_type = models.CharField("调度类型", max_length=32)
    gateways = JSONField("网关信息", default=dict)
    constants = JSONField("内部变量信息", default=dict)
    dag = JSONField("DAG", default=dict)

    create_by = models.CharField("创建者", max_length=64, null=True)
    create_time = models.DateTimeField("创建时间", default=datetime.now)
    update_time = models.DateTimeField("修改时间", auto_now=True)
    update_by = models.CharField("修改人", max_length=64, null=True)

    root_id = models.CharField("根节点uuid", max_length=255)


class SubNodeRun(BaseNode):
    subprocess_run = models.ForeignKey(SubProcessRun, on_delete=models.CASCADE, null=True, db_constraint=False,
                                       related_name="sub_nodes_run")
    inputs_component = JSONField("前端参数组件", default=list)
    subprocess_runtime_id = models.IntegerField("嵌套子流程的运行时id", null=True, blank=True)

    @staticmethod
    def field_names():
        return [field.name for field in NodeRun._meta.get_fields() if field.name not in ["id"]]


class NodeRun(BaseNode):
    process_run = models.ForeignKey(ProcessRun, on_delete=models.CASCADE, null=True, db_constraint=False,
                                    related_name="nodes_run")
    inputs_component = JSONField("前端参数组件", default=list)
    subprocess_runtime_id = models.IntegerField("子流程的运行时id", null=True, blank=True)

    @staticmethod
    def field_names():
        return [field.name for field in NodeRun._meta.get_fields() if field.name not in ["id"]]


class NodeTemplate(BaseNode):
    template_type = models.CharField("节点模板类型", max_length=1, default=NodeTemplateType.ContentTemplate)
    inputs_component = JSONField("前端参数组件", default=list)
    outputs_component = JSONField("前端参数组件", default=list)
    coding = models.TextField(default="")
    create_by = models.CharField("创建人", default="", max_length=255)
