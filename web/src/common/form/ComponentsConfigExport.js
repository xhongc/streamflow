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
                    enablePrint: true,
                    key: ''
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
                    enablePrint: true,
                    key: ''
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
                    enablePrint: true,
                    key: ''
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
                    key: '',
                    options: [{id: 1, name: '选项1'}, {id: 2, name: '选项2'}]
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
                    value: [],
                    key: '',
                    options: [{id: 1, name: '选项1'}, {id: 2, name: '选项2'}]
                }
            },
            {
                title: '字典对象',
                name: 'DictMap',
                icon: 'iconfont icon-duoxuankuang',
                value: [],
                valueType: ValueType.object,
                props: {
                    required: false,
                    enablePrint: true,
                    expanding: false,
                    key: '',
                    defaultValue: []
                }
            }
        ]
    }
]

export default {
    baseComponents
}
