<template>
    <div>
        <div v-if="mode === 'DESIGN'">
            <bk-select class="max-fill" multiple v-model="value" :disabled="true"
                :placeholder="placeholder">
                <bk-option v-for="option in options"
                    :key="option.id"
                    :id="option.name"
                    :name="option.name">
                </bk-option>
            </bk-select>
        </div>
        <div v-else>
            <bk-select class="max-fill" multiple v-model="_value"
                :placeholder="placeholder">
                <bk-option v-for="option in options"
                    :key="option.id"
                    :id="option.name"
                    :name="option.name">
                </bk-option>
            </bk-select>
        </div>
    </div>
</template>

<script>
    import componentMinxins from '../ComponentMinxins'

    export default {
        name: 'multiple-select',
        components: {},
        mixins: [componentMinxins],
        props: {
            placeholder: {
                type: String,
                default: '请选择选项'
            },
            value: {
                type: Array,
                default: () => {
                    return []
                }
            },
            expanding: {
                type: Boolean,
                default: false
            },
            options: {
                type: Array,
                default: () => {
                    return []
                }
            }
        },
        data() {
            return {
                checks: []
            }
        },
        computed: {},
        methods: {}
    }
</script>

<style scoped>

</style>
