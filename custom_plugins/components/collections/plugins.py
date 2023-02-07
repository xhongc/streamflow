# -*- coding: utf-8 -*-
import importlib
import json
import time

import requests

from applications.utils.json_helper import try_json
from applications.utils.notify_way import send_email
from bamboo_engine.api import logger
from pipeline.component_framework.component import Component
from pipeline.core.flow.activity import Service, StaticIntervalGenerator


# to adapter window pc
# import eventlet
# requests = eventlet.import_patched('requests')
class ServiceMixin:
    def before_service(self, node_info):
        if node_info["show"] == 0:
            return True
        return None

    def after_service(self, data, _result_content, _result_sign, node_info):
        old_outputs = data.get_one_of_outputs("outputs", "")
        if old_outputs:
            old_outputs += "\n"
        new_outputs = old_outputs + _result_content
        data.set_outputs("outputs", new_outputs)
        self.set_result_outputs(node_info["outputs"], data, _result_sign, new_outputs)

    def set_result_outputs(self, outputs, data, _result_sign, _result_content):
        """简单设置返回值"""
        try:
            for index, output in enumerate(outputs):
                if index == 0:
                    if output["reference"] == 1:
                        data.set_outputs(output["key"], _result_sign)
                elif index == 1:
                    if output["reference"] == 1:
                        data.set_outputs(output["key"], _result_content)
        except Exception as e:
            logger.exception(e)


class HttpRequestService(Service, ServiceMixin):
    __need_schedule__ = True
    interval = StaticIntervalGenerator(0)

    def execute(self, data, parent_data):
        return True

    # 使用schedule模式重试
    def schedule(self, data, parent_data, callback_data=None):
        node_info = data.get_one_of_inputs("node_info")
        fail_retry_count = node_info["fail_retry_count"]
        fail_offset = node_info["fail_offset"]
        is_skip_fail = node_info["is_skip_fail"]

        # 执行前检查
        validate_before = self.before_service(node_info)
        if validate_before is not None:
            return validate_before
        # 执行时
        _result_sign, _result_content = self.__execute(node_info)

        # 执行后保存日志
        self.after_service(data, _result_content, _result_sign, node_info)

        if _result_sign:
            self.finish_schedule()
            return True
        else:
            if self.interval.count < fail_retry_count:
                self.interval.interval = fail_offset
                return True
            else:
                if is_skip_fail:
                    data.set_outputs("outputs", "忽略失败！")
                    return True
                return False

    def __execute(self, node_info):
        _result_sign = True
        _result_content = ""
        inputs = node_info["inputs"]
        try:
            time.sleep(100)
            headers = self.parse_headers(inputs["header"])
            inputs["body"] = try_json(inputs["body"])
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
            _result_content = str(e)
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


class CustomService(Service):
    def execute(self, data, parent_data):
        node_info = data.get_one_of_inputs("node_info")
        if node_info["show"] == 0:
            return True

        template_id = node_info["content"]
        base_dir = "applications.flow.plugin_code"
        unique_name = f"plugin_{template_id}"

        try:
            module = importlib.import_module(f"{base_dir}.{unique_name}")
        except ModuleNotFoundError:
            return False
        try:
            module.Task().execute()
        except Exception:
            return False
        return True

    def inputs_format(self):
        return []

    def outputs_format(self):
        return []


class SendEmailService(Service):
    def execute(self, data, parent_data):
        node_info = data.get_one_of_inputs("node_info")
        if node_info["show"] == 0:
            return True
        inputs = node_info["inputs"]
        to_emails = inputs["to_emails"]
        if isinstance(inputs["to_emails"], str):
            try:
                to_emails = json.loads(inputs["to_emails"])
            except Exception:
                return False
        is_ok = send_email(title=inputs["title"],
                           msg=inputs["msg"],
                           from_email=inputs["from_email"],
                           to_emails=to_emails,
                           smtp_host=inputs["smtp_host"],
                           smtp_port=inputs["smtp_port"],
                           from_email_pwd=inputs["from_email_pwd"],
                           from_email_alias=inputs["from_email_alias"]
                           )
        return is_ok

    def inputs_format(self):
        return []

    def outputs_format(self):
        return []


class HttpRequestComponent(Component):
    name = "HttpRequestComponent"
    code = "http_request"
    bound_service = HttpRequestService


class CustomComponent(Component):
    name = "CustomComponent"
    code = "custom_plugin"
    bound_service = CustomService


class SendEmailComponent(Component):
    name = "SendEmailComponent"
    code = "send_email"
    bound_service = SendEmailService
