webpackJsonp([9],{"+zT3":function(e,t){},"8CQG":function(e,t){},Bma3:function(e,t){},OTIs:function(e,t,a){"use strict";t.a=[{label:"成功",key:"success",fill:"#2DCB56"},{label:"正在执行",key:"run",fill:"#3A84FF"},{label:"失败",key:"fail",fill:"#FF9C01"},{label:"终止",key:"stop",fill:"#A60505"},{label:"错误",key:"error",fill:"#EA3636"},{label:"等待",key:"wait",fill:"#FFFFFF"},{label:"就绪",key:"positive",fill:"#94F5A4"},{label:"挂起",key:"pause",fill:"#FD9C9C"},{label:"忽略",key:"ignore",fill:"#aa557f"},{label:"取消",key:"cancel",fill:"#C4C6CC"},{label:"待复核",key:"need_confirm",fill:"#aa55ff"},{label:"正在执行（存在审核）",key:"exists_need_confirm",fill:"#ffaaff"},{label:"正在执行（存在错误）",key:"exists_error",fill:"#ff0000"},{label:"正在执行（存在失败）",key:"exists_fail",fill:"#c30d0d"},{label:"正在执行（存在终止）",key:"exists_stop",fill:"#5500ff"},{label:"正在执行（存在挂起）",key:"exists_pause",fill:"#00557f"}]},UYXM:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var i=a("Xxa5"),o=a.n(i),n=a("exGp"),r=a.n(n),l=a("Dd8w"),s=a.n(l),d=a("s0MJ"),c=a("KMyz"),f=a("Ns9M"),u=a("gJBQ"),p=a("jnHa"),m=a("gaKv"),h=a("uutk"),g={components:{statusList:u.a,nodeInfo:p.a,addModeDialog:m.a,preFlowCanvas:h.a},props:{pid:{type:String,default:""}},data:function(){return{formLoading:!1,nodeSliderKey:0,flowModeDialogKey:0,form:{},graph:null,mainLoading:!1,opreateFlag:!1,tooltip:null,menu:null,cfg:{},nodeDrawer:{title:"",show:!1,width:600},nodeData:{},timer:null,flowModeDialog:{show:!1,curObj:{},preEdges:[],childDialog:{footerShow:!1,show:!1,width:960,title:""}},flowModeTipConfig:{content:"选择前置作业流中的某个节点作为前置依赖连线，不可重复选择节点连线，不可选择该作业流中的前置作业流节点！",placement:"right",width:300,zIndex:999999},stateList:[{id:1,name:"wait",label:"等待"},{id:2,name:"run",label:"正在执行"},{id:3,name:"fail",label:"失败"},{id:4,name:"error",label:"错误"},{id:5,name:"success",label:"成功"},{id:6,name:"pause",label:"挂起"},{id:7,name:"cancel",label:"取消"},{id:8,name:"positive",label:"就绪"},{id:9,name:"stop",label:"终止"},{id:10,name:"need_confirm",label:"待审核"},{id:11,name:"ignore",label:"忽略"}]}},created:function(){this.handleLoad(!1,!0)},mounted:function(){var e=this;this.$nextTick(function(){e.createGraphic(),e.initGraphEvent()}),this.timer=setInterval(function(){e.handleLoad(!1,!1)},3e3),window.addEventListener("resize",this.handleChangeCavasSize,!1)},beforeDestroy:function(){window.removeEventListener("resize",this.handleChangeCavasSize,!1),this.graph.destroy(),clearInterval(this.timer)},methods:{handleChangeCavasSize:function(){this.graph.changeSize(this.$refs.main.clientWidth,550),this.graph.fitView([20,30,30,80])},handlePreFlowNOdeAddConfirm:function(){var e=this;if(this.$refs.preFlowCanvas.currentChooseNode){var t=this;setTimeout(function(){var a=t.$refs.preFlowCanvas.currentChooseNode.name+"→"+t.flowModeDialog.curObj.targetNode.getModel().name;e.graph.addItem("edge",{id:Object(d.b)(32,16),source:t.flowModeDialog.curObj.sourceNode.get("id"),target:t.flowModeDialog.curObj.targetNode.get("id"),label:a.length>10?a.substr(0,10)+"...":a,rely_node:{name:a,label:a.length>10?a.substr(0,10)+"...":a,content:t.$refs.preFlowCanvas.currentChooseNode.content,id:t.$refs.preFlowCanvas.currentChooseNode.id},gateWay:{name:"",expression:""}}),t.flowModeDialog.childDialog.show=!1,t.flowModeDialog.show=!1},100)}else this.$cwMessage("当前作业节点未选择，至少选择一个作业节点！","warning")},handleFlowAddEdgeConfirm:function(){var e=this;if("flow"===this.$refs.addModeDialog.modeValue)setTimeout(function(){e.graph.addItem("edge",{id:Object(d.b)(32,16),source:e.flowModeDialog.curObj.sourceNode.get("id"),target:e.flowModeDialog.curObj.targetNode.get("id"),gateWay:{name:"",expression:""}})},100),this.flowModeDialog.show=!1;else{var t=this.flowModeDialog.curObj.sourceNode.getEdges();t.length&&(this.flowModeDialog.preEdges=t.filter(function(e){return e.getModel().hasOwnProperty("label")})),this.flowModeDialog.childDialog.title=this.flowModeDialog.curObj.sourceNode.getModel().name,this.flowModeDialog.childDialog.footerShow=!0,this.flowModeDialog.childDialog.show=!0}},handleOpenFlowDrawer:function(e){this.flowModeDialog.preEdges=[];var t=e.item.getEdges();console.log(1234,e.item.getModel()),t.length&&(this.flowModeDialog.preEdges=t.filter(function(e){return e.getModel().hasOwnProperty("label")})),this.flowModeDialog.curObj={sourceNode:e.item},this.flowModeDialog.childDialog.title=e.item.getModel().name,this.flowModeDialog.childDialog.footerShow=!1,this.flowModeDialog.childDialog.show=!0},initGraphEvent:function(){var e=this;this.graph.on("node:click",function(t){var a=t.item.get("model");if(0===a.nodeType||1===a.nodeType)return!1;3===a.nodeType?e.handleOpenFlowDrawer(t):2===a.nodeType&&(e.nodeData={data:Object(d.a)(a.node_data),log:a.log,state:a.state,script_content:a.script_content,start_time:a.start_time,end_time:a.end_time,id:a.id},e.nodeSliderKey+=1,e.nodeDrawer.show=!0,e.nodeDrawer.title=a.name)})},createGraphic:function(){this.createMenu(),this.initOption(),this.graph=new f.a.Graph(this.cfg)},renderCanvas:function(e,t){t&&(this.mainLoading=!0);var a=this;setTimeout(function(){var t={edges:a.form.pipeline_tree.lines.map(function(t){var a={detail:e,id:Object(d.b)(32,16),source:t.from,target:t.to,getWay:{name:t.hasOwnProperty("getWay")?t.getWay.name:"",expression:t.hasOwnProperty("getWay")?t.getWay.expression:""}};return""!==a.getWay.name&&(a.label=t.getWay.name.length>4?a.getWay.name.substr(0,4)+"...":t.getWay.name),a}),nodes:a.form.pipeline_tree.nodes.map(function(t,a){var i={};return i=0===t.type||1===t.type?{fill:"#fff",r:24}:{width:154,height:40,radius:20,iconCfg:{fill:"#3a84ff"}},s()({},t,{detail:e,label:t.name.length>8?t.name.substr(0,8)+"...":t.name,name:t.name,icon:t.ico,id:t.hasOwnProperty("end_uuid")?t.end_uuid:t.uuid,jobId:t.id,x:Number(t.left),y:Number(t.top),nodeType:t.type,state:t.state,type:0===t.type||1===t.type?"circle-node":"rect-node",labelCfg:{style:{textAlign:0===t.type||1===t.type?"center":"left"}},style:s()({},i)})})};console.log(t),a.graph.read(t),a.mainLoading=!1},100)},initOption:function(){this.cfg=Object(c.a)(f.a,{width:this.$refs.main.clientWidth,height:550,animate:!0,maxZoom:1,fitView:!0,defaultNode:{type:"rect-node",style:{radius:10},labelCfg:{fontSize:20}},defaultEdge:{type:"polyline-edge",style:{radius:0,offset:15,stroke:"#aab7c3",lineAppendWidth:10,endArrow:{path:"M 0,0 L 4,3 L 3,0 L 4,-3 Z",fill:"#aab7c3",stroke:"#aab7c3"},zIndex:999999},labelCfg:{refY:-15,style:{fill:"#1890ff",fontSize:14,cursor:"pointer",background:{fill:"#ffffff",stroke:"#9EC9FF",padding:[4,4,4,4],radius:2}}}},nodeStateStyles:{"nodeState:default":{opacity:1,fill:"#fff",stroke:"#DCDEE5",labelCfg:{style:{fill:"#333333"}}},"nodeState:hover":{opacity:.8},"nodeState:selected":{opacity:.9,stroke:"rgb(58,132,255)",labelCfg:{style:{fill:"rgb(58,132,255)"}}}},plugins:[this.tooltip,this.menu],modes:{default:["drag-canvas","zoom-canvas","hover-node","drag-node","hover-edge","active-edge","select-node"]}})},createMenu:function(){var e=this;this.tooltip=new f.a.Tooltip({offsetX:20,offsetY:-20,itemTypes:["node"],getContent:function(e){var t=document.createElement("div");return t.style.width="fit-content",t.innerHTML="<ul><li>"+e.item.getModel().name+"</li></ul>",t},shouldBegin:function(e){var t=e.item.get("model");return!(0===t.nodeType||1===t.nodeType||t.name.length<=8)}}),this.menu=new f.a.Menu({offsetX:20,offsetY:20,itemTypes:["node"],getContent:function(t){var a=t.item.get("model"),i=document.createElement("div");return i.style.width="60px",i.style.cursor="pointer",i.innerHTML=e.renderRightMenu(a),i},shouldBegin:function(e){var t=e.item.get("model");return 0!==t.nodeType&&1!==t.nodeType&&"ignore"!==t.state},handleMenuClick:function(t,a){var i=a.get("model"),o=t.id;console.log(i),e.handleOperationNode(o,i.id)}})},handleOperationNode:function(e,t){var a,i=this,n={pause:{preState:"等待",content:"作业暂停执行，不会继续后面的执行",width:450},resume:{preState:"挂起",content:"恢复挂起作业流",width:400},fail:{preState:"进行中",content:"终止后不会继续后面的执行，并且无法恢复。会强制终止此作业",width:400},stop:{preState:"进行中",content:"终止后不会继续后面的执行，并且无法恢复。会强制终止此作业",width:400},cancel:{preState:"除了正在执行",content:"将作业状态置为取消，可以继续往下执行",width:400},replay:{preState:"已完成、错误、失败，终止、取消",content:"复制一份该作业，并放入原作业流中。如果新的作业成功，那么对作业流就是成功了",width:650},release:{preState:"未执行、等待",content:"释放此作业的被依赖关系（包括时间依赖）",width:400},success:{preState:"错误，失败，终止",content:"针对错误，失败，终止的作业，设置为成功",width:400},confirm:{preState:"待复核",content:"针对待复核的作业，设置为等待",width:400}};this.$bkInfo({type:"primary",title:"执行前状态："+n[e].preState,subTitle:"功能说明："+n[e].content,width:n[e].width,confirmLoading:!1,confirmFn:(a=r()(o.a.mark(function a(){return o.a.wrap(function(a){for(;;)switch(a.prev=a.next){case 0:i.mainLoading=!0,i.opreateFlag=!0,i.$api.nodeRun.control({event:e,ids:[t]}).then(function(e){e.result?(i.$cwMessage("操作成功！","success"),i.opreateFlag=!1,i.handleLoad(!0,!0)):(i.$cwMessage(e.message,"error"),i.opreateFlag=!1,i.mainLoading=!1)});case 3:case"end":return a.stop()}},a,i)})),function(){return a.apply(this,arguments)})})},handleOperation:function(e,t){var a,i=this,n={pause:{preState:"等待",content:"作业暂停执行，不会继续后面的执行",width:450},resume:{preState:"挂起",content:"恢复挂起作业流",width:400},stop:{preState:"进行中",content:"终止后不会继续后面的执行，并且无法恢复。会强制终止此作业",width:400},fail:{preState:"进行中",content:"终止后不会继续后面的执行，并且无法恢复。会强制终止此作业",width:400},cancel:{preState:"除了正在执行",content:"将作业状态置为取消，可以继续往下执行",width:400},replay:{preState:"已完成、错误、失败，终止、取消",content:"复制一份该作业，并放入原作业流中。如果新的作业成功，那么对作业流就是成功了",width:650},release:{preState:"未执行、等待",content:"释放此作业的被依赖关系（包括时间依赖）",width:400},success:{preState:"错误，失败，终止",content:"针对错误，失败，终止的作业，设置为成功",width:400},confirm:{preState:"待复核",content:"针对待复核的作业，设置为等待",width:400}};this.$bkInfo({type:"primary",title:"执行前状态："+n[e].preState,subTitle:"功能说明："+n[e].content,width:n[e].width,confirmLoading:!1,confirmFn:(a=r()(o.a.mark(function a(){return o.a.wrap(function(a){for(;;)switch(a.prev=a.next){case 0:i.mainLoading=!0,i.opreateFlag=!0,i.$api.processRun.control({event:e,ids:[t]}).then(function(e){e.result?(i.$cwMessage("操作成功！","success"),i.opreateFlag=!1,i.handleLoad(!0,!0)):(i.$cwMessage(e.message,"error"),i.opreateFlag=!1,i.mainLoading=!1)});case 3:case"end":return a.stop()}},a,i)})),function(){return a.apply(this,arguments)})})},renderRightMenu:function(e){return"wait"===e.state?'<p id="pause" class="right-click-menu">暂停</p>\n                        ':"pause"===e.state?'<p id="resume" class="right-click-menu">恢复</p>\n                        ':"cancel"===e.state?'<p id="replay" class="right-click-menu">重新执行</p>':"fail"===e.state||"error"===e.state||"stop"===e.state?'\n                        <p id="success" class="right-click-menu">强制成功</p>\n                        <p id="replay" class="right-click-menu">重新执行</p>':"success"===e.state?"":"need_confirm"===e.state?'<p id="cancel" class="right-click-menu">取消</p>\n                        <p id="confirm" class="right-click-menu">复核</p>':"run"===e.state?'<p id="fail" class="right-click-menu">强制失败</p>':void 0},handleLoad:function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]&&arguments[0],a=arguments.length>1&&void 0!==arguments[1]&&arguments[1];if(this.opreateFlag)return!1;a&&(this.formLoading=!0),this.$api.processRun.retrieve(parseInt(this.$route.query.id)||parseInt(this.pid)).then(function(i){if(i.result){e.form=i.data,t&&e.graph.clear(),e.renderCanvas(!0,a);var o=i.data.pipeline_tree.process_state;"success"!==o&&"fail"!==o||clearInterval(e.timer)}else e.$cwMessage(i.message,"error");e.formLoading=!1})}}},b={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{directives:[{name:"bkloading",rawName:"v-bkloading",value:{isLoading:e.formLoading,zIndex:999999},expression:"{ isLoading: formLoading, zIndex: 999999 }"}],attrs:{id:"jobFlowViewDetail"}},[a("div",{staticClass:"box"},[a("p",{staticClass:"title"},[e._v("基本信息")]),e._v(" "),a("bk-container",[a("bk-form",{attrs:{"label-width":100}},[a("bk-row",[a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"作业流名称:"}},[e._v(e._s(e.form.name))])],1),e._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"作业流状态:"}},[e.form.hasOwnProperty("state")?a("span",[e._v(e._s(e.stateList[e.stateList.findIndex(function(t){return t.name===e.form.state})].label))]):e._e()])],1),e._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"启动人:"}},[e._v(e._s(e.form.create_by))])],1),e._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"开始时间:"}},[e._v(e._s(e.form.create_time))])],1)],1),e._v(" "),a("bk-row",[a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"完成时间:"}},[e._v(e._s(e.form.end_time))])],1),e._v(" "),a("bk-col",{attrs:{span:6}},[a("bk-form-item",{attrs:{label:"总共耗时:"}},[e._v(e._s(e.form.total_time))])],1)],1)],1)],1)],1),e._v(" "),a("div",{staticClass:"box"},[a("div",{staticClass:"title",staticStyle:{display:"flex","justify-content":"space-between"}},[a("div",[e._v("执行详情")]),e._v(" "),a("div",{staticStyle:{cursor:"pointer"}},[a("bk-icon",{attrs:{type:"play2"},on:{click:function(t){return e.handleOperation("resume",e.$route.query.id)}}}),e._v(" "),a("bk-icon",{attrs:{type:"pause"},on:{click:function(t){return e.handleOperation("pause",e.$route.query.id)}}}),e._v(" "),a("bk-icon",{staticStyle:{color:"red"},attrs:{type:"stop"},on:{click:function(t){return e.handleOperation("cancel",e.$route.query.id)}}})],1)]),e._v(" "),a("div",{directives:[{name:"bkloading",rawName:"v-bkloading",value:{isLoading:e.mainLoading,zIndex:999},expression:"{ isLoading: mainLoading, zIndex: 999 }"}],attrs:{id:"content"}},[a("div",{staticClass:"left-statusList"},[a("statusList",{staticStyle:{position:"absolute",left:"20px",top:"15px"}})],1),e._v(" "),a("div",{staticClass:"right-canvas"},[a("div",{ref:"main",attrs:{id:"main"}})])])]),e._v(" "),a("div",{staticClass:"node-drawer"},[a("bk-sideslider",{attrs:{"is-show":e.nodeDrawer.show,"quick-close":!0,title:e.nodeDrawer.title,width:e.nodeDrawer.width,"ext-cls":"custom-sidelider"},on:{"update:isShow":function(t){return e.$set(e.nodeDrawer,"show",t)},"update:is-show":function(t){return e.$set(e.nodeDrawer,"show",t)}}},[a("node-info",{key:e.nodeSliderKey,attrs:{slot:"content","node-data":e.nodeData},slot:"content"})],1)],1),e._v(" "),a("bk-dialog",{attrs:{title:"连线模式选择","confirm-fn":e.handleFlowAddEdgeConfirm,"ext-cls":"add-mode-dialog","mask-close":!1,"header-position":"left"},model:{value:e.flowModeDialog.show,callback:function(t){e.$set(e.flowModeDialog,"show",t)},expression:"flowModeDialog.show"}},[a("add-mode-dialog",{key:e.flowModeDialogKey,ref:"addModeDialog"}),e._v(" "),a("bk-dialog",{attrs:{"mask-close":!1,width:e.flowModeDialog.childDialog.width,"header-position":"left","render-directive":"if",position:{top:50},"ext-cls":"pre-flow-canvas-dialog","confirm-fn":e.handlePreFlowNOdeAddConfirm,"show-footer":e.flowModeDialog.childDialog.footerShow},model:{value:e.flowModeDialog.childDialog.show,callback:function(t){e.$set(e.flowModeDialog.childDialog,"show",t)},expression:"flowModeDialog.childDialog.show"}},[a("div",{attrs:{slot:"header"},slot:"header"},[a("span",{staticStyle:{color:"#313237"}},[e._v("当前作业流："+e._s(e.flowModeDialog.childDialog.title))]),e._v(" "),a("span",{directives:[{name:"bk-tooltips",rawName:"v-bk-tooltips",value:e.flowModeTipConfig,expression:"flowModeTipConfig"}],staticClass:"iconfont icon-mianxingtubiao-wenti",staticStyle:{"margin-left":"4px",color:"#979BA5","font-size":"16px"}})]),e._v(" "),a("pre-flow-canvas",{ref:"preFlowCanvas",attrs:{options:e.flowModeDialog.curObj,"pre-edges":e.flowModeDialog.preEdges}})],1)],1)],1)},staticRenderFns:[]};var v=a("VU/8")(g,b,!1,function(e){a("8CQG")},"data-v-7cd1e0c6",null);t.default=v.exports},gJBQ:function(e,t,a){"use strict";var i=a("OTIs"),o={data:function(){return{statusList:i.a}}},n={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"statusList"}},[a("ul",e._l(e.statusList,function(t,i){return a("li",{key:i,staticClass:"status-box",staticStyle:{"background-color":""}},[a("span",{staticClass:"left-color",class:["wait"===t.key?"left-color-border":""],style:{backgroundColor:t.fill}}),e._v(" "),a("span",{staticClass:"right-text"},[e._v(e._s(t.label))])])}),0)])},staticRenderFns:[]};var r=a("VU/8")(o,n,!1,function(e){a("Bma3")},"data-v-e5eca56e",null);t.a=r.exports},jnHa:function(e,t,a){"use strict";var i=a("OTIs"),o=a("VzGs"),n=a("Kp5p"),r={components:{editor:o.a,FormRender:n.a},props:{nodeData:{type:Object}},data:function(){return{statusList:i.a,disabled:!0,controlType:"",tableList:[{name:"执行结果",key:"_result",reference:"1"},{name:"作业输出变量",key:"_log_outputs",reference:"2"}],reviewList:[{label:"正常运行",value:1},{label:"禁止运行",value:0}],timeTypeList:[{value:"hours",label:"时"},{value:"minutes",label:"分"},{value:"seconds",label:"秒"}],requestTypeList:[{value:"get",label:"GET"},{value:"post",label:"POST"},{value:"put",label:"PUT"},{value:"head",label:"HEAD"},{value:"delete",label:"DELETE"}],form:{nodeData:{alarm_policy:{duration:{period:"",unit:""},time_point:""},eta:"",is_book_pause:!1,need_confirm:"",pre_commands:[{key:"",value:""}]}},log:"",state:"",start_time:"",end_time:"",script_content:""}},computed:{getUnit1:function(){var e=this,t=this.timeTypeList1.find(function(t){return t.value===e.form.nodeData.alarm_policy.duration.unit});return t?t.label:""},getUnit2:function(){var e=this,t=this.timeTypeList1.find(function(t){return t.value===e.form.nodeData.file_dependence.cycle.type});return t?t.label:""}},created:function(){this.form=this.nodeData.data,this.form.state=this.nodeData.state,this.form.start_time=this.nodeData.start_time,this.form.end_time=this.nodeData.end_time,this.form.script_content=this.nodeData.script_content}},l={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"nodeInfo"}},[a("div",{staticClass:"content"},[a("div",{staticClass:"box"},[a("p",{staticClass:"title"},[e._v("基本信息")]),e._v(" "),a("div",{staticClass:"info"},[a("bk-form",{ref:"form",attrs:{"label-width":144,model:e.form}},[a("bk-form-item",{attrs:{label:"节点名称:",required:!0,"error-display-type":"normal",property:"node_name"}},[a("bk-input",{staticStyle:{width:"350px","margin-right":"9px"},attrs:{type:"text",disabled:e.disabled},model:{value:e.form.node_name,callback:function(t){e.$set(e.form,"node_name",t)},expression:"form.node_name"}})],1),e._v(" "),a("bk-form-item",{attrs:{label:"运行标志:",required:!0,"error-display-type":"normal",property:"run_mark"}},[a("bk-radio-group",{model:{value:e.form.run_mark,callback:function(t){e.$set(e.form,"run_mark",t)},expression:"form.run_mark"}},e._l(e.reviewList,function(t,i){return a("bk-radio",{key:i,staticStyle:{"margin-right":"24px"},attrs:{value:t.value,disabled:e.disabled}},[e._v("\n                                "+e._s(t.label)+"\n                            ")])}),1)],1),e._v(" "),a("bk-form-item",{attrs:{label:"描述:"}},[a("bk-input",{staticStyle:{width:"350px","margin-right":"9px"},attrs:{type:"textarea",disabled:e.disabled,min:0},model:{value:e.form.description,callback:function(t){e.$set(e.form,"description",t)},expression:"form.description"}})],1),e._v(" "),a("bk-form-item",{attrs:{label:"失败重试次数:",required:!0,"error-display-type":"normal",property:"fail_retry_count"}},[a("bk-input",{staticStyle:{width:"350px","margin-right":"9px"},attrs:{type:"number",disabled:e.disabled,min:0},model:{value:e.form.fail_retry_count,callback:function(t){e.$set(e.form,"fail_retry_count",t)},expression:"form.fail_retry_count"}})],1),e._v(" "),a("bk-form-item",{attrs:{label:"失败重试间隔:"}},[a("bk-compose-form-item",[a("bk-input",{staticStyle:{width:"139px","margin-right":"9px"},attrs:{type:"number",disabled:e.disabled,min:0},model:{value:e.form.fail_offset,callback:function(t){e.$set(e.form,"fail_offset",t)},expression:"form.fail_offset"}}),e._v(" "),a("bk-select",{staticStyle:{"background-color":"#fff",width:"138px","margin-right":"14px"},attrs:{clearable:!0,placeholder:"请选择",disabled:e.disabled},model:{value:e.form.fail_offset_unit,callback:function(t){e.$set(e.form,"fail_offset_unit",t)},expression:"form.fail_offset_unit"}},e._l(e.timeTypeList,function(e,t){return a("bk-option",{key:t,attrs:{id:e.value,name:e.label}})}),1),e._v(" "),a("span",[e._v("产生重试")])],1)],1),e._v(" "),a("bk-form-item",{attrs:{label:"忽略失败:"}},[a("bk-switcher",{attrs:{disabled:e.disabled},model:{value:e.form.is_skip_fail,callback:function(t){e.$set(e.form,"is_skip_fail",t)},expression:"form.is_skip_fail"}})],1),e._v(" "),a("bk-form-item",{attrs:{label:"超时告警:"}},[a("bk-switcher",{attrs:{disabled:e.disabled},model:{value:e.form.is_timeout_alarm,callback:function(t){e.$set(e.form,"is_timeout_alarm",t)},expression:"form.is_timeout_alarm"}})],1),e._v(" "),a("bk-divider",{staticStyle:{width:"540px",position:"relative",right:"20px","border-color":"#dcdee5"}}),e._v(" "),a("p",{staticClass:"title"},[e._v("输入参数")]),e._v(" "),a("form-render",{ref:"form_render",attrs:{forms:e.form.inputs_component,mode:"DESIGN"},model:{value:e.form.inputs,callback:function(t){e.$set(e.form,"inputs",t)},expression:"form.inputs"}}),e._v(" "),a("bk-divider",{staticStyle:{width:"540px",position:"relative",right:"20px","border-color":"#dcdee5"}}),e._v(" "),a("p",{staticClass:"title"},[e._v("输出结果")]),e._v(" "),a("bk-form-item",{attrs:{label:"输出日志:"}},[a("editor",{ref:"editor",attrs:{height:"200px",codes:e.form.outputs,"read-only":!0,language:"shell"}})],1)],1)],1)])])])},staticRenderFns:[]};var s=a("VU/8")(r,l,!1,function(e){a("+zT3")},"data-v-74204a4c",null);t.a=s.exports}});