webpackJsonp([37],{"2J7Z":function(t,e){},"44e4":function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"newJob"}},[n("div",{staticClass:"content"},[n("p",{staticClass:"title"},[t._v("请选择新建作业方式")]),t._v(" "),n("div",{staticClass:"card-box"},[n("div",{staticClass:"card",staticStyle:{cursor:"pointer"},on:{click:function(e){return t.handleAddJob("single")}}},[n("i",{staticClass:"iconfont icon-mianxingtubiao-xinjiandangezuoye"}),t._v(" "),n("p",[t._v("通过定义单个作业的名称、描述、跑批系统、Agent等基本信息新建单个作业。")]),t._v(" "),t.auth.create?n("bk-button",{staticStyle:{"margin-top":"20px"},attrs:{"hover-theme":"primary"},on:{click:function(e){return t.handleAddJob("single")}}},[t._v("单个作业新建")]):t._e()],1),t._v(" "),n("div",{staticClass:"card",staticStyle:{"margin-left":"16px",cursor:"pointer"},on:{click:function(e){return t.handleAddJob("batch")}}},[n("i",{staticClass:"iconfont icon-mianxingtubiao-piliangzuoyeliudaoru"}),t._v(" "),n("p",[t._v("通过json文件定义作业的名称、跑批系统、Agent和基本信息批量新建作业。")]),t._v(" "),t.auth.create?n("bk-button",{staticStyle:{"margin-top":"20px"},attrs:{"hover-theme":"primary"},on:{click:function(e){return t.handleAddJob("batch")}}},[t._v("批量作业导入")]):t._e()],1)])])])},staticRenderFns:[]};var a=n("VU/8")({data:function(){return{auth:{}}},created:function(){this.auth=this.hasPerm(this.$route.path)},methods:{handleAddJob:function(t){"single"===t?this.$router.push({path:"/singlejob",query:{type:"add"}}):this.$router.push({path:"/multiplejob",query:{type:"add"}})}}},i,!1,function(t){n("2J7Z")},"data-v-03ac2689",null);e.default=a.exports}});