from rest_framework import serializers

from applications.task.models import Task, VarTable


class TaskSerializer(serializers.ModelSerializer):
    cron_time = serializers.CharField(allow_blank=True, allow_null=True)
    when_start = serializers.CharField(allow_blank=True, allow_null=True)
    process_id = serializers.CharField(write_only=True)
    process_name = serializers.CharField(source="process.name")

    class Meta:
        model = Task
        fields = "__all__"


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
