function WidgetStore () {
    this._widgetConfig = {};
    this.subscriptionTokens = [];
    this.registeredRequests = [];
    this.activeLoop = true;

    this.subscriptionTokens.push({token:PubSub.subscribe('widgetConfigReq', this.subscriptionHandler.bind(this)),msg:'widgetConfigReq'});
    this.subscriptionTokens.push({token:PubSub.subscribe('newWidget', this.subscriptionHandler.bind(this)),msg:'newWidget'});
    this.subscriptionTokens.push({token:PubSub.subscribe('modifyWidget', this.subscriptionHandler.bind(this)),msg:'modifyWidget'});
    this.subscriptionTokens.push({token:PubSub.subscribe('deleteWidget', this.subscriptionHandler.bind(this)),msg:'deleteWidget'});
    this.subscriptionTokens.push({token:PubSub.subscribe('newWidgetDsSnapshot', this.subscriptionHandler.bind(this)),msg:'newWidgetDsSnapshot'});
    this.subscriptionTokens.push({token:PubSub.subscribe('newWidgetDpSnapshot', this.subscriptionHandler.bind(this)),msg:'newWidgetDpSnapshot'});
    this.subscriptionTokens.push({token:PubSub.subscribe('newWidgetMpSnapshot', this.subscriptionHandler.bind(this)),msg:'newWidgetMpSnapshot'});
    
}

WidgetStore.prototype = {
    subscriptionHandler: function (msg, data) {
        switch (msg) {
            case 'widgetConfigReq':
                processMsgWidgetConfigReq(data)
                break;
            case 'newWidget':
                processMsgNewWidget(data)
                break;
            case 'modifyWidget':
                processMsgModifyWidget(data)
                break;
            case 'deleteWidget':
                processMsgDeleteWidget(data)
                break;
            case 'newWidgetDsSnapshot':
                processMsgNewWidgetDsSnapshot(data)
                break;
            case 'newWidgetDpSnapshot':
                processMsgNewWidgetDpSnapshot(data)
                break;
            case 'newWidgetMpSnapshot':
                processMsgNewWidgetMpSnapshot(data)
                break;
        }
    },
    shouldRequest: function (request) {
        var now = new Date();
        if (typeof request.lastRequest === "undefined"){
            return true;
        } else {
            nextRequest=new Date(request.lastRequest.getTime()+request.interval)
            if (nextRequest < now ) {
                return true;
            } else {
                return false;
            }
        }
    },
    requestLoop: function () {
        for (var i=0; i<this.registeredRequests.length;i++) {
            request=this.registeredRequests[i]
            if (this.shouldRequest(request)) {
                switch (request.requestType) {
                    case 'requestWidgetConfig':
                        requestWidgetConfig(request.wid)
                        break;
                }
            }
        }
        if (this.activeLoop === true ) {
            setTimeout(this.requestLoop.bind(this),15000)
        }
    },
    addLoopRequest: function (id,type,interval) {
        reqArray=$.grep(this.registeredRequests, function (e) {return e.wid == id && e.requestType == type})
        if (reqArray.length == 0) {
            this.registeredRequests.push({requestType:type,wid:id,interval:interval})
        }
    },
    deleteLoopRequest: function (id,type) {
        this.registeredRequests=this.registeredRequests.filter(function (el) {
            if (el.wid==id && el.requestType==type) {
                return false
            } else {
                return true
            }
        });
    },
    slowDownRequest: function (id, type) {
        reqArray=$.grep(this.registeredRequests, function (e) {return e.wid == id && e.requestType == type})
        if (reqArray.length == 1 && reqArray[0].interval<1800000) {
            reqArray[0].interval=parseInt(reqArray[0].interval*1.2)
            reqArray[0].lastRequest=new Date();
        }
    },
    speedUpRequest: function (id, type) {
        reqArray=$.grep(this.registeredRequests, function (e) {return e.wid == id && e.requestType == type})
        if (reqArray.length == 1 && reqArray[0].interval>300000) {
            reqArray[0].interval=parseInt(reqArray[0].interval*0.8)
            reqArray[0].lastRequest=new Date();
        }
    },
    storeConfig: function (wid, data) {
        doStore=false
        if (!this._widgetConfig.hasOwnProperty(wid)) {
            this._widgetConfig[wid]={}
            $.each(data, function (key,value) {
                this._widgetConfig[wid][key]=value
            }.bind(this));
            doStore=true
        }
        else {
            $.each(data, function (key,value) {
                if (!(this._widgetConfig[wid].hasOwnProperty(key) && this._widgetConfig[wid][key]==value)) {
                    doStore=true
                }
            }.bind(this));
            if (doStore) {
                this._widgetConfig[wid]=data
            }
        }
        if (doStore == false) {
            this.slowDownRequest(wid,'requestWidgetConfig')
        } else if (doStore == true) {
            this.speedUpRequest(wid,'requestWidgetConfig')
        }
        return doStore;
    }
};

var widgetStore = new WidgetStore();
widgetStore.requestLoop()


function processMsgNewWidget(msgData) {
    requestData={type:msgData.type,widgetname:msgData.widgetname}
    $.ajax({
        url: '/etc/wg/',
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify(requestData),
    })
    .done(function (data) {
        PubSub.publish('loadSlide',{wid:data.wid})
    })
    .fail(function (data) {
        PubSub.publish('barMessage',{message:{type:'danger',message:'Error creating graph. Code: '+data.responseJSON.error},messageTime:(new Date).getTime()})
    })
}

function processMsgModifyWidget(msgData) {
    var modifyWidgetname = function (widgetname) {
        requestData={widgetname:widgetname}
        return $.ajax({
            url: '/etc/wg/'+msgData.wid,
            dataType: 'json',
            type: 'PUT',
            data: JSON.stringify(requestData),
        })
    }
    var addDatapoint = function (pid) {
        return $.ajax({
            url: '/etc/wg/'+msgData.wid+'/dp/'+pid,
            dataType: 'json',
            type: 'POST',
        })
    }
    var deleteDatapoint = function (pid) {
        return $.ajax({
            url: '/etc/wg/'+msgData.wid+'/dp/'+pid,
            dataType: 'json',
            type: 'DELETE',
        })
    }
    var endModify = function () {
        PubSub.publish('widgetConfigReq',{wid:msgData.wid})
    }
    requests=[]
    if (msgData.hasOwnProperty('new_widgetname')) {
        requests.push({method:'widgetname',widgetname:msgData.new_widgetname})
    }
    if (msgData.hasOwnProperty('new_datapoints')) {
        for (var i=0;i<msgData.new_datapoints.length;i++) {
            requests.push({method:'add',pid:msgData.new_datapoints[i]})
        }
    }
    if (msgData.hasOwnProperty('delete_datapoints')) {
        for (var i=0;i<msgData.delete_datapoints.length;i++) {
            requests.push({method:'delete',pid:msgData.delete_datapoints[i]})
        }
    }
    chainRequests=[]
    for (var i=0;i<requests.length;i++) {
        if (i==0) {
            if (requests[i].method=='widgetname') {
                chainRequests.push(modifyWidgetname(requests[i].widgetname))
            } else if (requests[i].method=='add') {
                chainRequests.push(addDatapoint(requests[i].pid))
            } else if (requests[i].method=='delete') {
                chainRequests.push(deleteDatapoint(requests[i].pid))
            }
        } else {
            if (requests[i].method=='widgetname') {
                chainRequests.push(chainRequests[i-1].then(modifyWidgetname(requests[i].widgetname)))
            } else if (requests[i].method=='add') {
                chainRequests.push(chainRequests[i-1].then(addDatapoint(requests[i].pid)))
            } else if (requests[i].method=='delete') {
                chainRequests.push(chainRequests[i-1].then(deleteDatapoint(requests[i].pid)))
            }
        }
    }
    if (chainRequests.length>0) {
        chainRequests[chainRequests.length-1].then(endModify())
    }
}

function processMsgDeleteWidget(msgData) {
    if (msgData.hasOwnProperty('wid')) {
        $.ajax({
            url: '/etc/wg/'+msgData.wid,
            dataType: 'json',
            type: 'DELETE',
        })
        .then(function(data){
            widgetStore.deleteLoopRequest(msgData.wid,'requestWidgetConfig')
        }, function(data){
            PubSub.publish('barMessage',{message:{type:'danger',message:'Error deleting widget. Code: '+data.responseJSON.error},messageTime:(new Date).getTime()})
        });
    }
}

function processMsgWidgetConfigReq (data) {
    if (data.hasOwnProperty('wid')) {
        widgetStore.addLoopRequest(data.wid,'requestWidgetConfig',120000)
        if (widgetStore._widgetConfig.hasOwnProperty(data.wid)) {
            sendWidgetConfigUpdate(data.wid)
        }
        requestWidgetConfig(data.wid)
    }
}

function requestWidgetConfig (wid) {
    $.ajax({
        url: '/etc/wg/'+wid,
        dataType: 'json',
    })
    .done(function (data) {
        changed=widgetStore.storeConfig(wid, data);
        if (changed == true) {
            sendWidgetConfigUpdate(wid);
        }
    })
}

function sendWidgetConfigUpdate (wid) {
    if (widgetStore._widgetConfig.hasOwnProperty(wid)) {
        PubSub.publish('widgetConfigUpdate-'+wid,wid)
    }
}

function processMsgNewWidgetDsSnapshot(msgData) {
    requestData={seq:msgData.seq,ul:msgData.user_list}
    $.ajax({
        url: '/etc/wg/'+msgData.wid+'/sn/',
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify(requestData),
    })
    .done(function (data) {
        PubSub.publish('barMessage',{message:{type:'success',message:'Snapshot shared successfully'},messageTime:(new Date).getTime()})
    })
    .fail(function (data) {
        PubSub.publish('barMessage',{message:{type:'danger',message:'Error creating snapshot. Code: '+data.responseJSON.error},messageTime:(new Date).getTime()})
    })
}

function processMsgNewWidgetDpSnapshot(msgData) {
    requestData={its:msgData.interval.its, ets:msgData.interval.ets, ul:msgData.user_list}
    $.ajax({
        url: '/etc/wg/'+msgData.wid+'/sn/',
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify(requestData),
    })
    .done(function (data) {
        PubSub.publish('barMessage',{message:{type:'success',message:'Snapshot shared successfully'},messageTime:(new Date).getTime()})
    })
    .fail(function (data) {
        PubSub.publish('barMessage',{message:{type:'danger',message:'Error creating snapshot. Code: '+data.responseJSON.error},messageTime:(new Date).getTime()})
    })
}

function processMsgNewWidgetMpSnapshot(msgData) {
    requestData={its:msgData.interval.its, ets:msgData.interval.ets, ul:msgData.user_list}
    $.ajax({
        url: '/etc/wg/'+msgData.wid+'/sn/',
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify(requestData),
    })
    .done(function (data) {
        PubSub.publish('barMessage',{message:{type:'success',message:'Snapshot shared successfully'},messageTime:(new Date).getTime()})
    })
    .fail(function (data) {
        PubSub.publish('barMessage',{message:{type:'danger',message:'Error creating snapshot. Code: '+data.responseJSON.error},messageTime:(new Date).getTime()})
    })
}

