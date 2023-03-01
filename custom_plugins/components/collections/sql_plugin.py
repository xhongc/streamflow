import subprocess

from sqlalchemy import create_engine

from custom_plugins.components.collections.base import ServiceMixin
from pipeline.component_framework.component import Component
from pipeline.core.flow.activity import Service, StaticIntervalGenerator


class SqlService(Service, ServiceMixin):
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
            db_type = inputs["db_type"]
            db_user = inputs["db_user"]
            db_pwd = inputs["db_pwd"]
            db_host = inputs["db_host"]
            db_port = inputs["db_port"]
            database = inputs["database"]
            sql_text = inputs["sql_text"]
        except KeyError as e:
            return False, f"参数缺失: {e}"
        if db_type == "mysql":
            engine = create_engine(f"mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{database}?charset=utf8",
                                   max_overflow=5)
        elif db_type == "postgresql":
            engine = create_engine(f'postgresql://{db_user}:{db_pwd}@{db_host}:{db_port}/{database}')
        else:
            return False, "Unknown database type"
        with engine.connect() as con:
            rs = con.execute(sql_text)
            _result_content = rs.fetchall()
        return True, _result_content

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


class SqlComponent(Component):
    name = "SqlComponent"
    code = "sql"
    bound_service = SqlService
