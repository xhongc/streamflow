webpackJsonp([15],{WaYp:function(t,e){},eobH:function(t,e){},gnEc:function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=i("Dd8w"),a=i.n(n),o=i("Xxa5"),s=i.n(o),r=i("exGp"),l=i.n(r),c={data:function(){var t=[{id:"name",label:"作业流名",overflowTooltip:!0,sortable:!1},{id:"category",label:"分类",overflowTooltip:!1,sortable:!1},{id:"create_by",label:"创建者",overflowTooltip:!1,sortable:!1},{id:"create_time",label:"创建时间",overflowTooltip:!0,sortable:!0},{id:"update_time",label:"更新时间",overflowTooltip:!0,sortable:!0},{id:"description",label:"作业流描述",overflowTooltip:!0,sortable:!1}];return{maxTableHeight:"",auth:{},tableList:[],tableLoading:!1,runSysList:[],selectionList:[],searchFrom:{name:"",creator:"",category:""},isDropdownShow:!1,pagination:{current:1,count:1,limit:10},setting:{size:"small",fields:t,selectedFields:t.slice(0,6)}}},created:function(){this.getRunSysList(),this.handleLoad(),this.auth=this.hasPerm(this.$route.path),this.maxTableHeight=this.$store.state.common.defaultTableHeight-52},methods:{handleClone:function(t){this.$router.push({path:"/singlejobflow",query:{job_flow_data:t.id,type:"clone"}})},handleDelete:function(t){var e,i=this;this.$bkInfo({type:"primary",title:"确认要删除吗？",confirmLoading:!1,confirmFn:(e=l()(s.a.mark(function e(){return s.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:i.tableLoading=!0,i.$api.process.delete(t.id).then(function(t){t.result?(i.$cwMessage("删除成功！","success"),1===i.tableList.length&&1!==i.pagination.current&&(i.pagination.current-=1),i.handleLoad()):i.$cwMessage(t.message,"error"),i.tableLoading=!1});case 2:case"end":return e.stop()}},e,i)})),function(){return e.apply(this,arguments)})})},handleJumpHistory:function(t){this.$router.push({path:"/jobflowview",query:{job_flow_id:t.id}})},handleSettingChange:function(t){var e=t.fields,i=t.size;this.setting.size=i,this.setting.selectedFields=e},handlePageLimitChange:function(t){this.pagination.current=1,this.pagination.limit=t,this.handleLoad()},handlePageChange:function(t){this.pagination.current=t,this.handleLoad()},handleImplement:function(t){this.$router.push({path:"/taskCreate",query:{job_flow_data:t.id,job_name:t.name,type:"detail"}})},handleOpenUpdate:function(t){this.$router.push({path:"/singlejobflow",query:{job_flow_data:t.id,type:"update"}})},handleOpenDetail:function(t){this.$router.push({path:"/singlejobflow",query:{job_flow_data:t.id,type:"detail"}})},handleSelectAll:function(t){var e=this;t.length>0?this.selectionList=this.selectionList.concat(t):this.tableList.forEach(function(t){e.selectionList=e.selectionList.filter(function(e){return e.id!==t.id})})},handleSelect:function(t,e){var i=this.selectionList.find(function(t){return t.id===e.id});i?this.selectionList=this.selectionList.filter(function(t){return t.id!==i.id}):this.selectionList.push(e)},handleExportFiles:function(){if(0===this.selectionList.length)return this.$cwMessage("至少选择一条数据！","warning");var t=[];this.selectionList.forEach(function(e){t.indexOf(e.id)<0&&t.push(e.id)}),window.open(window.siteUrl+"/export/process/?id="+t.join(","))},handleCreate:function(){this.$router.push({path:"/newjobflow"})},handleSearch:function(){this.pagination.current=1,this.handleLoad()},handleReset:function(){this.searchFrom={name:"",creator:"",category:""}},handleOpenSeniorSearch:function(){this.isDropdownShow=!this.isDropdownShow},getRunSysList:function(){this.runSysList=[]},defaultCheck:function(){var t=this;this.$nextTick(function(){t.selectionList.forEach(function(e){t.tableList.forEach(function(i){e.id===i.id&&t.$refs.table.toggleRowSelection(i,!0)})})})},handleLoad:function(){var t=this;this.tableLoading=!0,this.$api.process.list(a()({},this.searchFrom,{page:this.pagination.current,page_size:this.pagination.limit})).then(function(e){e.result?(t.pagination.count=e.data.count,t.tableList=e.data.items,t.selectionList.length>0&&t.defaultCheck()):t.$cwMessage(e.message,"error"),t.tableLoading=!1})}}},d={render:function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{attrs:{id:"jobFlowList"}},[i("div",{staticClass:"header"},[i("div",{staticStyle:{float:"left"}},[i("div",{staticStyle:{"margin-right":"10px"}},[i("bk-button",{attrs:{theme:"primary"},on:{click:t.handleCreate}},[t._v("新建")])],1)]),t._v(" "),t.auth.search?i("div",{staticStyle:{float:"right"}},[i("bk-input",{staticStyle:{width:"240px","margin-right":"8px"},attrs:{clearable:"",width:"240px",placeholder:"请输入作业流名称","right-icon":"bk-icon icon-search"},on:{"right-icon-click":t.handleSearch,enter:t.handleSearch},model:{value:t.searchFrom.name,callback:function(e){t.$set(t.searchFrom,"name",e)},expression:"searchFrom.name"}}),t._v(" "),i("bk-button",{attrs:{slot:"dropdown-trigger",theme:!0===t.isDropdownShow?"primary":"default","icon-right":!0===t.isDropdownShow?"angle-double-up":"angle-double-down"},on:{click:t.handleOpenSeniorSearch},slot:"dropdown-trigger"},[t._v("高级搜索\n            ")])],1):t._e(),t._v(" "),t.isDropdownShow?i("div",{staticClass:"senior-search-box"},[i("bk-container",{attrs:{margin:0}},[i("bk-form",{attrs:{"label-width":100}},[i("bk-row",[i("bk-col",{attrs:{span:6}},[i("bk-form-item",{attrs:{label:"作业流名称:"}},[i("bk-input",{attrs:{placeholder:"请输入作业流名称",clearable:""},model:{value:t.searchFrom.name,callback:function(e){t.$set(t.searchFrom,"name",e)},expression:"searchFrom.name"}})],1)],1),t._v(" "),i("bk-col",{attrs:{span:6}},[i("bk-form-item",{attrs:{label:"创建人:"}},[i("bk-input",{attrs:{placeholder:"请输入创建人",clearable:""},model:{value:t.searchFrom.creator,callback:function(e){t.$set(t.searchFrom,"creator",e)},expression:"searchFrom.creator"}})],1)],1),t._v(" "),i("bk-col",{attrs:{span:6}},[i("bk-form-item",{attrs:{label:"分类:"}},[i("bk-select",{staticClass:"header-select",staticStyle:{"background-color":"#fff"},attrs:{clearable:!0},model:{value:t.searchFrom.category,callback:function(e){t.$set(t.searchFrom,"category",e)},expression:"searchFrom.category"}},t._l(t.runSysList,function(t,e){return i("bk-option",{key:e,attrs:{id:t.id,name:t.name}})}),1)],1)],1)],1),t._v(" "),i("bk-row",{staticStyle:{display:"flex","justify-content":"center","margin-top":"16px"}},[i("bk-button",{attrs:{theme:"primary"},on:{click:t.handleSearch}},[t._v("查询")]),t._v(" "),i("bk-button",{staticStyle:{"margin-left":"8px"},on:{click:t.handleReset}},[t._v("重置")]),t._v(" "),i("bk-button",{staticStyle:{"margin-left":"8px"},on:{click:t.handleOpenSeniorSearch}},[t._v("取消")])],1)],1)],1)],1):t._e()]),t._v(" "),i("div",{staticStyle:{clear:"both"}}),t._v(" "),i("div",{staticClass:"content"},[i("bk-table",{directives:[{name:"bkloading",rawName:"v-bkloading",value:{isLoading:t.tableLoading,zIndex:10},expression:"{ isLoading: tableLoading, zIndex: 10 }"}],ref:"table",attrs:{data:t.tableList,pagination:t.pagination,"ext-cls":"customTable",size:t.setting.size,"max-height":t.maxTableHeight},on:{"page-change":t.handlePageChange,"page-limit-change":t.handlePageLimitChange,"select-all":t.handleSelectAll,select:t.handleSelect}},[i("bk-table-column",{attrs:{type:"selection",width:"60"}}),t._v(" "),t._l(t.setting.selectedFields,function(e,n){return i("bk-table-column",{key:n,attrs:{label:e.label,prop:e.id,"show-overflow-tooltip":e.overflowTooltip,sortable:e.sortable},scopedSlots:t._u([{key:"default",fn:function(n){return["run_type"!==e.id&&"name"!==e.id&&"category"!==e.id?i("div",[t._v("\n                        "+t._s(""===n.row[e.id]||null===n.row[e.id]?"- -":n.row[e.id])+"\n                    ")]):"name"===e.id?i("div",{staticStyle:{color:"#3a84ff",cursor:"pointer"},on:{click:function(e){return t.handleOpenDetail(n.row)}}},[t._v(t._s(n.row[e.id])+"\n                    ")]):"category"===e.id?i("div",t._l(n.row[e.id],function(e){return i("bk-tag",{key:e,attrs:{theme:"info"}},[t._v(t._s(e)+"\n                        ")])}),1):t._e()]}}],null,!0)})}),t._v(" "),i("bk-table-column",{attrs:{label:"操作",width:"180"},scopedSlots:t._u([{key:"default",fn:function(e){return[i("div",{staticStyle:{display:"flex","align-items":"center"}},[t.auth.operate?i("bk-button",{staticClass:"mr10",attrs:{theme:"primary",text:""},on:{click:function(i){return t.handleImplement(e.row)}}},[t._v("新建任务\n                        ")]):t._e(),t._v(" "),t.auth.modify?i("bk-button",{staticClass:"mr10",attrs:{theme:"primary",text:""},on:{click:function(i){return t.handleOpenUpdate(e.row)}}},[t._v("修改\n                        ")]):t._e(),t._v(" "),t.auth.del?i("bk-button",{staticClass:"mr10",attrs:{theme:"primary",text:""},on:{click:function(i){return t.handleDelete(e.row)}}},[t._v("删除\n                        ")]):t._e(),t._v(" "),i("bk-popover",{attrs:{"ext-cls":"dot-menu",placement:"bottom-start",theme:"dot-menu light",trigger:"click",arrow:!1,distance:0,offset:"15"}},[i("span",{staticClass:"dot-menu-trigger"}),t._v(" "),i("ul",{staticClass:"dot-menu-list",attrs:{slot:"content"},slot:"content"},[t.auth.modify?i("li",{staticClass:"dot-menu-item",on:{click:function(i){return t.handleClone(e.row)}}},[t._v("克隆")]):t._e(),t._v(" "),i("li",{staticClass:"dot-menu-item",on:{click:function(i){return t.handleJumpHistory(e.row)}}},[t._v("执行历史")])])])],1)]}}])}),t._v(" "),i("bk-table-column",{attrs:{type:"setting"}},[i("bk-table-setting-content",{attrs:{fields:t.setting.fields,selected:t.setting.selectedFields,size:t.setting.size},on:{"setting-change":t.handleSettingChange}})],1)],2)],1)])},staticRenderFns:[]};var h=i("VU/8")(c,d,!1,function(t){i("eobH"),i("WaYp")},"data-v-154ce4f5",null);e.default=h.exports}});