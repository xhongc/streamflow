<template>
    <!--渲染表单-->
    <bk-form ref="form" class="process-form" label-position="top" :rules="rules" :model="_value">
        <bk-form-item v-if="item.name !== 'SpanLayout' && item.name !== 'Description'" :prop="item.id"
            :label="item.title" v-for="(item, index) in forms" :key="item.name + index">
            <form-design-render :ref="`sub-item_${item.id}`" v-model="_value[item.props.key]" :mode="mode" :config="item" />
        </bk-form-item>
        <form-design-render ref="span-layout" v-else v-model="_value" :mode="mode" :config="item" />
    </bk-form>
</template>

<script>
    import FormDesignRender from '@/views/job_monitor_large_screen/FormDesignRender'

    export default {
        name: 'form-render',
        components: {FormDesignRender},
        props: {
            forms: {
                type: Array,
                default: () => {
                    return []
                }
            },
            value: {
                type: Object,
                default: () => {
                    return {}
                }
            },
            mode: {
                type: String,
                default: 'PC'
            }
        },
        data() {
            return {
                rules: {}
            }
        },
        computed: {
            _value: {
                get() {
                    return this.value
                },
                set(val) {
                    this.$emit('input', val)
                }
            }
        },
        created() {
            this.loadFormConfig(this.forms)
        },
        methods: {
            validate(call) {
                let success = true
                this.$refs.form.validate(valid => {
                    success = valid
                    if (valid) {
                        // 校验成功再校验内部
                        for (let i = 0; i < this.forms.length; i++) {
                            if (this.forms[i].name === 'TableList') {
                                const formRef = this.$refs[`sub-item_${this.forms[i].id}`]
                                if (formRef && Array.isArray(formRef) && formRef.length > 0) {
                                    formRef[0].validate(subValid => {
                                        success = subValid
                                    })
                                    if (!success) {
                                        break
                                    }
                                }
                            }
                        }
                    }
                    call(success)
                })
            },
            loadFormConfig(forms) {
                forms.forEach(item => {
                    if (item.name === 'SpanLayout') {
                        this.loadFormConfig(item.props.items)
                    } else {
                        this.$set(this._value, item.id, this.value[item.id])
                        if (item.props.required) {
                            this.$set(this.rules, item.id, [{
                                type: item.valueType === 'Array' ? 'array' : undefined,
                                required: true,
                                message: `请填写${item.title}`,
                                trigger: 'blur'
                            }])
                        }
                    }
                })
            }
        }
    }
</script>

<style lang="scss" scoped>
.process-form {
    /deep/ .el-form-item__label {
        padding: 0 0;
    }
}
</style>
