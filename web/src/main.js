// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
// 按需引入 bk-magic-vue
import bkMagic from 'bk-magic-vue'

// 全量引入 bk-magic-vue 样式
import 'bk-magic-vue/dist/bk-magic-vue.min.css'

import App from './App'
import router from './router'
import store from './vuex'
import axios from 'axios'
import 'view-design/dist/styles/iview.css'
// 按需引入iview css
// import './components/iview/drawer.css'
// 按需引入iview
import './components/iview/index'
// 几何图
import * as Echarts from 'echarts'
import G6 from '@antv/g6'
// 引用API文件
import api from './api/index'
// 时间格式化插件
// import moment from 'moment'
// filter统一引入
import './fiter/index.js'
// 统一样式引入
// import './assets/index'
import cwMessage from './common/message'
// 引入自定义组件1
// import Component from './components/index.js'
// vuex
import '@/vuex/index' // 全局
// import './promission.js' // 路由后台获取
import {hasPermission} from './promission.js' // 路由后台获取
// 引入jquery
// import $ from 'jquery'
// 引入字体图标库
import 'font-awesome/css/font-awesome.min.css'
// 引入lodash
import lodash from 'lodash'
// 引入自定义icon 图标
import './assets/custom_icon/iconfont.css'
// import '../static/cw-icon/iconfont.css'
import 'echarts/dist/extension/dataTool'
import VeeValidate, {Validator} from 'vee-validate'
import cron from '@/assets/js/cron-validator.js'

const config = {
    errorBagName: 'veeErrors',
    fieldsBagName: 'veeFields'
}
Vue.use(bkMagic)

Vue.use(VeeValidate, config)
Vue.use(Echarts)
Vue.use(G6)
// Vue.use(Component)
Vue.use(axios)
Vue.prototype.$echarts = Echarts
Vue.prototype.$G6 = G6
// Vue.prototype.$moment = moment
Vue.prototype.$cwMessage = cwMessage
// 将API方法绑定到全局
// Vue.prototype.$http = axios
Vue.prototype.$api = api
Vue.prototype.$lodash = lodash
Vue.prototype.hasPerm = hasPermission
Vue.config.productionTip = false
Vue.prototype.cloneDeep = function(data) {
    return lodash.cloneDeep(data)
}
Vue.prototype.setCookie = function(name, value, day) {
    if (day !== 0) {
        const expdate = new Date()
        expdate.setTime(expdate.getTime() + 7 * 24 * 60 * 60 * 1000)
        document.cookie = name + '=' + escape(value) + ';expires=' + expdate.toGMTString()
    } else {
        document.cookie = name + '=' + escape(value)
    }
}
Vue.prototype.getCookie = function(name) {
    const reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)')
    const arr = document.cookie.match(reg)
    if (arr) {
        return unescape(arr[2])
    } else {
        return null
    }
}
Validator.extend('cronRlue', {
    getMessage: (field, args) => args + '输入定时表达式非法，请校验',
    validate: value => cron.validate(value).status
})
Validator.extend('integer', {
    getMessage: (field, args) => args + '间隔时间必须是正整数',
    validate: value => Number(value) >= 1 && Number(value) % 1 === 0
})
/* eslint-disable no-new */
const vue = new Vue({
    el: '#app',
    router,
    store,
    components: {App},
    data() {
        return {
            website: '我是全局变量'
        }
    },
    template: '<App/>'
})
export default vue
