<template>
    <div>
        <div v-if="mode === 'DESIGN'">
            <bk-select class="max-fill" v-if="!expanding" multiple v-model="value" :disabled="true"
                :placeholder="placeholder">
                <bk-option v-for="option in options"
                    :key="option.id"
                    :id="option.id"
                    :name="option.name">
                </bk-option>
            </bk-select>
        </div>
        <div v-else>
            <bk-select class="max-fill" v-if="!expanding" multiple v-model="value" :disabled="true"
                :placeholder="placeholder">
                <bk-option v-for="option in options"
                    :key="option.id"
                    :id="option.id"
                    :name="option.name">
                </bk-option>
            </bk-select>
        </div>
    </div>
</template>

<script>
    import componentMinxins from '../ComponentMinxins'

    export default {
        name: 'select-input',
        components: {},
        mixins: [componentMinxins],
        props: {
            value: {
                type: String,
                default: null
            },
            placeholder: {
                type: String,
                default: '请选择选项'
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
            return {}
        },
        methods: {}
    }
</script>

<style scoped>

</style>
