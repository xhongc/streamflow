webpackJsonp([11],{C8xT:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var i=a("Dd8w"),n=a.n(i),o=a("Xxa5"),s=a.n(o),r=a("exGp"),l=a.n(r),c={components:{FormRender:a("Kp5p").a},props:{nodeData:{type:Object,default:{}},isShowBtn:{type:Boolean,default:!0}},data:function(){return{disabled:!1,isChecking:!1,inputsData:{},rules:{node_name:[{required:!0,message:"必填项",trigger:"change"}],fail_retry_count:[{required:!0,message:"必填项",trigger:"change"}]},controlType:"",tableList:[],reviewList:[{label:"正常运行",value:1},{label:"禁止运行",value:0}],timeTypeList:[{value:"hours",label:"时"},{value:"minutes",label:"分"},{value:"seconds",label:"秒"}],requestTypeList:[{value:"get",label:"GET"},{value:"post",label:"POST"},{value:"put",label:"PUT"},{value:"head",label:"HEAD"},{value:"delete",label:"DELETE"}],checkPointTypeList:[{value:"status_code",label:"默认响应码"},{value:"code",label:"自定义响应码"},{value:"content",label:"返回内容"}],checkPointConditionList:[{value:"equal",label:"等于"},{value:"not_equal",label:"不等于"},{value:"contain",label:"包含"},{value:"not_contain",label:"不包含"}],form:{inputs:{url:"",method:"",header:[{key:"",value:""}],body:"",timeout:"",check_point:{key:"",condition:"",values:""}},outputs:[],node_name:"",run_mark:1,description:"",fail_retry_count:0,fail_offset:"",fail_offset_unit:"seconds",is_skip_fail:!1,is_timeout_alarm:!1}}},created:function(){this.form=this.nodeData.data,"[object Object]"!==Object.prototype.toString.call(this.form.inputs)&&(this.form.inputs=JSON.parse(this.form.inputs)),"[object Array]"!==Object.prototype.toString.call(this.form.inputs_component)&&(this.form.inputs_component=JSON.parse(this.form.inputs_component)),"[object Array]"!==Object.prototype.toString.call(this.form.outputs)?this.tableList=JSON.parse(this.form.outputs):this.tableList=this.form.outputs,"detail"===this.$route.query.type&&(this.disabled=!0)},methods:{handleEtaChange:function(e){this.form.eta=e},handleTimePointChange:function(e){},handleConfim:function(){var e=this;this.isChecking=!0,this.$refs.form.validate().then(function(t){e.isChecking=!1,e.form.outputs=e.tableList,e.$emit("update-node-data",e.form,e.nodeData.id),e.$cwMessage("保存成功！","success"),e.$emit("node-drawer-close",!0)},function(t){e.isChecking=!1})},handleCancel:function(){var e=this;this.isChecking=!0,this.$refs.form.validate().then(function(t){e.isChecking=!1,e.$emit("update-node-data",e.form,e.nodeData.id),e.form.name=e.form.node_name,e.form.component_code="http_request",e.$api.content.create(e.form).then(function(t){t.result?e.$cwMessage("保存成功！","success"):e.$cwMessage(t.message,"error")}),e.$emit("node-drawer-close",!0)},function(t){e.isChecking=!1})},handleDeleteCommand:function(e){this.form.inputs.header.splice(e,1)},handleAddCommand:function(){this.form.inputs.header.push({key:"",value:""})}}},d={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"nodeInfo"}},[a("div",{staticClass:"content"},[a("div",{staticClass:"box"},[a("p",{staticClass:"title"},[e._v("节点设置")]),e._v(" "),a("div",{staticClass:"info"},[a("bk-form",{ref:"form",attrs:{"label-width":144,rules:e.rules,model:e.form}},[a("bk-form-item",{attrs:{label:"节点名称:",required:!0,"error-display-type":"normal",property:"node_name"}},[a("bk-input",{staticStyle:{width:"350px","margin-right":"9px"},attrs:{type:"text",disabled:e.disabled},model:{value:e.form.name,callback:function(t){e.$set(e.form,"name",t)},expression:"form.name"}})],1),e._v(" "),a("bk-form-item",{attrs:{label:"运行标志:",required:!0,"error-display-type":"normal",property:"run_mark"}},[a("bk-radio-group",{model:{value:e.form.run_mark,callback:function(t){e.$set(e.form,"run_mark",t)},expression:"form.run_mark"}},e._l(e.reviewList,function(t,i){return a("bk-radio",{key:i,staticStyle:{"margin-right":"24px"},attrs:{value:t.value,disabled:e.disabled}},[e._v("\n                                "+e._s(t.label)+"\n                            ")])}),1)],1),e._v(" "),a("bk-form-item",{attrs:{label:"描述:"}},[a("bk-input",{staticStyle:{width:"350px","margin-right":"9px"},attrs:{type:"textarea",disabled:e.disabled,min:0},model:{value:e.form.description,callback:function(t){e.$set(e.form,"description",t)},expression:"form.description"}})],1),e._v(" "),a("bk-form-item",{attrs:{label:"失败重试次数:",required:!0,"error-display-type":"normal",property:"fail_retry_count"}},[a("bk-input",{staticStyle:{width:"350px","margin-right":"9px"},attrs:{type:"number",disabled:e.disabled,min:0},model:{value:e.form.fail_retry_count,callback:function(t){e.$set(e.form,"fail_retry_count",t)},expression:"form.fail_retry_count"}})],1),e._v(" "),a("bk-form-item",{attrs:{label:"失败重试间隔:"}},[a("bk-compose-form-item",[a("bk-input",{staticStyle:{width:"139px","margin-right":"9px"},attrs:{type:"number",disabled:e.disabled,min:0},model:{value:e.form.fail_offset,callback:function(t){e.$set(e.form,"fail_offset",t)},expression:"form.fail_offset"}}),e._v(" "),a("bk-select",{staticStyle:{"background-color":"#fff",width:"138px","margin-right":"14px"},attrs:{clearable:!0,placeholder:"请选择",disabled:e.disabled},model:{value:e.form.fail_offset_unit,callback:function(t){e.$set(e.form,"fail_offset_unit",t)},expression:"form.fail_offset_unit"}},e._l(e.timeTypeList,function(e,t){return a("bk-option",{key:t,attrs:{id:e.value,name:e.label}})}),1),e._v(" "),a("span",[e._v("产生重试")])],1)],1),e._v(" "),a("bk-form-item",{attrs:{label:"忽略失败:"}},[a("bk-switcher",{attrs:{disabled:e.disabled},model:{value:e.form.is_skip_fail,callback:function(t){e.$set(e.form,"is_skip_fail",t)},expression:"form.is_skip_fail"}})],1),e._v(" "),a("bk-form-item",{attrs:{label:"超时告警:"}},[a("bk-switcher",{attrs:{disabled:e.disabled},model:{value:e.form.is_timeout_alarm,callback:function(t){e.$set(e.form,"is_timeout_alarm",t)},expression:"form.is_timeout_alarm"}})],1),e._v(" "),a("bk-divider",{staticStyle:{width:"540px",position:"relative",right:"20px","border-color":"#dcdee5"}}),e._v(" "),a("p",{staticClass:"title"},[e._v("输入参数")]),e._v(" "),a("form-render",{ref:"form_render",attrs:{forms:e.form.inputs_component,mode:e.disabled?"DESIGN":"PC"},model:{value:e.form.inputs,callback:function(t){e.$set(e.form,"inputs",t)},expression:"form.inputs"}}),e._v(" "),a("bk-divider",{staticStyle:{width:"540px",position:"relative",right:"20px","border-color":"#dcdee5"}})],1)],1)]),e._v(" "),a("div",{staticClass:"box"},[a("p",{staticClass:"title"},[e._v("输出参数")]),e._v(" "),a("bk-form",[a("bk-table",{attrs:{data:e.tableList}},[a("bk-table-column",{attrs:{label:"名称",prop:"name","show-overflow-tooltip":!0},scopedSlots:e._u([{key:"default",fn:function(t){return[a("bk-input",{model:{value:t.row.name,callback:function(a){e.$set(t.row,"name",a)},expression:"props.row.name"}})]}}])}),e._v(" "),a("bk-table-column",{attrs:{label:"KEY",prop:"key","show-overflow-tooltip":!0},scopedSlots:e._u([{key:"default",fn:function(t){return[a("bk-input",{model:{value:t.row.key,callback:function(a){e.$set(t.row,"key",a)},expression:"props.row.key"}})]}}])}),e._v(" "),a("bk-table-column",{attrs:{label:"引用",prop:"reference"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("bk-checkbox",{attrs:{disabled:e.disabled,"true-value":1,"false-value":0},model:{value:t.row.reference,callback:function(a){e.$set(t.row,"reference",a)},expression:"props.row.reference"}})]}}])})],1)],1)],1)]),e._v(" "),e.disabled?e._e():a("div",{directives:[{name:"show",rawName:"v-show",value:e.isShowBtn,expression:"isShowBtn"}],staticClass:"footer"},[a("bk-button",{staticStyle:{"margin-right":"8px"},attrs:{theme:"primary",loading:e.isChecking},on:{click:e.handleConfim}},[e._v("确定\n        ")]),e._v(" "),a("bk-button",{on:{click:e.handleCancel}},[e._v("保存为模板")])],1)])},staticRenderFns:[]};var u={components:{jobDialog:a("VU/8")(c,d,!1,function(e){a("jIhf")},"data-v-3d39bc4b",null).exports},data:function(){var e=[{id:"name",label:"作业名",overflowTooltip:!0,sortable:!1},{id:"template_type",label:"模板类型",overflowTooltip:!0,sortable:!1},{id:"description",label:"作业描述",overflowTooltip:!0,sortable:!1}];return{maxTableHeight:"",auth:{},dialogKey:0,jobFrom:{},setting:{size:"small",fields:e,selectedFields:e.slice(0,8)},tableLoading:!1,tableList:[],runSysList:[{id:"0",name:"标准节点"},{id:"1",name:"自定义节点"},{id:"2",name:"节点模版"}],isDropdownShow:!1,searchFrom:{name:"",template_type:"",description:"",creator:""},pagination:{current:1,count:1,limit:10},selectionList:[],dialogShow:!1}},created:function(){this.handleLoad(),this.auth=this.hasPerm(this.$route.path),this.maxTableHeight=this.$store.state.common.defaultTableHeight-52},methods:{handCreate:function(){this.$router.push({path:"/singlejob",query:{type:"add"}})},handleJumpHistory:function(e){this.$store.commit("changeTabActive","jobviewhistory"),this.$router.push({path:"/jobviewhistory",query:{job_id:e.id}})},handleClone:function(e){this.$router.push({path:"/singlejob",query:{type:"clone",job_id:e.id}})},handleSettingChange:function(e){var t=e.fields,a=e.size;this.setting.size=a,this.setting.selectedFields=t},handleOpenDetail:function(e){this.dialogKey+=1,this.jobFrom=e,this.dialogShow=!0},handleSelectAll:function(e){var t=this;e.length>0?this.selectionList=this.selectionList.concat(e):this.tableList.forEach(function(e){t.selectionList=t.selectionList.filter(function(t){return t.id!==e.id})})},handleSelect:function(e,t){var a=this.selectionList.find(function(e){return e.id===t.id});a?this.selectionList=this.selectionList.filter(function(e){return e.id!==a.id}):this.selectionList.push(t)},handleExportFiles:function(){if(0===this.selectionList.length)return this.$cwMessage("至少选择一条数据！","warning");var e=[];this.selectionList.forEach(function(t){e.indexOf(t.id)<0&&e.push(t.id)}),window.open(window.siteUrl+"/export/content/?id="+e.join(","))},handleOpenUpdate:function(e){this.$router.push({path:"/singlejob",query:{type:"update",job_id:e.id}})},handleDelete:function(e){var t,a=this;this.$bkInfo({type:"primary",title:"确认要删除吗？",confirmLoading:!1,confirmFn:(t=l()(s.a.mark(function t(){return s.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:a.tableLoading=!0,a.$api.content.delete(e.id).then(function(e){e.result?(a.$cwMessage("删除成功！","success"),1===a.tableList.length&&1!==a.pagination.current&&(a.pagination.current-=1),a.handleLoad()):a.$cwMessage(e.message,"error"),a.tableLoading=!1});case 2:case"end":return t.stop()}},t,a)})),function(){return t.apply(this,arguments)})})},getRunSysList:function(){var e=this;this.$api.category.list().then(function(t){t.result?e.runSysList=t.data.items:e.$cwMessage(t.message,"error")})},handleReset:function(){this.searchFrom={name:"",station_name:"",category:"",ip:"",process_name:"",creator:""},this.handleLoad()},handleOpenSeniorSearch:function(){this.isDropdownShow=!this.isDropdownShow},handlePageLimitChange:function(e){this.pagination.current=1,this.pagination.limit=e,this.handleLoad()},handleSearch:function(){this.pagination.current=1,this.handleLoad()},handlePageChange:function(e){this.pagination.current=e,this.handleLoad()},defaultCheck:function(){var e=this;this.$nextTick(function(){e.selectionList.forEach(function(t){e.tableList.forEach(function(a){t.id===a.id&&e.$refs.table.toggleRowSelection(a,!0)})})})},handleLoad:function(){var e=this;this.tableLoading=!0,this.$api.content.list(n()({},this.searchFrom,{page:this.pagination.current,page_size:this.pagination.limit})).then(function(t){t.result?(e.pagination.count=t.data.count,e.tableList=t.data.items,e.selectionList.length>0&&e.defaultCheck()):e.$cwMessage(t.message,"error"),e.tableLoading=!1})}}},h={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"jobList"}},[a("div",{staticClass:"header"},[a("div",{staticClass:"search-box"},[a("div",{staticClass:"add-in"},[a("bk-button",{staticStyle:{width:"110px","margin-left":"20px"},attrs:{theme:"primary"},on:{click:e.handCreate}},[e._v("新建")])],1),e._v(" "),e.auth.search?a("div",{staticClass:"search-in"},[a("bk-input",{staticStyle:{width:"240px","margin-right":"8px"},attrs:{clearable:"",width:"240px",placeholder:"请输入作业名称","right-icon":"bk-icon icon-search"},on:{"right-icon-click":e.handleSearch,enter:e.handleSearch},model:{value:e.searchFrom.name,callback:function(t){e.$set(e.searchFrom,"name",t)},expression:"searchFrom.name"}}),e._v(" "),a("bk-button",{attrs:{slot:"dropdown-trigger",theme:!0===e.isDropdownShow?"primary":"default","icon-right":!0===e.isDropdownShow?"angle-double-up":"angle-double-down"},on:{click:e.handleOpenSeniorSearch},slot:"dropdown-trigger"},[e._v("高级搜索\n                ")])],1):e._e()]),e._v(" "),e.isDropdownShow?a("div",{staticClass:"senior-search-box"},[a("bk-container",{attrs:{margin:0}},[a("bk-form",{attrs:{"label-width":100}},[a("bk-row",[a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"作业名称:"}},[a("bk-input",{attrs:{placeholder:"请输入作业名称",clearable:""},model:{value:e.searchFrom.name,callback:function(t){e.$set(e.searchFrom,"name",t)},expression:"searchFrom.name"}})],1)],1),e._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"模版类型:"}},[a("bk-select",{staticClass:"header-select",staticStyle:{"background-color":"#fff"},attrs:{clearable:!0},model:{value:e.searchFrom.template_type,callback:function(t){e.$set(e.searchFrom,"template_type",t)},expression:"searchFrom.template_type"}},e._l(e.runSysList,function(e,t){return a("bk-option",{key:t,attrs:{id:e.id,name:e.name}})}),1)],1)],1),e._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"作业描述:"}},[a("bk-input",{attrs:{placeholder:"请输入作业描述",clearable:""},model:{value:e.searchFrom.description,callback:function(t){e.$set(e.searchFrom,"description",t)},expression:"searchFrom.description"}})],1)],1),e._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"创建人:"}},[a("bk-input",{attrs:{placeholder:"请输入创建人",clearable:""},model:{value:e.searchFrom.creator,callback:function(t){e.$set(e.searchFrom,"creator",t)},expression:"searchFrom.creator"}})],1)],1)],1),e._v(" "),a("bk-row",{staticStyle:{display:"flex","justify-content":"center","margin-top":"16px"}},[a("bk-button",{attrs:{theme:"primary"},on:{click:e.handleSearch}},[e._v("查询")]),e._v(" "),a("bk-button",{staticStyle:{"margin-left":"8px"},on:{click:e.handleReset}},[e._v("重置")]),e._v(" "),a("bk-button",{staticStyle:{"margin-left":"8px"},on:{click:e.handleOpenSeniorSearch}},[e._v("取消")])],1)],1)],1)],1):e._e()]),e._v(" "),a("div",{staticClass:"content"},[a("bk-table",{directives:[{name:"bkloading",rawName:"v-bkloading",value:{isLoading:e.tableLoading,zIndex:10},expression:"{ isLoading: tableLoading, zIndex: 10 }"}],ref:"table",attrs:{data:e.tableList,pagination:e.pagination,"ext-cls":"customTable",size:e.setting.size,"max-height":e.maxTableHeight},on:{"page-change":e.handlePageChange,"page-limit-change":e.handlePageLimitChange,"select-all":e.handleSelectAll,select:e.handleSelect}},[a("bk-table-column",{attrs:{type:"selection",width:"60"}}),e._v(" "),e._l(e.setting.selectedFields,function(t,i){return a("bk-table-column",{key:i,attrs:{label:t.label,prop:t.id,"show-overflow-tooltip":t.overflowTooltip,sortable:t.sortable},scopedSlots:e._u([{key:"default",fn:function(i){return["name"===t.id?a("span",{staticStyle:{color:"#3a84ff",cursor:"pointer"},on:{click:function(t){return e.handleOpenDetail(i.row)}}},[e._v(e._s(i.row[t.id]))]):"template_type"===t.id?a("span",["0"===i.row.template_type?a("span",[e._v("标准节点")]):"2"===i.row.template_type?a("span",[e._v("节点模版")]):"1"===i.row.template_type?a("span",[e._v("自定义节点")]):e._e()]):a("span",[e._v(e._s(""===i.row[t.id]||null===i.row[t.id]?"- -":i.row[t.id]))])]}}],null,!0)})}),e._v(" "),a("bk-table-column",{attrs:{label:"操作",width:"180"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("div",{staticStyle:{display:"flex","align-items":"center"}},[e.auth.modify?a("bk-button",{staticClass:"mr10",attrs:{theme:"primary",text:""},on:{click:function(a){return e.handleOpenUpdate(t.row)}}},[e._v("修改\n                        ")]):e._e(),e._v(" "),e.auth.modify?a("bk-button",{staticClass:"mr10",attrs:{theme:"primary",text:""},on:{click:function(a){return e.handleClone(t.row)}}},[e._v("克隆\n                        ")]):e._e(),e._v(" "),"0"!==t.row.template_type?a("bk-button",{staticClass:"mr10",attrs:{theme:"primary",text:""},on:{click:function(a){return e.handleDelete(t.row)}}},[e._v("删除\n                        ")]):e._e()],1)]}}])}),e._v(" "),a("bk-table-column",{attrs:{type:"setting"}},[a("bk-table-setting-content",{attrs:{fields:e.setting.fields,selected:e.setting.selectedFields,size:e.setting.size},on:{"setting-change":e.handleSettingChange}})],1)],2)],1),e._v(" "),a("div",[a("bk-sideslider",{attrs:{"is-show":e.dialogShow,"quick-close":!0,title:"作业详情",width:600,"ext-cls":"custom-sidelider"},on:{"update:isShow":function(t){e.dialogShow=t},"update:is-show":function(t){e.dialogShow=t}}},[a("div",{staticStyle:{height:"100%"},attrs:{slot:"content"},slot:"content"},[a("job-dialog",{attrs:{slot:"content","node-data":{data:e.jobFrom},"is-show-btn":!1},slot:"content"})],1)])],1)])},staticRenderFns:[]};var p=a("VU/8")(u,h,!1,function(e){a("feNa"),a("Dmb3")},"data-v-362305f6",null);t.default=p.exports},Dmb3:function(e,t){},feNa:function(e,t){},jIhf:function(e,t){}});