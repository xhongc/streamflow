<template>
    <div>
        <bk-form-item label="提示文字" :label-width="100">
            <bk-input v-model="value.placeholder" placeholder="请设置提示语"></bk-input>
        </bk-form-item>
        <bk-form label-position="top">
            <bk-form-item label="选项设置" class="options" :label-width="100">
                <div class="option-item-label">
                    <span>选项设置</span>
                    <bk-button size="small" icon="plus" class="mr10" :text="true"
                        @click="value.options.push('新选项')">新选项
                    </bk-button>
                </div>
                <draggable :list="value.options" group="option" handler=".el-icon-rank" :options="dragOption">
                    <div v-for="(op, index) in value.options" :key="index" class="option-item">
                        <i class="el-icon-rank"></i>
                        <bk-input v-model="value.options[index]" size="medium" placeholder="请设置选项值" clearable>
                            <template slot="append">
                                <bk-button size="small" icon="delete" :text="true"
                                    @click="value.options.splice(index, 1)">
                                </bk-button>
                            </template>
                        </bk-input>
                    </div>
                </draggable>
            </bk-form-item>
        </bk-form>
        <bk-form-item label="选项展开" :label-width="100">
            <bk-switcher v-model="value.expanding"></bk-switcher>
        </bk-form-item>

    </div>
</template>

<script>
    import draggable from 'vuedraggable'

    export default {
        name: 'select-input-config',
        components: {draggable},
        props: {
            value: {
                type: Object,
                default: () => {
                    return {}
                }
            }
        },
        data() {
            return {
                dragOption: {
                    animation: 300,
                    sort: true
                }
            }
        },
        methods: {}
    }
</script>

<style lang="scss" scoped>
/deep/ .options {
    .el-form-item__label {
        display: block;
        width: 100%;
        text-align: left;
    }

    .el-icon-rank {
        padding-right: 5px;
        cursor: move;
    }

    .option-item {
        .el-input {
            width: 250px;
            float: right;
        }
    }
}

.option-item-label {
    height: 30px;
    line-height: 30px;

    button {
        float: right;
    }
}

/*/deep/ .el-form-item {
  margin-bottom: 10px;

  .el-form-item__label {
    padding: 0;
  }
  .options{
    .el-icon-rank{
      cursor: move;
    }
  }
}*/
</style>
