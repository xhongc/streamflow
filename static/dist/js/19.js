webpackJsonp([19],{kdYu:function(t,e){},zKIK:function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a={data:function(){return{statusList1:[{tag:"pony审批通过，并附“同意”",content:'<span class="timeline-update-time">2020-03-06 11:23</span>',color:"green",filled:!0},{tag:"tony审批通过，并附“同意”",content:'<span class="timeline-update-time">2020-03-07 10:20</span>',color:"green",filled:!0},{tag:"allen正在审批",color:"green",filled:!0,content:'<span class="timeline-update-time">2020-03-06 11:23</span>'},{tag:"等待mark审批",color:"green",filled:!0,content:'<span class="timeline-update-time">2020-03-06 11:23</span>'},{tag:"等待mark审批",color:"green",filled:!0,content:'<span class="timeline-update-time">2020-03-06 11:23</span>'}],overViewLoading:!1,todayJobLoading:!1,top5AgentLoading:!1,weeklyJobLoading:!1,jobDynamicLoading:!1,jobDynamicState:[],weeklyJobChart:null,top5AgentChart:null,todayJobChart:null,weeklyJob:{weekly_time:[],weekly_job_num:[],weekly_error_job_num:[]},todayJob:{finished_job_num:[],error_job_num:[],unfinished_job_num:[],time_line:[]},top5Agent:{top5_agent_name:[],top5_agent_num:[]},overview_data:{today_wait_job_num:0,today_job_num:0,today_job_flow_num:0,today_error_job_num:0,jobDynamicState:[]}}},computed:{weeklyJobId:function(){return"weeklyJobId"+this._uid},top5AgentId:function(){return"top5AgentId"+this._uid},todayJobId:function(){return"todayJobId"+this._uid}},mounted:function(){this.getWeeklyJob(),this.getTop5Agent(),this.getTodayJob(),this.getJobtTrend();var t=this,e=i("uk2G")();this.$nextTick(function(){e.listenTo(document.getElementById("home"),function(e){t.weeklyJobChart.resize(),t.top5AgentChart.resize(),t.todayJobChart.resize()})})},created:function(){this.getOverViewData()},methods:{handleCheckMore:function(){this.$router.push({path:"/log",query:{object_repr:"作业",log:"fromHome"}})},getOverViewData:function(){var t=this;this.overViewLoading=!0,this.$api.home.overview().then(function(e){e.result?t.overview_data=e.data:t.$cwMessage(e.message,"error"),t.overViewLoading=!1})},getWeeklyJob:function(){var t=this;this.weeklyJobLoading=!0,this.weeklyJobChart=this.$echarts.init(document.getElementById(this.weeklyJobId));var e={color:["#3A84FF","#FF5656"],tooltip:{trigger:"axis",axisPointer:{type:"shadow"}},title:{text:"近七天作业执行情况"},legend:{x:"15",y:"top",top:"13%",data:["作业总数","异常作业数"],textStyle:{color:"rgba(0, 0, 0, 0.45)"}},grid:{height:210,width:"98%",left:"20px",right:"0px",bottom:"40px",containLabel:!0},toolbox:{feature:{saveAsImage:{show:!0,emphasis:{iconStyle:{textFill:"#fff"}}}}},calculable:!0,xAxis:[{type:"category",axisTick:{show:!1},axisLine:{lineStyle:{color:"#DCDEE5"}},axisLabel:{color:"rgba(0, 0, 0, 0.45)"},data:this.weeklyJob.weekly_time}],yAxis:[{type:"value",axisLine:{show:!1},axisTick:{show:!1},splitLine:{lineStyle:{color:"#F0F1F5"}},min:0,minInterval:1,axisLabel:{formatter:"{value}",color:"rgba(0, 0, 0, 0.45)"}}],series:[{name:"作业总数",type:"bar",barWidth:24,label:"1222",data:this.weeklyJob.weekly_job_num},{name:"异常作业数",type:"bar",barGap:"20%",barWidth:24,label:"2333",data:this.weeklyJob.weekly_error_job_num}]};this.$api.home.weekly_job().then(function(i){i.result?(t.weeklyJob=i.data,e.xAxis[0].data=t.weeklyJob.weekly_time,e.series[0].data=t.weeklyJob.weekly_job_num,e.series[1].data=t.weeklyJob.weekly_error_job_num,t.drawline(t.weeklyJobChart,e)):(t.$cwMessage(i.message,"error"),t.drawline(t.weeklyJobChart,e)),t.weeklyJobLoading=!1})},getTop5Agent:function(){var t=this;this.top5AgentLoading=!0,this.top5AgentChart=this.$echarts.init(document.getElementById(this.top5AgentId));var e={color:["#3A84FF"],xAxis:{type:"category",data:this.top5Agent.top5_agent_name,axisTick:{show:!1},axisLine:{lineStyle:{color:"#DCDEE5"}},axisLabel:{color:"rgba(0, 0, 0, 0.45)"}},legend:{data:[]},title:{text:"日均作业Top5的Agent"},grid:{height:210,width:"100%",left:"20px",bottom:"30px",containLabel:!0},toolbox:{feature:{saveAsImage:{show:!0,emphasis:{iconStyle:{textFill:"#fff"}}}}},tooltip:{trigger:"axis",axisPointer:{type:"shadow"}},yAxis:{type:"value",axisLine:{show:!1},axisTick:{show:!1},splitLine:{lineStyle:{color:"#F0F1F5"}},name:"日均作业数",nameTextStyle:{color:"#63656E"},min:0,minInterval:1,axisLabel:{formatter:"{value}",color:"rgba(0, 0, 0, 0.45)"}},series:[{data:this.top5Agent.top5_agent_num,barWidth:24,type:"bar"}]};this.$api.home.top5_agent().then(function(i){i.result?(t.top5Agent.top5_agent_name=i.data.top5_agent_name,t.top5Agent.top5_agent_num=i.data.top5_agent_num,e.xAxis.data=t.top5Agent.top5_agent_name,e.series[0].data=t.top5Agent.top5_agent_num,t.drawline(t.top5AgentChart,e)):(t.$cwMessage(i.message,"error"),t.drawline(t.top5AgentChart,e)),t.top5AgentLoading=!1})},getTodayJob:function(){var t=this;this.todayJobLoading=!0,this.todayJobChart=this.$echarts.init(document.getElementById(this.todayJobId));var e={color:["#45E35F","#FF9C01","#FF5656"],tooltip:{trigger:"axis",axisPointer:{type:"shadow"}},title:{text:"当日作业执行情况"},grid:{height:190,width:"100%",left:"40px",bottom:"60px"},toolbox:{feature:{saveAsImage:{show:!0,emphasis:{iconStyle:{textFill:"#fff"}}}}},legend:{x:"10",y:"top",top:"15%",data:["已完成的作业总数","待完成的作业总数","异常作业总数"],textStyle:{color:"rgba(0, 0, 0, 0.45)"}},xAxis:[{type:"category",axisTick:{show:!1},axisLine:{lineStyle:{color:"#DCDEE5"}},axisLabel:{color:"rgba(0, 0, 0, 0.45)"},data:this.todayJob.time_line}],yAxis:[{type:"value",axisLine:{show:!1},axisTick:{show:!1},splitLine:{lineStyle:{color:"#F0F1F5"}},min:0,axisLabel:{formatter:"{value}",color:"rgba(0, 0, 0, 0.45)"}}],series:[{name:"已完成的作业总数",type:"line",data:this.todayJob.finished_job_num},{name:"待完成的作业总数",type:"line",barWidth:30,data:this.todayJob.unfinished_job_num},{name:"异常作业总数",type:"line",data:this.todayJob.error_job_num}]};this.$api.home.today_job().then(function(i){i.result?(t.todayJob.finished_job_num=i.data.finished_job_num,t.todayJob.error_job_num=i.data.error_job_num,t.todayJob.unfinished_job_num=i.data.unfinished_job_num,t.todayJob.time_line=i.data.time_line,e.series[0].data=t.todayJob.finished_job_num,e.series[1].data=t.todayJob.unfinished_job_num,e.series[2].data=t.todayJob.error_job_num,e.xAxis[0].data=t.todayJob.time_line,t.drawline(t.todayJobChart,e)):(t.$cwMessage(i.message,"error"),t.drawline(t.todayJobChart,e)),t.todayJobLoading=!1})},getJobtTrend:function(){var t=this;this.jobDynamicLoading=!0,this.$api.home.job_dynamic().then(function(e){if(e.result){var i=e.data.slice(0,4);t.jobDynamicState=i.map(function(t){return{tag:t.condition,color:"green",filled:!0,content:'<span class="timeline-update-time">'+t.finish_time+"</span>"}})}else t.$cwMessage(e.message,"error");t.jobDynamicLoading=!1})},drawline:function(t,e){t.setOption(e)}}},o={render:function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{attrs:{id:"home"}},[i("div",{attrs:{id:"result"}}),t._v(" "),i("bk-container",{attrs:{margin:0}},[i("bk-row",{directives:[{name:"bkloading",rawName:"v-bkloading",value:{isLoading:t.overViewLoading,zIndex:10},expression:"{ isLoading: overViewLoading, zIndex: 10 }"}],staticClass:"first-line"},[i("bk-col",{attrs:{span:6}},[i("div",{staticClass:"first-line-box"},[i("div",{staticClass:"first-line-box-left"},[i("div",{staticClass:"num"},[t._v(t._s(t.overview_data.today_error_job_num))]),t._v(" "),i("div",{staticClass:"text"},[t._v("当日异常作业数")])]),t._v(" "),i("div",{staticClass:"first-line-box-right"},[i("div",{staticClass:"circle",staticStyle:{"background-color":"#FFDDDD",color:"#FF5656"}},[i("i",{staticClass:"iconfont icon-mianxingtubiao-shijianzhongxin"})])])])]),t._v(" "),i("bk-col",{attrs:{span:6}},[i("div",{staticClass:"first-line-box"},[i("div",{staticClass:"first-line-box-left"},[i("div",{staticClass:"num"},[t._v(t._s(t.overview_data.today_job_num))]),t._v(" "),i("div",{staticClass:"text"},[t._v("当日作业数")])]),t._v(" "),i("div",{staticClass:"first-line-box-right"},[i("div",{staticClass:"circle",staticStyle:{"background-color":"#E1ECFF",color:"#3A84FF"}},[i("i",{staticClass:"iconfont icon-mianxingtubiao-dangrizuoyezongshu"})])])])]),t._v(" "),i("bk-col",{attrs:{span:6}},[i("div",{staticClass:"first-line-box"},[i("div",{staticClass:"first-line-box-left"},[i("div",{staticClass:"num"},[t._v(t._s(t.overview_data.today_wait_job_num))]),t._v(" "),i("div",{staticClass:"text"},[t._v("当日未执行作业数")])]),t._v(" "),i("div",{staticClass:"first-line-box-right"},[i("div",{staticClass:"circle",staticStyle:{"background-color":"#FFE8C3",color:"#FF9C01"}},[i("i",{staticClass:"iconfont icon-mianxingtubiao-zuoyelishi"})])])])]),t._v(" "),i("bk-col",{attrs:{span:6}},[i("div",{staticClass:"first-line-box"},[i("div",{staticClass:"first-line-box-left"},[i("div",{staticClass:"num"},[t._v(t._s(t.overview_data.today_job_flow_num))]),t._v(" "),i("div",{staticClass:"text"},[t._v("当日作业流数")])]),t._v(" "),i("div",{staticClass:"first-line-box-right"},[i("div",{staticClass:"circle",staticStyle:{"background-color":"#DCFFE2",color:"#45E35F"}},[i("i",{staticClass:"iconfont icon-mianxingtubiao-dangrizuoyeliushu"})])])])])],1),t._v(" "),i("bk-row",{staticClass:"second-line"},[i("bk-col",{attrs:{span:12}},[i("div",{directives:[{name:"bkloading",rawName:"v-bkloading",value:{isLoading:t.todayJobLoading,zIndex:10},expression:"{ isLoading: todayJobLoading, zIndex: 10 }"}],staticClass:"second-line-box"},[i("div",{staticClass:"content"},[i("div",{staticStyle:{height:"100%",width:"100%"},attrs:{id:t.todayJobId}})])])]),t._v(" "),i("bk-col",{attrs:{span:12}},[i("div",{directives:[{name:"bkloading",rawName:"v-bkloading",value:{isLoading:t.weeklyJobLoading,zIndex:10},expression:"{ isLoading: weeklyJobLoading, zIndex: 10 }"}],staticClass:"second-line-box"},[i("div",{staticClass:"content"},[i("div",{staticStyle:{height:"100%",width:"100%"},attrs:{id:t.weeklyJobId}})])])])],1),t._v(" "),i("bk-row",{staticClass:"third-line"},[i("bk-col",{attrs:{span:12}},[i("div",{directives:[{name:"bkloading",rawName:"v-bkloading",value:{isLoading:t.top5AgentLoading,zIndex:10},expression:"{ isLoading: top5AgentLoading, zIndex: 10 }"}],staticClass:"third-line-box"},[i("div",{staticClass:"content"},[i("div",{staticStyle:{height:"100%",width:"100%"},attrs:{id:t.top5AgentId}})])])]),t._v(" "),i("bk-col",{attrs:{span:12}},[i("div",{directives:[{name:"bkloading",rawName:"v-bkloading",value:{isLoading:t.jobDynamicLoading,zIndex:10},expression:"{ isLoading: jobDynamicLoading, zIndex: 10 }"}],staticClass:"third-line-box"},[i("div",{staticClass:"header"},[i("p",{staticStyle:{color:"rgb(60,60,60)","margin-left":"5px"}},[t._v("作业管理动态")]),t._v(" "),i("span",{on:{click:t.handleCheckMore}},[t._v("查看更多")])]),t._v(" "),i("div",{staticClass:"content"},[i("bk-timeline",{attrs:{list:t.jobDynamicState,"ext-cls":"custom-timeline"}})],1)])])],1)],1)],1)},staticRenderFns:[]};var n=i("VU/8")(a,o,!1,function(t){i("kdYu")},"data-v-8f653944",null);e.default=n.exports}});