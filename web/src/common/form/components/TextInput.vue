<template>
    <div>
        <div v-if="mode === 'DESIGN'">
            <bk-input :disabled="true" v-model="value" :placeholder="placeholder"></bk-input>
        </div>
        <div v-else>
            <bk-input :clearable="true" v-model="value" :placeholder="placeholder"></bk-input>
        </div>
    </div>
</template>

<script>
    import componentMinxins from '../ComponentMinxins'

    export default {
        name: 'text-input',
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
        methods: {}
    }
</script>

<style scoped>
</style>
