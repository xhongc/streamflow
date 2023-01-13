<template>
    <div>
        <div v-if="mode === 'DESIGN'">
            <bk-input disabled :placeholder="placeholder" type="number" v-model="value"></bk-input>
        </div>
        <div v-else>
            <bk-input v-model="_value" clearable :placeholder="placeholder" type="number"></bk-input>
        </div>
    </div>
</template>

<script>
    import componentMinxins from '../ComponentMinxins'

    export default {
        name: 'number-input',
        components: {},
        mixins: [componentMinxins],
        props: {
            value: {
                type: String,
                default: null
            },
            placeholder: {
                type: String,
                default: '请输入数值'
            }
        },
        data() {
            return {}
        },
        methods: {}
    }
</script>

<style scoped>

</style>
