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
        "inputs_component": [{"key": "url", "type": "textarea", "label": "请求地址232："},
                             {"key": "method", "type": "select", "label": "请求类型：",
                              "choices": [{"label": "GET", "value": "get"}]},
                             {"key": "header", "type": "dict_map", "label": "Header"},
                             {"key": "body", "type": "textarea", "label": "Body："},
                             {"key": "timeout", "type": "number", "label": "超时时间："}],
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
        "inputs_component": [{"key": "title", "type": "text", "label": "标题"},
                             {"key": "msg", "type": "textarea", "label": "内容"},
                             {"key": "from_email", "type": "text", "label": "发件人邮箱"},
                             {"key": "to_emails", "type": "textarea", "label": "收件人列表"},
                             {"key": "smtp_host", "type": "text", "label": "smtp_host"},
                             {"key": "smtp_port", "type": "number", "label": "smtp_port"},
                             {"key": "from_email_pwd", "type": "text", "label": "发件人密码"},
                             {"key": "from_email_alias", "type": "text", "label": "发件人别名"}],
        "content": 0,
        "template_type": "0",
        "uuid": get_uuid()

    })
