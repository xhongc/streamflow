from rest_framework import serializers

from applications.task.models import Task, VarTable
from applications.task.tasks import run_by_task_in_celery, cycle_run_by_task_in_celery
from applications.task.utils import create_cron_check_task
from applications.utils.timer import string_to_datetime
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    cron_time = serializers.CharField(allow_blank=True, allow_null=True)
    when_start = serializers.CharField(allow_blank=True, allow_null=True)
    process_id = serializers.CharField(write_only=True)
    process_name = serializers.CharField(source="process.name", read_only=True)

    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        instance = super(TaskSerializer, self).create(validated_data)
        if validated_data["run_type"] == "time":
            when_start = string_to_datetime(instance.when_start)
            when_start = timezone.make_aware(when_start)
            celery_task_id = run_by_task_in_celery.apply_async(args=[instance.id], eta=when_start)
            instance.celery_task_id = celery_task_id
            instance.save()
        elif validated_data["run_type"] == "cycle":
            when_start = string_to_datetime(instance.when_start)
            when_start = timezone.make_aware(when_start)

            celery_task_id = cycle_run_by_task_in_celery.apply_async(args=[instance.id], eta=when_start)
            instance.celery_task_id = celery_task_id
            instance.save()
        elif validated_data["run_type"] == "cron":
            create_cron_check_task(instance.id)
        self._data = {}
        return instance


class VarTableSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    processes = serializers.SerializerMethodField()
    total_var_num = serializers.SerializerMethodField()

    def get_processes(self, obj):
        return []

    def get_total_var_num(self, obj):
        return len(obj.data)

    class Meta:
        model = VarTable

        fields = "__all__"


class ExecuteTaskSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(required=True)


class VarTableIDSSerializer(serializers.Serializer):
    ids = serializers.ListField(required=True)
