<template>
    <div class="form-box">
        <div class="sub-box1">
            <div class="components-nav">
                <span @click="libSelect = 0">组件库</span>
            </div>
            <div>
                <div class="components" v-for="(group, i) in baseComponents" :key="i">
                    <p style="margin: 10px 0 10px 0;">{{ group.name }}</p>
                    <ul>
                        <draggable class="drag" :list="group.components" :options="{ sort: false }"
                            :group="{ name: 'form', pull: 'clone', put: false }"
                            @start="isStart = true" @end="isStart = false" :clone="clone">
                            <li v-for="(cp, id) in group.components" :key="id"
                                style="display: flex;flex-direction: row;">
                                <i :class="cp.icon"></i>
                                <span>{{ cp.title }}</span>
                            </li>
                        </draggable>
                    </ul>
                </div>
            </div>
        </div>
        <div class="sub-box2 layout-main">
            <div class="work-form">
                <div :class="{ 'mobile': showMobile, 'pc': !showMobile }">
                    <div :class="{ 'bd': showMobile }">
                        <div :class="{ 'form-content': showMobile }">
                            <div class="form">
                                <div class="tip" v-show="forms.length === 0 && !isStart">👈 请在左侧选择控件并拖至此处</div>
                                <draggable class="drag-from" :list="forms" group="form"
                                    :options="{ animation: 300, chosenClass: 'choose', sort: true }"
                                    @start="drag = true; selectFormItem = null" @end="drag = false">

                                    <div v-for="(cp, id) in forms" :key="id" class="form-item" @click="selectItem(cp)"
                                        :style="getSelectedClass(cp)">
                                        <div class="form-header">
                                            <p><span v-if="cp.props.required">*</span>{{ cp.title }}</p>
                                            <div class="option">
                                                <!--<i class="el-icon-copy-document" @click="copy"></i>-->
                                                <bk-icon type="close" @click="del(id)"></bk-icon>
                                            </div>
                                            <form-design-render :config="cp" v-model="cp.props.defaultValue"></form-design-render>
                                        </div>
                                    </div>
                                </draggable>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="sub-box3 layout-param">
            <div class="tool-nav-r" v-if="selectFormItem">
                <i :class="selectFormItem.icon" style="margin-right: 5px; font-size: medium;"></i>
                <span>{{ selectFormItem.title }}</span>
            </div>
            <div v-if="!selectFormItem || forms.length === 0" class="tip">
                选中控件后在这里进行编辑
            </div>
            <div style="text-align: left; padding: 0;margin-top: 10px;" v-else>
                <form-component-config :form="selectFormItem"></form-component-config>
            </div>
        </div>
        <bk-dialog width="800px" title="表单预览"
            v-model="viewFormVisible">
            <form-render ref="form" :forms="forms" v-model="formData"></form-render>
        </bk-dialog>
    </div>
</template>

<script>
    import draggable from 'vuedraggable'
    import FormRender from '@/common/form/FormRender'
    import FormDesignRender from '@/views/job_monitor_large_screen/FormDesignRender'
    import FormComponentConfig from '@/common/form/FormComponentConfig'
    import {baseComponents} from '@/common/form/ComponentsConfigExport'

    export default {
        name: 'form-design',
        components: {draggable, FormComponentConfig, FormDesignRender, FormRender},
        data() {
            return {
                formData: {},
                libSelect: 0,
                viewFormVisible: false,
                isStart: false,
                showMobile: false,
                baseComponents,
                select: null,
                drag: false,
                forms: [],
                selectFormItem: {
                    props: {
                        required: false,
                        enablePrint: true,
                        key: ''
                    }
                },
                nodeMap: []
            }
        },
        computed: {
        },
        methods: {
            copy(node, index) {
                this.form.splice(index + 1, 0, Object.assign({}, node))
            },
            getId() {
                return 'field' + (Math.floor(Math.random() * (99999 - 10000)) + 10000).toString() + new Date().getTime().toString().substring(5)
            },
            del(index) {
                this.$bkInfo({
                    title: '删除组件将会连带删除包含该组件的条件以及相关设置，是否继续?',
                    confirmLoading: false,
                    confirmFn: () => {
                        if (this.forms[index].name === 'SpanLayout') {
                            // 删除的是分栏则遍历删除分栏内所有子组件
                            this.forms[index].props.items.forEach(item => {
                                this.removeFormItemAbout(item)
                            })
                            this.forms[index].props.items.length = 0
                        } else {
                            this.removeFormItemAbout(this.forms[index])
                        }
                        this.forms.splice(index, 1)
                    }
                })
            },
            async removeFormItemAbout(item) {
                this.nodeMap.forEach(node => {
                    // 搜寻条件，进行移除
                    if (node.type === 'CONDITION') {
                        node.props.groups.forEach(group => {
                            const i = group.cids.remove(item.id)
                            if (i > -1) {
                                // 从子条件移除
                                group.conditions.splice(i, 1)
                            }
                        })
                    }
                    // 搜寻权限，进行移除
                    if (node.type === 'ROOT' || node.type === 'APPROVAL' || node.type === 'CC') {
                        node.props.formPerms.removeByKey('id', item.id)
                        if (node.props.formUser === item.id) {
                            node.props.formUser = ''
                        }
                    }
                })
            },
            clone(obj) {
                obj.id = this.getId()
                return JSON.parse(JSON.stringify(obj))
            },
            viewForms() {
                this.viewFormVisible = true
            },
            selectItem(cp) {
                this.selectFormItem = cp
            },
            getSelectedClass(cp) {
                return this.selectFormItem && this.selectFormItem.id === cp.id ? 'border-left: 4px solid #409eff' : ''
            },
            validateItem(err, titleSet, item) {
                console.log(titleSet, item)
                if (!item.props.key) {
                    err.push(`${item.title} 英文名称不能为空`)
                } else {
                    if (titleSet.has(item.props.key)) {
                        err.push(`表单 ${item.title} 英文名称重复`)
                    } else {
                        titleSet.add(item.props.key)
                    }
                }
                if (item.name === 'SelectInput' || item.name === 'MultipleSelect') {
                    if (item.props.options.length === 0) {
                        err.push(`${item.title} 未设置选项`)
                    }
                } else if (item.name === 'TableList') {
                    if (item.props.columns.length === 0) {
                        err.push(`明细表 ${item.title} 内未添加组件`)
                    }
                } else if (item.name === 'SpanLayout') {
                    if (item.props.items.length === 0) {
                        err.push('分栏内未添加组件')
                    } else {
                        item.props.items.forEach(sub => this.validateItem(err, titleSet, sub))
                    }
                }
            },
            validate() {
                const err = []
                if (this.forms.length > 0) {
                    const titleSet = new Set()
                    this.forms.forEach(item => {
                        // 主要校验表格及分栏/选择器/表单名称/是否设置
                        this.validateItem(err, titleSet, item)
                    })
                } else {
                    // err.push('表单为空，请添加组件')
                }
                return err
            }
        }
    }
</script>

<style lang="scss" scoped>
.choose {
    border: 1px dashed #000000 !important;
}

.process-form {
    /deep/ .el-form-item__label {
        padding: 0 0;
    }
}

.components-nav {
    box-sizing: content-box;
    display: flex;
    align-items: center;
    margin: 12px 12px 0;
    height: 28px;
    box-shadow: 0 2px 4px 0 rgba(17, 31, 44, 0.04);
    border: 1px solid #ecedef;
    border-radius: 16px;
    background-color: #fff;

    .selected {
        color: #000000;
    }

    .border {
        border-left: 1px solid #f5f6f6;
        border-right: 1px solid #f5f6f6;
    }

    span {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        font-size: 12px;
        color: rgba(17, 31, 44, 0.72);
        cursor: pointer;

        &:hover {
            color: #000000;
        }
    }
}

.components {
    overflow-x: hidden;
    overflow-y: scroll;
    //margin-top: 20px;
    //padding: 0 20px;
    font-size: 12px;
    width: 100%;
    color: rgba(17, 31, 44, 0.85);

    & > p {
        padding: 0 20px;
    }

    .drag {
        margin-left: 20px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;

        li {
            text-align: center;
            display: flex;
            align-items: center;
            width: 124px;
            height: 38px;
            margin-bottom: 12px;
            border: 1px solid #C4C6CC;
            border-radius: 8px;
            cursor: grab;
            background-color: #fff;

            &:hover {
                border: 1px solid #000000;
                color: #000000;
            }

            i {
                margin: 0 12px;
            }
        }

        li:nth-child(odd) {
            margin-right: 8px;
        }
    }
}

/deep/ .el-main {
    padding: 0;
}

.layout-main {
    background-color: #feffff;

    .tool-nav {
        font-size: medium;
        padding: 8px 20px;
        background: #fafafb;
        border-bottom: 1px solid #ebecee;

        div:first-child {
            display: inline-block;
            text-align: left;

            i {
                margin-right: 10px;
            }
        }

        div:last-child {
            float: right;

            i {
                margin-left: 10px;
            }
        }

        i {
            color: #7a7a7a;
            cursor: pointer;

            &:hover {
                color: #4b4b4b;
            }
        }
    }

    .work-form {
        margin: 0 auto;
        height: 100%;
        overflow-y: auto;
        background: rgb(245, 246, 246);
        border-left: 1px solid rgb(235, 236, 238);
        border-right: 1px solid rgb(235, 236, 238);
        padding: 10px;

        .pc {
            margin-top: 2%;

            .drag-from {
                height: calc(100vh - 450px);
                background-color: rgb(245, 246, 246);

                .form-item, li {
                    cursor: grab;
                    background: #ffffff;
                    padding: 10px;
                    border: 1px solid #ebecee;
                    margin: 5px 0;
                }
            }
        }

        .mobile {
            margin-left: auto;
            margin-right: auto;
            width: 360px;
            max-height: 640px;
            margin-top: 4%;
            border-radius: 24px;
            box-shadow: 0 8px 40px 0 rgba(17, 31, 44, 0.12);

            .bd {
                border: 1px solid rgba(17, 31, 44, 0.08);
                border-radius: 24px;
                padding: 10px 10px;
                background-color: #ffffff;

                .form-content {
                    padding: 3px 2px;
                    border-radius: 14px;
                    background-color: #f2f4f5;

                    .drag-from {
                        width: 100%;
                        height: calc(100vh - 190px);
                        min-height: 200px;
                        max-height: 600px;
                    }

                    .form {
                        overflow-y: auto;
                        width: 100%;
                        display: inline-block;
                        max-height: 640px;

                        .form-item, li {
                            border: 1px solid #ffffff;
                            list-style: none;
                            background: #ffffff;
                            padding: 10px;
                            margin: 5px 0;
                            cursor: grab;
                        }
                    }
                }
            }
        }

        .tip {
            //float: left;
            margin: 0 auto;
            width: 65%;
            max-width: 400px;
            padding: 35px 20px;
            border-radius: 10px;
            border: 1px dashed rgba(25, 31, 37, 0.12);
            margin-top: 50px;
            text-align: center;
            font-size: 14px;
            color: rgb(122, 122, 122);
            z-index: 9999;

            &:hover {
                border: 1px dashed #000000;
            }
        }
    }

}

.layout-param {
    text-align: center;
    font-size: 14px;
    color: rgb(122, 122, 122);

    .tool-nav-r {
        text-align: left;
        font-size: small;
        border-left: 1px solid #ebecee;
        padding: 10px 20px;
        background: #fafafb;
        border-bottom: 1px solid #ebecee;
    }

    .tip {
        margin-top: 150px;
    }
}

.flip-list-move {
    transition: transform 0.5s;
}

.no-move {
    transition: transform 0s;
}

.select {
    color: #4b4b4b !important;
}

.form-header {
    font-size: small;
    color: #818181;
    text-align: left;
    position: relative;
    background-color: #fff;

    p {
        position: relative;
        margin: 0 0 10px 0;

        span {
            position: absolute;
            left: -8px;
            top: 3px;
            color: rgb(217, 0, 19);
        }
    }

    .option {
        position: absolute;
        top: -10px;
        right: -10px;

        i {
            font-size: large;
            cursor: pointer;
            color: #8c8c8c;
            padding: 5px;

            &:hover {
                color: #f56c6c;
            }
        }
    }
}

::-webkit-scrollbar {
    width: 4px;
    height: 4px;
    background-color: #f8f8f8;
}

::-webkit-scrollbar-thumb {
    border-radius: 16px;
    background-color: #e8e8e8;
}

.form-box {
    display: flex;
    width: 100%;
    height: calc(100vh - 280px);
}

.sub-box1 {
    width: 23%;
}

.sub-box2 {
    flex: 1;
}

.sub-box3 {
    width: 20%;
}
</style>
