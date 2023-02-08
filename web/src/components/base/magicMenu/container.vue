<template>
    <div id="container">
        <div class="header-title" v-if="['home', 'login'].indexOf($route.name) === -1">
            <div v-if="$route.meta.hasOwnProperty('back')" class="header-title2">
                <span class="header-title-icon" @click="handleBack">
                    <svg class="icon"
                        style="width: 1em; height: 1em;vertical-align: middle;fill: currentColor;overflow: hidden;"
                        viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4756">
                        <path d="M416 480h320v64H416l96 96-48 48-176-176 176-176 48 48-96 96z" p-id="4757"></path>
                    </svg>
                </span>
                <div class="back-text2">{{ headerTitle }}</div>
            </div>
            <div v-else class="back-text">{{ headerTitle }}</div>
        </div>
        <router-view></router-view>
    </div>

</template>

<script>
    export default {
        data() {
            return {}
        },
        methods: {
            handleBack() {
                this.$router.go(-1)
            }
        },
        computed: {
            headerTitle() {
                let title = this.$route.meta.title
                if (title === '变量表') {
                    if (this.$route.query.type === 'detail') {
                        title = '变量表详情'
                    }
                    if (this.$route.query.type === 'update') {
                        title = '修改变量表'
                    }
                    if (this.$route.query.type === 'add') {
                        title = '新增变量表'
                    }
                } else if (title === '单个作业流') {
                    if (this.$route.query.type === 'detail') {
                        title = '单个作业流详情'
                    }
                    if (this.$route.query.type === 'update') {
                        title = '单个作业流修改'
                    }
                } else if (title === '单个作业') {
                    if (this.$route.query.type === 'update') {
                        title = '单个作业修改'
                    }
                } else if (title === '新建任务') {
                    if (this.$route.query.task_type === 'update') {
                        title = '修改任务'
                    }
                } else {
                    return title
                }
                return title
            },
        }
    }
</script>

<style scoped>
#container {
    height: calc(100vh - 100px);
}

.header-title {
    background-color: #FAFBFD;
    height: 40px;
    border-bottom: 1px solid #F5F7FA;
    flex-direction: row;
    align-items: center;
    display: flex;
}

.header-title2 {
    display: flex;
    flex-direction: row;
    align-items: center;
    height: 40px;
}

.header-title-icon {
    font-size: 30px;
    line-height: 24px;
    color: #699DF4;
    cursor: pointer;
    margin-left: 10px;
}

.back-text {
    font-size: 14px;
    color: #313238;
    margin-left: 22px;
}

.back-text2 {
    font-size: 14px;
    color: #465e65;
    margin-left: 3px;
}
</style>
