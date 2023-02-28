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
             "title": "定时时间", "value": 0, "valueType": "Number"}
        ],
        "content": 0,
        "template_type": "0",
        "uuid": get_uuid()

    })

    NodeTemplate.objects.update_or_create(component_code="shell", defaults={
        "name": "Shell",
        "description": "执行shell命令",
        "inputs": {"command": "", "timeout": 15},
        "outputs": [{"key": "_result", "name": "执行结果", "reference": 1},
                    {"key": "_log_outputs", "name": "作业输出变量", "reference": 0}],
        "inputs_component": [
            {"id": "field6242437192692", "icon": "el-icon-edit-outline", "name": "NumberInput",
             "props": {"key": "timeout", "required": False, "enablePrint": True},
             "title": "超时时间", "value": 15, "valueType": "Number"},
            {"id": "field2556437102366", "icon": "el-icon-edit", "name": "TextareaInput",
             "props": {"key": "command", "required": False, "enablePrint": True}, "title": "shell命令",
             "value": "", "valueType": "String"}
        ],
        "content": 0,
        "template_type": "0",
        "uuid": get_uuid()

    })

    NodeTemplate.objects.update_or_create(component_code="sql", defaults={
        "name": "SQL",
        "description": "执行SQL语句",
        "inputs": {"db_port": "3306", "db_type": "mysql", "db_user": "root"},
        "outputs": [{"key": "_result", "name": "执行结果", "reference": 1},
                    {"key": "_log_outputs", "name": "作业输出变量", "reference": 0}],
        "inputs_component": [{"id": "field5872740859200", "icon": "el-icon-circle-check", "name": "SelectInput",
                              "props": {"key": "db_type",
                                        "options": [{"id": 1, "name": "mysql"}, {"id": 2, "name": "postgresql"}],
                                        "required": False, "expanding": False, "enablePrint": True,
                                        "placeholder": "选择数据库类型", "defaultValue": "mysql"}, "title": "数据库类型",
                              "value": "", "valueType": "String"},
                             {"id": "field6002840970782", "icon": "el-icon-edit", "name": "TextInput",
                              "props": {"key": "db_host", "required": False, "enablePrint": True,
                                        "defaultValue": ""}, "title": "数据库IP", "value": "", "valueType": "String"},
                             {"id": "field6543340925183", "icon": "el-icon-edit", "name": "TextInput",
                              "props": {"key": "db_user", "required": False, "enablePrint": True,
                                        "defaultValue": "root"}, "title": "数据库账户", "value": "", "valueType": "String"},
                             {"id": "field6718240954166", "icon": "el-icon-edit", "name": "TextInput",
                              "props": {"key": "db_pwd", "required": False, "enablePrint": True}, "title": "数据库密码",
                              "value": "", "valueType": "String"},
                             {"id": "field6002840970782", "icon": "el-icon-edit", "name": "TextInput",
                              "props": {"key": "db_port", "required": False, "enablePrint": True,
                                        "defaultValue": "3306"}, "title": "端口号", "value": "", "valueType": "String"},
                             {"id": "field5205640992111", "icon": "el-icon-edit", "name": "TextInput",
                              "props": {"key": "database", "required": False, "enablePrint": True}, "title": "数据库名",
                              "value": "", "valueType": "String"},
                             {"id": "field1579641008295", "icon": "el-icon-more-outline", "name": "TextareaInput",
                              "props": {"key": "sql_text", "required": False, "enablePrint": True}, "title": "执行SQL语句",
                              "value": "", "valueType": "String"}],
        "content": 0,
        "template_type": "0",
        "uuid": get_uuid()

    })
    NodeTemplate.objects.update_or_create(component_code="redis", defaults={
        "name": "Redis",
        "description": "执行Redis",
        "inputs": {"port": "6379", "db_index": 0,
                   "action_dict": [{"key": "", "value": ""}, {"key": "", "value": ""}, {"key": "", "value": ""}]},
        "outputs": [{"key": "_result", "name": "执行结果", "reference": 1},
                    {"key": "_log_outputs", "name": "作业输出变量", "reference": 0}],
        "inputs_component": [
            {"id": "field6002840970782", "icon": "el-icon-edit", "name": "TextInput",
             "props": {"key": "host", "required": False, "enablePrint": True,
                       "defaultValue": ""}, "title": "Host", "value": "", "valueType": "String"},
            {"id": "field6718240954166", "icon": "el-icon-edit", "name": "TextInput",
             "props": {"key": "password", "required": False, "enablePrint": True}, "title": "Redis密码",
             "value": "", "valueType": "String"},
            {"id": "field6002840970782", "icon": "el-icon-edit", "name": "TextInput",
             "props": {"key": "port", "required": False, "enablePrint": True,
                       "defaultValue": "6379"}, "title": "端口号", "value": "", "valueType": "String"},
            {"id": "field5202297758179", "icon": "el-icon-edit-outline", "name": "NumberInput",
             "props": {"key": "db_index", "required": False, "enablePrint": True}, "title": "数据库名",
             "value": 0, "valueType": "Number"},
            {"id": "field5872740859200", "icon": "el-icon-circle-check", "name": "SelectInput",
             "props": {"key": "action",
                       "options": [{"id": 1, "name": "get"}, {"id": 2, "name": "set"}],
                       "required": False, "expanding": False, "enablePrint": True,
                       "placeholder": "操作类型", "defaultValue": "mysql"}, "title": "操作类型",
             "value": "", "valueType": "String"},
            {"id": "field5186697624430", "icon": "iconfont icon-duoxuankuang", "name": "DictMap",
             "props": {"key": "action_dict", "required": False, "expanding": False, "enablePrint": True,
                       "defaultValue": [{"key": "", "value": ""}]}, "title": "操作", "value": [],
             "valueType": "Object"},
            {"id": "field5202297758179", "icon": "el-icon-edit-outline", "name": "NumberInput",
             "props": {"key": "expire", "required": False, "enablePrint": True}, "title": "过期时间",
             "value": 60, "valueType": "Number"}
        ],
        "content": 0,
        "template_type": "0",
        "uuid": get_uuid()

    })
