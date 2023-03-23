from django_celery_beat.models import PeriodicTask
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.task.filters import VarTableFilter, TaskFilter
from applications.task.models import Task, VarTable
from applications.task.serializers import TaskSerializer, VarTableSerializer, ExecuteTaskSerializer, \
    VarTableIDSSerializer, RetrieveVarTableSerializer, PostVarTableSerializer, ReadTaskSerializer, OperateTaskSerializer
from applications.task.services.base import delete_period_task, create_period_task
from applications.task.tasks import run_by_task
from component.drf.viewsets import GenericViewSet


class TaskViewSets(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    queryset = Task.objects.order_by("-id")
    filterset_class = TaskFilter

    def get_serializer_class(self):
        if self.action == "execute":
            return ExecuteTaskSerializer
        elif self.action == "retrieve":
            return ReadTaskSerializer
        elif self.action == "operate":
            return OperateTaskSerializer
        return TaskSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer_data = serializer.data
            task_names = [f"job_task.{i['id']}" for i in serializer_data]
            task_map = dict(PeriodicTask.objects.filter(name__in=task_names).values_list("name", "enabled"))
            for each in serializer_data:
                job_name = f"job_task.{each['id']}"
                each["enabled"] = task_map.get(job_name, False)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["POST"], detail=False)
    def execute(self, request, *args, **kwargs):
        validated_data = self.is_validated_data(request.data)
        task_id = validated_data["task_id"]
        is_ok, msg = run_by_task(task_id)
        if is_ok:
            return Response({})
        else:
            return self.failure_response(msg=msg)

    @action(methods=["POST"], detail=False)
    def operate(self, request, *args, **kwargs):
        validated_data = self.is_validated_data(request.data)
        operate = validated_data["operate"]
        task_id = validated_data["task_id"]

        if operate == "pause":
            delete_period_task(task_id)
        elif operate == "resume":
            delete_period_task(task_id)
            create_period_task(task_id)
        else:
            return self.failure_response()
        return self.success_response()

    def perform_destroy(self, instance):
        delete_period_task(instance.id)
        instance.delete()


class VarTableViewSets(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       GenericViewSet):
    queryset = VarTable.objects.order_by("-id")
    filterset_class = VarTableFilter

    def get_serializer_class(self):
        if self.action == "group":
            return VarTableIDSSerializer
        elif self.action == "retrieve":
            return RetrieveVarTableSerializer
        elif self.action == "list":
            return VarTableSerializer

        return PostVarTableSerializer

    @action(methods=["POST"], detail=False)
    def group(self, request, *args, **kwargs):
        validated_data = self.is_validated_data(request.data)
        ids = validated_data["ids"]
        var_list = list(VarTable.objects.filter(id__in=ids).values_list("data", flat=True))
        flat_var_list = sum(var_list, [])
        for each in flat_var_list:
            if each["type"] == "sensitive":
                each["value"] = "******"
        return Response(flat_var_list)
