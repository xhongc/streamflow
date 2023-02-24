<template>
    <div id="jobFlowList">
        <div class="header">
            <div class="search-box">
                <div class="add-in">
                    <button theme="primary" @click="handleCreate" class="button">新建</button>
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
        <div style="clear: both;"></div>
        <div class="content">
            <bk-table ref="table" :data="tableList" :pagination="pagination" @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange" v-bkloading="{ isLoading: tableLoading, zIndex: 10 }"
                ext-cls="customTable" @select-all="handleSelectAll" @select="handleSelect" :size="setting.size"
                :max-height="maxTableHeight">
                <bk-table-column :label="item.label" :prop="item.id" v-for="(item, index) in setting.selectedFields"
                    :key="index" :show-overflow-tooltip="item.overflowTooltip" :sortable="item.sortable">
                    <template slot-scope="props">
                        <div v-if="item.id !== 'run_type' && item.id !== 'name' && item.id !== 'category'">
                            {{
                                (props.row[item.id] === '' || props.row[item.id] === null) ? '- -' : props.row[item.id]
                            }}
                        </div>
                        <div v-else-if="item.id === 'name'" style="color: #052150;cursor: pointer;font-weight: 400;text-decoration: underline;"
                            @click="handleOpenDetail(props.row)">{{ props.row[item.id] }}
                        </div>
                        <div v-else-if="item.id === 'category'">
                            <bk-tag
                                :key="each"
                                v-for="each in props.row[item.id]"
                                theme="info"
                            >{{ each }}
                            </bk-tag>
                        </div>
                    </template>
                </bk-table-column>
                <bk-table-column label="操作" width="180">
                    <template slot-scope="props">
                        <div style="display: flex;align-items: center;">
                            <bk-button class="mr10 btn-color" theme="primary" text @click="handleImplement(props.row)"
                                v-if="auth.operate">新建任务
                            </bk-button>
                            <bk-button class="mr10 btn-color" theme="primary" text @click="handleOpenUpdate(props.row)"
                                v-if="auth.modify">修改
                            </bk-button>
                            <bk-button class="mr10 btn-color" theme="primary" text @click="handleDelete(props.row)"
                                v-if="auth.del">删除
                            </bk-button>
                            <bk-popover ext-cls="dot-menu" placement="bottom-start" theme="dot-menu light"
                                trigger="click" :arrow="false" :distance="0" offset="15">
                                <span class="dot-menu-trigger"></span>
                                <ul class="dot-menu-list" slot="content">
                                    <li class="dot-menu-item" v-if="auth.modify" @click="handleClone(props.row)">克隆</li>
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
    </div>
</template>

<script>
    export default {
        data() {
            const fields = [{
                id: 'name',
                label: '作业流名',
                overflowTooltip: true,
                sortable: false
            }, {
                id: 'category',
                label: '分类',
                overflowTooltip: false,
                sortable: false
            }, {
                id: 'create_by',
                label: '创建者',
                overflowTooltip: false,
                sortable: false
            }, {
                id: 'create_time',
                label: '创建时间',
                overflowTooltip: true,
                sortable: true
            }, {
                id: 'update_time',
                label: '更新时间',
                overflowTooltip: true,
                sortable: true
            }, {
                id: 'description',
                label: '作业流描述',
                overflowTooltip: true,
                sortable: false
            }]
            return {
                maxTableHeight: '',
                auth: {},
                tableList: [],
                tableLoading: false,
                runSysList: [], // 跑批系统下拉列表
                selectionList: [], // 表格多选
                searchFrom: {
                    name: '', // 作业流名称
                    creator: '', // 创建人
                    category: '' // 跑批系统id
                },
                isDropdownShow: false,
                pagination: {
                    current: 1,
                    count: 1,
                    limit: 10
                },
                setting: {
                    size: 'small', // 表格大小
                    fields: fields, // 表格所有列
                    selectedFields: fields.slice(0, 6) // 表格当前显示列
                },
                searchData: [
                    {
                        name: '作业流名称',
                        id: 'name',
                        multiable: false,
                        children: []
                    },
                    {
                        name: '创建人',
                        id: 'create_by',
                        multiable: false,
                        children: []
                    }
                ],
                demo1: {
                    value: []
                }
            }
        },
        created() {
            this.getRunSysList()
            this.handleLoad()
            this.auth = this.hasPerm(this.$route.path)
            this.maxTableHeight = this.$store.state.common.defaultTableHeight - 52
        },
        methods: {
            // 处理克隆
            handleClone(row) {
                this.$router.push({
                    path: '/singlejobflow',
                    query: {
                        job_flow_data: row.id,
                        type: 'clone'
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
                        this.$api.process.delete(row.id).then(res => {
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
            // 处理跳转查看历史
            handleJumpHistory(row) {
                // this.$store.commit('changeTabActive', 'jobflowviewhistory')
                this.$router.push({
                    path: '/jobflowview',
                    query: {
                        job_flow_id: row.id
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
            // 处理表格size切换
            handlePageLimitChange(val) {
                this.pagination.current = 1
                this.pagination.limit = val
                this.handleLoad()
            },
            // 处理页面跳转
            handlePageChange(page) {
                this.pagination.current = page
                this.handleLoad()
            },
            // 处理执行
            handleImplement(row) {
                this.$router.push({
                    path: '/taskCreate',
                    query: {
                        job_flow_data: row.id,
                        job_name: row.name,
                        type: 'detail'
                    }
                })
            },
            // 处理打开修改
            handleOpenUpdate(row) {
                this.$router.push({
                    path: '/singlejobflow',
                    query: {
                        job_flow_data: row.id,
                        type: 'update'
                    }
                })
            },
            // 处理打开详情
            handleOpenDetail(row) {
                this.$router.push({
                    path: '/singlejobflow',
                    query: {
                        job_flow_data: row.id,
                        type: 'detail'
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
                window.open(window.siteUrl + '/export/process/?id=' + ids.join(','))
            },
            handleCreate() {
                this.$router.push({
                    path: '/singlejobflow',
                    query: {
                        type: 'add'
                    }
                })
            },
            // 处理搜索
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
            // 处理搜索重置
            handleReset() {
                this.searchFrom = {
                    name: '', // 作业流名称
                    creator: '', // 创建人
                    category: '' // 跑批系统id
                }
            },
            // 处理打开高级搜索
            handleOpenSeniorSearch() {
                this.isDropdownShow = !this.isDropdownShow
                // this.handleReset()
            },
            // 获取跑批系统下拉列表
            getRunSysList() {
                this.runSysList = []
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
            handleLoad() {
                this.tableLoading = true
                this.$api.process.list({
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
#jobFlowList {
    padding: 20px;
    height: 100%;
    overflow: auto;

    .header {
        width: 100%;
        font-size: 0;
        float: left;
        margin-bottom: 20px;
        // position: relative;

        .senior-search-box {
            background-color: #fff;
            padding: 20px;
            width: 100%;
            margin-top: 20px;
            float: left;
            box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, .1);
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
    border-bottom: 1px solid #07386d;
    border-top: 0;
    border-left: 0;
    border-right: 1px solid #07386d;
    border-bottom-right-radius: 6px;
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
