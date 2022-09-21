from django.db.models import F
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.flow.models import Process
from applications.flow.utils import build_and_create_process
from applications.task.filters import VarTableFilter
from applications.task.models import Task, VarTable
from applications.task.serializers import TaskSerializer, VarTableSerializer, ExecuteTaskSerializer
from component.drf.viewsets import GenericViewSet
from rest_framework import mixins

from pipeline.eri.runtime import BambooDjangoRuntime
from bamboo_engine import api


class TaskViewSets(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    queryset = Task.objects.order_by("-id")

    def get_serializer_class(self):
        if self.action == "execute":
            return ExecuteTaskSerializer
        return TaskSerializer

    @action(methods=["POST"], detail=False)
    def execute(self, request, *args, **kwargs):
        validated_data = self.is_validated_data(request.data)
        task_id = validated_data["task_id"]
        pipeline = build_and_create_process(task_id)
        # 执行
        runtime = BambooDjangoRuntime()
        api.run_pipeline(runtime=runtime, pipeline=pipeline)

        return Response({})


class VarTableViewSets(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       GenericViewSet):
    queryset = VarTable.objects.order_by("-id")
    serializer_class = VarTableSerializer
    filterset_class = VarTableFilter
