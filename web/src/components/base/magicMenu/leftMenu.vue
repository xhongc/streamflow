<template>
    <bk-navigation-menu ref="menu" :default-active="navName" :before-nav-change="beforeNavChange"
        :toggle-active="nav.toggle" :item-active-bg-color="'linear-gradient(90deg, rgb(17, 64, 108) 0%, rgb(17, 64, 108) 100%)'">
        <bk-navigation-menu-item v-for="item in nav.menuMap[navName]" :key="item.name"
            :has-child="item.children && !!item.children.length"
            :group="item.group" :icon="item.icon" :disabled="item.disabled" :url="item.to"
            :id="item.name" @click="handleRouterJump(item, false)">
            <span>{{ item.cnName }}</span>
            <div slot="child">
                <bk-navigation-menu-item :key="child.name" v-for="child in item.children" :id="child.name"
                    :disabled="child.disabled"
                    :icon="child.icon" :default-active="child.active"
                    @click="handleRouterJump(child, true)">
                    <span>{{ child.cnName }}</span>
                </bk-navigation-menu-item>
            </div>
        </bk-navigation-menu-item>
    </bk-navigation-menu>
</template>

<script>
    export default {
        data() {
            return {
                nav: {
                    menuMap: {
                        'JobList': [
                            {
                                'name': 'JobList',
                                'cnName': '节点列表',
                                'to': '/joblist',
                                'icon': 'iconfont icon-mianxingtubiao-fangkuai',
                                'hasChild': false,
                                'children': []
                            }
                        ],
                        'JobFlowList': [{
                            'name': 'VariableMgmt',
                            'cnName': '变量管理',
                            'to': '/variablemgmt',
                            'icon': 'iconfont icon-mianxingtubiao-mokuai',
                            'hasChild': false
                        },
                            {
                                'name': 'JobFlowList',
                                'cnName': '作业流列表',
                                'to': '/jobflowlist',
                                'icon': 'iconfont icon-mianxingtubiao-zuzhiguanli',
                                'hasChild': false
                            }],
                        'TaskList': [{
                            'name': 'TaskList',
                            'cnName': '任务管理',
                            'to': '/taskList',
                            'icon': 'iconfont icon-mianxingtubiao-zuoyejiankong',
                            'hasChild': false
                        }],
                        'JobMonitor': [{
                            'name': 'JobMonitor',
                            'cnName': '作业监视',
                            'to': '/jobmonitor',
                            'icon': 'iconfont icon-mianxingtubiao-yingyongqiang',
                            'hasChild': false
                        }]
                    },
                    id: '', // 当前激活侧边栏
                    toggle: true
                }
            }
        },
        mounted() {
        },
        computed: {
            navName() {
                const name = this.$route.meta.hasOwnProperty('fatherName') ? this.$route.meta.fatherName : this.$route.name
                console.log("cur:", name)
                return name
            }
        },
        methods: {
            beforeNavChange(newId, oldId) {
                return true
            },
            handleRouterJump(item) {
                this.$store.commit('getJobFlowHistorySearch', {})
                this.$store.commit('getJobFlowViewSearch', {})
                if (item.to === '/jobmonitor') {
                    this.$store.commit('changeTabActive', 'jobflowview')
                    return this.$router.push({
                        path: '/jobflowview'
                    })
                }
                if (item.to === '/jobhistory') {
                    this.$store.commit('changeTabActive', 'jobflowviewhistory')
                    return this.$router.push({
                        path: '/jobflowviewhistory'
                    })
                }
                this.$router.push({
                    path: `${item.to}`
                })
            }
        }
    }
</script>

<style>
/* 以下样式是为了适应例子父级的宽高而设置 */
.bk-navigation {
    /* width: 100vw; */
    width: 100% !important;
    /* width: 100vw; */
    height: 100vh;
    outline: 1px solid #ebebeb;
}

.bk-navigation .bk-navigation-wrapper {
    height: 100%;
    /* height: calc(100vh - 252px) !important; */
    width: 100%;
}

.monitor-navigation-nav {
    width: 150px;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    -ms-flex-direction: column;
    flex-direction: column;
    background: #FFFFFF;
    border: 1px solid #E2E2E2;
    -webkit-box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
    box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
    padding: 6px 0;
    margin: 0;
    color: #63656E;
}

.monitor-navigation-nav .nav-item {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 32px;
    flex: 0 0 32px;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    padding: 0 20px;
    list-style: none
}

.monitor-navigation-nav .nav-item:hover {
    color: #3A84FF;
    cursor: pointer;
    background-color: #F0F1F5;
}
</style>
