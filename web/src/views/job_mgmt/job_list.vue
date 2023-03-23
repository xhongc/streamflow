<template>
    <transition name="bk-slide-fade-down">
        <div id="jobList" v-show="!tableLoading">
            <div class="header">
                <div class="search-box">
                    <div class="add-in">
                        <button theme="primary" @click="handCreate" class="button">新建</button>
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
            </div>
            <div class="content">
                <bk-table ref="table"
                    :data="tableList"
                    :pagination="pagination"
                    @page-change="handlePageChange"
                    @page-limit-change="handlePageLimitChange"
                    v-bkloading="{ isLoading: tableLoading, zIndex: 10 }"
                    ext-cls="customTable"
                    @select-all="handleSelectAll"
                    @select="handleSelect"
                    :size="setting.size"
                    :max-height="maxTableHeight">
                    <bk-table-column :label="item.label" :prop="item.id" v-for="(item, index) in setting.selectedFields"
                        :key="index" :show-overflow-tooltip="item.overflowTooltip" :sortable="item.sortable">
                        <template slot-scope="props">
                            <span v-if="item.id === 'name'" style="color: #052150;cursor: pointer;font-weight: 400;text-decoration: underline;"
                                @click="handleOpenDetail(props.row)">{{ props.row[item.id] }}</span>
                            <span v-else-if="item.id === 'template_type'">
                                <span v-if="props.row.template_type === '0'">
                                    <bk-tag radius="5px">标准节点</bk-tag></span>
                                <span v-else-if="props.row.template_type === '2'">
                                    <bk-tag radius="5px" style="color: #153c6b;">节点模版</bk-tag></span>
                                <span v-else-if="props.row.template_type === '1'">
                                    <bk-tag radius="5px" style="color: #07254f;">自定义节点</bk-tag></span>
                            </span>
                            <span
                                v-else>{{ (props.row[item.id] === '' || props.row[item.id] === null) ? '- -' : props.row[item.id] }}</span>
                        </template>
                    </bk-table-column>
                    <bk-table-column label="操作" width="180">
                        <template slot-scope="props">
                            <div style="display: flex;align-items: center;">
                                <bk-button class="mr10 btn-color" theme="primary" text @click="handleOpenUpdate(props.row)"
                                    v-if="auth.modify">修改
                                </bk-button>
                                <bk-button class="mr10 btn-color" theme="primary" text @click="handleClone(props.row)"
                                    v-if="auth.modify">克隆
                                </bk-button>
                                <bk-button class="mr10 btn-color" theme="primary" text @click="handleDelete(props.row)"
                                    v-if="props.row.template_type !== '0'">删除
                                </bk-button>
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
                <bk-sideslider :is-show.sync="dialogShow" :quick-close="true" title="作业详情" :width="600"
                    ext-cls="custom-sidelider">
                    <div slot="content" style="height: 100%;">
                        <job-dialog slot="content" :node-data="{ 'data': jobFrom }" :is-show-btn="false"></job-dialog>
                    </div>
                </bk-sideslider>
            </div>
        </div>
    </transition>
</template>

<script>
    import jobDialog from './job_dialog.vue'
    import _ from 'lodash'

    export default {
        components: {
            jobDialog
        },
        data() {
            const fields = [{
                id: 'name',
                label: '作业名',
                overflowTooltip: true,
                sortable: false
            }, {
                id: 'template_type',
                label: '模板类型',
                overflowTooltip: true,
                sortable: false
            }, {
                id: 'description',
                label: '作业描述',
                overflowTooltip: true,
                sortable: false
            }]
            return {
                searchData: [
                    {
                        name: '作业名称',
                        id: 'name',
                        multiable: false,
                        children: []
                    },
                    {
                        name: '模版类型',
                        id: 'template_type',
                        multiable: true,
                        children: [
                            {
                                id: '0',
                                name: '标准节点',
                                value: '0'
                            },
                            {
                                id: '1',
                                name: '自定义节点',
                                value: '1'
                            },
                            {
                                id: '2',
                                name: '节点模版',
                                value: '2'
                            }
                        ]
                    },
                    {
                        name: '作业描述',
                        id: 'description',
                        multiable: false,
                        children: []
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
                auth: {},
                dialogKey: 0,
                jobFrom: {},
                setting: {
                    size: 'small', // 表格大小
                    fields: fields, // 表格所有列
                    selectedFields: fields.slice(0, 8) // 表格当前显示列
                },
                tableLoading: false,
                tableList: [],
                runSysList: [
                    {
                        id: '0',
                        name: '标准节点'
                    },
                    {
                        id: '1',
                        name: '自定义节点'
                    },
                    {
                        id: '2',
                        name: '节点模版'
                    }
                ], // 跑批系统下拉列表
                isDropdownShow: false,
                searchFrom: {
                    name: '', // 作业名称
                    template_type: '',
                    description: '', // 跑批系统
                    creator: '' // 创建人
                },
                pagination: {
                    current: 1,
                    count: 1,
                    limit: 10
                },
                selectionList: [], // 表格多选
                dialogShow: false,
                searchVal: ''
            }
        },
        created() {
            this.handleLoad()
            // this.getRunSysList()
            this.auth = this.hasPerm(this.$route.path)
            this.maxTableHeight = this.$store.state.common.defaultTableHeight - 52
        },
        methods: {
            handCreate() {
                this.$router.push({
                    path: '/singlejob',
                    query: {
                        type: 'add'
                    }
                })
            },
            handleJumpHistory(row) {
                this.$store.commit('changeTabActive', 'jobviewhistory')
                this.$router.push({
                    path: '/jobviewhistory',
                    query: {
                        job_id: row.id
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
            // 处理打开详情
            handleOpenDetail(row) {
                this.dialogKey += 1
                this.jobFrom = row
                this.dialogShow = true
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
                this.$router.push({
                    path: '/singlejob',
                    query: {
                        type: 'update',
                        job_id: row.id
                    }
                })
            },
            // 处理删除
            handleDelete(row) {
                this.$bkInfo({
                    type: 'primary',
                    title: '确认要删除吗？',
                    confirmLoading: false,
                    confirmFn: async() => {
                        this.tableLoading = true
                        this.$api.content.delete(row.id).then(res => {
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
            getSearchVal(interimList) {
                const arr = _.cloneDeep(interimList)
                this.searchVal = arr.map((item) => {
                    return item.multiable
                        ? item
                        : Object.assign(item, {
                            values: item.values
                                ? item.values.length
                                    ? [item.values[item.values.length - 1]]
                                    : []
                                : []
                        })
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
                this.handleLoad()
            },
            // 处理打开高级搜索
            handleOpenSeniorSearch() {
                this.isDropdownShow = !this.isDropdownShow
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
                this.$api.content.list({
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
        margin-bottom: 16px;
        float: left;
        // position: relative;
        .senior-search-box {
            background-color: #fff;
            padding: 20px;
            width: 100%;
            margin-top: 16px;
            float: left;
            border-radius: 5px;
            border: 1px solid #dcdee4;
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

            .dot-menu-trigger::before {
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
.button {
    --color: rgb(138, 171, 202);
    padding: 0 2.3em;
    background-color: rgb(17, 64, 108);
    border-radius: .3em;
    position: relative;
    overflow: hidden;
    cursor: pointer;
    transition: .5s;
    font-weight: 400;
    font-size: 17px;
    border: 1px solid;
    font-family: inherit;
    text-transform: uppercase;
    color: #fff;
    z-index: 1;
    line-height: 30px;
}

.button::before, .button::after {
    content: " ";
    display: block;
    width: 50px;
    height: 50px;
    transform: translate(-50%, -50%);
    position: absolute;
    border-radius: 50%;
    z-index: -1;
    background-color: var(--color);
    transition: 1s ease;
}

.button::before {
    top: -1em;
    left: -1em;
}

.button::after {
    left: calc(100% + 1em);
    top: calc(100% + 1em);
}

.button:hover::before, .button:hover::after {
    height: 410px;
    width: 410px;
}

.button:hover {
    color: #fff;
}

.button:active {
    filter: brightness(.8);
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
