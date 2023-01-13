<template>
    <div>
        <div v-if="mode === 'DESIGN'">
            <div v-for="(item, index) in value" :key="index">
                <div class="dict-map">
                    <bk-input v-model="item.key" style="margin-right: 20px;" disabled>
                        <template slot="prepend">
                            <div class="group-text">Key</div>
                        </template>
                    </bk-input>
                    <bk-input v-model="item.value" disabled>
                        <template slot="prepend">
                            <div class="group-text">Value</div>
                        </template>
                    </bk-input>
                </div>
            </div>
        </div>
        <div v-else>
            <div v-for="(item, index) in value" :key="index">
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
        </div>
    </div>
</template>

<script>
    import componentMinxins from '../ComponentMinxins'

    export default {
        name: 'dict-map',
        components: {},
        mixins: [componentMinxins],
        props: {
            value: {
                type: Array,
                default: () => {
                    return []
                }
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
.dict-map {
    display: flex;
    margin-bottom: 10px;
}
</style>
