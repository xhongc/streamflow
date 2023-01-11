<template>
    <div>
        <bk-form-item label="提示文字" :label-width="100">
            <bk-input v-model="value.placeholder" placeholder="请设置提示语"></bk-input>
        </bk-form-item>
        <bk-form-item label="输入值" :label-width="100">
            <bk-input placeholder="请输入" :rows="2" :type="'textarea'" v-model="value.value"></bk-input>

        </bk-form-item>
    </div>
</template>

<script>
    export default {
        name: 'textarea-input',
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
        methods: {}
    }
</script>

<style scoped>

</style>
