import json

import redis

from applications.utils.json_helper import try_json
from custom_plugins.components.collections.base import ServiceMixin
from pipeline.component_framework.component import Component
from pipeline.core.flow.activity import Service, StaticIntervalGenerator


class RedisService(Service, ServiceMixin):
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
            if retry_count < fail_retry_count + 1:
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
            host = inputs["host"]
            password = inputs.get("password", "")
            port = inputs["port"]
            action = inputs["action"]
            action_dict = inputs["action_dict"]
            expire = int(inputs["expire"])
            db_index = int(inputs["db_index"])
            assert 0 <= db_index <= 16
        except KeyError as e:
            return False, f"Params missing:{e}"
        except Exception as e:
            return False, f"{e}"

        try:
            pool = redis.ConnectionPool(host=host, password=password, port=port, db=db_index)
            r = redis.Redis(connection_pool=pool)
            action_dict = {header["key"]: header["value"] for header in action_dict if header["key"]}
            if action == "get":
                result = {}
                for key, value in action_dict.items():
                    if not key:
                        continue
                    result["key"] = r.get(key) or value
                _result_content = json.dumps(result)
            elif action == "set":
                try:
                    for key, value in action_dict.items():
                        if not key:
                            continue
                        r.set(key, value, ex=expire)
                    _result_content = "success set value"
                except Exception as e:
                    _result_sign = False
                    _result_content = f"Invalid: {e}"
            else:
                _result_sign = False
                _result_content = "invalid action"
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


class RedisComponent(Component):
    name = "RedisComponent"
    code = "redis"
    bound_service = RedisService
