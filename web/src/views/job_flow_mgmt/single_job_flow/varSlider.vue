<template>
    <div v-bkloading="{ isLoading: baseInfoLoading, zIndex: 999999 }">
        <bk-table ref="table" :data="varTableList" ext-cls="customTable">
            <bk-table-column label="变量类型" prop="type" :show-overflow-tooltip="true" align="center">
                <template slot-scope="props">
                    <span v-if="props.row.type === 'common'">普通变量</span>
                    <span v-if="props.row.type === 'sensitive'">敏感变量</span>
                </template>
            </bk-table-column>
            <bk-table-column label="变量名" prop="name" :show-overflow-tooltip="true" align="center">
                <template slot-scope="props">
                    <span>{{props.row.name}}</span>
                </template>
            </bk-table-column>
            <bk-table-column label="变量值（默认值）" prop="value" :show-overflow-tooltip="true" align="center">
                <template slot-scope="props">
                    <span>{{props.row.value}}</span>
                </template>
            </bk-table-column>
        </bk-table>
    </div>
</template>

<script>
    export default {
        inject: ['father_this'],
        data() {
            return {
                baseInfoLoading: false,
                varTableList: []
            }
        },
        created() {
            console.log(this.father_this.$refs.baseInfo.form.var_table)
            const params = {
                'ids': this.father_this.$refs.baseInfo.form.var_table
            }
            this.fetchVarTable(params)
        },
        mounted() {
        },
        methods: {
            fetchVarTable(params) {
                this.baseInfoLoading = true
                this.$api.varTable.group(params).then(res => {
                    this.baseInfoLoading = false
                    this.varTableList = res.data
                    console.log(res)
                })
            }
        }
    }
</script>

<style lang="scss" scoped>
#baseInfo {
    /deep/ .custom-form-item {
        display: none;
    }

    .pre-commands {
        display: flex;

        i {
            font-size: 32px;
            color: #979BA5;
            width: 32px;
            text-align: center;
            height: 32px;
            line-height: 32px;
            cursor: pointer;

            &:active {
                color: rgb(58, 132, 255);
            }
        }
    }
}
</style>
