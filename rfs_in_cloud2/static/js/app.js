jQuery(function(a) {
  ace.handle_side_menu(jQuery);
});

ace.handle_side_menu = function(a) {
  a("#menu-toggler").on("click", function() {
    a("#sidebar").toggleClass("display");
    a(this).toggleClass("display");
    return false
  });
  var c = a("#sidebar").hasClass("menu-min");
  a("#sidebar-collapse").on("click", function() {
    c = a("#sidebar").hasClass("menu-min");
    ace.settings.sidebar_collapsed(!c)
  });
  var b = navigator.userAgent.match(/OS (5|6|7)(_\d)+ like Mac OS X/i);
  a(".nav-list").on("click", function(h) {
    var g = a(h.target).closest("a");
    if (!g || g.length == 0) {
      return
    }
    c = a("#sidebar").hasClass("menu-min");
    if (!g.hasClass("dropdown-toggle")) {
      if (c && g.get(0).parentNode.parentNode == this) {
        var i = g.find(".menu-text").get(0);
        if (h.target != i && !a.contains(i, h.target)) {
          return false
        }
      }
      if (b) {
        document.location = g.attr("href");
        return false
      }
      return
    }
    var f = g.next().get(0);
    if (!a(f).is(":visible")) {
      var d = a(f.parentNode).closest("ul");
      if (c && d.hasClass("nav-list")) {
        return
      }
      d.find("> .open > .submenu").each(function() {
        if (this != f && !a(this.parentNode).hasClass("active")) {
          a(this).slideUp(200).parent().removeClass("open")
        }
      })
    } else {}
    if (c && a(f.parentNode.parentNode).hasClass("nav-list")) {
      return false
    }
    a(f).slideToggle(200).parent().toggleClass("open");
    return false
  })
};

var bathUrl = "http://" + location.host;
//var bathUrl = "http://192.168.2.2:8000";

if(!parent.window.runCaseData){
	parent.window.runCaseData = {};
}

var initData = ""
initData += "<pre style='background-color:#FFFFFF; border:none;max-height:600px;overflow:scroll'> <blockquote><dl>"
initData += '<dd><p style="font-size: 11px">正在初始化数据，请稍后……</p></dd>'
initData += "</dl></blockquote></pre>"
var platform = "";
if(window.location.href.indexOf("android") != -1){
	platform = "android";
}
else{
	platform = "ios";
}

$.ajax({
  url: bathUrl + "/app_suite_data/?platfrom=" + platform,
  type: 'get',
  dataType: 'json',
  success: function(result) {
    var tree = [];
	for(var key in result){
      var obj = {
        text: key,
        nodes: [],
        state: {
          expanded: false
	  	}
      };
      if(key != "path"){
        for(var i = 0,length = result[key].length; i < length; i++){
          obj.nodes.push({text: result[key][i],state: {parentName: key}});
        }
        tree.push(obj);
      }
    }
    var suiteTreeState = {};
    var rightTree = $('#tree1').treeview({
      data: tree,
      showIcon: false,
      showCheckbox: true,
      onNodeSelected: function(event, node){
      },
      onNodeChecked: function(event, node) {
        if(node.parentId !== undefined){
            if (!(parent.window.runCaseData[node.state.parentName] instanceof Array))
        		parent.window.runCaseData[node.state.parentName] = [];
			parent.window.runCaseData[node.state.parentName].push(node.text);
        }
		else{
          if(result[node.text]){
            node.state.expanded = true;
            for(var i = 0; i < result[node.text].length; i++){
				if(!(parent.window.runCaseData[node.text] instanceof Array))
        			parent.window.runCaseData[node.text] = [];
                parent.window.runCaseData[node.text].push(result[node.text][i]);
            }
            rightTree.treeview('expandNode', [ node.nodeId, { levels: 2, silent: true } ]);
            for (i=0;i<=node.nodes.length;i++){
                if (node.nodes[i]){
                    rightTree.treeview("checkNode",[node.nodes[i].nodeId,{silent: true}]);

                }
            }
          }
        }
      },
      onNodeUnchecked: function (event, node) {
        if (node.nodes){
          var testSuite = node.text;
          for (i=0;i<=node.nodes.length;i++){
            if (node.nodes[i]){
              parent.window.runCaseData[testSuite].remove(node.nodes[i].text);
              rightTree.treeview("uncheckNode",[node.nodes[i].nodeId,{silent: true}]);
            }
          }
        }else{
          var testSuite = node.state.parentName;
          parent.window.runCaseData[testSuite].remove(node.text);
        }
      }
    });
    var findCheckableNodess = function() {
      return rightTree.treeview('search', [ $('.auto_input_search').val(), { ignoreCase: false, exactMatch: false } ]);
    };
    $('.auto_input_search').on('keyup', function (e) {
      findCheckableNodess();
    });
  },
  error: function(xhr, type) {
  }
});
$("#home").on("click", function(){
	$("#main-page",parent.document).css("display","");
	$("#insideP", parent.document).css("display", "none");
});

Array.prototype.remove=function(value)
{
    for(var i=0,n=0;i<this.length;i++)
    {
        if(this[i]["udid"]!= value)
        {
            this[n++]=this[i]
        }
    }
    this.length-=1
}

var udidArr = [], statusObj = {};


$(".submenu input").on("click",function(){
	console.log(111111111)
	if(this.className == "runStatus"){
		if(this.checked){
			udidArr.push({udid: $(this).closest("a").attr("node-udid"), name: $(this).closest("a").attr("node-name"), host: $(this).closest("li").attr("data-host")});
		}
		else{
			udidArr.remove($(this).closest("a").attr("node-udid"));
		}
	}
	else if(this.className == "isAble"){
		if(this.checked){
			statusObj[$(this).closest("li").attr("host")] = statusObj[$(this).closest("li").attr("host")] || {};
			statusObj[$(this).closest("li").attr("host")][$(this).closest("a").attr("node-udid")] = true;
		}
		else{
			delete statusObj[$(this).closest("li").attr("host")][$(this).closest("a").attr("node-udid")];
		}
	}
});

var tabElement = $("#auto_tab");

var tabStates = function(){
  var me = this;
  me.activeId = 0;
  me.nextId = 1;
  me.items = [{name: "Log", id: -1}];
  me.setActiveId = function(activeId){
    me.activeId = activeId;
  },
  me.getActiveId = function(){
    return me.activeId;
  },
  me.setNextId = function(nextId){
    me.nextId =nextId;
  },
  me.getNextId = function(){
    return me.nextId++;
  },
  me.addItem = function(item){
    me.items.push(item);
  },
  me.changeItem = function(id,flag){
    for(var i = 0, length = me.items.length; i < length; i++){
      if(me.items[i].id == id){
        me.items[i].isShow = flag;
        //隐藏或则显示div
        break;
      }
    }
  },
  me.findItem = function(name){
    for(var i = 0, length = me.items.length; i < length; i++){
      if(me.items[i].name == name){
        return me.items[i].id;
      }
    }
  }
};

var handlerTabs = function(dom){
  var me = this;
  this.tableId = 0;
  me.state = new tabStates();
  this.tab = dom;
  this.navTabs = dom.children(".nav-tabs");
  this.tabContent = dom.children(".tab-content");
  this.navTabs.on("click", function(e){
    var selectTabid = $(e.target).attr("tabid");
    if(selectTabid !== undefined && selectTabid != "")
      me.state.setActiveId(selectTabid);
    else{
      $(e.target).closest("li").css("display","none");
      $("#auto_tab li").removeClass("active");
      $("#auto_tab .tab-content .tab-pane").removeClass("active");
      $("#autoTab-0").addClass("active");
      $("#autoTadNav-0").addClass("active");
      me.state.setActiveId(0);
      e.stopPropagation();
    }
  });
  this.setTabTpl = function(name, tpl){
    $("#autoTadNav-" + me.state.getActiveId()).removeClass("active");
    $("#autoTab-" + me.state.getActiveId()).removeClass("active");
    if(me.state.findItem(name) == 0 || me.state.findItem(name)){
      var tabId = me.state.findItem(name);
      me.state.setActiveId(tabId);
      $("#autoTadNav-" + tabId).css("display", "").addClass("active");
      $("#autoTab-" + tabId).addClass("active");
      return false;
    }
    else{
      var tabId = me.state.getNextId();
      var tabTitle = '<li class="active" id="autoTadNav-' + tabId + '"><a data-toggle="tab" tabid="' + tabId + '" href="#autoTab-' + tabId + '" >' + name + '<i class="icon-remove"></i></a></li>';
      var tabContent = '<div id="autoTab-' + tabId + '" class="tab-pane active">' + tpl + '</div>';
      me.state.setActiveId(tabId);
      me.state.addItem({id: tabId, name: name, isShow: true});
      return {
        "tabTitle": tabTitle,
        "tabContent": tabContent,
        "tabId": tabId
      }
    }
  };
  this.addTab = function(name, tpl){
    var obj = this.setTabTpl(name, tpl);
    if(obj){
      this.navTabs.append(obj.tabTitle);
      this.tabContent.append(obj.tabContent);
    }
  };
  this.deleteTab = function(id){

  }
};

var tabs = new handlerTabs(tabElement);


function fetchLog(fetchFlag){
    var json_data = {'type':fetchFlag};
    json_data['platform'] = platform;
    $.ajax({
        url: bathUrl + "/app_report/",
		type: 'post',
		dataType: 'json',
        data:JSON.stringify(json_data),
        success: function(result){
            var logList = result.data;
            for (i=0;i<=logList.length;i++){
                if (logList[i]){
                    if (logList[i].line){
                        var tabname = "#autoTab-" + tabs.state.findItem(logList[i].name);
                        var msg = '<dd><p style="font-size: 11px">' + logList[i].line + '</p></dd>';
                        $(tabname + " pre blockquote dl").append(msg);
                        if (logList[i].flag){
                            var udid ="#" + logList[i].udid;
                            $(udid + " a span").attr("class","finish");
                            $(udid + " a input").removeAttr("disabled");
                        }
                    }
                }
            }
            if (!(result.flag)){
                fetchLog('line');
            }
        }
    });
}

function fetchLogAll(obj){
    var deviceName = obj.getAttribute("node-name");
    var deviceUdid = obj.getAttribute("node-udid");
    var deviceState = obj.childNodes[5].getAttribute('class');
    var udidList = []
    if (deviceState == 'finish' || deviceState == 'run'){
        if (tabs.state.findItem(deviceName)){
            tabs.addTab(deviceName);
        }else{
            tabs.addTab(deviceName,initData);
            udidList.push(deviceUdid)
            var json_data = {type: 'all',udid_list:udidList};
			json_data["platform"] = platform;
			console.log(JSON.stringify(json_data));
            $.ajax({
                url: bathUrl + "/app_report/",
                type: 'post',
                dataType: 'json',
                data:JSON.stringify(json_data),
                success: function(result){
                    var logList = result.data;
                    for (i=0;i<=logList.length;i++){
                        if (logList[i]){
                            if (logList[i].line){
                                var tabname = "#autoTab-" + tabs.state.findItem(logList[i].name);
                                var logLine = logList[i].line
                                for (j=0;j<=logLine.length;j++){
                                    if (logLine[j]){
                                        var msg = '<dd><p style="font-size: 11px">' + logLine[j] + '</p></dd>';
                                        $(tabname + " pre blockquote dl").append(msg);
                                    }
                                }
                                if (logList[i].flag){
                                    var udid ="#" + logList[i].udid;
                                    $(udid + " a span").attr("class","finish");
                                    $(udid + " a input").removeAttr("disabled");
                                }
                            }
                        }
                    }
                    if ( !(result.flag)){
                        fetchLog('line');
                    }
                }
            });
        }
    }
}
$("#setStatus").on("click", function(){
	$.ajax({
		url: bathUrl + "/set_phone_state/",
		type: 'post',
		dataType: 'json',
		data: JSON.stringify(statusObj),
		success: function(result) {
		alert('设置成功,勾选的手机可以被其他用户使用');

		}
	});
});
$("#runCase").on("click", function(){
//	console.log(udidArr);
//	console.log("finalRunCaseData",runCaseData);
    if ($.isEmptyObject(parent.window.runCaseData)){
        alert("请在右边树中选择需要执行的用例……");
        return;
    }
    if (udidArr.length == 0){
        alert("请在左边树中选择需要测试的设备……");
        return;
    }
    var udidArrNew = [];
    var localArray = [], serverArray = [], temArray = [];
    for (i=0;i<=udidArr.length;i++){
        if (udidArr[i]){
            var udid ="#" + udidArr[i].udid;
            if ($(udid + " a span")[0].className !== 'run'){
                $(udid + " a span").attr("class","run");
                $(udid + " a input").attr("disabled","disabled");
                if (tabs.state.findItem(udidArr[i].name)){
                    var tabname = "#autoTab-" + tabs.state.findItem(udidArr[i].name);
                    $(tabname).html(initData);
                }else{
                    tabs.addTab(udidArr[i].name,initData);
                }
//                if(udidArr[i].host == "local"){
//
//					localArray.push(udidArr[i]);
//                }
//                else{
                	temArray = serverArray[udidArr[i].host] || [];
                	temArray.push(udidArr[i]);
                	serverArray[udidArr[i].host] = temArray;
               // }
                //udidArrNew.push(udidArr[i])
            }
        }
    }

   // localArray []   // serverArray []
    //var obj = {phone_list: udidArrNew, case_dict: parent.window.runCaseData};
    var obj = {
    	case_dict: parent.window.runCaseData
    	//server: [{host:"", phone_list: ""}],
    	//192.1692.23:[]
    }
    $.extend(obj, serverArray);
	obj["type"] = platform;
	$.ajax({
		url: bathUrl + "/run_app_case/",
		type: 'post',
		dataType: 'json',
		data: JSON.stringify(obj),
		success: function(result) {
			var result = result[platform]
            var offlineDevice = result.offline_devices;
            for (i=0;i<=offlineDevice.length;i++){
                if (offlineDevice[i]){
                    var tabname = "#autoTab-" + tabs.state.findItem(offlineDevice[i].name);
                    var msg = '<dd><p style="font-size: 11px">没有匹配到该手机设备，请检查连接线是否松动</p></dd>';
                    $(tabname + " pre blockquote dl").append(msg);
                    var udid ="#" + offlineDevice[i].udid;
                    $(udid + " a span").attr("class","finish");
                    $(udid + " a input").removeAttr("disabled");

                }
            }
            if (result.code == 0){
                var errDevice = result.err_devices;
                var doDevice = result.do_devices;
                for (i=0;i<=errDevice.length;i++){
                    if (errDevice[i]){
                        var tabname = "#autoTab-" + tabs.state.findItem(errDevice[i].name);
                        var msg = '<dd><p style="font-size: 11px">' + errDevice[i].msg + '</p></dd>';
                        $(tabname + " pre blockquote dl").append(msg);
                        var udid ="#" + errDevice[i].udid;
                        $(udid + " a span").attr("class","finish");
                        $(udid + " a input").removeAttr("disabled");
                    }
                };
                if (doDevice.length != 0){
                    fetchLog("line");
                };
            }else{
            	for (i=0;i<=udidArrNew.length;i++){
            		if (udidArrNew[i]){
            			var tabname = "#autoTab-" + tabs.state.findItem(udidArrNew[i].name);
                        var msg = '<dd><p style="font-size: 11px">' + result.msg + '</p></dd>';
                        $(tabname + " pre blockquote dl").append(msg);
            			var udid = "#" + udidArrNew[i].udid;
            			$(udid + " a span").attr("class","undo");
                        $(udid + " a input").removeAttr("disabled");
            		}
            	}
            }
		}
	});
})