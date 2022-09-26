from rest_framework.decorators import action
from rest_framework.response import Response

from applications.flow.utils import build_and_create_process
from applications.task.filters import VarTableFilter
from applications.task.models import Task, VarTable
from applications.task.serializers import TaskSerializer, VarTableSerializer, ExecuteTaskSerializer, \
    VarTableIDSSerializer
from applications.task.tasks import run_by_task
from applications.task.utils import CronTaskUtils
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
        is_ok = run_by_task(task_id)
        if is_ok:
            return Response({})
        else:
            # todo add error response
            return Response({})

    def perform_destroy(self, instance):
        from dj_flow.celery_app import app
        if instance.celery_task_id:
            app.control.revoke(instance.celery_task_id)
        CronTaskUtils.del_task(instance.id)
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
        return VarTableSerializer

    @action(methods=["POST"], detail=False)
    def group(self, request, *args, **kwargs):
        validated_data = self.is_validated_data(request.data)
        ids = validated_data["ids"]
        var_list = list(VarTable.objects.filter(id__in=ids).values_list("data", flat=True))
        flat_var_list = sum(var_list, [])
        return Response(flat_var_list)
