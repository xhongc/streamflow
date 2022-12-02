<template>
    <div style="height: 100%;">
        <div style="display: flex;align-items: center;justify-content: space-between;">
            <bk-steps ext-cls="custom-icon"
                :controllable="controllableSteps.controllable"
                :steps="controllableSteps.steps"
                :cur-step.sync="controllableSteps.curStep"
                @step-changed="stepChanged">
            </bk-steps>
            <div style="display: flex;margin-right: 2%;">
                <div class="next-icon left-icon" @click="lastStep">
                    <bk-icon type="arrows-m-left-shape" />
                </div>
                <div class="next-icon right-icon" @click="nextStep">
                    <bk-icon type="arrows-m-right-shape" />
                </div>
            </div>
        </div>
        <div class="step-1" v-if="controllableSteps.curStep === 1">
            <single-job-flow></single-job-flow>
        </div>
        <div class="step-2" v-if="controllableSteps.curStep === 2">
            <div style="padding-top: 26px;padding-left: 30px;">
                <div style="font-size: 14px;color: #2b2929;">基础信息</div>
            </div>
            <bk-divider></bk-divider>

            <div style="padding: 30px;">
                <bk-form :label-width="150" :model="formData">
                    <bk-form-item label="任务名称" :required="true" :property="'name'">
                        <bk-input v-model="formData.name" style="width: 350px;"></bk-input>
                    </bk-form-item>
                </bk-form>
            </div>
            <div style="padding-top: 26px;padding-left: 30px;">
                <div style="font-size: 14px;color: #2b2929;">参数信息</div>
            </div>
            <bk-divider></bk-divider>
            <div style="padding: 30px;">
                <bk-form :label-width="150" style="overflow: scroll;height: 300px;">
                    <div v-for="(each, index) in formData.var_table" :key="index" style="margin-bottom: 20px;">
                        <bk-form-item :label="each.name" :required="true" :property="'name'">
                            <bk-input v-model="each.value" style="width: 350px;" clearable></bk-input>
                        </bk-form-item>
                    </div>
                </bk-form>
            </div>
        </div>
        <div class="step-2" v-if="controllableSteps.curStep === 3">
            <div style="padding-top: 26px;padding-left: 30px;">
                <div style="font-size: 14px;color: #2b2929;">执行方式</div>
            </div>
            <bk-divider></bk-divider>
            <div style="padding: 30px;">
                <bk-form :label-width="100" :model="formData">
                    <bk-form-item label="执行时间">
                        <bk-radio-group v-model="formData.run_type">
                            <div style="margin-top: 8px;">
                                <bk-radio :value="'hand'">单次</bk-radio>
                            </div>
                            <div style="margin-top: 16px;">
                                <bk-radio :value="'time'">定时</bk-radio>
                                <div style="display: inline-block;">
                                    <bk-date-picker
                                        :disabled="formData.run_type !== 'time'"
                                        v-model="formData.when_start"
                                        style="width: 240px;margin-left: 20px;"
                                        :type="'datetime'"
                                        :options="disableTime"
                                        @change="changeTime"
                                        value-format="yyyy-MM-dd HH:mm:ss"
                                        placeholder="选择开始的日期时间">
                                    </bk-date-picker>
                                </div>
                            </div>
                            <div style="color: #EA3636;font-size: 12px;margin: 8px 0 0 68px;" v-show="displayImmediate">
                                请填写定时时间
                            </div>
                            <div style="margin-top: 16px;height: 32px;">
                                <bk-radio :value="'cycle'">周期</bk-radio>
                                <bk-date-picker
                                    :disabled="formData.run_type !== 'cycle'"
                                    v-model="formData.when_start"
                                    style="width: 240px;margin-left: 20px;"
                                    :type="'datetime'"
                                    :options="disableTime"
                                    @change="changeTime"
                                    value-format="yyyy-MM-dd HH:mm:ss"
                                    placeholder="选择开始的日期时间">
                                </bk-date-picker>
                                <div style="margin-top: -32px;margin-left: 310px;">
                                    <bk-button
                                        style="float: left;border: none;background: transparent;width: 54px;padding: 0 8px;">
                                        每隔：
                                    </bk-button>
                                    <bk-input
                                        style="width: 80px;float: left;"
                                        type="number"
                                        v-model="formData.cycle_time"
                                        :min="1"
                                        :precision="0"
                                        ext-cls="interval-wrap"
                                        :disabled="formData.run_type !== 'cycle'">
                                    </bk-input>
                                    <bk-select
                                        v-model="formData.cycle_type"
                                        :clearable="false"
                                        style="width: 80px;float: left;margin-left: 10px;background-color: #fff;"
                                        :disabled="formData.run_type !== 'cycle'">
                                        <bk-option name="分钟" key="min" id="min"></bk-option>
                                        <bk-option name="小时" key="hour" id="hour"></bk-option>
                                        <bk-option name="天" key="day" id="day"></bk-option>
                                    </bk-select>
                                    <span style="margin-left: 10px;">执行一次</span>
                                </div>
                                <div
                                    style="color: #EA3636;font-size: 12px;margin: 28px 0 0 68px;position: absolute;line-height: 32px;"
                                    v-show="displayCycle">请填写周期时间及间隔
                                </div>
                            </div>
                            <div style="margin-top: 16px;">
                                <bk-radio :value="'cron'">自定义</bk-radio>
                                <LoopRuleSelect
                                    v-if="formData.run_type === 'cron'"
                                    ref="loopRuleSelect"
                                    style="margin-left: 70px;margin-top: -20px;"
                                    :manual-input-value="periodicCron"
                                    @change="changeCrontab"
                                >
                                </LoopRuleSelect>
                            </div>
                        </bk-radio-group>
                    </bk-form-item>
                </bk-form>
            </div>
        </div>
        <div class="step-2" v-if="controllableSteps.curStep === 4">
        </div>
    </div>
</template>

<script>
    import singleJobFlow from '../job_flow_mgmt/single_job_flow'
    import LoopRuleSelect from '@/components/time_crontab/crontab'

    export default {
        name: 'task-create',
        components: {
            'single-job-flow': singleJobFlow,
            'LoopRuleSelect': LoopRuleSelect
        },
        data() {
            return {
                controllableSteps: {
                    controllable: false,
                    steps: [
                        {title: '节点选择', icon: 1},
                        {title: '参数填写', icon: 2},
                        {title: '执行方式', icon: 3},
                        {title: this.$route.query.task_type === 'update' ? '修改任务' : '创建任务', icon: 4}
                    ],
                    curStep: 1
                },
                formData: {
                    name: '任务-' + this.$route.query.job_name,
                    run_type: 'hand',
                    var_table: [],
                    when_start: '',
                    cycle_time: '1',
                    cycle_type: 'hour',
                    cron_time: '',
                    process_id: this.$route.query.job_flow_data
                },
                varTableList: [],
                formItem: {
                    taskName: '', // 任务名称
                    notifier: [], // 当前通知人
                    runtimeType: 'now', // 立即:now/定时:time/周期:cycle
                    beginTime: '', // 定时任务
                    cyclebeginTime: '', // 周期任务
                    cycleDat: '', // 每隔多少cycleType执行一次
                    cycleType: 'day',
                    modelList: [], // 当前选中模块集合
                    disabledGroup: [], // 当前选中业务的集合 *
                    nowModalData: [],
                    single: false

                },
                disableTime: {
                    disabledDate: function(val) {
                        const nowTime = new Date(new Date().toLocaleDateString()).getTime()
                        const calendarTime = new Date(val.toLocaleDateString()).getTime()
                        return calendarTime < nowTime
                    }
                },
                displayImmediate: false,
                displayCycle: false,
                periodicCron: '*/5 * * * *'
            }
        },
        created() {
            this.$api.process.var_table({'process_id': this.$route.query.job_flow_data}).then(res => {
                this.formData.var_table = res.data
            })
        },
        methods: {
            stepChanged(index) {
                this.controllableSteps.curStep = index
            },
            changeCrontab(val) {
                this.formData.cron_time = val
            },
            changeTime(val) {
                this.formData.when_start = val
            },
            lastStep() {
                if (this.controllableSteps.curStep === 1 || this.controllableSteps.curStep === 4) {
                    return false
                } else {
                    this.controllableSteps.curStep = this.controllableSteps.curStep - 1
                }
            },
            nextStep() {
                if (this.controllableSteps.curStep < 3) {
                    this.controllableSteps.curStep = this.controllableSteps.curStep + 1
                } else if (this.controllableSteps.curStep === 3) {
                    this.$bkInfo({
                        title: this.$route.query.task_type === 'update' ? '确认要修改任务吗？' : '确认要创建任务吗？',
                        confirmLoading: false,
                        confirmFn: async() => {
                            this.tableLoading = true
                            console.log(this.formData)
                            this.$api.task.create(this.formData).then(res => {
                                if (res.result) {
                                    this.$cwMessage('执行成功!', 'success')
                                    this.$router.push({
                                        path: '/taskList'
                                    })
                                } else {
                                    this.$cwMessage(res.message, 'error')
                                }
                                this.tableLoading = false
                            })
                        }
                    })
                }
            }
        }
    }
</script>

<style scoped>
.custom-icon {
    margin: 20px 0 20px 20px;
    width: 88%;
    background-color: #ffffff;
    padding: 10px;
    border-radius: 15px;
}

.step-1 {
    margin: 0 30px 30px 20px;
    height: 80vh;
    padding: 10px;
    border-radius: 15px;
    background-color: #ffffff;
}

.step-2 {
    margin: 20px 30px 30px 20px;
    height: 80%;
    background: #ffffff;
}

.step-footer {
    background: #ffffff;
    margin-bottom: -10px;
    height: 50px;
    border-top: 1px solid #cacedb;
}
.next-icon {
    background-color: #ffffff;
    border-radius: 20px;
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    cursor: pointer;
    color: #979BA5;
    margin-left: 15px;
}
.left-icon {
    padding-left: 14px;
}
.right-icon {
    padding-left: 15px;
}
.next-icon:hover {
    color: #699DF4;
}
.next-btn {
    margin: 13px 20px;
    width: 100px;
}
</style>
