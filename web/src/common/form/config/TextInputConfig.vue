<template>
    <div>
        <bk-form-item label="提示文字" :label-width="100">
            <bk-input v-model="value.placeholder" placeholder="请设置提示语"></bk-input>
        </bk-form-item>
        <bk-form-item label="默认值" :label-width="100">
            <bk-input clearable v-model="value.defaultValue"></bk-input>
        </bk-form-item>
    </div>
</template>

<script>
    export default {
        name: 'text-input',
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
            return {}
        },
        computed: {
        },
        methods: {}
    }
</script>

<style scoped>

</style>
