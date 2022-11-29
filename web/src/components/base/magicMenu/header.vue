<template>
    <div class="navigation-header">
        <div>
            <bk-popover v-for="(item,index) in header.list" :key="item.id" theme="light navigation-message" :arrow="false"
                offset="0, -5" placement="bottom" :tippy-options="{ 'hideOnClick': false, flipBehavior: ['bottom'] }">
                <li v-show="item.show" class="header-nav-item" :class="{ 'item-active': index === header.active }">
                    {{ item.name }}
                </li>
            </bk-popover>
        </div>
        <div>
            <bk-popover theme="light navigation-message" :arrow="false" placement="bottom" :tippy-options="{ 'hideOnClick': false }">
                <div class="header-user">
                    {{userData.username}}
                    <i class="bk-icon icon-down-shape"></i>
                </div>
                <template slot="content">
                    <ul class="monitor-navigation-admin" @click="handleUserListClick">
                        <li class="nav-item" v-for="userItem in user.list" :key="userItem" :data-key="userItem">
                            {{userItem}}
                        </li>
                    </ul>
                </template>
            </bk-popover>
        </div>
    </div>
</template>

<script>
    import {
        clearStore
    } from '../../../common/store.js'

    export default {
        data() {
            return {
                logout_url: '',
                pageTitle: '测试',
                userData: {
                    username: 'admin'
                },
                user: {
                    list: [
                        '退出'
                    ]
                },
                header: {
                    list: [
                        {
                            name: '节点管理',
                            id: 2,
                            show: true
                        },
                        {
                            name: '流程管理',
                            id: 3,
                            show: true
                        },
                        {
                            name: '任务管理',
                            id: 4,
                            show: true
                        },
                        {
                            name: '任务记录',
                            id: 5,
                            show: true
                        }
                        ],
                    active: 1
                }
            }
        },
        computed: {
        },
        created() {
            // this.loginUser()
        },
        methods: {
            changeTitle() {
            },
            handleUserListClick(e) {
                const btn = document.createElement('a')
                btn.setAttribute('href', this.logout_url)
                document.body.appendChild(btn)
                btn.click()
                clearStore()
            },
            loginUser() {
                this.$api.user.login().then(res => {
                    if (res.result) {
                        this.userData = res.data
                        this.logout_url = res.data.logout_url
                    }
                })
            }
        }
    }
</script>

<style scoped>
.navigation-header {
    display: flex;
    justify-content: space-between;
    width: 100%;
    align-items: center;
    font-size: 14px;
}

.monitor-navigation-header .header-user {
    height: 100%;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    -webkit-box-pack: center;
    -ms-flex-pack: center;
    justify-content: center;
    color: #96A2B9;
    /*       margin-left: 8px; */
}

.monitor-navigation-header .header-user .bk-icon {
    margin-left: 5px;
    font-size: 12px;
}

.monitor-navigation-header .header-user:hover {
    cursor: pointer;
    color: #3A84FF;
}

.monitor-navigation-admin {
    width: 170px;
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
.header-user:hover {
    cursor: pointer;
}
.monitor-navigation-admin .nav-item {
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
    list-style: none;
}

.monitor-navigation-admin .nav-item:hover {
    color: #3A84FF;
    cursor: pointer;
    background-color: #F0F1F5;
}

.header-nav-item {
    list-style: none;
    height: 50px;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin-right: 40px;
    color: #96A2B9;
    min-width: 56px;
}
.header-nav-item:hover {
    cursor: pointer;
    color: #000;
}
.header-nav-item::before {
    content: "";
    position: absolute;
    left: 25%;
    bottom: 10px;
    width: 0;
    height: 2px;
    background: #699DF4;
    transition: all .3s;
}
.header-nav-item:hover::before {
    width: calc(100% - 40px);
    left: 0;
    right: 0;
}
.item-active {
    color: #000;
}
.item-active::before {
    color: #000;
    content: "";
    position: absolute;
    left: 0;
    bottom: 10px;
    height: 2px;
    background: #699DF4;
    width: calc(100% - 40px);
}
</style>

<style>
.tippy-popper .tippy-tooltip.navigation-message-theme {
    padding: 0;
    border-radius: 0;
    -webkit-box-shadow: none;
    box-shadow: none;
}
</style>
