webpackJsonp([22],{"3rZQ":function(t,a,e){"use strict";Object.defineProperty(a,"__esModule",{value:!0});var o={render:function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{directives:[{name:"bkloading",rawName:"v-bkloading",value:{isLoading:t.scanFileLoading,zIndex:10},expression:"{ isLoading: scanFileLoading, zIndex: 10 }"}],attrs:{id:"scanFile"}},[e("div",{staticClass:"content-box"},[e("div",{staticClass:"title"},[t._v("导入结果")]),t._v(" "),e("div",{staticClass:"job-info"},[e("p",{staticStyle:{width:"152px"}},[t._v("作业流配置检测：OK")]),t._v(" "),0!==t.createData.length?e("p",{staticClass:"mt16"},[t._v("新增作业数："),e("span",[t._v(t._s(t.createData.length))])]):t._e(),t._v(" "),0!==t.updateData.length?e("p",{staticClass:"mt16"},[t._v("修改作业数："),e("span",[t._v(t._s(t.updateData.length))])]):t._e(),t._v(" "),0!==t.messageData.length?e("p",{staticClass:"mt16"},[t._v("异常作业数："),e("span",[t._v(t._s(t.messageData.length))])]):t._e()])]),t._v(" "),0!==t.createData.length?e("div",{staticClass:"content-box"},[e("div",{staticClass:"title"},[t._v("新增作业")]),t._v(" "),e("div",{staticClass:"table"},[e("bk-table",{ref:"table",attrs:{data:t.createData}},[e("bk-table-column",{attrs:{label:"作业名",prop:"name"}}),t._v(" "),e("bk-table-column",{attrs:{label:"Agent",prop:"agent.name","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"IP",prop:"agent.data.bk_host_innerip"}}),t._v(" "),e("bk-table-column",{attrs:{label:"系统类型",prop:"agent.data.bk_os_name","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"执行账号",prop:"account","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"脚本",prop:"script_content","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"作业描述",prop:"desc","show-overflow-tooltip":!0}})],1)],1)]):t._e(),t._v(" "),0!==t.updateData.length?e("div",{staticClass:"content-box"},[e("div",{staticClass:"title"},[t._v("修改作业")]),t._v(" "),e("div",{staticClass:"table"},[e("bk-table",{ref:"table",attrs:{data:t.updateData}},[e("bk-table-column",{attrs:{label:"作业名",prop:"name"}}),t._v(" "),e("bk-table-column",{attrs:{label:"Agent",prop:"agent.name","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"IP",prop:"agent.data.bk_host_innerip"}}),t._v(" "),e("bk-table-column",{attrs:{label:"系统类型",prop:"agent.data.bk_os_name","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"执行账号",prop:"account","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"脚本",prop:"script_content","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"作业描述",prop:"desc","show-overflow-tooltip":!0}})],1)],1)]):t._e(),t._v(" "),0!==t.messageData.length?e("div",{staticClass:"content-box"},[e("div",{staticClass:"title"},[t._v("异常作业")]),t._v(" "),e("div",{staticClass:"table"},[e("bk-table",{ref:"table",attrs:{data:t.messageData}},[e("bk-table-column",{attrs:{label:"作业名",prop:"name"}}),t._v(" "),e("bk-table-column",{attrs:{label:"Agent",prop:"ip.name","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"IP",prop:"ip.bk_host_innerip"}}),t._v(" "),e("bk-table-column",{attrs:{label:"系统类型",prop:"ip.bk_os_name","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"执行账号",prop:"account","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"脚本",prop:"script_content","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"作业描述",prop:"desc","show-overflow-tooltip":!0}}),t._v(" "),e("bk-table-column",{attrs:{label:"错误信息",prop:"message","show-overflow-tooltip":!0}})],1)],1)]):t._e(),t._v(" "),e("div",{staticClass:"footer"},[e("bk-button",{staticStyle:{"margin-right":"12px"},attrs:{theme:"primary"},on:{click:t.handleSave}},[t._v("保存")]),t._v(" "),e("bk-button",{on:{click:t.handleCancel}},[t._v("取消本次上传")])],1)])},staticRenderFns:[]};var l=e("VU/8")({data:function(){return{createData:[],updateData:[],messageData:[],scanFileLoading:!1}},created:function(){this.$route.params.data?this.handleCheckData():this.$cwMessage("请上传文件！","error")},methods:{handleSave:function(){var t=this;this.scanFileLoading=!0,this.$api.content.save_job_data({update:this.updateData,create:this.createData}).then(function(a){a.result?(t.$cwMessage("添加成功！","success"),t.$router.push({path:"/joblist"})):t.$cwMessage(a.message,"error"),t.scanFileLoading=!1})},handleCancel:function(){this.$router.go(-1)},handleCheckData:function(){var t=this;this.scanFileLoading=!0,this.$api.content.check_job(this.$route.params).then(function(a){a.result?(t.createData=a.data.create,t.updateData=a.data.update,t.messageData=a.data.message):t.$cwMessage(a.message,"error"),t.scanFileLoading=!1})}}},o,!1,function(t){e("76Js")},"data-v-62fae0fd",null);a.default=l.exports},"76Js":function(t,a){}});