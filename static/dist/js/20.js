webpackJsonp([20],{cPaS:function(t,n){},sRD9:function(t,n,a){"use strict";Object.defineProperty(n,"__esModule",{value:!0});var e={render:function(){var t=this,n=t.$createElement,a=t._self._c||n;return a("div",{attrs:{id:"newJobFlow"}},[a("div",{staticClass:"content"},[a("p",{staticClass:"title"},[t._v("请选择新建作业流方式")]),t._v(" "),a("div",{staticClass:"card-box"},[a("div",{staticClass:"card",staticStyle:{cursor:"pointer"},on:{click:function(n){return t.handleAddJobFlow("single")}}},[a("i",{staticClass:"iconfont icon-mianxingtubiao-xinjiandangezuoyeliu"}),t._v(" "),a("p",[t._v("通过定义作业流的名称、调度方式、前置依赖和任务编排等信息新建单个作业流。")]),t._v(" "),t.auth.create?a("bk-button",{staticStyle:{"margin-top":"20px"},attrs:{"hover-theme":"primary"},on:{click:function(n){return t.handleAddJobFlow("single")}}},[t._v("单个作业流新建")]):t._e()],1),t._v(" "),a("div",{staticClass:"card",staticStyle:{"margin-left":"16px",cursor:"pointer"},on:{click:function(n){return t.handleAddJobFlow("batch")}}},[a("i",{staticClass:"iconfont icon-mianxingtubiao-piliangzuoyedaoru"}),t._v(" "),a("p",[t._v("通过json文件定义作业流名称、调度方式、作业节点的关联和前置依赖等信息批量新建作业流。")]),t._v(" "),t.auth.create?a("bk-button",{staticStyle:{"margin-top":"20px"},attrs:{"hover-theme":"primary"},on:{click:function(n){return t.handleAddJobFlow("batch")}}},[t._v("批量作业流导入")]):t._e()],1)])])])},staticRenderFns:[]};var i=a("VU/8")({data:function(){return{auth:{}}},created:function(){this.auth=this.hasPerm(this.$route.path)},methods:{handleAddJobFlow:function(t){"single"===t?this.$router.push({path:"/singlejobflow",query:{type:"add"}}):this.$router.push({path:"/multiplejobflow",query:{type:"add"}})}}},e,!1,function(t){a("cPaS")},"data-v-75637a1f",null);n.default=i.exports}});