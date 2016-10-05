function DatapointStore () {
    this._datapointData = {};
    this._datapointConfig = {};
    this.subscriptionTokens = [];
    this.registeredRequests = [];
    this.activeLoop = true;

    this.subscriptionTokens.push({token:PubSub.subscribe('datapointDataReq', this.subscriptionHandler.bind(this)),msg:'datapointDataReq'});
    this.subscriptionTokens.push({token:PubSub.subscribe('datapointConfigReq', this.subscriptionHandler.bind(this)),msg:'datapointConfigReq'});
    this.subscriptionTokens.push({token:PubSub.subscribe('monitorDatapoint', this.subscriptionHandler.bind(this)),msg:'monitorDatapoint'});
    this.subscriptionTokens.push({token:PubSub.subscribe('markPositiveVar', this.subscriptionHandler.bind(this)),msg:'markPositiveVar'});
    this.subscriptionTokens.push({token:PubSub.subscribe('loadDatapointSlide', this.subscriptionHandler.bind(this)),msg:'loadDatapointSlide'});
    this.subscriptionTokens.push({token:PubSub.subscribe('deleteDatapoint', this.subscriptionHandler.bind(this)),msg:'deleteDatapoint'});
    this.subscriptionTokens.push({token:PubSub.subscribe('modifyDatapoint', this.subscriptionHandler.bind(this)),msg:'modifyDatapoint'});

}

DatapointStore.prototype = {
    subscriptionHandler: function (msg, data) {
        switch (msg) {
            case 'datapointDataReq':
                processMsgDatapointDataReq(data)
                break;
            case 'datapointConfigReq':
                processMsgDatapointConfigReq(data)
                break;
            case 'monitorDatapoint':
                processMsgMonitorDatapoint(data)
                break;
            case 'markPositiveVar':
                processMsgMarkPositiveVar(data)
                break;
            case 'loadDatapointSlide':
                processMsgLoadDatapointSlide(data)
                break;
            case 'deleteDatapoint':
                processMsgDeleteDatapoint(data)
                break;
            case 'modifyDatapoint':
                processMsgModifyDatapoint(data)
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
        now=new Date().getTime()/1000;
        for (var i=0; i<this.registeredRequests.length;i++) {
            request=this.registeredRequests[i]
            if (this.shouldRequest(request)) {
                switch (request.requestType) {
                    case 'requestDatapointData':
                        datapointTsArray=[]
                        $.each(this._datapointData[request.pid], function (key, object) {
                            datapointTsArray.push(key)
                        });
                        if (datapointTsArray.length > 0) {
                            maxDatapointTs=Math.max.apply(null, datapointTsArray)
                        } else {
                            maxDatapointTs=now-3600
                        }
                        interval={its:maxDatapointTs,ets:now}
                        requestDatapointData(request.pid, interval)
                        break;
                    case 'requestDatapointConfig':
                        requestDatapointConfig(request.pid)
                        break;
                }
            }
        }
        if (this.activeLoop === true ) {
            setTimeout(this.requestLoop.bind(this),15000)
        }
    },
    addLoopRequest: function (id,type,interval) {
        reqArray=$.grep(this.registeredRequests, function (e) {return e.pid == id && e.requestType == type})
        if (reqArray.length == 0) {
            if (type == 'requestDatapointData') {
                this.registeredRequests.push({requestType:type,pid:id,interval:interval,intervalsRequested:[]})
            } else {
                this.registeredRequests.push({requestType:type,pid:id,interval:interval})
            }
        }
    },
    deleteLoopRequest: function (id,type) {
        this.registeredRequests=this.registeredRequests.filter(function (el) {
            if (el.pid==id && el.requestType==type) {
                return false
            } else {
                return true
            }
        });
    },
    slowDownRequest: function (id, type) {
        reqArray=$.grep(this.registeredRequests, function (e) {return e.pid == id && e.requestType == type})
        if (reqArray.length == 1 && reqArray[0].interval<1800000) {
            reqArray[0].interval=parseInt(reqArray[0].interval*1.2)
            reqArray[0].lastRequest=new Date();
        }
    },
    speedUpRequest: function (id, type) {
        reqArray=$.grep(this.registeredRequests, function (e) {return e.pid == id && e.requestType == type})
        if (reqArray.length == 1 && reqArray[0].interval>300000) {
            reqArray[0].interval=parseInt(reqArray[0].interval*0.8)
            reqArray[0].lastRequest=new Date();
        }
    },
    storeDatapointData: function (pid, data) {
        if (!this._datapointData.hasOwnProperty(pid)) {
            this._datapointData[pid]={}
            $.each(data, function (index,object) {
                this._datapointData[pid][object.ts]=object.value
            }.bind(this));
        }
        else {
            $.each(data, function (index,object) {
                this._datapointData[pid][object.ts]=object.value
            }.bind(this));
        }
    },
    updateIntervalsRequested: function (pid, interval) {
        reqArray=$.grep(this.registeredRequests, function (e) {return e.pid == pid && e.requestType == 'requestDatapointData'})
        if (reqArray.length==1) {
            this.speedUpRequest(pid,'requestDatapointData')
            reqArray[0].lastRequest=new Date();
            reqArray[0].intervalsRequested.push($.extend({},interval));
            intervals=reqArray[0].intervalsRequested
            for (var i=0;i<intervals.length;i++) {
                for (var j=0;j<intervals.length;j++) {
                    if (i!=j && intervals[i].ets == intervals[j].its) {
                        intervals.push({its:intervals[i].its,ets:intervals[j].ets})
                        if (j>i) {
                            intervals.splice(j,1);
                            intervals.splice(i,1);
                        } else {
                            intervals.splice(i,1);
                            intervals.splice(j,1);
                        }
                        j--;
                        i--;
                    } else if (i!=j && intervals[i].its <= intervals[j].its && intervals[i].ets > intervals[j].its && intervals[i].ets <= intervals[j].ets) {
                        intervals.push({its:intervals[i].its,ets:intervals[j].ets})
                        if (j>i) {
                            intervals.splice(j,1);
                            intervals.splice(i,1);
                        } else {
                            intervals.splice(i,1);
                            intervals.splice(j,1);
                        }
                        j--;
                        i--;
                    } else if (i!=j && intervals[i].its <= intervals[j].its && intervals[i].ets >= intervals[j].ets) {
                        if (j>i) {
                            intervals.splice(j,1);
                            j--;
                        } else {
                            intervals.splice(i,1);
                            i--;
                        }
                    }
                }
            }
            reqArray[0].intervalsRequested=intervals
        }
    },
    storeDatapointConfig: function (pid, data) {
        doStore=false
        if (!this._datapointConfig.hasOwnProperty(pid)) {
            this._datapointConfig[pid]={}
            $.each(data, function (key,value) {
                this._datapointConfig[pid][key]=value
            }.bind(this));
            doStore=true
        }
        else {
            $.each(data, function (key,value) {
                if (!(this._datapointConfig[pid].hasOwnProperty(key) && this._datapointConfig[pid][key]==value)) {
                    doStore=true
                }
            }.bind(this));
            if (doStore) {
                this._datapointConfig[pid]=data
            }
        }
        if (doStore == false) {
            this.slowDownRequest(pid,'requestDatapointConfig')
        } else if (doStore == true) {
            this.speedUpRequest(pid,'requestDatapointConfig')
        }
        return doStore;
    },
};

var datapointStore = new DatapointStore();
datapointStore.requestLoop()

function processMsgDatapointDataReq (data) {
    if (data.hasOwnProperty('pid')) {
        if (!data.hasOwnProperty('tid')) {
            datapointStore.addLoopRequest(data.pid,'requestDatapointData',60000)
        }
        requestDatapointData(data.pid, data.interval, undefined, data.tid)
    }
}

function requestDatapointData (pid, interval, originalInterval, tid) {
    if (tid && interval) {
        doRequest=true
        parameters=getMissingSubInterval(pid, interval)
        parameters.t=tid
    }
    else if (!interval) {
        doRequest=true
        parameters={}
    } else {
        parameters=getMissingSubInterval(pid, interval)
        if (parameters.hasOwnProperty('its')) {
            doRequest=true
        } else {
            doRequest=false
        }
    }
    if (doRequest == false) {
        if (!originalInterval) {
            sendDatapointDataUpdate(pid, interval)
        } else {
            sendDatapointDataUpdate(pid, originalInterval)
        }
    } else {
        $.ajax({
            url: '/var/dp/'+pid,
            dataType: 'json',
            data: parameters,
        })
        .done(function (response) {
            datapointStore.storeDatapointData(pid,response)
            receivedTs=$.map(response, function (e) {
                return e.ts
            });
            if (receivedTs.length>0) {
                maxTs=Math.max.apply(null, receivedTs)
                minTs=Math.min.apply(null, receivedTs)
                notifInterval={its:minTs, ets:maxTs}
            }
            if (0 < response.length && response.length < 300) {
                if (originalInterval) {
                    datapointStore.updateIntervalsRequested(pid,interval);
                    sendDatapointDataUpdate(pid,originalInterval)
                } else if (interval) {
                    datapointStore.updateIntervalsRequested(pid,interval);
                    sendDatapointDataUpdate(pid,interval)
                } else {
                    datapointStore.updateIntervalsRequested(pid,notifInterval);
                    sendDatapointDataUpdate(pid,notifInterval)
                }
            } else if (response.length == 300) {
                if (!interval && !originalInterval) {
                    datapointStore.updateIntervalsRequested(pid,notifInterval)
                    sendDatapointDataUpdate(pid,notifInterval)
                } else if (interval && !originalInterval) {
                    datapointStore.updateIntervalsRequested(pid,{its:notifInterval.its,ets:interval.ets});
                    newInterval={its:interval.its,ets:notifInterval.its}
                    requestDatapointData(pid, newInterval, interval, tid)
                } else if (interval && originalInterval) {
                    datapointStore.updateIntervalsRequested(pid,{its:notifInterval.its,ets:interval.ets});
                    newInterval={its:interval.its,ets:notifInterval.its}
                    requestDatapointData(pid, newInterval, originalInterval, tid)
                }
            }
        })
    }
}

function getMissingSubInterval (pid, interval) {
    reqArray=$.grep(datapointStore.registeredRequests, function (e) {return e.pid == pid && e.requestType == 'requestDatapointData'})
    if (reqArray.length==0) {
        return interval
    }
    var its=interval.its
    var ets=interval.ets
    for (var i=0; i<reqArray[0].intervalsRequested.length; i++) {
        if (interval.its <=reqArray[0].intervalsRequested[i].ets && interval.its >= reqArray[0].intervalsRequested[i].its) {
            its=reqArray[0].intervalsRequested[i].ets
        }
        if (interval.ets <=reqArray[0].intervalsRequested[i].ets && interval.ets >= reqArray[0].intervalsRequested[i].its) {
            ets=reqArray[0].intervalsRequested[i].its
        }
    }
    if (its > ets) {
        return {}
    } else {
        return {its:its,ets:ets}
    }
}

function sendDatapointDataUpdate (pid, interval) {
    if (datapointStore._datapointData.hasOwnProperty(pid)) {
        PubSub.publish('datapointDataUpdate-'+pid,{interval:interval})
    }
}

function getIntervalData (pid, interval) {
    intervalData=[]
    if (datapointStore._datapointData.hasOwnProperty(pid)) {
        $.each(datapointStore._datapointData[pid], function (key,value) {
            if (interval.its<= key && key <= interval.ets) {
                intervalData.push({ts:key,value:value})
            }
        });
    }
    intervalData.sort(function (a,b) { return a.ts - b.ts });
    return intervalData
}

function getDataSummary (data) {
    totalSamples=data.length;
    if (totalSamples>0) {
        maxValue=Math.max.apply(Math,data.map(function(o){return o.value;}));
        minValue=Math.min.apply(Math,data.map(function(o){return o.value;}));
        sumValues=0;
        meanValue=0;
        for (var j=0;j<data.length;j++) {
            sumValues+=data[j].value;
        }
        if (totalSamples>0) {
            meanValue=sumValues/totalSamples;
        }
        if ((maxValue % 1) != 0 || (minValue % 1) != 0) {
            if (typeof maxValue % 1 == 'number' && maxValue % 1 != 0) {
                numDecimalsMaxValue=maxValue.toString().split('.')[1].length
            } else {
                numDecimalsMaxValue=2
            }
            if (typeof minValue % 1 == 'number' && minValue % 1 != 0) {
                numDecimalsMinValue=minValue.toString().split('.')[1].length
            } else {
                numDecimalsMinValue=2
            }
            numDecimals=Math.max(numDecimalsMaxValue,numDecimalsMinValue)
        } else {
            numDecimals=2
        }
        meanValue=meanValue.toFixed(numDecimals)
        summary={'max':d3.format(",")(maxValue),'min':d3.format(",")(minValue),'mean':d3.format(",")(meanValue)}
    } else {
        summary={'max':0,'min':0,'mean':0}
    }
    return summary
}

function processMsgDatapointConfigReq (data) {
    if (data.hasOwnProperty('pid')) {
        datapointStore.addLoopRequest(data.pid,'requestDatapointConfig',120000)
        if (datapointStore._datapointConfig.hasOwnProperty(data.pid)) {
            sendDatapointConfigUpdate(data.pid)
        }
        requestDatapointConfig(data.pid)
    }
}

function requestDatapointConfig (pid) {
    $.ajax({
        url: '/etc/dp/'+pid,
        dataType: 'json',
    })
    .done(function (data) {
        changed=datapointStore.storeDatapointConfig(pid, data);
        if (changed == true) {
            sendDatapointConfigUpdate(pid);
        }
    })
}

function sendDatapointConfigUpdate (pid) {
    if (datapointStore._datapointConfig.hasOwnProperty(pid)) {
        PubSub.publish('datapointConfigUpdate-'+pid,pid)
    }
}

function processMsgLoadDatapointSlide (data) {
    if (data.hasOwnProperty('pid')) {
        pid=data.pid
        if (datapointStore._datapointConfig.hasOwnProperty(pid)) {
            if (datapointStore._datapointConfig[pid].hasOwnProperty('wid')) {
                PubSub.publish('loadSlide',{wid:datapointStore._datapointConfig[pid].wid})
            }
        } else {
            $.ajax({
                url: '/etc/dp/'+pid,
                dataType: 'json',
            })
            .done(function (data) {
                datapointStore.storeDatapointConfig(pid, data);
                if (data.hasOwnProperty('wid')) {
                    PubSub.publish('loadSlide',{wid:data.wid})
                }
            });
        }
    }
}

function processMsgMonitorDatapoint (data) {
    if (data.hasOwnProperty('did') && data.hasOwnProperty('seq') && data.hasOwnProperty('p') && data.hasOwnProperty('l') && data.hasOwnProperty('datapointname')) {
        requestData={did:data.did,seq:data.seq,p:data.p,l:data.l,datapointname:data.datapointname}
        $.ajax({
            url: '/etc/dp/',
            dataType: 'json',
            type: 'POST',
            data: JSON.stringify(requestData),
        })
        .done(function (data) {
            PubSub.publish('barMessage',{message:{type:'success', message:'New datapoint monitored'},messageTime:(new Date).getTime()})
            setTimeout(PubSub.publish('datapointConfigReq',{pid:data.pid}),5000)
            setTimeout(PubSub.publish('datasourceConfigReq',{did:requestData.did}),5000)
            setTimeout(PubSub.publish('datasourceDataReq',{did:requestData.did}),5000)
        })
        .fail(function (data) {
            PubSub.publish('barMessage',{message:{type:'danger', message:'Error monitoring new datapoint. Code: '+data.responseJSON.error},messageTime:(new Date).getTime()})
        });
    }
}

function processMsgMarkPositiveVar (data) {
    if (data.hasOwnProperty('pid') && data.hasOwnProperty('seq') && data.hasOwnProperty('p') && data.hasOwnProperty('l')) {
        requestData={seq:data.seq,p:data.p,l:data.l}
        $.ajax({
            url: '/etc/dp/'+data.pid+'/positives/',
            dataType: 'json',
            type: 'POST',
            data: JSON.stringify(requestData),
        })
        .done(function (responseData) {
            setTimeout(PubSub.publish('datapointConfigReq',{pid:data.pid}),5000)
            setTimeout(PubSub.publish('datapointDataReq',{pid:data.pid}),5000)
            var datapointConfig = datapointStore._datapointConfig[data.pid]
            if (datapointConfig.hasOwnProperty('did')) {
                setTimeout(PubSub.publish('datasourceConfigReq',{did:datapointConfig.did}),5000)
            }
        })
    }
}

function processMsgDeleteDatapoint(msgData) {
    if (msgData.hasOwnProperty('pid')) {
        $.ajax({
                url: '/etc/dp/'+msgData.pid,
                dataType: 'json',
                type: 'DELETE',
            })
            .then(function(data){
                datapointStore.deleteLoopRequest(msgData.pid,'requestDatapointConfig')
                datapointStore.deleteLoopRequest(msgData.pid,'requestDatapointData')
                var datapointConfig = datapointStore._datapointConfig[msgData.pid]
                if (datapointConfig.hasOwnProperty('wid')) {
                    widgetStore.deleteLoopRequest(datapointConfig.wid,'requestWidgetConfig')
                }
            }, function(data){
                PubSub.publish('barMessage',{message:{type:'danger', message:'Error deleting datapoint. Code: '+data.responseJSON.error},messageTime:(new Date).getTime()})
            });
    }
}

function processMsgModifyDatapoint(msgData) {
    if (msgData.hasOwnProperty('color')) {
        requestData={color:msgData.color}
        $.ajax({
            url: '/etc/dp/'+msgData.pid,
            dataType: 'json',
            type: 'PUT',
            data: JSON.stringify(requestData),
        }).then(function(data){
            PubSub.publish('datapointConfigReq',{pid:msgData.pid})
        }, function(data){
            PubSub.publish('barMessage',{message:{type:'danger', message:'Error updating datapoint. Code: '+data.responseJSON.error},messageTime:(new Date).getTime()})
        });
    }
}

