<template>
    <div>
        <bk-form :label-width="90" v-if="form.name !== 'SpanLayout'">
            <bk-form-item label="表单名称" :label-width="100">
                <bk-input clearable v-model="form.title" />
            </bk-form-item>
            <bk-form-item label="英文名称" :label-width="100">
                <bk-input clearable v-model="form.props.key" />
            </bk-form-item>
            <component :is="form.name" v-model="form.props" />
            <bk-form-item label="必填项" :label-width="100">
                <bk-switcher v-model="form.props.required"></bk-switcher>
            </bk-form-item>
        </bk-form>
        <div v-else>当前组件不支持配置</div>
    </div>

</template>

<script>
    import TextInput from './config/TextInputConfig.vue'
    import NumberInput from './config/NumberInputConfig.vue'
    import AmountInput from './config/AmountInputConfig.vue'
    import TextareaInput from './config/TextareaInputConfig.vue'
    import MultipleSelect from './config/MultipleSelectConfig.vue'
    import SelectInput from './config/SelectInputConfig.vue'
    import DateTime from './config/DateTimeConfig.vue'
    import DateTimeRange from './config/DateTimeRangeConfig.vue'
    import ImageUpload from './config/ImageUploadConfig.vue'
    import FileUpload from './config/FileUploadConfig.vue'
    import Description from './config/DescriptionConfig.vue'
    import MoneyInput from './config/MoneyInputConfig.vue'
    import DictMap from './config/DictMapConfig.vue'
    // import DeptPicker from './config/OrgPickerConfig.vue'
    // import UserPicker from './config/OrgPickerConfig.vue'
    import TableList from './config/TableListConfig.vue'

    export default {
        name: 'form-component-config',
        components: {
            TextInput,
            NumberInput,
            AmountInput,
            TextareaInput,
            SelectInput,
            MultipleSelect,
            DateTime,
            DateTimeRange,
            ImageUpload,
            FileUpload,
            Description,
            MoneyInput,
            // DeptPicker,
            // UserPicker,
            TableList,
            DictMap
        },
        props: {
            form: {
                type: Object
            }
        },
        data() {
            return {}
        },
        computed: {
        },
        created() {
        },
        methods: {}
    }
</script>

<style scoped>

</style>
