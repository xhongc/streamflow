FAIL_OFFSET_UNIT_CHOICE = (
    ("seconds", "秒"),
    ("hours", "时"),
    ("minutes", "分"),

)
node_type = (
    (0, "开始节点"),
    (1, "结束节点"),
    (2, "作业节点"),
    (3, "子流程"),
    (4, "条件分支"),
    (5, "汇聚网关"),
)


class StateType(object):
    CREATED = "CREATED"
    READY = "READY"
    RUNNING = "RUNNING"
    SUSPENDED = "SUSPENDED"
    BLOCKED = "BLOCKED"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    REVOKED = "REVOKED"


PIPELINE_STATE_TO_FLOW_STATE = {
    StateType.READY: "wait",
    StateType.RUNNING: "run",
    StateType.FAILED: "fail",
    StateType.FINISHED: "success",
    StateType.SUSPENDED: "pause",
    StateType.REVOKED: "cancel",
    StateType.BLOCKED: "stop",
    StateType.CREATED: "positive",

}


class NodeTemplateType:
    # 空节点模板(标准节点)
    EmptyTemplate = "0"
    # 带内容的节点模板
    ContentTemplate = "2"
    # 用户自定义模版
    CustomTemplate = "1"
