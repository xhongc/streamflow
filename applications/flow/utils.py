import json

from applications.flow.models import ProcessRun, NodeRun, Process, Node, SubProcessRun, SubNodeRun
from applications.task.models import Task
from applications.utils.dag_helper import PipelineBuilder, instance_dag, instance_gateways


def build_and_create_process(task_id):
    """构建pipeline和创建运行时数据"""
    task = Task.objects.filter(id=task_id).first()
    p_builder = PipelineBuilder(task_id)
    pipeline = p_builder.build()

    process = p_builder.process
    node_map = p_builder.node_map
    process_run_uuid = p_builder.instance

    # 保存的实例数据
    process_run_data = process.clone_data
    # 运算时节点uid重新生成所以需要映射回节点uid
    process_run_data["dag"] = instance_dag(process_run_data["dag"], process_run_uuid)
    process_run_data["gateways"] = instance_gateways(process_run_data["gateways"], process_run_uuid)
    process_run = ProcessRun.objects.create(process_id=process.id,
                                            root_id=pipeline["id"],
                                            task_id=task_id,
                                            **process_run_data)
    task.process_run_id = process_run.id
    task.save()
    node_run_bulk = []
    for pipeline_id, node in node_map.items():
        _node = {k: v for k, v in node.__dict__.items() if k in NodeRun.field_names()}
        _node["uuid"] = process_run_uuid[pipeline_id].id
        if node.node_type == Node.SUB_PROCESS_NODE:
            subprocess_run_id = create_subprocess(node.content, process_run.id, process_run_uuid, pipeline["id"])
            node_run_bulk.append(NodeRun(process_run=process_run, subprocess_runtime_id=subprocess_run_id, **_node))
        else:
            node_run_bulk.append(NodeRun(process_run=process_run, **_node))

    NodeRun.objects.bulk_create(node_run_bulk, batch_size=500)
    return pipeline


def create_subprocess(process_id, process_run_id, process_run_uuid, root_id):
    """
    创建子流程运行时记录
    process_id: 子流程id
    process_id: 主流程运行实例id
    """
    process = Process.objects.filter(id=process_id).first()
    process_run_data = process.clone_data
    process_run_data["dag"] = instance_dag(process_run_data["dag"], process_run_uuid)
    process_run = SubProcessRun.objects.create(process_id=process_id, process_run_id=process_run_id, root_id=root_id,
                                               **process_run_data)
    subprocess_node_map = Node.objects.filter(process_id=process_id).in_bulk(field_name="uuid")
    node_run_bulk = []
    for pipeline_id, node in subprocess_node_map.items():
        _node = {k: v for k, v in node.__dict__.items() if k in NodeRun.field_names()}
        _node["uuid"] = process_run_uuid[pipeline_id].id
        if node.node_type == Node.SUB_PROCESS_NODE:
            subprocess_run_id = create_subprocess(node.content, process_run_id, process_run_uuid, root_id)
            node_run_bulk.append(
                SubNodeRun(subprocess_run=process_run, subprocess_runtime_id=subprocess_run_id, **_node))
        else:
            node_run_bulk.append(SubNodeRun(subprocess_run=process_run, **_node))

    SubNodeRun.objects.bulk_create(node_run_bulk, batch_size=500)
    return process_run.id
