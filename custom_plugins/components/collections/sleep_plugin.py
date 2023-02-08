import datetime

from custom_plugins.components.collections.base import ServiceMixin
from pipeline.core.flow.activity import Service, StaticIntervalGenerator
from pipeline.component_framework.component import Component


class SleepTimerService(Service, ServiceMixin):
    __need_schedule__ = True
    # 间隔一定是整型
    interval = StaticIntervalGenerator(0)

    def execute(self, data, parent_data):
        node_info = data.get_one_of_inputs("node_info")
        inputs = node_info["inputs"]
        timing = inputs.get("timing", 0)
        now = datetime.datetime.now()
        eta = now + datetime.timedelta(seconds=int(timing))
        data.outputs.timing_time = eta
        return True

    def schedule(self, data, parent_data, callback_data=None):
        node_info = data.get_one_of_inputs("node_info")
        fail_retry_count = node_info["fail_retry_count"]
        fail_offset = node_info["fail_offset"]
        is_skip_fail = node_info["is_skip_fail"]

        # 执行前检查，是否跳过，跳过状态为成功
        validate_before = self.before_service(node_info)
        if not validate_before:
            data.set_outputs("outputs", "跳过节点！")
            self.finish_schedule()
            return True

        timing_time = data.outputs.timing_time
        now = datetime.datetime.now()
        t_delta = timing_time - now
        if t_delta.total_seconds() < 1:
            self.finish_schedule()
            return True
        self.interval.interval = int(t_delta.total_seconds() - 0.5)
        return True


class SleepTimerComponent(Component):
    name = "SleepTimerComponent"
    code = "sleep_timer"
    bound_service = SleepTimerService
