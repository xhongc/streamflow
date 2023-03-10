from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.task.filters import VarTableFilter, TaskFilter
from applications.task.models import Task, VarTable
from applications.task.serializers import TaskSerializer, VarTableSerializer, ExecuteTaskSerializer, \
    VarTableIDSSerializer, RetrieveVarTableSerializer, PostVarTableSerializer, ReadTaskSerializer
from applications.task.services.clock_task import delete_clock_task
from applications.task.services.cycle_task import delete_cycle_task
from applications.task.tasks import run_by_task
from applications.task.utils import delete_cron_task
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
        return TaskSerializer

    @action(methods=["POST"], detail=False)
    def execute(self, request, *args, **kwargs):
        validated_data = self.is_validated_data(request.data)
        task_id = validated_data["task_id"]
        is_ok, msg = run_by_task(task_id)
        if is_ok:
            return Response({})
        else:
            return self.failure_response(msg=msg)

    def perform_destroy(self, instance):
        if instance.run_type == "time":
            delete_clock_task(instance.id)
        elif instance.run_type == "cycle":
            delete_cycle_task(instance.id)
        elif instance.run_type == "cron":
            delete_cron_task(instance.id)
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
