<template>
    <div id="singleJob" v-bkloading="{ isLoading: formLoading, zIndex: 10 }">
        <div class="wrapper">
            <bk-container :col="12" :gutter="4">
                <bk-row>
                    <bk-col :span="8">
                        <div class="job-content content">
                            <p class="job-title">自定义节点</p>
                            <bk-form ref="form" :label-width="144" :model="form">
                                <bk-form-item label="节点名称:" :required="true" :error-display-type="'normal'"
                                    :property="'node_name'">
                                    <bk-input v-model="form.name" type="text" style="width: 350px;margin-right: 9px;"
                                        :disabled="disabled"></bk-input>
                                </bk-form-item>
                                <bk-form-item label="运行标志:" :required="true" :error-display-type="'normal'"
                                    :property="'run_mark'">
                                    <bk-radio-group v-model="form.run_mark">
                                        <bk-radio :value="item.value" v-for="(item, index) in reviewList" :key="index"
                                            style="margin-right: 24px;" :disabled="disabled">
                                            {{ item.label }}
                                        </bk-radio>
                                    </bk-radio-group>
                                </bk-form-item>
                                <bk-form-item label="描述:">
                                    <bk-input v-model="form.description" type="textarea"
                                        style="width: 350px;margin-right: 9px;" :disabled="disabled"
                                        :min="0"></bk-input>
                                </bk-form-item>
                                <bk-form-item label="失败重试次数:" :required="true" :error-display-type="'normal'"
                                    :property="'fail_retry_count'">
                                    <bk-input v-model="form.fail_retry_count" type="number"
                                        style="width: 350px;margin-right: 9px;" :disabled="disabled"
                                        :min="0"></bk-input>
                                </bk-form-item>
                                <bk-form-item label="失败重试间隔:">
                                    <bk-compose-form-item>
                                        <bk-input v-model="form.fail_offset" type="number"
                                            style="width: 139px;margin-right: 9px;" :disabled="disabled"
                                            :min="0"></bk-input>
                                        <bk-select :clearable="true"
                                            style="background-color: #fff;width: 138px;margin-right: 14px;"
                                            v-model="form.fail_offset_unit" placeholder="请选择" :disabled="disabled">
                                            <bk-option v-for="(item, index) in timeTypeList" :key="index"
                                                :id="item.value" :name="item.label">
                                            </bk-option>
                                        </bk-select>
                                        <span>产生重试</span>
                                    </bk-compose-form-item>
                                </bk-form-item>
                                <bk-form-item label="忽略失败:">
                                    <bk-switcher v-model="form.is_skip_fail" :disabled="disabled"></bk-switcher>
                                </bk-form-item>
                                <bk-form-item label="超时告警:">
                                    <bk-switcher v-model="form.is_timeout_alarm" :disabled="disabled"></bk-switcher>
                                </bk-form-item>
                                <bk-divider
                                    style="width: 100%;position: relative;right: 20px;border-color: #dcdee5;"></bk-divider>
                                <p class="job-title">输入参数</p>
                                <bk-form-item label="表单组件: ">
                                    <editor :height="'200px'" ref="editor1"
                                        :codes="JSON.stringify(form.inputs_component)" :read-only="false"
                                        :language="'shell'"></editor>
                                </bk-form-item>
                                <bk-form-item label="默认值: ">
                                    <editor :height="'200px'" ref="editor2" :codes="JSON.stringify(form.inputs)"
                                        :read-only="false" :language="'shell'"></editor>
                                </bk-form-item>
                                <bk-divider
                                    style="width: 100%;position: relative;right: 20px;border-color: #dcdee5;"></bk-divider>
                                <div class="box">
                                    <p class="job-title" style="margin-bottom: 10px">输出参数</p>
                                    <bk-form>
                                        <bk-table :data="form.outputs">
                                            <bk-table-column label="名称" prop="name" :show-overflow-tooltip="true">
                                                <template slot-scope="props">
                                                    <bk-input v-model="props.row.name"></bk-input>
                                                </template>
                                            </bk-table-column>
                                            <bk-table-column label="KEY" prop="key" :show-overflow-tooltip="true">
                                                <template slot-scope="props">
                                                    <bk-input v-model="props.row.key"></bk-input>
                                                </template>
                                            </bk-table-column>
                                            <bk-table-column label="引用" prop="reference">
                                                <template slot-scope="props">
                                                    <bk-checkbox :disabled="disabled" v-model="props.row.reference" :true-value="1"
                                                        :false-value="0"></bk-checkbox>
                                                </template>
                                            </bk-table-column>
                                        </bk-table>
                                    </bk-form>
                                </div>
                            </bk-form>
                        </div>
                    </bk-col>
                    <bk-col :span="4">
                        <div class="job-content">
                            <p class="job-title">帮助文档：</p>
                            <div>支持的表单类型：</div>
                            <div>
                                <div>文本类型：</div>
                                <div>{
                                    "key": "url",
                                    "type": "text",
                                    "label": "请求地址"
                                    }</div>
                            </div>
                            <div>
                                <div>长文本类型：</div>
                                <div>{
                                    "key": "url",
                                    "type": "textarea",
                                    "label": "请求地址"
                                    }</div>
                            </div>
                            <div>
                                <div>下拉框类型：</div>
                                <div>{
                                    "key": "method",
                                    "type": "select",
                                    "label": "请求类型：",
                                    "choices": [
                                    {
                                    "label": "GET",
                                    "value": "get"
                                    }
                                    ]
                                    }</div>
                            </div>
                            <div>
                                <div>字典类型：</div>
                                <div>{
                                    "key": "header",
                                    "type": "dict_map",
                                    "label": "Header"
                                    }</div>
                            </div>
                            <div>
                                <div>数字类型：</div>
                                <div>{
                                    "key": "timeout",
                                    "type": "number",
                                    "label": "超时时间："
                                    }</div>
                            </div>
                        </div>
                    </bk-col>
                </bk-row>
            </bk-container>
        </div>
        <bk-sideslider :is-show.sync="customSettings.isShow" :quick-close="true" :width="536" :title="'预览'">
            <node-info slot="content" :node-data="nodeData" :is-show-btn="false"></node-info>
        </bk-sideslider>
        <template v-if="overScreenFlag">
            <div style="height: 72px;"></div>
            <div class="footer">
                <bk-button theme="primary" style="margin: 0 10px 0 140px;" @click="handleConfim">确定</bk-button>
                <bk-button @click="handleCancel" style="margin-right: 10px;">取消</bk-button>
                <bk-button @click="handlePreView">预览</bk-button>
            </div>
        </template>
    </div>
</template>

<script>
    import {
        deepClone
    } from '../../common/util.js'
    import editor from '@/components/monacoEditor'
    import nodeInfo from '../job_flow_mgmt/single_job_flow/nodeInfo'

    export default {
        components: {
            editor,
            nodeInfo // 节点信息
        },
        data() {
            return {
                customSettings: {
                    isShow: false,
                    title: '更多参数配置'
                },
                headerHolder: '请输入请求头, 例如： {"Content-type": "application/json"}',
                paramsHolder: '请输入填写请求体, 例如： {"name": "abc"}',
                checkFlag: true,
                overScreenFlag: false, // 是否超出一屏标志位
                pageKey: 0,
                agnetListShow: true,
                accountListShow: true,
                formLoading: false,
                disabled: false,
                timeTypeList: [
                    { // 执行时长告警时间类型下拉列表
                        value: 'hours',
                        label: '时'
                    },
                    {
                        value: 'minutes',
                        label: '分'

                    },
                    {
                        value: 'seconds',
                        label: '秒'
                    }
                ],
                reviewList: [{ // 执行前人工复核单选列表
                    label: '正常运行',
                    value: 1
                }, {
                    label: '禁止运行',
                    value: 0
                }],
                scriptMap: {
                    1: 'shell',
                    2: 'bat',
                    3: 'perl',
                    4: 'python',
                    5: 'powershell',
                    8: 'sql',
                    9: 'json'
                },
                sqlTypeList: [{
                    key: 'MySQL',
                    label: 'MySQL'
                }, {
                    key: 'Oracle',
                    label: 'Oracle'
                }],
                httpReqTypeList: [{
                    key: 'get',
                    label: 'GET'
                }, {
                    key: 'post',
                    label: 'POST'
                }, {
                    key: 'put',
                    label: 'PUT'
                }, {
                    key: 'delete',
                    label: 'DELETE'
                }], // HTTP请求方式
                scriptTypeList: [
                    {
                        key: 1,
                        label: 'Shell(Linux)',
                        value: 'shell-linux-1'
                    },
                    {
                        key: 2,
                        label: 'Bat(Windows)',
                        value: 'bat-win-2'
                    },
                    {
                        key: 3,
                        label: 'perl',
                        value: 'perl-3'
                    },
                    {
                        key: 4,
                        label: 'Python(Linux)',
                        value: 'python-linux-4'
                    },
                    {
                        key: 5,
                        label: 'PowerShell(Windows)',
                        value: 'powershell-win-5'
                    },
                    {
                        key: 6,
                        label: 'HTTP',
                        value: 'HTTP'
                    }
                    // {
                    //     key: 7,
                    //     label: 'Java',
                    //     value: 'Java'
                    // },
                    // {
                    //     key: 8,
                    //     label: 'SQL',
                    //     value: 'SQL'
                    // }
                ], // 脚本类型下拉列表
                accountList: [], // 执行账号下拉列表
                runSysList: [], // 跑批系统下拉列表
                agentList: [], // agent下拉列表
                form: {
                    name: '', // 作业名称
                    description: '', // 作业描述
                    category: '', // 跑批系统
                    station: '', // agnet
                    os: '', // 系统类型
                    exit_code: '', // 作业退出码
                    data: {
                        account: '', // 执行账号
                        script_type: 1, // 脚本类型
                        script_content: '', // 脚本内容
                        script_timeout: 8600, // 超时时间
                        request_type: '', // http请求，请求方式
                        request_url: '', // http请求，请求url
                        headers: '', // http请求，请求头
                        params: '' // http请求，请求体
                    }
                },
                cloneForm: {},
                otherRules: {
                    'data.script_content': [{
                        required: true,
                        message: '脚本内容不能为空',
                        trigger: 'blur'
                    }]
                },
                baseRules: {
                    name: [{
                        required: true,
                        message: '作业名称不能为空',
                        trigger: 'blur'
                    }],
                    description: [{
                        required: true,
                        message: '作业描述不能为空',
                        trigger: 'blur'
                    }],
                    category: [{
                        required: true,
                        message: '跑批系统不能为空',
                        trigger: 'change'
                    }],
                    station: [{
                        required: true,
                        message: 'agent不能为空',
                        trigger: 'change'
                    }],
                    'data.account': [{
                        required: true,
                        message: '执行账号不能为空',
                        trigger: 'change'
                    }],
                    'data.script_type': [{
                        required: true,
                        message: '脚本类型不能为空',
                        trigger: 'change'
                    }],
                    'data.script_timeout': [{
                        required: true,
                        message: '超时时间不能为空',
                        trigger: 'blur'
                    }]
                }
            }
        },
        computed: {
            rules() {
                const rules = {}
                Object.assign(rules, this.baseRules, this.otherRules)
                return rules
            },
            nodeData() {
                return {
                    'data': this.cloneForm
                }
            }
        },
        watch: {
        },
        created() {
            if (this.$route.query.type === 'update' || this.$route.query.type === 'clone') {
                this.initJobData()
            } else {
                this.pageKey += 1
            }
        },
        mounted() {
            const _this = this
            const elementResizeDetectorMaker = require('element-resize-detector') // 导入element-resize-detector
            // 创建实例
            const erd = elementResizeDetectorMaker()
            // 监听id为singleJob的元素 大小变化
            this.$nextTick(() => {
                erd.listenTo(document.getElementById('singleJob'), function(element) {
                    if ((element.offsetHeight - (document.documentElement.clientHeight - 52)) > 0) {
                        _this.overScreenFlag = true
                    } else {
                        _this.overScreenFlag = false
                    }
                })
            })
        },
        beforeRouteLeave(to, from, next) {
            if (this.checkFlag) {
                this.$bkInfo({
                    type: 'warning',
                    width: 480,
                    title: '该操作会导致您的编辑无保存, 确认吗？',
                    confirmLoading: false,
                    confirmFn: async() => {
                        next()
                    }
                })
            } else {
                next()
            }
        },
        methods: {
            // 处理新建作业
            handleAddJob() {
                this.formLoading = true
                const params = deepClone(this.form)
                console.log(this.form)
                this.$api.content.create(params).then(res => {
                    if (res.result) {
                        this.checkFlag = false
                        this.$cwMessage('创建成功！', 'success')
                        this.$router.push({
                            path: '/joblist'
                        })
                    } else {
                        this.$cwMessage(res.message, 'error')
                    }
                    this.formLoading = false
                })
            },
            // 处理修改作业
            handleUpdateJob() {
                this.formLoading = true
                const id = parseInt(this.$route.query.job_id)
                const params = deepClone(this.form)
                params['inputs_component'] = this.$refs.editor1.monacoEditor.getValue()
                params['inputs'] = this.$refs.editor2.monacoEditor.getValue()
                this.$api.content.update(id, params).then(res => {
                    if (res.result) {
                        this.checkFlag = false
                        this.$cwMessage('更新成功！', 'success')
                        this.$router.push({
                            path: '/joblist'
                        })
                    } else {
                        this.$cwMessage(res.message, 'error')
                    }
                    this.formLoading = false
                })
            },
            // 处理克隆作业
            handleCloneJob() {
                this.formLoading = true
                const params = deepClone(this.form)
                this.$api.content.clone(params).then(res => {
                    if (res.result) {
                        this.$cwMessage('克隆成功！', 'success')
                        this.$router.push({
                            path: '/joblist'
                        })
                    } else {
                        this.$cwMessage(res.message, 'error')
                    }
                    this.formLoading = false
                })
            },
            // 处理确定
            handleConfim() {
                this.$refs.form.validate().then(validator => {
                    if (this.$route.query.type === 'add') {
                        this.handleAddJob()
                    } else if (this.$route.query.type === 'update') {
                        this.handleUpdateJob()
                    } else if (this.$route.query.type === 'clone') {
                        this.handleCloneJob()
                    }
                }).catch(e => {
                    // this.$cwMessage('输入有误，请检查您的输入！', 'warning')
                    // this.overScreen()
                })
            },
            // 处理取消
            handleCancel() {
                this.$router.go(-1)
            },
            // 处理预览
            handlePreView() {
                this.cloneForm = deepClone(this.form)
                this.cloneForm['inputs_component'] = this.$refs.editor1.monacoEditor.getValue()
                this.cloneForm['inputs'] = this.$refs.editor2.monacoEditor.getValue()
                this.cloneForm['outputs'] = JSON.stringify(this.form.outputs)
                this.customSettings.isShow = true
            },
            // 设置默认编辑器
            setDefaultEditor(e, str1, str2) {
                this.$refs.editor1.changeModel(this.scriptMap[e], str1)
                this.$refs.editor2.changeModel(this.scriptMap[e], str2)
            },
            // 当前为修改，初始化作业
            initJobData() {
                this.formLoading = true
                const id = parseInt(this.$route.query.job_id)
                this.$api.content.retrieve(id).then(res => {
                    if (res.result) {
                        this.form = res.data
                        this.setDefaultEditor(1, JSON.stringify(this.form.inputs_component), JSON.stringify(this.form.inputs))
                    } else {
                        this.$cwMessage(res.message, 'error')
                    }
                    this.formLoading = false
                })
            }
        }
    }
</script>

<style lang="scss" scoped>
#singleJob {
    padding-top: 20px;
    // height: 100%;
    // overflow: auto;
    position: relative;

    .content {
        height: 100%;
        width: 700px;
        padding-left: 20px;

        .custom-textarea {
            /deep/ textarea {
                padding: 20px;
                background-color: rgb(49, 50, 56) !important;
                color: #C4C6CC !important;
            }
        }

        .os-button {
            display: inline-block;
            padding: 0 5px 0 5px;
            height: 32px;
            line-height: 32px;
            background-color: #fff;
            font-size: 12px;
            color: #63656E;
            border: 1px solid #C4C6CC;
        }
    }

    .footer {
        position: fixed;
        width: 100%;
        bottom: 0px;
        height: 52px;
        line-height: 52px;
        background: #FFFFFF;
        box-shadow: 0px -2px 6px 0px rgba(0, 0, 0, 0.1);
        font-size: 0;
        z-index: 999;
    }
}

.demo-grid {
    .wrapper {
        overflow: hidden;
        border: 1px solid #ddd;
        border-radius: 2px;
        padding: 20px 0;
    }

    .content {
        background-color: #e1ecff;
        height: 100%;
        line-height: 60px;
        border-radius: 2px;
        font-size: 12px;
    }

    .bk-grid-row {
        text-align: center;
    }

    .bk-grid-row + .bk-grid-row {
        margin-top: 30px;
    }

    .flex {
        .bk-grid-row + .bk-grid-row {
            margin-top: 10px;
        }
    }
}

.job-title {
    width: 160px;
    height: 21px;
    font-size: 14px;
    font-weight: bold;
    color: #313238;
    line-height: 21px;
}

.job-content {
    background: #ffffff;
    padding: 20px;
}
</style>
