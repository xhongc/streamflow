import requests

from applications.utils.json_helper import try_json
from custom_plugins.components.collections.base import ServiceMixin
from pipeline.component_framework.component import Component
from pipeline.core.flow.activity import Service, StaticIntervalGenerator


class HttpRequestService(Service, ServiceMixin):
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
        """
        return Boolean, String
        """
        _result_sign = True
        _result_content = ""
        inputs = node_info["inputs"]
        try:
            headers = try_json(inputs["header"].replace("\r", "").replace("\n", ""))
        except Exception as e:
            _result_sign = False
            _result_content = "headers解析错误！" + str(e)
            return _result_sign, _result_content

        try:
            inputs["body"] = try_json(inputs["body"].replace("\r", "").replace("\n", ""))
        except Exception as e:
            _result_sign = False
            _result_content = "body解析错误！" + str(e)
            return _result_sign, _result_content
        try:
            req_data = [{"params": inputs["body"]}, {"json": inputs["body"]}][inputs["method"] != "get"]
            res = requests.request(inputs["method"], url=inputs["url"], headers=headers, timeout=int(inputs["timeout"]),
                                   verify=False,
                                   **req_data)
            _result_content = res.text
            if 200 <= res.status_code < 300:
                _result_sign = True
            else:
                _result_sign = False

        except Exception as e:
            _result_sign = False
            _result_content = "request请求失败！"+ str(e)
        finally:
            return _result_sign, _result_content

    def parse_headers(self, headers):
        return {header["key"]: header["value"] for header in headers if header["key"]}

    def inputs_format(self):
        return [
            Service.InputItem(name="输入参数", key="inputs", type="dict", required=True),
            Service.InputItem(name="节点信息", key="node_info", type="dict", required=True),
        ]

    def outputs_format(self):
        return [
            Service.OutputItem(name="输出参数", key="outputs", type="dict", required=True)
        ]


class HttpRequestComponent(Component):
    name = "HttpRequestComponent"
    code = "http_request"
    bound_service = HttpRequestService
