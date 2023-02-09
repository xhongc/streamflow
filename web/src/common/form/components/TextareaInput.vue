<template>
    <div>
        <div v-if="mode === 'DESIGN'">
            <div style="display: none;">123</div>
            <bk-input :disabled="true" :placeholder="placeholder" :rows="2" :type="'textarea'" v-model="value"></bk-input>
        </div>
        <div v-else>
            <bk-input v-model="_value" clearable :maxlength="255" :placeholder="placeholder"
                :rows="3" :type="'textarea'"></bk-input>
        </div>
    </div>
</template>

<script>
    import componentMinxins from '../ComponentMinxins'

    export default {
        name: 'textarea-input',
        components: {},
        mixins: [componentMinxins],
        props: {
            value: {
                type: String,
                default: null
            },
            placeholder: {
                type: String,
                default: '请输入内容'
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
        methods: {}
    }
</script>

<style scoped>

</style>
