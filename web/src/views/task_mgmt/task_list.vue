<template>
    <transition name="bk-slide-fade-down">
        <div id="jobList" v-show="!tableLoading">
            <div class="header">
                <div class="search-box">
                    <div class="add-in">
                    </div>
                    <div class="search-in" v-if="auth.search">
                        <bk-search-select
                            :show-popover-tag-change="true"
                            :data="searchData"
                            :show-condition="false"
                            :placeholder="'请输入过滤条件'"
                            @change="handleSearch"
                            v-model="demo1.value"></bk-search-select>
                    </div>
                </div>
                <div style="float: left;">
                </div>
            </div>
            <div style="clear: both;"></div>
            <div class="content">
                <bk-table ref="table" :data="tableList" :pagination="pagination" @page-change="handlePageChange"
                    @page-limit-change="handlePageLimitChange" v-bkloading="{ isLoading: tableLoading, zIndex: 10 }"
                    ext-cls="customTable" @select-all="handleSelectAll" @select="handleSelect" :size="setting.size"
                    :max-height="maxTableHeight">
                    <bk-table-column :label="item.label" :prop="item.id" v-for="(item, index) in setting.selectedFields"
                        :key="index" :show-overflow-tooltip="item.overflowTooltip" :sortable="item.sortable">
                        <template slot-scope="props">
                            <span v-if="item.id === 'name'"
                                style="color: #052150;cursor: pointer;font-weight: 400;text-decoration: underline;"
                                @click="handleOpenDetail(props.row)">
                                {{ props.row[item.id] }}
                            </span>
                            <div v-else-if="item.id === 'run_type'">
                                <span v-if="props.row.run_type === 'hand'">
                                    <bk-tag radius="5px">单次</bk-tag>
                                </span>
                                <span v-else-if="props.row.run_type === 'cron'">
                                    <bk-tag radius="5px">自定义</bk-tag></span>
                                <span v-else-if="props.row.run_type === 'time'">
                                    <bk-tag radius="5px">定时</bk-tag></span>
                                <span v-else-if="props.row.run_type === 'cycle'">
                                    <bk-tag radius="5px">周期</bk-tag></span>
                            </div>
                            <span v-else>{{(props.row[item.id] === '' || props.row[item.id] === null) ? '- -' : props.row[item.id] }}</span>
                        </template>
                    </bk-table-column>
                    <bk-table-column label="操作" width="180">
                        <template slot-scope="props">
                            <div style="display: flex;align-items: center;">
                                <div v-if="props.row.run_type === 'hand'">
                                    <bk-button class="mr10 btn-color" theme="primary" text
                                        @click="handleImplement(props.row)">执行
                                    </bk-button>
                                </div>
                                <div v-else>
                                    <div v-if="props.row.enabled">
                                        <bk-button class="mr10 btn-color-red" theme="primary" text
                                            @click="handleOperate(props.row, 'pause')">暂停
                                        </bk-button>
                                    </div>
                                    <div v-else>
                                        <div v-if="props.row.run_type === 'time'">
                                            <bk-button class="mr10 btn-color-blue" theme="primary" text>
                                                完成
                                            </bk-button>
                                        </div>
                                        <div v-else>
                                            <bk-button class="mr10 btn-color-green" theme="primary" text
                                                @click="handleOperate(props.row, 'resume')">恢复
                                            </bk-button>
                                        </div>
                                    </div>
                                </div>
                                <bk-button class="mr10 btn-color" theme="primary" text
                                    @click="handleOpenDetail(props.row)">修改
                                </bk-button>
                                <bk-button class="mr10 btn-color" theme="primary" text @click="handleDelete(props.row)">
                                    删除
                                </bk-button>
                                <bk-popover ext-cls="dot-menu" placement="bottom-start" theme="dot-menu light"
                                    trigger="click" :arrow="false" :distance="0" offset="15">
                                    <span class="dot-menu-trigger"></span>
                                    <ul class="dot-menu-list" slot="content">
                                        <li class="dot-menu-item" @click="handleJumpHistory(props.row)">执行历史</li>
                                    </ul>
                                </bk-popover>
                            </div>
                        </template>
                    </bk-table-column>
                    <bk-table-column type="setting">
                        <bk-table-setting-content :fields="setting.fields" :selected="setting.selectedFields"
                            @setting-change="handleSettingChange" :size="setting.size">
                        </bk-table-setting-content>
                    </bk-table-column>
                </bk-table>
            </div>
            <div>
                <bk-sideslider :is-show.sync="dialogShow" :quick-close="true" title="作业详情" :width="500"
                    ext-cls="custom-sidelider">
                    <div slot="content" style="height: 100%;">
                        <job-dialog :job-from="jobFrom" :key="dialogKey">
                        </job-dialog>
                    </div>
                </bk-sideslider>
            </div>
        </div>
    </transition>

</template>

<script>
    export default {
        components: {},
        data() {
            const fields = [{
                id: 'name',
                label: '作业名',
                overflowTooltip: true,
                sortable: false
            }, {
                id: 'process_name',
                label: '作业流名称',
                overflowTooltip: true,
                sortable: false
            }, {
                id: 'run_type',
                label: '执行方式',
                overflowTooltip: true,
                sortable: false
            }, {
                id: 'when_start',
                label: '执行时间',
                overflowTooltip: true,
                sortable: false
            }
            ]
            return {
                searchData: [
                    {
                        name: '任务名称',
                        id: 'name',
                        multiable: false,
                        children: []
                    },
                    {
                        name: '作业流名称',
                        id: 'process__name',
                        multiable: false,
                        children: []
                    },
                    {
                        name: '模版类型',
                        id: 'run_type',
                        multiable: true,
                        children: [
                            {id: 'hand', name: '单次'},
                            {id: 'time', name: '定时'},
                            {id: 'cycle', name: '周期'},
                            {id: 'cron', name: '自定义'}
                        ]
                    },
                    {
                        name: '创建人',
                        id: 'creator',
                        multiable: false,
                        children: []
                    }
                ],
                demo1: {
                    value: []
                },
                maxTableHeight: '',
                auth: {
                    modify: true,
                    del: true
                },
                dialogKey: 0,
                jobFrom: {},
                setting: {
                    size: 'small', // 表格大小
                    fields: fields, // 表格所有列
                    selectedFields: fields.slice(0, 8) // 表格当前显示列
                },
                tableLoading: false,
                tableList: [],
                runSysList: [], // 跑批系统下拉列表
                isDropdownShow: false,
                searchFrom: {
                    name: '', // 作业名称
                    process__name: '', // 作业流名称
                    creator: '', // 创建人
                    run_type: ''
                },
                pagination: {
                    current: 1,
                    count: 1,
                    limit: 10
                },
                selectionList: [], // 表格多选
                dialogShow: false,
                runTypeList: [
                    {id: 'hand', name: '单次'},
                    {id: 'time', name: '定时'},
                    {id: 'cycle', name: '周期'},
                    {id: 'cron', name: '自定义'}
                ]
            }
        },
        created() {
            this.handleLoad()
            this.auth = this.hasPerm(this.$route.path)
            this.maxTableHeight = this.$store.state.common.defaultTableHeight - 52
        },
        methods: {
            handleJumpHistory(row) {
                this.$router.push({
                    path: '/jobflowview',
                    query: {
                        task_id: row.id
                    }
                })
            },
            // 处理克隆作业
            handleClone(row) {
                this.$router.push({
                    path: '/singlejob',
                    query: {
                        type: 'clone',
                        job_id: row.id
                    }
                })
            },
            // 处理表格字段显隐
            handleSettingChange({
                fields,
                size
            }) {
                this.setting.size = size
                this.setting.selectedFields = fields
            },
            // 处理执行
            handleImplement(row) {
                this.$bkInfo({
                    title: '确认要执行吗？',
                    confirmLoading: false,
                    confirmFn: async() => {
                        this.tableLoading = true
                        this.$api.task.execute({'task_id': row.id}).then(res => {
                            if (res.result) {
                                this.$cwMessage('执行成功!', 'success')
                                this.$store.commit('changeTabActive', 'jobview')
                                this.$router.push({
                                    path: '/jobflowview'
                                })
                            } else {
                                this.$cwMessage(res.message, 'error')
                            }
                            this.tableLoading = false
                        })
                    }
                })
            },
            // 处理打开详情
            handleOpenDetail(row) {
                this.$router.push({
                    name: 'taskCreate',
                    query: {
                        job_flow_data: row.process,
                        job_name: row.process_name,
                        type: 'detail',
                        task_type: 'update',
                        task_id: row.id
                    }
                })
            },
            handleOperate(row, operate) {
                this.$bkInfo({
                    title: '确认要执行？',
                    confirmLoading: true,
                    confirmFn: () => {
                        try {
                            this.$api.task.operate({'task_id': row.id, 'operate': operate}).then(res => {
                                if (res.result) {
                                    this.$cwMessage('执行成功！', 'success')
                                    this.handleLoad(false)
                                }
                            })
                            return true
                        } catch (e) {
                            console.warn(e)
                            return false
                        }
                    }
                })
            },
            // 处理全选
            handleSelectAll(selection) {
                if (selection.length > 0) {
                    this.selectionList = this.selectionList.concat(selection)
                } else {
                    this.tableList.forEach(ms => {
                        this.selectionList = this.selectionList.filter(item => item.id !== ms.id)
                    })
                }
            },
            // 处理单选
            handleSelect(selection, row) {
                const isHaveItem = this.selectionList.find(item => item.id === row.id)
                if (isHaveItem) {
                    this.selectionList = this.selectionList.filter(item => item.id !== isHaveItem.id)
                } else {
                    this.selectionList.push(row)
                }
            },
            // 处理导出
            handleExportFiles() {
                if (this.selectionList.length === 0) {
                    return this.$cwMessage('至少选择一条数据！', 'warning')
                }
                const ids = []
                // 数组去重
                this.selectionList.forEach(item => {
                    if (ids.indexOf(item.id) < 0) {
                        ids.push(item.id)
                    }
                })
                window.open(window.siteUrl + '/export/content/?id=' + ids.join(','))
            },
            // 处理跳转修改
            handleOpenUpdate(row) {
            },
            // 处理删除
            handleDelete(row) {
                this.$bkInfo({
                    type: 'primary',
                    title: '确认要删除吗？',
                    confirmLoading: false,
                    confirmFn: async() => {
                        this.tableLoading = true
                        this.$api.task.delete(row.id).then(res => {
                            if (res.result) {
                                this.$cwMessage('删除成功！', 'success')
                                if (this.tableList.length === 1 && this.pagination.current !== 1) {
                                    this.pagination.current -= 1
                                }
                                this.handleLoad()
                            } else {
                                this.$cwMessage(res.message, 'error')
                            }
                            this.tableLoading = false
                        })
                    }
                })
            },
            // 获取跑批系统
            getRunSysList() {
                this.$api.category.list().then(res => {
                    if (res.result) {
                        this.runSysList = res.data.items
                    } else {
                        this.$cwMessage(res.message, 'error')
                    }
                })
            },
            // 处理搜索重置
            handleReset() {
                this.searchFrom = {
                    name: '', // 作业名称
                    station_name: '', // agent
                    category: '', // 跑批系统
                    ip: '', // ip
                    process_name: '', // 作业流名称
                    creator: '' // 创建人
                }
            },
            // 处理打开高级搜索
            handleOpenSeniorSearch() {
                this.isDropdownShow = !this.isDropdownShow
                // this.handleReset()
            },
            // 处理表格size切换
            handlePageLimitChange(val) {
                this.pagination.current = 1
                this.pagination.limit = val
                this.handleLoad(false)
            },
            // 处理查找
            handleSearch(list) {
                const params = {}
                list.forEach((r) => {
                    if (!params[r.id]) {
                        params[r.id] = r.values.map((s) => s.value || s.id)
                    } else {
                        params[r.id] = params[r.id].concat(
                            r.values.map((s) => s.value || s.id)
                        )
                    }
                })

                for (const key in params) {
                    params[key] = params[key].join(',')
                }
                this.pagination.current = 1
                this.searchFrom = params
                this.handleLoad()
            },
            // 处理页面跳转
            handlePageChange(page) {
                this.pagination.current = page
                this.handleLoad(false)
            },
            // 处理表格默认选择
            defaultCheck() {
                this.$nextTick(() => {
                    this.selectionList.forEach(item1 => {
                        this.tableList.forEach(item2 => {
                            if (item1.id === item2.id) {
                                this.$refs.table.toggleRowSelection(item2, true)
                            }
                        })
                    })
                })
            },
            handleLoad(first = true) {
                if (first) {
                    this.tableLoading = true
                }
                this.$api.task.list({
                    ...this.searchFrom,
                    page: this.pagination.current,
                    page_size: this.pagination.limit
                }).then(res => {
                    if (res.result) {
                        this.pagination.count = res.data.count
                        this.tableList = res.data.items
                        if (this.selectionList.length > 0) {
                            this.defaultCheck()
                        }
                    } else {
                        this.$cwMessage(res.message, 'error')
                    }
                    this.tableLoading = false
                })
            }
        }
    }
</script>

<style lang="scss">
.dot-menu {
    display: inline-block;
    vertical-align: middle;

    .tippy-tooltip.dot-menu-theme {
        padding: 0;
    }
}

.dot-menu-list {
    margin: 0;
    padding: 5px 0;
    min-width: 50px;
    list-style: none;
}

.dot-menu-list .dot-menu-item {
    padding: 0 10px;
    font-size: 12px;
    line-height: 26px;
    cursor: pointer;
    text-align: center;

    &:hover {
        background-color: #eaf3ff;
        color: #3a84ff;
    }
}
</style>
<style lang="scss" scoped>
#jobList {
    padding: 20px;
    height: 100%;
    overflow: auto;

    .header {
        width: 100%;
        font-size: 0;
        margin-bottom: 20px;
        float: left;
        // position: relative;

        .senior-search-box {
            background-color: #fff;
            padding: 20px;
            width: 100%;
            margin-top: 20px;
            float: left;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, .1);
            border: 1px solid rgba(0, 0, 0, .2);
        }
    }

    .content {

        .customTable {
            border: 0 !important;

            /deep/ .bk-table-pagination-wrapper {
                background-color: #fff;
            }

            /deep/ .bk-table-empty-block {
                background-color: #fff;
            }

            .dot-menu-trigger {
                display: block;
                width: 20px;
                height: 20px;
                line-height: 20px;
                border-radius: 50%;
                text-align: center;
                font-size: 0;
                cursor: pointer;
            }

            .dot-menu-trigger:hover {
                color: #3A84FF;
                background-color: #DCDEE5;
            }

            .dot-menu-trigger:before {
                content: "";
                display: inline-block;
                width: 3px;
                height: 3px;
                border-radius: 50%;
                background-color: currentColor;
                box-shadow: 0 -4px 0 currentColor, 0 4px 0 currentColor;
            }
        }
    }

    .custom-sidelider {
        /deep/ .bk-sideslider-wrapper {
            overflow-y: hidden;
        }
    }
}

.search-box {
    display: flex;
    justify-content: space-between;
    background-color: #fff;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #07386d;
    height: 65px;
    align-items: center;
}

.btn-color {
    color: rgb(1, 158, 213) !important;
}
.btn-color-red {
    color: #FF5656 !important;
}
.btn-color-green {
    color: #34ba85 !important;
}
.btn-color-blue {
    color: #0b254f !important;
}
/deep/ .search-input-chip {
    background: #83a7ca !important;
    color: #fff !important;
}

/deep/ .bk-search-select {
    border-bottom: 1px solid #07386d !important;
    border-top: 0 !important;
    border-left: 0 !important;
    border-right: 1px solid #07386d !important;
    border-bottom-right-radius: 6px !important;
}

/deep/ .search-select-wrap .bk-search-select.is-focus {
    border-color: #052150 !important;
    color: #052150 !important;
}

/deep/ .search-select-wrap .bk-search-select .search-nextfix .search-nextfix-icon.is-focus {
    border-color: #052150 !important;
    color: #052150 !important;
}
</style>
