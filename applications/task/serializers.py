from rest_framework import serializers

from applications.flow.models import Process
from applications.task.models import Task, VarTable
from applications.task.services.clock_task import create_clock_check_task
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
        # todo 改为clock schedule 模式
        if validated_data["run_type"] == "time":
            create_clock_check_task(instance.id)
        elif validated_data["run_type"] == "cycle":
            when_start = string_to_datetime(instance.when_start)
            when_start = timezone.make_aware(when_start)
            # todo 改为clock schedule 模式
            celery_task_id = cycle_run_by_task_in_celery.apply_async(args=[instance.id], eta=when_start)
            instance.celery_task_id = celery_task_id
            instance.save()
        elif validated_data["run_type"] == "cron":
            create_cron_check_task(instance.id)
        self._data = {}
        return instance

    def update(self, instance, validated_data):
        instance = super(TaskSerializer, self).update(instance, validated_data)
        if validated_data["run_type"] == "time":
            pass
        elif validated_data["run_type"] == "cycle":
            pass
        elif validated_data["run_type"] == "cron":
            pass
        return instance


class ReadTaskSerializer(serializers.ModelSerializer):
    cron_time = serializers.CharField(allow_blank=True, allow_null=True)
    when_start = serializers.CharField(allow_blank=True, allow_null=True)
    process_id = serializers.CharField(source="process.id")
    process_name = serializers.CharField(source="process.name", read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class VarTableSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    processes = serializers.SerializerMethodField()
    total_var_num = serializers.SerializerMethodField()

    def get_processes(self, obj):
        return list(Process.objects.filter(var_table__icontains=obj.id).values_list("name", flat=True))

    def get_total_var_num(self, obj):
        return len(obj.data)

    class Meta:
        model = VarTable
        exclude = ("data",)


class RetrieveVarTableSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        new_data = []
        for each in obj.data:
            if each["type"] == "sensitive":
                each["value"] = "******"
            new_data.append(each)
        return new_data

    class Meta:
        model = VarTable

        fields = "__all__"


class PostVarTableSerializer(serializers.ModelSerializer):
    def validate_data(self, data):
        keys = [i["name"] for i in data]
        if len(set(keys)) != len(keys):
            raise serializers.ValidationError("变量名不能重复！")
        return data

    def update(self, instance, validated_data):
        db_data = instance.data
        db_data_dict = {i["name"]: i for i in db_data}
        for each in validated_data["data"]:
            if each["type"] == "sensitive":
                if each["value"] == "******":
                    each["value"] = db_data_dict[each["name"]]["value"]
        print(validated_data)
        instance = super(PostVarTableSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = VarTable
        fields = "__all__"


class ExecuteTaskSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(required=True)


class VarTableIDSSerializer(serializers.Serializer):
    ids = serializers.ListField(required=True)
