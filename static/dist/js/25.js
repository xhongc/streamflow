webpackJsonp([25],{"/2MP":function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var o=a("mvHQ"),s=a.n(o),r={components:{editor:a("VzGs").a},data:function(){return{jobDetailLoading:!1,form:{name:"",state:"",executor:"",station:"",eta:"",start_time:"",end_time:"",total_time:"",log:"",script_content:"",upstream_nodes:[],downstream_nodes:[]},stateList:[{id:1,name:"wait",label:"等待"},{id:2,name:"run",label:"正在执行"},{id:3,name:"fail",label:"失败"},{id:4,name:"error",label:"错误"},{id:5,name:"success",label:"成功"},{id:6,name:"pause",label:"挂起"},{id:7,name:"stop",label:"终止"},{id:8,name:"cancel",label:"取消"},{id:9,name:"need_confirm",label:"待复核"},{id:10,name:"ignore",label:"忽略"}]}},created:function(){this.handleLoad()},methods:{handleLoad:function(){var t=this;this.jobDetailLoading=!0,this.$api.nodeHistory.retrieve(parseInt(this.$route.query.id)).then(function(e){e.result?(t.form=e.data,t.form.hasOwnProperty("log")&&t.$refs.editorLog.monacoEditor.setValue(t.form.log),t.form.hasOwnProperty("script_content")&&t.$refs.editorScript.monacoEditor.setValue(t.form.script_content),t.form.hasOwnProperty("pre_commands")&&t.$refs.editorPrecommd.monacoEditor.setValue(s()(t.form.pre_commands))):t.$cwMessage(e.message,"error"),t.jobDetailLoading=!1})}}},l={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{directives:[{name:"bkloading",rawName:"v-bkloading",value:{isLoading:t.jobDetailLoading,zIndex:10},expression:"{ isLoading: jobDetailLoading, zIndex: 10 }"}],attrs:{id:"jobViewDetail"}},[a("div",{staticClass:"box"},[a("p",{staticClass:"title"},[t._v("基本信息")]),t._v(" "),a("bk-container",[a("bk-form",{attrs:{"label-width":130}},[a("bk-row",[a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"作业名称:"}},[t._v(t._s(t.form.name))])],1),t._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"作业状态:"}},[""!==t.form.state?a("span",[t._v(t._s(t.stateList[t.stateList.findIndex(function(e){return e.name===t.form.state})].label))]):t._e()])],1),t._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"启动人:"}},[t._v(t._s(t.form.executor))])],1),t._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"计划开始时间:"}},[t._v(t._s(t.form.station))])],1)],1),t._v(" "),a("bk-row",[a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"计划开始时间:"}},[t._v(t._s(t.form.eta))])],1),t._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"实际开始时间:"}},[t._v(t._s(t.form.start_time))])],1),t._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"完成时间:"}},[t._v(t._s(t.form.end_time))])],1),t._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"总共耗时:"}},[t._v(t._s(t.form.total_time))])],1)],1)],1)],1)],1),t._v(" "),a("div",{staticClass:"box"},[a("p",{staticClass:"title"},[t._v("执行日志")]),t._v(" "),a("editor",{ref:"editorLog",attrs:{height:"200px",codes:t.form.log,"read-only":!0,language:"shell"}})],1),t._v(" "),a("div",{staticClass:"box"},[a("p",{staticClass:"title"},[t._v("执行脚本")]),t._v(" "),a("editor",{ref:"editorScript",attrs:{height:"200px",codes:t.form.script_content,"read-only":!0,language:"shell"}})],1),t._v(" "),a("div",{staticClass:"box"},[a("p",{staticClass:"title"},[t._v("前置命令检测")]),t._v(" "),a("editor",{ref:"editorPrecommd",attrs:{height:"200px","read-only":!0,language:"json"}})],1),t._v(" "),a("div",{staticClass:"box"},[a("p",{staticClass:"title"},[t._v("先行作业/作业流")]),t._v(" "),a("bk-table",{attrs:{data:t.form.upstream_nodes,"ext-cls":"customTable"}},[a("bk-table-column",{attrs:{prop:"type",label:"类型"}}),t._v(" "),a("bk-table-column",{attrs:{prop:"name",label:"名称"}}),t._v(" "),a("bk-table-column",{attrs:{prop:"station",label:"Agent"}}),t._v(" "),a("bk-table-column",{attrs:{prop:"state",label:"状态"}}),t._v(" "),a("bk-table-column",{attrs:{prop:"eta",label:"计划开始时间"}}),t._v(" "),a("bk-table-column",{attrs:{prop:"start_time",label:"实际开始时间"}}),t._v(" "),a("bk-table-column",{attrs:{prop:"end_time",label:"实际完成时间"}})],1)],1),t._v(" "),a("div",{staticClass:"box"},[a("p",{staticClass:"title"},[t._v("后续作业/作业流")]),t._v(" "),a("bk-table",{attrs:{data:t.form.downstream_nodes,"ext-cls":"customTable"}},[a("bk-table-column",{attrs:{prop:"type",label:"类型"}}),t._v(" "),a("bk-table-column",{attrs:{prop:"name",label:"名称"}}),t._v(" "),a("bk-table-column",{attrs:{prop:"station",label:"Agent"}}),t._v(" "),a("bk-table-column",{attrs:{prop:"state",label:"状态"}}),t._v(" "),a("bk-table-column",{attrs:{prop:"eta",label:"计划开始时间"}}),t._v(" "),a("bk-table-column",{attrs:{prop:"start_time",label:"实际开始时间"}}),t._v(" "),a("bk-table-column",{attrs:{prop:"end_time",label:"实际完成时间"}})],1)],1)])},staticRenderFns:[]};var n=a("VU/8")(r,l,!1,function(t){a("NPZC")},"data-v-571f0530",null);e.default=n.exports},NPZC:function(t,e){}});