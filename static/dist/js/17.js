webpackJsonp([17],{"8iS9":function(t,e){},"U/qz":function(t,e){},qyGP:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a=n("Dd8w"),i=n.n(a),s=n("Xxa5"),o=n.n(s),r=n("exGp"),l=n.n(r),c={components:{},data:function(){var t=[{id:"name",label:"作业名",overflowTooltip:!0,sortable:!1},{id:"process_name",label:"作业流名称",overflowTooltip:!0,sortable:!1},{id:"run_type",label:"执行方式",overflowTooltip:!0,sortable:!1},{id:"when_start",label:"执行时间",overflowTooltip:!0,sortable:!1}];return{maxTableHeight:"",auth:{modify:!0,del:!0},dialogKey:0,jobFrom:{},setting:{size:"small",fields:t,selectedFields:t.slice(0,8)},tableLoading:!1,tableList:[],runSysList:[],isDropdownShow:!1,searchFrom:{name:"",process__name:"",creator:"",run_type:""},pagination:{current:1,count:1,limit:10},selectionList:[],dialogShow:!1,runTypeList:[{id:"hand",name:"单次"},{id:"time",name:"定时"},{id:"cycle",name:"周期"},{id:"cron",name:"自定义"}]}},created:function(){this.handleLoad(),this.auth=this.hasPerm(this.$route.path),this.maxTableHeight=this.$store.state.common.defaultTableHeight-52},methods:{handleJumpHistory:function(t){this.$router.push({path:"/jobflowview",query:{job_flow_id:t.process}})},handleClone:function(t){this.$router.push({path:"/singlejob",query:{type:"clone",job_id:t.id}})},handleSettingChange:function(t){var e=t.fields,n=t.size;this.setting.size=n,this.setting.selectedFields=e},handleImplement:function(t){var e,n=this;this.$bkInfo({title:"确认要执行吗？",confirmLoading:!1,confirmFn:(e=l()(o.a.mark(function e(){return o.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:n.tableLoading=!0,n.$api.task.execute({task_id:t.id}).then(function(t){t.result?(n.$cwMessage("执行成功!","success"),n.$store.commit("changeTabActive","jobview"),n.$router.push({path:"/jobflowview"})):n.$cwMessage(t.message,"error"),n.tableLoading=!1});case 2:case"end":return e.stop()}},e,n)})),function(){return e.apply(this,arguments)})})},handleOpenDetail:function(t){this.$router.push({name:"taskCreate",query:{job_flow_data:t.process,job_name:t.process_name,type:"detail",task_type:"update",task_id:t.id}})},handleSelectAll:function(t){var e=this;t.length>0?this.selectionList=this.selectionList.concat(t):this.tableList.forEach(function(t){e.selectionList=e.selectionList.filter(function(e){return e.id!==t.id})})},handleSelect:function(t,e){var n=this.selectionList.find(function(t){return t.id===e.id});n?this.selectionList=this.selectionList.filter(function(t){return t.id!==n.id}):this.selectionList.push(e)},handleExportFiles:function(){if(0===this.selectionList.length)return this.$cwMessage("至少选择一条数据！","warning");var t=[];this.selectionList.forEach(function(e){t.indexOf(e.id)<0&&t.push(e.id)}),window.open(window.siteUrl+"/export/content/?id="+t.join(","))},handleOpenUpdate:function(t){},handleDelete:function(t){var e,n=this;this.$bkInfo({type:"primary",title:"确认要删除吗？",confirmLoading:!1,confirmFn:(e=l()(o.a.mark(function e(){return o.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:n.tableLoading=!0,n.$api.task.delete(t.id).then(function(t){t.result?(n.$cwMessage("删除成功！","success"),1===n.tableList.length&&1!==n.pagination.current&&(n.pagination.current-=1),n.handleLoad()):n.$cwMessage(t.message,"error"),n.tableLoading=!1});case 2:case"end":return e.stop()}},e,n)})),function(){return e.apply(this,arguments)})})},getRunSysList:function(){var t=this;this.$api.category.list().then(function(e){e.result?t.runSysList=e.data.items:t.$cwMessage(e.message,"error")})},handleReset:function(){this.searchFrom={name:"",station_name:"",category:"",ip:"",process_name:"",creator:""}},handleOpenSeniorSearch:function(){this.isDropdownShow=!this.isDropdownShow},handlePageLimitChange:function(t){this.pagination.current=1,this.pagination.limit=t,this.handleLoad()},handleSearch:function(){this.pagination.current=1,this.handleLoad()},handlePageChange:function(t){this.pagination.current=t,this.handleLoad()},defaultCheck:function(){var t=this;this.$nextTick(function(){t.selectionList.forEach(function(e){t.tableList.forEach(function(n){e.id===n.id&&t.$refs.table.toggleRowSelection(n,!0)})})})},handleLoad:function(){var t=this;this.tableLoading=!0,this.$api.task.list(i()({},this.searchFrom,{page:this.pagination.current,page_size:this.pagination.limit})).then(function(e){e.result?(t.pagination.count=e.data.count,t.tableList=e.data.items,t.selectionList.length>0&&t.defaultCheck()):t.$cwMessage(e.message,"error"),t.tableLoading=!1})}}},d={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"jobList"}},[n("div",{staticClass:"header"},[n("div",{staticClass:"search-box"},[n("div",{staticClass:"add-in"}),t._v(" "),t.auth.search?n("div",{staticClass:"search-in"},[n("bk-input",{staticStyle:{width:"240px","margin-right":"8px"},attrs:{clearable:"",width:"240px",placeholder:"请输入作业名称","right-icon":"bk-icon icon-search"},on:{"right-icon-click":t.handleSearch,enter:t.handleSearch},model:{value:t.searchFrom.name,callback:function(e){t.$set(t.searchFrom,"name",e)},expression:"searchFrom.name"}}),t._v(" "),n("bk-button",{attrs:{slot:"dropdown-trigger",theme:!0===t.isDropdownShow?"primary":"default","icon-right":!0===t.isDropdownShow?"angle-double-up":"angle-double-down"},on:{click:t.handleOpenSeniorSearch},slot:"dropdown-trigger"},[t._v("高级搜索\n                ")])],1):t._e()]),t._v(" "),n("div",{staticStyle:{float:"left"}}),t._v(" "),t.isDropdownShow?n("div",{staticClass:"senior-search-box"},[n("bk-container",{attrs:{margin:0}},[n("bk-form",{attrs:{"label-width":100}},[n("bk-row",[n("bk-col",{attrs:{span:6}},[n("bk-form-item",{attrs:{label:"作业名称:"}},[n("bk-input",{attrs:{placeholder:"请输入作业名称",clearable:""},model:{value:t.searchFrom.name,callback:function(e){t.$set(t.searchFrom,"name",e)},expression:"searchFrom.name"}})],1)],1),t._v(" "),n("bk-col",{attrs:{span:6}},[n("bk-form-item",{attrs:{label:"作业流名称:"}},[n("bk-input",{attrs:{placeholder:"请输入作业流名称",clearable:""},model:{value:t.searchFrom.process__name,callback:function(e){t.$set(t.searchFrom,"process__name",e)},expression:"searchFrom.process__name"}})],1)],1),t._v(" "),n("bk-col",{attrs:{span:6}},[n("bk-form-item",{attrs:{label:"执行方式:"}},[n("bk-select",{staticClass:"header-select",staticStyle:{"background-color":"#fff"},attrs:{clearable:!0},model:{value:t.searchFrom.run_type,callback:function(e){t.$set(t.searchFrom,"run_type",e)},expression:"searchFrom.run_type"}},t._l(t.runTypeList,function(t,e){return n("bk-option",{key:e,attrs:{id:t.id,name:t.name}})}),1)],1)],1),t._v(" "),n("bk-col",{attrs:{span:6}},[n("bk-form-item",{attrs:{label:"创建人:"}},[n("bk-input",{attrs:{placeholder:"请输入创建人",clearable:""},model:{value:t.searchFrom.creator,callback:function(e){t.$set(t.searchFrom,"creator",e)},expression:"searchFrom.creator"}})],1)],1)],1),t._v(" "),n("bk-row",{staticStyle:{display:"flex","justify-content":"center","margin-top":"16px"}},[n("bk-button",{attrs:{theme:"primary"},on:{click:t.handleSearch}},[t._v("查询")]),t._v(" "),n("bk-button",{staticStyle:{"margin-left":"8px"},on:{click:t.handleReset}},[t._v("重置")]),t._v(" "),n("bk-button",{staticStyle:{"margin-left":"8px"},on:{click:t.handleOpenSeniorSearch}},[t._v("取消")])],1)],1)],1)],1):t._e()]),t._v(" "),n("div",{staticStyle:{clear:"both"}}),t._v(" "),n("div",{staticClass:"content"},[n("bk-table",{directives:[{name:"bkloading",rawName:"v-bkloading",value:{isLoading:t.tableLoading,zIndex:10},expression:"{ isLoading: tableLoading, zIndex: 10 }"}],ref:"table",attrs:{data:t.tableList,pagination:t.pagination,"ext-cls":"customTable",size:t.setting.size,"max-height":t.maxTableHeight},on:{"page-change":t.handlePageChange,"page-limit-change":t.handlePageLimitChange,"select-all":t.handleSelectAll,select:t.handleSelect}},[n("bk-table-column",{attrs:{type:"selection",width:"60"}}),t._v(" "),t._l(t.setting.selectedFields,function(e,a){return n("bk-table-column",{key:a,attrs:{label:e.label,prop:e.id,"show-overflow-tooltip":e.overflowTooltip,sortable:e.sortable},scopedSlots:t._u([{key:"default",fn:function(a){return["name"===e.id?n("span",{staticStyle:{color:"#3a84ff",cursor:"pointer"},on:{click:function(e){return t.handleOpenDetail(a.row)}}},[t._v(t._s(a.row[e.id]))]):"run_type"===e.id?n("div",["hand"===a.row.run_type?n("span",[t._v("单次")]):"cron"===a.row.run_type?n("span",[t._v("自定义")]):"time"===a.row.run_type?n("span",[t._v("定时")]):"cycle"===a.row.run_type?n("span",[t._v("周期")]):t._e()]):n("span",[t._v(t._s(""===a.row[e.id]||null===a.row[e.id]?"- -":a.row[e.id]))])]}}],null,!0)})}),t._v(" "),n("bk-table-column",{attrs:{label:"操作",width:"180"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("div",{staticStyle:{display:"flex","align-items":"center"}},[n("bk-button",{staticClass:"mr10",attrs:{theme:"primary",text:""},on:{click:function(n){return t.handleImplement(e.row)}}},[t._v("执行\n                        ")]),t._v(" "),n("bk-button",{staticClass:"mr10",attrs:{theme:"primary",text:""},on:{click:function(n){return t.handleOpenDetail(e.row)}}},[t._v("修改\n                        ")]),t._v(" "),n("bk-button",{staticClass:"mr10",attrs:{theme:"primary",text:""},on:{click:function(n){return t.handleDelete(e.row)}}},[t._v("删除\n                        ")]),t._v(" "),n("bk-popover",{attrs:{"ext-cls":"dot-menu",placement:"bottom-start",theme:"dot-menu light",trigger:"click",arrow:!1,distance:0,offset:"15"}},[n("span",{staticClass:"dot-menu-trigger"}),t._v(" "),n("ul",{staticClass:"dot-menu-list",attrs:{slot:"content"},slot:"content"},[n("li",{staticClass:"dot-menu-item",on:{click:function(n){return t.handleJumpHistory(e.row)}}},[t._v("执行历史")])])])],1)]}}])}),t._v(" "),n("bk-table-column",{attrs:{type:"setting"}},[n("bk-table-setting-content",{attrs:{fields:t.setting.fields,selected:t.setting.selectedFields,size:t.setting.size},on:{"setting-change":t.handleSettingChange}})],1)],2)],1),t._v(" "),n("div",[n("bk-sideslider",{attrs:{"is-show":t.dialogShow,"quick-close":!0,title:"作业详情",width:500,"ext-cls":"custom-sidelider"},on:{"update:isShow":function(e){t.dialogShow=e},"update:is-show":function(e){t.dialogShow=e}}},[n("div",{staticStyle:{height:"100%"},attrs:{slot:"content"},slot:"content"},[n("job-dialog",{key:t.dialogKey,attrs:{"job-from":t.jobFrom}})],1)])],1)])},staticRenderFns:[]};var h=n("VU/8")(c,d,!1,function(t){n("8iS9"),n("U/qz")},"data-v-1540663b",null);e.default=h.exports}});