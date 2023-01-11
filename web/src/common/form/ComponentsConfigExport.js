export const ValueType = {
    string: 'String',
    object: 'Object',
    array: 'Array',
    number: 'Number',
    date: 'Date',
    user: 'User',
    dept: 'Dept',
    dateRange: 'DateRange'
}

export const baseComponents = [
    {
        name: '基础组件',
        components: [
            {
                title: '单行文本输入',
                name: 'TextInput',
                icon: 'el-icon-edit',
                value: '',
                valueType: ValueType.string,
                props: {
                    required: false,
                    enablePrint: true
                }
            },
            {
                title: '多行文本输入',
                name: 'TextareaInput',
                icon: 'el-icon-more-outline',
                value: '',
                valueType: ValueType.string,
                props: {
                    required: false,
                    enablePrint: true
                }
            },
            {
                title: '数字输入框',
                name: 'NumberInput',
                icon: 'el-icon-edit-outline',
                value: '',
                valueType: ValueType.number,
                props: {
                    required: false,
                    enablePrint: true
                }
            },
            {
                title: '单选框',
                name: 'SelectInput',
                icon: 'el-icon-circle-check',
                value: '',
                valueType: ValueType.string,
                props: {
                    required: false,
                    enablePrint: true,
                    expanding: false,
                    options: ['选项1', '选项2']
                }
            },
            {
                title: '多选框',
                name: 'MultipleSelect',
                icon: 'iconfont icon-duoxuankuang',
                value: [],
                valueType: ValueType.array,
                props: {
                    required: false,
                    enablePrint: true,
                    expanding: false,
                    options: ['选项1', '选项2']
                }
            }
        ]
    }
]

export default {
    baseComponents
}
