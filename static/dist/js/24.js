webpackJsonp([24],{UCgx:function(e,t){},fnck:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s={data:function(){return{requestHeader:{},currentFiles:[]}},computed:{uploadUrl:function(){return window.siteUrl+"/process/upload_process/"}},created:function(){this.getRequestHeader()},methods:{handleDelete:function(e,t){this.currentFiles=[]},handleSave:function(){this.$router.push({name:"importFile",params:{objs:this.currentFiles}})},handleCancel:function(){this.$router.go(-1)},handleRes:function(e){return e.result?(this.$cwMessage("上传成功！","success"),this.currentFiles=e.data.objs,!0):(this.$cwMessage(e.message,"error"),!1)},handleDownload:function(){window.open(window.siteUrl+"/export/demo_batch_import_processes")},getRequestHeader:function(){var e=window.CSRF_COOKIE_NAME||"csrftoken",t="NOTPROVIDED";if(document.cookie&&""!==document.cookie)for(var n=document.cookie.split(";"),s=0;s<n.length;s++){var r=n[s].trim();if(r.substring(0,e.length+1)===e+"="){t=decodeURIComponent(r.substring(e.length+1));break}}this.requestHeader={name:"X-CSRFToken",value:t}}}},r={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{attrs:{id:"multipleJobFlow"}},[n("div",{staticClass:"content",style:{height:0===e.currentFiles.length?"240px":"290px"}},[n("div",{staticClass:"title"},[e._v("文件来源")]),e._v(" "),n("div",{staticClass:"upload-box"},[n("bk-upload",{attrs:{theme:"button",tip:"拓展名为json后缀","with-credentials":!0,url:e.uploadUrl,"ext-cls":"custom-upload",header:e.requestHeader,"handle-res-code":e.handleRes,limit:1},on:{"on-delete":e.handleDelete}}),e._v(" "),n("p",{on:{click:e.handleDownload}},[e._v("下载实例文件")]),e._v(" "),e.currentFiles.length?n("div",{staticClass:"footer"},[n("bk-button",{staticStyle:{"margin-right":"12px"},attrs:{theme:"primary"},on:{click:e.handleSave}},[e._v("保存")]),e._v(" "),n("bk-button",{on:{click:e.handleCancel}},[e._v("取消")])],1):e._e()],1)])])},staticRenderFns:[]};var o=n("VU/8")(s,r,!1,function(e){n("UCgx")},"data-v-5dd193ae",null);t.default=o.exports}});