from applications.flow.models import NodeTemplate
from applications.utils.uuid_helper import get_uuid


def init_node_template(sender, **kwargs):
    NodeTemplate.objects.update_or_create(component_code="http_request", defaults={
        "name": "HTTP请求",
        "description": "HTTP请求",
        "inputs": {"url": "", "body": "{}", "header": [{"key": "test", "value": "value"}], "method": "get",
                   "timeout": 60, "check_point": {"key": "", "values": "", "condition": ""}},
        "outputs": [{"key": "_result", "name": "执行结果", "reference": 1},
                    {"key": "_log_outputs", "name": "作业输出变量", "reference": 0}],
        "inputs_component": [{"id": "field9826197484136", "icon": "el-icon-more-outline", "name": "TextareaInput",
                              "props": {"key": "url", "required": False, "enablePrint": True, "defaultValue": ""},
                              "title": "请求地址", "value": "", "valueType": "String"},
                             {"id": "field3606697510269", "icon": "el-icon-circle-check", "name": "SelectInput",
                              "props": {"key": "method",
                                        "options": [{"id": 1, "name": "get"}, {"id": 2, "name": "post"}],
                                        "required": False, "expanding": False, "enablePrint": True,
                                        "defaultValue": "get"}, "title": "请求类型", "value": "", "valueType": "String"},
                             {"id": "field5186697624430", "icon": "iconfont icon-duoxuankuang", "name": "DictMap",
                              "props": {"key": "header", "required": False, "expanding": False, "enablePrint": True,
                                        "defaultValue": [{"key": "", "value": ""}]}, "title": "Header", "value": [],
                              "valueType": "Object"},
                             {"id": "field5535297741066", "icon": "el-icon-more-outline", "name": "TextareaInput",
                              "props": {"key": "body", "required": False, "enablePrint": True}, "title": "Body",
                              "value": "", "valueType": "String"},
                             {"id": "field5202297758179", "icon": "el-icon-edit-outline", "name": "NumberInput",
                              "props": {"key": "timeout", "required": False, "enablePrint": True}, "title": "超时时间",
                              "value": "", "valueType": "Number"}],
        "content": 0,
        "template_type": "0",
        "uuid": get_uuid()
    })
    NodeTemplate.objects.update_or_create(component_code="send_email", defaults={
        "name": "发送邮件",
        "description": "发送邮件",
        "inputs": {"msg": "", "title": "", "smtp_host": "", "smtp_port": 0, "to_emails": [], "from_email": "",
                   "from_email_pwd": "", "from_email_alias": ""},
        "outputs": [{"key": "_result", "name": "执行结果", "reference": 1},
                    {"key": "_log_outputs", "name": "作业输出变量", "reference": 0}],
        "inputs_component": [{"id": "field7584737052650", "icon": "el-icon-edit", "name": "TextInput",
                              "props": {"key": "title", "required": False, "enablePrint": True}, "title": "标题",
                              "value": "", "valueType": "String"},
                             {"id": "field3632637081695", "icon": "el-icon-more-outline", "name": "TextareaInput",
                              "props": {"key": "msg", "required": False, "enablePrint": True}, "title": "内容",
                              "value": "", "valueType": "String"},
                             {"id": "field2556437102366", "icon": "el-icon-edit", "name": "TextInput",
                              "props": {"key": "from_email", "required": False, "enablePrint": True}, "title": "发件人邮箱",
                              "value": "", "valueType": "String"},
                             {"id": "field6568137128942", "icon": "el-icon-more-outline", "name": "TextareaInput",
                              "props": {"key": "to_emails", "required": False, "enablePrint": True}, "title": "收件人列表",
                              "value": "", "valueType": "String"},
                             {"id": "field4221037163324", "icon": "el-icon-edit", "name": "TextInput",
                              "props": {"key": "smtp_host", "required": False, "enablePrint": True},
                              "title": "smtp_host", "value": "", "valueType": "String"},
                             {"id": "field6242437192692", "icon": "el-icon-edit-outline", "name": "NumberInput",
                              "props": {"key": "smtp_port", "required": False, "enablePrint": True},
                              "title": "smtp_port", "value": "", "valueType": "Number"},
                             {"id": "field1961537219657", "icon": "el-icon-edit", "name": "TextInput",
                              "props": {"key": "from_email_pwd", "required": False, "enablePrint": True},
                              "title": "发件人密码", "value": "", "valueType": "String"},
                             {"id": "field7239237239690", "icon": "el-icon-edit", "name": "TextInput",
                              "props": {"key": "from_email_alias", "required": False, "enablePrint": True},
                              "title": "发件人别名", "value": "", "valueType": "String"}],
        "content": 0,
        "template_type": "0",
        "uuid": get_uuid()

    })
    NodeTemplate.objects.update_or_create(component_code="sleep_timer", defaults={
        "name": "定时",
        "description": "定时",
        "inputs": {"timing": 0},
        "outputs": [{"key": "_result", "name": "执行结果", "reference": 1},
                    {"key": "_log_outputs", "name": "作业输出变量", "reference": 0}],
        "inputs_component": [
                             {"id": "field6242437192692", "icon": "el-icon-edit-outline", "name": "NumberInput",
                              "props": {"key": "timing", "required": False, "enablePrint": True},
                              "title": "定时时间", "value": "", "valueType": "Number"}
                             ],
        "content": 0,
        "template_type": "0",
        "uuid": get_uuid()

    })
