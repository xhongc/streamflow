# -*- coding: utf-8 -*-
import importlib
import math

from applications.utils.notify_way import send_email
from bamboo_engine.api import logger
from bamboo_engine.builder import Var
from pipeline.core.flow.activity import Service, StaticIntervalGenerator
from pipeline.component_framework.component import Component
import json
import time
import requests


# to adapter window pc
# import eventlet
# requests = eventlet.import_patched('requests')


class HttpRequestService(Service):
    __need_schedule__ = False

    def execute(self, data, parent_data):
        _result_sign = True
        _result_content = ""
        node_info = data.get_one_of_inputs("node_info")

        try:
            inputs = data.get_one_of_inputs("inputs")

            headers = self.parse_headers(inputs["header"])
            inputs["body"] = json.loads(inputs["body"])
            req_data = [{"params": inputs["body"]}, {"json": inputs["body"]}][inputs["method"] != "get"]
            res = requests.request(inputs["method"], url=inputs["url"], headers=headers, timeout=inputs["timeout"],
                                   **req_data)
            print("执行了", res)
            data.outputs.outputs = res.content[:250]
            _result_content = res.content
            time.sleep(2)
            if 200 <= res.status_code < 300:
                _result_sign = True
            else:
                _result_sign = False

        except Exception as e:
            data.outputs.outputs = str(e)
            _result_sign = False
            _result_content = str(e)
        finally:
            self.parse_result(node_info["outputs"], data, _result_sign, _result_content)
            return _result_sign

    def parse_result(self, outputs, data, _result_sign, _result_content):
        try:
            for index, output in enumerate(outputs):
                if index == 0:
                    if output["reference"] == 1:
                        data.outputs[output["key"]] = _result_sign
                elif index == 1:
                    if output["reference"] == 1:
                        data.outputs[output["key"]] = _result_content
        except Exception as e:
            logger.exception(e)

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
