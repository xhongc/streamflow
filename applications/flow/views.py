import random
from datetime import datetime

from django.http import JsonResponse
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.flow.filters import NodeTemplateFilter, ProcessRunFilter, SubProcessRunFilter
from applications.flow.models import Process, ProcessRun, NodeTemplate, SubProcessRun, Category
from applications.flow.serializers import ProcessViewSetsSerializer, ListProcessViewSetsSerializer, \
    RetrieveProcessViewSetsSerializer, ExecuteProcessSerializer, ListProcessRunViewSetsSerializer, \
    RetrieveProcessRunViewSetsSerializer, NodeTemplateSerializer, ListSubProcessRunViewSetsSerializer, \
    RetrieveSubProcessRunViewSetsSerializer, CategorySerializer
from applications.task.models import VarTable
from bamboo_engine import api
from bamboo_engine.builder import *
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


class TestViewSets(GenericViewSet):
    def list(self, request, *args, **kwargs):
        random_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        sign = random.choice(random_list)
        if sign:
            return Response({"now": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "data": request.query_params})
        else:
            raise Exception("随机抛出异常")


class NodeTemplateViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):
    queryset = NodeTemplate.objects.order_by("-id")
    serializer_class = NodeTemplateSerializer
    filterset_class = NodeTemplateFilter


class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.order_by("-id")
    serializer_class = CategorySerializer


# Create your views here.
def flow(request):
    # 使用 builder 构造出流程描述结构
    start = EmptyStartEvent()
    act = ServiceActivity(component_code="http_request")

    act2 = ServiceActivity(component_code="http_request")
    act2.component.inputs.n = Var(type=Var.PLAIN, value=50)

    act3 = ServiceActivity(component_code="http_request")
    act3.component.inputs.n = Var(type=Var.PLAIN, value=5)

    act4 = ServiceActivity(component_code="http_request")
    act5 = ServiceActivity(component_code="http_request")
    eg = ExclusiveGateway(
        conditions={
            0: '${exe_res} >= 0',
            1: '${exe_res} < 0'
        },
        name='act_2 or act_3'
    )
    pg = ParallelGateway()
    cg = ConvergeGateway()

    end = EmptyEndEvent()

    start.extend(act).extend(eg).connect(act2, act3).to(act2).extend(act4).extend(act5).to(eg).converge(end)
    # 全局变量
    pipeline_data = Data()
    pipeline_data.inputs['${exe_res}'] = NodeOutput(type=Var.PLAIN, source_act=act.id, source_key='exe_res')

    pipeline = builder.build_tree(start, data=pipeline_data)
    print(pipeline)
    # 执行流程对象
    runtime = BambooDjangoRuntime()

    api.run_pipeline(runtime=runtime, pipeline=pipeline)

    result = api.get_pipeline_states(runtime=runtime, root_id=pipeline["id"])

    result_output = api.get_execution_data_outputs(runtime, act.id).data
    # api.pause_pipeline(runtime=runtime, pipeline_id=pipeline["id"])
    return JsonResponse({})
