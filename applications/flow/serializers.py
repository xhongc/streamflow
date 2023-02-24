import json
import os
from collections import defaultdict

from applications.utils.dag_helper import PipelineBuilder
from bamboo_engine import api
from django.db import transaction

from dj_flow.settings import BASE_DIR
from pipeline.eri.models import State
from pipeline.eri.runtime import BambooDjangoRuntime
from rest_framework import serializers

from applications.flow.constants import PIPELINE_STATE_TO_FLOW_STATE
from applications.flow.models import Process, Node, ProcessRun, NodeRun, NodeTemplate, SubProcessRun, SubNodeRun, \
    Category
from applications.utils.uuid_helper import get_uuid


class NodeDataSerializer(serializers.Serializer):
    component_code = serializers.CharField(required=False, default="node")
    description = serializers.CharField(required=False, allow_blank=True)
    fail_offset = serializers.IntegerField(required=False, default=0)
    fail_retry_count = serializers.IntegerField(required=True)
    run_mark = serializers.IntegerField(required=False, default=1)
    fail_offset_unit = serializers.CharField(required=False, default="seconds")
    inputs = serializers.JSONField(required=False)
    outputs = serializers.JSONField(required=False)
    node_name = serializers.CharField(required=True)
    is_skip_fail = serializers.BooleanField(required=True)
    is_timeout_alarm = serializers.BooleanField(required=True)

    def validate_inputs(self, obj):
        if isinstance(obj, dict):
            return obj
        else:
            return json.loads(obj)

    def validate_outputs(self, obj):
        if isinstance(obj, list):
            return obj
        else:
            return json.loads(obj)

    def validate(self, attrs):
        attrs["name"] = attrs.pop("node_name")
        attrs["show"] = attrs.pop("run_mark")
        return attrs


class NodeSerializer(serializers.Serializer):
    content = serializers.IntegerField(required=True, allow_null=True)
    ico = serializers.CharField(required=True)
    node_data = NodeDataSerializer(required=True)
    left = serializers.IntegerField(required=True)
    top = serializers.IntegerField(required=True)
    type = serializers.IntegerField(required=True)
    uuid = serializers.CharField(required=True)

    def validate(self, attrs):
        attrs["node_type"] = attrs.pop("type")
        attrs["content"] = attrs.get("content", 0) or 0
        return attrs


class PipelineTreeSerializer(serializers.Serializer):
    nodes = NodeSerializer(many=True)
    lines = serializers.ListField(required=True)


class ProcessViewSetsSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    category = serializers.ListField(default="null")
    var_table = serializers.ListField(default="null")
    run_type = serializers.CharField(default="null")
    mode = serializers.CharField(required=False)
    pipeline_tree = PipelineTreeSerializer()

    def save(self, **kwargs):
        if self.instance is not None:
            self.update(instance=self.instance, validated_data=self.validated_data)
        else:
            self.create(validated_data=self.validated_data)

    def create(self, validated_data):
        if validated_data.get("mode", "") == "clone":
            for node in validated_data["pipeline_tree"]["nodes"]:
                node["uuid"] = f"c{node['uuid']}"
        node_template_ids = []
        node_map = {}
        for node in validated_data["pipeline_tree"]["nodes"]:
            node_map[node["uuid"]] = node
            if node["node_type"] == 2:
                node_template_ids.append(node["content"])
        node_template_bulk = NodeTemplate.objects.filter(id__in=node_template_ids).in_bulk(field_name="pk")
        dag = {k: [] for k in node_map.keys()}
        gateways = defaultdict(dict)
        for line in self.validated_data["pipeline_tree"]["lines"]:
            from_uuid = line["from"] if validated_data.get("mode", "") != "clone" else f"c{line['from']}"
            to_uuid = line["to"] if validated_data.get("mode", "") != "clone" else f"c{line['to']}"

            dag[from_uuid].append(to_uuid)
            if line["getWay"]["name"] and line["getWay"]["expression"]:
                gateways[from_uuid][to_uuid] = line["getWay"]
        try:
            with transaction.atomic():
                category_list = validated_data.get("category", [])
                process = Process.objects.create(name=validated_data["name"],
                                                 description=validated_data["description"],
                                                 run_type=validated_data["run_type"],
                                                 category=category_list,
                                                 var_table=validated_data.get("var_table", []),
                                                 gateways=gateways,
                                                 dag=dag)
                for category in category_list:
                    Category.objects.update_or_create(name=category)

                bulk_nodes = []
                for node in node_map.values():
                    node_data = node.pop("node_data")
                    if node_template_bulk.get(node["content"]):
                        node_data["inputs_component"] = node_template_bulk[node["content"]].inputs_component
                    bulk_nodes.append(Node(process=process, **node, **node_data))
                Node.objects.bulk_create(bulk_nodes, batch_size=500)
                try:
                    PipelineBuilder(process_id=process.id).build()
                except Exception as e:
                    raise Exception(f"验证编译错误:{e}")
        except Exception as e:
            raise serializers.ValidationError(f"流程编排错误，请检查!：{e}")
        else:
            self._data = {}

    def update(self, instance, validated_data):
        node_map = {}
        pipeline_tree = validated_data.pop("pipeline_tree")
        for node in pipeline_tree["nodes"]:
            node_map[node["uuid"]] = node
        dag = {k: [] for k in node_map.keys()}
        gateways = defaultdict(dict)
        for line in pipeline_tree["lines"]:
            dag[line["from"]].append(line["to"])
            if line["getWay"]["name"] and line["getWay"]["expression"]:
                gateways[line["from"]][line["to"]] = line["getWay"]
        try:
            with transaction.atomic():
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.dag = dag
                instance.gateways = gateways
                instance.save()

                bulk_update_nodes, bulk_create_nodes = [], []
                Node.objects.filter(process_id=instance.id).exclude(uuid__in=list(node_map.keys())).delete()
                node_bulk = Node.objects.filter(process_id=instance.id).in_bulk(field_name="uuid")

                for node in node_map.values():
                    node_data = node["node_data"]
                    node_obj = node_bulk.get(node["uuid"], None)
                    if node_obj:
                        node_obj.content = node.get("content", 0) or 0
                        node_obj.node_type = node.get("node_type", 3)
                        node_obj.show = node_data["show"]
                        node_obj.top = node["top"]
                        node_obj.left = node["left"]
                        node_obj.ico = node["ico"]

                        node_obj.name = node_data["name"]
                        node_obj.description = node_data["description"]
                        node_obj.fail_retry_count = node_data.get("fail_retry_count", 0) or 0
                        node_obj.fail_offset = node_data.get("fail_offset", 0) or 0
                        node_obj.fail_offset_unit = node_data.get("fail_offset_unit", "seconds")
                        node_obj.is_skip_fail = node_data["is_skip_fail"]
                        node_obj.is_timeout_alarm = node_data["is_timeout_alarm"]
                        node_obj.inputs = node_data["inputs"]
                        node_obj.outputs = node_data["outputs"]
                        node_obj.component_code = node_data.get("component_code", "node")
                        bulk_update_nodes.append(node_obj)
                    else:
                        node_obj = Node()
                        node_obj.content = node.get("content", 0) or 0
                        node_obj.name = node_data["name"]
                        node_obj.description = node_data["description"]
                        node_obj.fail_retry_count = node_data.get("fail_retry_count", 0) or 0
                        node_obj.fail_offset = node_data.get("fail_offset", 0) or 0
                        node_obj.fail_offset_unit = node_data.get("fail_offset_unit", "seconds")
                        node_obj.node_type = node.get("node_type", 3)
                        node_obj.is_skip_fail = node_data["is_skip_fail"]
                        node_obj.is_timeout_alarm = node_data["is_timeout_alarm"]
                        node_obj.inputs = node_data["inputs"]
                        node_obj.show = node_data["show"]
                        node_obj.top = node["top"]
                        node_obj.left = node["left"]
                        node_obj.ico = node["ico"]
                        node_obj.outputs = node_data["outputs"]
                        node_obj.component_code = node_data.get("component_code", "node")
                        node_obj.uuid = node["uuid"]
                        node_obj.process_id = instance.id
                        bulk_create_nodes.append(node_obj)
                Node.objects.bulk_update(bulk_update_nodes,
                                         fields=["name", "description", "fail_retry_count", "fail_offset",
                                                 "fail_offset_unit", "node_type", "is_skip_fail",
                                                 "is_timeout_alarm", "inputs", "show", "top", "left", "ico",
                                                 "outputs", "component_code"], batch_size=500)
                Node.objects.bulk_create(bulk_create_nodes, batch_size=500)
                try:
                    PipelineBuilder(process_id=instance.id).build()
                except Exception as e:
                    raise Exception(f"验证编译错误:{e}")
        except Exception as e:
            raise serializers.ValidationError(f"流程编排错误，请检查!：{e}")

        self._data = {}


class ListProcessViewSetsSerializer(serializers.ModelSerializer):
    category = serializers.ListField()
    var_table = serializers.ListField()

    class Meta:
        model = Process
        # fields = "__all__"
        exclude = ("dag",)


class ListProcessRunViewSetsSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    has_sub = serializers.SerializerMethodField()

    class Meta:
        model = ProcessRun
        exclude = ("dag", "gateways")

    def _get_state(self, obj):
        if obj.state:
            return obj.state
        runtime = BambooDjangoRuntime()
        states = runtime.get_state_by_root(obj.root_id)
        flow_state = "error"
        for state in states:
            flow_state = PIPELINE_STATE_TO_FLOW_STATE[state.name]
            if state.node_id == obj.root_id:

                if flow_state != "run":
                    return flow_state
            else:
                if flow_state != "success":
                    return flow_state
        return flow_state

    def get_state(self, obj):
        try:
            return self._get_state(obj)
        except Exception as e:
            print(f"{e}")
            return "error"

    def get_has_sub(self, obj):
        return obj.sub.exists()


class ListSubProcessRunViewSetsSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()

    class Meta:
        model = SubProcessRun
        fields = "__all__"

    def get_state(self, obj):
        runtime = BambooDjangoRuntime()
        process_info = api.get_pipeline_states(runtime, root_id=obj.root_id)
        try:
            process_state = PIPELINE_STATE_TO_FLOW_STATE.get(process_info.data[obj.root_id]["state"])
        except Exception:
            process_state = "error"
        return process_state


class RetrieveProcessViewSetsSerializer(serializers.ModelSerializer):
    pipeline_tree = serializers.SerializerMethodField()
    category = serializers.ListField()
    var_table = serializers.ListField()

    def get_pipeline_tree(self, obj):
        lines = []
        nodes = []
        gateways = obj.gateways
        for _from, to_list in obj.dag.items():
            for _to in to_list:
                get_way = gateways.get(_from, {}).get(_to, {"name": "", "expression": ""})
                lines.append({
                    "from": _from,
                    "to": _to,
                    "getWay": get_way
                })
        node_list = Node.objects.filter(process_id=obj.id).values()
        node_content_id = [node["content"] for node in node_list if node.get("content", 0)]
        content_map = NodeTemplate.objects.filter(id__in=node_content_id).in_bulk()
        for node in node_list:
            node_template = content_map.get(node.get("content", 0), "")
            inputs_component = ""
            if node_template:
                inputs_component = json.dumps(node_template.inputs_component)
            nodes.append({"show": node["show"],
                          "top": node["top"],
                          "left": node["left"],
                          "ico": node["ico"],
                          "type": node["node_type"],
                          "name": node["name"],
                          "content": node["content"],
                          "node_data": {
                              "inputs": json.dumps(node["inputs"]),
                              "outputs": json.dumps(node["outputs"]),
                              "inputs_component": inputs_component,
                              "component_code": node["component_code"],
                              "run_mark": int(node["show"]),
                              "node_name": node["name"],
                              "description": node["description"],
                              "fail_retry_count": node["fail_retry_count"],
                              "fail_offset": node["fail_offset"],
                              "fail_offset_unit": node["fail_offset_unit"],
                              "is_skip_fail": node["is_skip_fail"],
                              "is_timeout_alarm": node["is_timeout_alarm"]},
                          "uuid": node["uuid"]})
        return {"lines": lines, "nodes": nodes}

    class Meta:
        model = Process
        fields = ("id", "name", "description", "category", "run_type", "pipeline_tree", "var_table")


class RetrieveProcessRunViewSetsSerializer(serializers.ModelSerializer):
    pipeline_tree = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    def _get_state(self, obj):
        if obj.state:
            return obj.state
        runtime = BambooDjangoRuntime()
        states = runtime.get_state_by_root(obj.root_id)
        flow_state = "error"
        for state in states:
            flow_state = PIPELINE_STATE_TO_FLOW_STATE[state.name]
            if state.node_id == obj.root_id:

                if flow_state != "run":
                    return flow_state
            else:
                if flow_state != "success":
                    return flow_state
        return flow_state

    def get_state(self, obj):
        try:
            return self._get_state(obj)
        except Exception as e:
            print(f"{e}")
            return "error"

    def get_pipeline_tree(self, obj):
        lines = []
        nodes = []
        gateways = obj.gateways

        for _from, to_list in obj.dag.items():
            for _to in to_list:
                get_way = gateways.get(_from, {}).get(_to, {"name": "", "expression": ""})
                lines.append({
                    "from": _from,
                    "to": _to,
                    "getWay": get_way
                })
        runtime = BambooDjangoRuntime()
        process_info = api.get_pipeline_states(runtime, root_id=obj.root_id)
        process_state = PIPELINE_STATE_TO_FLOW_STATE.get(process_info.data[obj.root_id]["state"])
        state_map = process_info.data[obj.root_id]["children"]
        node_list = NodeRun.objects.filter(process_run_id=obj.id).values()
        for node in node_list:
            pipeline_state = state_map.get(node["uuid"], {}).get("state", "READY")
            flow_state = PIPELINE_STATE_TO_FLOW_STATE[pipeline_state]
            outputs = ""
            # print(flow_state)
            if node["node_type"] not in [0, 1] and flow_state not in ["wait"]:
                output_data = api.get_execution_data_outputs(runtime, node_id=node["uuid"])
                outputs = output_data.data.get("outputs", "")
                if node["node_type"] == 3:
                    # todo 先简单判断node有fail，process就为fail
                    if State.objects.filter(parent_id=node["uuid"], name="FAILED").exists():
                        flow_state = "fail"
            # todo 先简单判断node有fail，process就为fail
            if flow_state == "fail":
                process_state = "fail"
            nodes.append({"show": node["show"],
                          "top": node["top"],
                          "left": node["left"],
                          "ico": node["ico"],
                          "type": node["node_type"],
                          "name": node["name"],
                          "state": flow_state,
                          "content": node["content"],
                          "subprocess_runtime_id": node.get("subprocess_runtime_id", None),
                          "node_data": {
                              "inputs": node["inputs"],
                              "inputs_component": node.get("inputs_component", []),
                              "outputs": outputs,
                              "run_mark": int(node["show"]),
                              "node_name": node["name"],
                              "description": node["description"],
                              "fail_retry_count": node["fail_retry_count"],
                              "fail_offset": node["fail_offset"],
                              "fail_offset_unit": node["fail_offset_unit"],
                              "is_skip_fail": node["is_skip_fail"],
                              "is_timeout_alarm": node["is_timeout_alarm"]},
                          "uuid": node["uuid"]})
        return {"lines": lines, "nodes": nodes, "process_state": process_state}

    class Meta:
        model = ProcessRun
        fields = ("id", "name", "description", "run_type", "pipeline_tree", "create_by", "create_time", "state")


class RetrieveSubProcessRunViewSetsSerializer(serializers.ModelSerializer):
    pipeline_tree = serializers.SerializerMethodField()

    def get_pipeline_tree(self, obj):
        lines = []
        nodes = []
        for _from, to_list in obj.dag.items():
            for _to in to_list:
                lines.append({
                    "from": _from,
                    "to": _to
                })
        runtime = BambooDjangoRuntime()
        process_info = api.get_pipeline_states(runtime, root_id=obj.root_id)
        process_state = PIPELINE_STATE_TO_FLOW_STATE.get(process_info.data[obj.root_id]["state"])
        state_map = process_info.data[obj.root_id]["children"]
        node_list = SubNodeRun.objects.filter(subprocess_run_id=obj.id).values()
        for node in node_list:
            pipeline_state = state_map.get(node["uuid"], {}).get("state", "READY")
            flow_state = PIPELINE_STATE_TO_FLOW_STATE[pipeline_state]
            outputs = ""
            # print(flow_state)
            if node["node_type"] not in [0, 1] and flow_state not in ["wait"]:
                output_data = api.get_execution_data_outputs(runtime, node_id=node["uuid"])
                outputs = output_data.data.get("outputs", "")
                if node["node_type"] == 3:
                    # todo先简单判断node有fail，process就为fail
                    if State.objects.filter(parent_id=node["uuid"], name="FAILED").exists():
                        flow_state = "fail"
            # todo先简单判断node有fail，process就为fail
            if flow_state == "fail":
                process_state = "fail"
            nodes.append({"show": node["show"],
                          "top": node["top"],
                          "left": node["left"],
                          "ico": node["ico"],
                          "type": node["node_type"],
                          "name": node["name"],
                          "state": flow_state,
                          "content": node["content"],
                          "node_data": {
                              "inputs": node["inputs"],
                              "outputs": outputs,
                              "run_mark": int(node["show"]),
                              "node_name": node["name"],
                              "description": node["description"],
                              "fail_retry_count": node["fail_retry_count"],
                              "fail_offset": node["fail_offset"],
                              "fail_offset_unit": node["fail_offset_unit"],
                              "is_skip_fail": node["is_skip_fail"],
                              "is_timeout_alarm": node["is_timeout_alarm"]},
                          "uuid": node["uuid"]})
        return {"lines": lines, "nodes": nodes, "process_state": process_state}

    class Meta:
        model = SubProcessRun
        fields = ("id", "name", "description", "run_type", "pipeline_tree")


class ExecuteProcessSerializer(serializers.Serializer):
    process_id = serializers.IntegerField(required=True)


class CtrlSerializer(serializers.Serializer):
    event = serializers.CharField(required=True)
    ids = serializers.ListField(required=True)


class NodeTemplateSerializer(serializers.ModelSerializer):
    component_code = serializers.CharField(read_only=True)
    create_by = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs["uuid"] = get_uuid()
        attrs["inputs_component"] = self.try_json(attrs["inputs_component"])
        attrs["inputs"] = self.try_json(attrs["inputs"])
        return attrs

    def try_json(self, val):
        if isinstance(val, str):
            try:
                val = json.loads(val)
                return val
            except Exception:
                raise serializers.ValidationError("json序列化失败")
        else:
            return val

    def save_file(self, name, content):
        coding_path = os.path.join(BASE_DIR, "applications", "flow", "plugin_code")
        with open(f"{coding_path}/{name}.py", "wb") as f:
            f.write(content.encode())

    def create(self, validated_data):
        if not validated_data.get("component_code"):
            validated_data["component_code"] = "custom_plugin"
            validated_data["template_type"] = "1"
        else:
            validated_data["template_type"] = "2"
        coding = validated_data.get("coding", "")
        instance = super(NodeTemplateSerializer, self).create(validated_data)

        self.save_file(name=f"plugin_{instance.id}", content=coding)
        return instance

    def update(self, instance, validated_data):
        coding = validated_data.get("coding", "")
        self.save_file(name=f"plugin_{instance.id}", content=coding)
        instance = super(NodeTemplateSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = NodeTemplate
        exclude = ("uuid",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "id")
