import importlib

from custom_plugins.components.collections.base import ServiceMixin
from pipeline.component_framework.component import Component
from pipeline.core.flow import StaticIntervalGenerator
from pipeline.core.flow.activity import Service


class CustomService(Service, ServiceMixin):
    __need_schedule__ = True
    interval = StaticIntervalGenerator(0)

    def execute(self, data, parent_data):
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
        # 执行时
        _result_sign, _result_content = self.__execute(node_info)

        # 执行后保存日志
        self.after_service(data, _result_content, _result_sign, node_info)

        if _result_sign:
            self.finish_schedule()
            return True
        else:
            retry_count = data.get_one_of_outputs("retry_count", 0)
            if retry_count < fail_retry_count:
                data.set_outputs("retry_count", retry_count + 1)
                self.interval.interval = int(fail_offset)
                data.set_outputs("outputs", f"重试次数：{retry_count}")
                return True
            else:
                if is_skip_fail:
                    data.set_outputs("outputs", "忽略失败！")
                    self.finish_schedule()
                    return True
                return False

    def __execute(self, node_info):
        template_id = node_info["content"]
        base_dir = "applications.flow.plugin_code"
        unique_name = f"plugin_{template_id}"

        try:
            module = importlib.import_module(f"{base_dir}.{unique_name}")
        except ModuleNotFoundError:
            return False, "找不到执行脚本！"
        try:
            module.Task().execute()
        except Exception as e:
            return False, f"脚本执行失败{e}"
        return True, "success"

    def inputs_format(self):
        return []

    def outputs_format(self):
        return []


class CustomComponent(Component):
    name = "CustomComponent"
    code = "custom_plugin"
    bound_service = CustomService
