<template>
    <div>
        {{config.props}}
        <component ref="form" :is="config.name" :mode="mode" v-bind="config.props" />
    </div>
</template>
<script>

    import components from '@/common/form/ComponentExport'

    export default {
        name: 'from-render',
        components: components,
        props: {
            mode: {
                type: String,
                default: 'DESIGN'
            },
            value: {
                default: undefined,
                type: String
            },
            config: {
                type: Object,
                default: () => {
                    return {}
                }
            }
        },
        data() {
            return {}
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
        methods: {
            validate(call) {
                this.$refs.form.validate(call)
            }
        }
    }
</script>

<style lang="scss" scoped>

</style>
