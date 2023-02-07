import random
from datetime import datetime

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.flow.constants import NodeTemplateType
from applications.flow.filters import NodeTemplateFilter, ProcessRunFilter, SubProcessRunFilter
from applications.flow.models import Process, ProcessRun, NodeTemplate, SubProcessRun, Category, NodeRun
from applications.flow.serializers import ProcessViewSetsSerializer, ListProcessViewSetsSerializer, \
    RetrieveProcessViewSetsSerializer, ExecuteProcessSerializer, ListProcessRunViewSetsSerializer, \
    RetrieveProcessRunViewSetsSerializer, NodeTemplateSerializer, ListSubProcessRunViewSetsSerializer, \
    RetrieveSubProcessRunViewSetsSerializer, CategorySerializer, CtrlSerializer
from applications.task.models import VarTable
from bamboo_engine import api
from component.drf.viewsets import GenericViewSet
from pipeline.eri.runtime import BambooDjangoRuntime


class ProcessViewSets(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      GenericViewSet):
    queryset = Process.objects.order_by("-update_time")

    def get_serializer_class(self):
        if self.action == "list":
            return ListProcessViewSetsSerializer
        elif self.action == "retrieve":
            return RetrieveProcessViewSetsSerializer
        elif self.action == "execute":
            return ExecuteProcessSerializer
        elif self.action == "var":
            return ExecuteProcessSerializer
        return ProcessViewSetsSerializer

    @action(methods=["GET"], detail=False)
    def var(self, request, *args, **kwargs):
        validated_data = self.is_validated_data(request.query_params)
        process_id = validated_data["process_id"]
        process = Process.objects.filter(id=process_id).first()
        result = []
        if process:
            var_table_ids = process.var_table
            var_tables = VarTable.objects.filter(id__in=var_table_ids).values_list("data", flat=True)
            result = sum(list(var_tables), [])
        return Response(result)


class ProcessRunViewSets(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         GenericViewSet):
    queryset = ProcessRun.objects.order_by("-update_time")
    filterset_class = ProcessRunFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ListProcessRunViewSetsSerializer
        elif self.action == "retrieve":
            return RetrieveProcessRunViewSetsSerializer
        elif self.action == "execute":
            return ExecuteProcessSerializer
        elif self.action == "control":
            return CtrlSerializer

    @action(methods=["POST"], detail=False)
    def control(self, request, *args, **kwargs):
        validated_data = self.is_validated_data(request.data)
        action_event = validated_data["event"]
        ids = validated_data["ids"]
        instance = ProcessRun.objects.filter(id=ids[0]).first()
        runtime = BambooDjangoRuntime()
        if action_event == "pause":
            result = api.pause_pipeline(runtime=runtime, pipeline_id=instance.root_id)
        elif action_event == "resume":
            result = api.resume_pipeline(runtime=runtime, pipeline_id=instance.root_id)
        elif action_event == "cancel":
            result = api.revoke_pipeline(runtime=runtime, pipeline_id=instance.root_id)
        else:
            return self.failure_response(msg="未知event")
        if result.result:
            return self.success_response()
        else:
            return self.failure_response(msg=result.exc.args[0])


class NodeRunViewSets(GenericViewSet):
    queryset = NodeRun.objects.order_by("-update_time")
    serializer_class = CtrlSerializer

    @action(methods=["POST"], detail=False)
    def control(self, request, *args, **kwargs):
        validated_data = self.is_validated_data(request.data)
        action_event = validated_data["event"]
        ids = validated_data["ids"]
        if action_event == "replay":
            runtime = BambooDjangoRuntime()
            api.retry_node(runtime=runtime, node_id=ids[0])
        elif action_event == "success":
            runtime = BambooDjangoRuntime()
            api.skip_node(runtime=runtime, node_id=ids[0])
        elif action_event == "fail":
            runtime = BambooDjangoRuntime()
            api.forced_fail_activity(runtime=runtime, node_id=ids[0], ex_data="强制失败")
        elif action_event == "pause":
            runtime = BambooDjangoRuntime()
            api.pause_node_appoint(runtime=runtime, node_id=ids[0])
        elif action_event == "resume":
            runtime = BambooDjangoRuntime()
            api.resume_node_appoint(runtime=runtime, node_id=ids[0])
        return self.success_response()


class SubProcessRunViewSets(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            GenericViewSet):
    queryset = SubProcessRun.objects.order_by("-update_time")
    filterset_class = SubProcessRunFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ListSubProcessRunViewSetsSerializer
        elif self.action == "retrieve":
            return RetrieveSubProcessRunViewSetsSerializer

    @action(methods=["POST"], detail=False)
    def control(self, request, *args, **kwargs):
        return self.success_response()


class TestViewSets(GenericViewSet):
    def list(self, request, *args, **kwargs):
        random_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        sign = random.choice(random_list)

        if sign:
            return Response({"now": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "data": request.query_params})
        else:
            return Response({"result": False, "data": [], "code": "300", "message": ""}, status=400)


class NodeTemplateViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):
    queryset = NodeTemplate.objects.order_by("-id")
    serializer_class = NodeTemplateSerializer
    filterset_class = NodeTemplateFilter

    def perform_update(self, serializer):
        # 暂时设计不能修改标准节点
        if serializer.validated_data.get("template_type") == NodeTemplateType.EmptyTemplate:
            pass
        else:
            serializer.save()


class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.order_by("-id")
    serializer_class = CategorySerializer
