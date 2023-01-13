<template>
    <div>
        <bk-form-item label="提示文字" :label-width="100">
            <bk-input v-model="value.placeholder" placeholder="请设置提示语"></bk-input>
        </bk-form-item>
        <bk-form label-position="top">
            <bk-form-item label="选项设置" class="options" :label-width="100">
                <div class="option-item-label">
                    <bk-button size="small" icon="plus" class="mr10" :text="true"
                        @click="addOption">新选项
                    </bk-button>
                </div>
                <div v-for="(item, index) in value.defaultValue" :key="index" class="option-item">
                    <i class="el-icon-rank"></i>
                    <div class="dict-map">
                        <bk-input v-model="item.key" style="margin-right: 20px;">
                            <template slot="prepend">
                                <div class="group-text">Key</div>
                            </template>
                        </bk-input>
                        <bk-input v-model="item.value">
                            <template slot="prepend">
                                <div class="group-text">Value</div>
                            </template>
                        </bk-input>
                    </div>
                </div>
            </bk-form-item>
        </bk-form>
    </div>
</template>

<script>
    export default {
        name: 'dict-map-config',
        components: {},
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
        methods: {
            addOption() {
                console.log(this.value.value)
                this.value.defaultValue.push({key: '', value: ''})
            }
        }
    }
</script>

<style scoped>

</style>
