from bamboo_engine.api import logger


class ServiceMixin:

    def before_service(self, node_info):
        if node_info["show"] == 0:
            return False
        return True

    def after_service(self, data, _result_content, _result_sign, node_info):
        old_outputs = data.get_one_of_outputs("outputs", "")
        if old_outputs:
            old_outputs += "\n"
        new_outputs = old_outputs + str(_result_content)
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

    def __execute(self, *args, **kwargs):
        raise NotImplemented
