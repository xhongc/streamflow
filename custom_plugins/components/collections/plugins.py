# -*- coding: utf-8 -*-
import math

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


class HttpRequestComponent(Component):
    name = "HttpRequestComponent"
    code = "http_request"
    bound_service = HttpRequestService
