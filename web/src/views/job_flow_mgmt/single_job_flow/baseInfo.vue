<template>
    <div id="baseInfo" v-bkloading="{ isLoading: baseInfoLoading, zIndex: 999999 }">
        <bk-form ref="form" :label-width="110" :rules="rules" :model="form">
            <bk-form-item label="作业流名称" :error-display-type="'normal'" :required="true" :property="'jobFlowName'">
                <bk-input placeholder="请输入作业流名称" v-model="form.jobFlowName" :disabled="disabled"></bk-input>
            </bk-form-item>
            <bk-form-item label="作业流描述">
                <bk-input placeholder="请输入作业流描述" v-model="form.jobFlowDescribe" :disabled="disabled"></bk-input>
            </bk-form-item>
            <bk-form-item label="分类">
                <bk-tag-input
                    v-model="form.category"
                    :trigger="'focus'"
                    :allow-next-focus="false"
                    :list="categoryList"
                    :allow-create="true"
                    :allow-auto-match="true"
                    :has-delete-icon="true"
                    :disabled="disabled">
                </bk-tag-input>
            </bk-form-item>
            <bk-form-item label="变量表">
                <bk-select
                    searchable
                    multiple
                    display-tag
                    v-model="form.var_table">
                    <bk-option v-for="option in varTableList"
                        :key="option.id"
                        :id="option.id"
                        :name="option.name">
                    </bk-option>
                </bk-select>
            </bk-form-item>
            <bk-divider style="width: 536px;position: relative;right: 20px;border-color: #e8eaec;"></bk-divider>
            <!-- 这个地方是为了解决在一个bk-form-item的情况下组合两个表单项如何做校验，默认渲染所有的校验项，然后动态改变rules的规则即可 -->
            <!-- 调度方式为定时 -->
            <bk-form-item :property="'fixedTime'" :required="true" ext-cls="custom-form-item">
            </bk-form-item>
            <!-- 调度方式为周期 -->
            <bk-form-item :property="'periodTime'" :required="true" ext-cls="custom-form-item">
            </bk-form-item>
            <bk-form-item :property="'cycleDat'" :required="true" ext-cls="custom-form-item">
            </bk-form-item>
            <bk-form-item :property="'timeOption'" :required="true" ext-cls="custom-form-item">
            </bk-form-item>
            <!-- 调度方式为日历 -->
            <bk-form-item :property="'calendarValue'" :required="true" ext-cls="custom-form-item">
            </bk-form-item>
            <bk-form-item :property="'calendarTime'" :required="true" ext-cls="custom-form-item">
            </bk-form-item>
        </bk-form>
    </div>
</template>

<script>
    export default {
        inject: ['father_this'],
        data() {
            return {
                crossDayTipConfig: {
                    content: '跨日依赖: 指作业流在周期性或日历的调度方式下,作业流如果在前一次的执行中未成功执行,则当时间点到达后一次的计划开始时间时,该作业流不进行自动调度执行。',
                    placement: 'right',
                    width: 300
                },
                pageKey: 0,
                runSysList: [],
                agentList: [],
                agentShow: true,
                baseInfoLoading: false,
                disabled: false,
                midType: '', // 调度方式切换缓冲值
                timeTypeList1: [ // 每隔xxx时间类型下拉选择
                    {
                        value: 'days',
                        label: '天'
                    },
                    {
                        value: 'hours',
                        label: '时'

                    },
                    {
                        value: 'minutes',
                        label: '分'
                    }
                ],
                timeTypeList2: [ // 巡检每隔xxx时间类型下拉选择
                    {
                        value: 'hour',
                        label: '时'
                    },
                    {
                        value: 'min',
                        label: '分'
                    },
                    {
                        value: 'second',
                        label: '秒'
                    }
                ],
                valList: [], // 变量表下拉列表
                calendarList: [], // 日历下拉列表
                controlList: [{ // 调度方式单选列表
                    label: '无',
                    value: 'null'
                }, {
                    label: '定时',
                    value: 'time'
                }, {
                    label: '周期',
                    value: 'cycle'
                }, {
                    label: '日历',
                    value: 'calendar'
                }], // 调度方式单选列表
                varList: [], // 变量表下拉列表
                categoryList: [
                ],
                varTableList: [],
                form: {
                    jobFlowName: '', // 作业流名称
                    jobFlowDescribe: '', // 作业流描述
                    var_table: [], // 变量表
                    category: [],
                    run_type: '', // 调度方式
                    calendarValue: '', // 调度方式为日历，日历值
                    calendarTime: '', // 调度方式为日历，日历时间值
                    fixedTime: '', // 调度方式为定时，开始时间
                    periodTime: '', // 调度方式为周期， 开始时间
                    cycleDat: '', // 调度方式为周期，每隔xxx
                    timeOption: '', // 调度方式为周期，时间类型
                    cross_day_dependence: '', // 跨日依赖
                    pre_category: '', // 前置跑批id
                    pre_agent: '', // 前置agent
                    pre_commands: [{ // 前置依赖命令检测
                        key: '',
                        value: ''
                    }],
                    file_dependence: {
                        file_path: '', // 前置文件路径
                        max_num: '', // 巡检次数
                        cycle: { // 巡检周期
                            type: '', // 时间类型
                            value: '' // 时间值
                        }
                    }
                },
                rules: {
                    jobFlowName: [{
                        required: true,
                        message: '作业流名称不能为空，请检查您的输入！',
                        trigger: 'blur'
                    }],
                    run_type: [{
                        required: true,
                        message: '调度方式不能为空，请检查您的选择！',
                        trigger: 'blur'
                    }]
                }
            }
        },
        created() {
            this.initValList()
            this.getRunSysList()
            this.initCalendarList()
        },
        mounted() {
            if (this.$route.query.type !== 'add') {
                this.baseInfoLoading = true
                if (this.$route.query.type === 'detail') {
                    this.disabled = true
                }
                setTimeout(() => {
                    // if (this.father_this.jobFlowFrom.hasOwnProperty('cross_day_dependence')) {
                    //     this.form.cross_day_dependence = true
                    // }
                    this.form.cross_day_dependence = this.father_this.jobFlowFrom.cross_day_dependence
                    this.form.run_type = this.father_this.jobFlowFrom.run_type // 调度方式初始化
                    this.handleChangeRules()
                    this.form.var_table = this.father_this.jobFlowFrom.var_table // 表量表值初始化
                    this.form.category = this.father_this.jobFlowFrom.category // 表量表值初始化
                    this.midType = this.form.run_type
                    this.form.jobFlowName = this.father_this.jobFlowFrom.name // 作业流名称初始化
                    this.form.jobFlowDescribe = this.father_this.jobFlowFrom.description // 作业流描述初始化
                    // this.form.calendarTime = this.father_this.jobFlowFrom.trigger_data.eta // 调度方式为日历，开始时间初始化
                    this.form.calendarTime = '' // 调度方式为日历，开始时间初始化
                    if (this.father_this.jobFlowFrom.pre_commands !== null) {
                        this.form.pre_commands = this.father_this.jobFlowFrom.pre_commands // 作业流前置依赖初始化
                    }
                    if (this.father_this.jobFlowFrom.hasOwnProperty('pre_category')) {
                        this.form.pre_category = this.father_this.jobFlowFrom.pre_category // 作业流前置跑批id初始化
                    }
                    if (this.father_this.jobFlowFrom.hasOwnProperty('pre_agent')) {
                        this.form.pre_agent = this.father_this.jobFlowFrom.pre_agent // 作业流前置agnet初始化
                    }
                    this.baseInfoLoading = false
                }, 2000)
            }
        },
        methods: {
            // 获取作业库跑批系统
            getRunSysList() {
                this.$api.process.category({'page': 1, 'page_size': 9999}).then(res => {
                    this.categoryList = res.data.items
                })
                this.runSysList = []
            },
            handleRunIdChange() {
                if (this.form.pre_category === '') {
                    this.agentList = []
                    this.form.pre_agent = ''
                    return false
                }
                this.getAgentList()
            },
            // 获取agent列表
            getAgentList() {
                // pageKey用于处理首次加载页面时假如前置agent有值而由于前置跑批id初始化改变触发change事件使其清空。
                if (this.pageKey !== 0) {
                    this.form.pre_agent = ''
                    this.agentList = []
                }
                this.baseInfoLoading = true
                this.agentShow = false
                this.$api.station.list({
                    'category': this.form.pre_category
                }).then(res => {
                    if (res.result) {
                        this.agentList = res.data.items
                        this.agentShow = true
                    } else {
                        this.$cwMessage(res.message, 'error')
                    }
                    this.pageKey += 1
                    this.baseInfoLoading = false
                })
            },
            // 处理删除前置条件检测命令
            handleDeleteCommand(index) {
                this.form.pre_commands.splice(index, 1)
            },
            // 处理添加前置条件检测命令
            handleAddCommand() {
                this.form.pre_commands.push({
                    key: '',
                    value: ''
                })
            },
            // 初始化日历下拉
            initCalendarList() {
                this.calendarList = []
            },
            // 初始化变量表下拉
            initValList() {
                this.varList = []
                const params = {
                    page: 1,
                    page_size: 9999
                }
                this.$api.varTable.list(params).then(res => {
                    this.varTableList = res.data.items
                })
            },
            handleCalendarTimeChange(e) {
                this.form.calendarTime = e
            },
            handleFixedTimeChange(e) {
                this.form.fixedTime = e
            },
            handlePeriodTimeChange(e) {
                this.form.periodTime = e
            },
            // 处理动态切换表单校验规则
            handleChangeRules() {
                this.rules = {
                    jobFlowName: [{
                        required: true,
                        message: '作业流名称不能为空，请检查您的输入！',
                        trigger: 'blur'
                    }],
                    run_type: [{
                        required: true,
                        message: '调度方式不能为空，请检查您的选择！',
                        trigger: 'blur'
                    }]
                }
            },
            // 处理调度方式切换确认
            confim(e) {
                this.midType = e
                this.form.calendarValue = ''
                this.form.calendarTime = ''
                this.form.fixedTime = ''
                this.form.periodTime = ''
                this.form.cycleDat = ''
                this.form.timeOption = ''
                this.form.cross_day_dependence = ''
                this.handleChangeRules()
            },
            // 处理调度方式改变
            handleControlChange(e) {
                if (this.midType === '') {
                    this.midType = e
                }
                // 其他切日历
                if (e === 'calendar' && this.midType !== 'calendar') {
                    return this.$bkInfo({
                        type: 'primary',
                        title: '此操作将请空画布及任务编排, 确认吗？',
                        width: 500,
                        confirmLoading: false,
                        confirmFn: async() => {
                            this.$emit('empty-task-make', true)
                            this.confim(e)
                        },
                        cancelFn: async() => {
                            this.form.run_type = this.midType
                        }
                    })
                }
                if (this.midType === 'calendar' && e !== 'calendar') {
                    return this.$bkInfo({
                        type: 'primary',
                        title: '此操作将请空画布及任务编排, 确认吗？',
                        width: 500,
                        confirmLoading: false,
                        confirmFn: async() => {
                            this.$emit('empty-task-make', true)
                            this.confim(e)
                        },
                        cancelFn: async() => {
                            this.form.run_type = this.midType
                        }
                    })
                }
                this.confim(e)
            }
        }
    }
</script>

<style lang="scss" scoped>
#baseInfo {
    /deep/ .custom-form-item {
        display: none;
    }

    .pre-commands {
        display: flex;

        i {
            font-size: 32px;
            color: #979BA5;
            width: 32px;
            text-align: center;
            height: 32px;
            line-height: 32px;
            cursor: pointer;

            &:active {
                color: rgb(58, 132, 255);
            }
        }
    }
}
</style>
