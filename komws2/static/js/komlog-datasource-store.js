function DatasourceStore () {
    this._datasourceData = [];
    this._datasourceConfig = [];
    this.subscriptionTokens = [];
    this.registeredRequests = [];
    this.activeLoop = true;

    this.subscriptionTokens.push({token:PubSub.subscribe('datasourceDataReq', this.subscriptionHandler.bind(this)),msg:'datasourceDataReq'});
    this.subscriptionTokens.push({token:PubSub.subscribe('datasourceConfigReq', this.subscriptionHandler.bind(this)),msg:'datasourceConfigReq'});
    this.subscriptionTokens.push({token:PubSub.subscribe('loadDatasourceSlide', this.subscriptionHandler.bind(this)),msg:'loadDatasourceSlide'});
    
}

DatasourceStore.prototype = {
    subscriptionHandler: function (msg, data) {
        switch (msg) {
            case 'datasourceDataReq':
                processMsgDatasourceDataReq(data)
                break;
            case 'datasourceConfigReq':
                processMsgDatasourceConfigReq(data)
                break;
            case 'loadDatasourceSlide':
                processMsgLoadDatasourceSlide(data)
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
                    case 'requestDatasourceData':
                        requestDatasourceData(request.did)
                        break;
                    case 'requestDatasourceConfig':
                        requestDatasourceConfig(request.did)
                        break;
                }
            }
        }
        if (this.activeLoop === true ) {
            setTimeout(this.requestLoop.bind(this),15000)
        }
    },
};

var datasourceStore = new DatasourceStore();
datasourceStore.requestLoop()

function processMsgDatasourceDataReq (data) {
    if (data.hasOwnProperty('did')) {
        reqArray=$.grep(datasourceStore.registeredRequests, function (e) {return e.did == data.did && e.requestType == 'requestDatasourceData'})
        if (reqArray.length == 0) {
            datasourceStore.registeredRequests.push({requestType:'requestDatasourceData',did:data.did,interval:60000})
        }
        if (datasourceStore._datasourceData.hasOwnProperty(data.did)) {
            sendDatasourceDataUpdate(data.did)
        }
        requestDatasourceData(data.did)
    }
}

function processMsgDatasourceConfigReq (data) {
    if (data.hasOwnProperty('did')) {
        reqArray=$.grep(datasourceStore.registeredRequests, function (e) {return e.did == data.did && e.requestType == 'requestDatasourceConfig'})
        if (reqArray.length == 0) {
            datasourceStore.registeredRequests.push({requestType:'requestDatasourceConfig',did:data.did,interval:120000})
        }
        if (datasourceStore._datasourceConfig.hasOwnProperty(data.did)) {
            sendDatasourceConfigUpdate(data.did)
        }
        requestDatasourceConfig(data.did)
    }
}

function requestDatasourceData (did) {
    $.ajax({
        url: '/var/ds/'+did,
        dataType: 'json',
    })
    .done(function (data) {
        updated = storeDatasourceData(did, data)
        if (updated) {
            sendDatasourceDataUpdate(did)
        }
    })
}

function storeDatasourceData (did, data) {
    changed=false
    if (!datasourceStore._datasourceData.hasOwnProperty(did)) {
        datasourceStore._datasourceData[did]=data
        changed=true
    } else if (data.hasOwnProperty('ts') && data['ts']>datasourceStore._datasourceData[did]['ts']) {
        datasourceStore._datasourceData[did]=data
        changed=true
    }
    reqArray=$.grep(datasourceStore.registeredRequests, function (e) {return e.did == did && e.requestType == 'requestDatasourceData'})
    if (reqArray.length == 1) {
        reqArray[0].lastRequest=new Date();
        if (changed == true && reqArray[0].interval > 30000) {
            reqArray[0].interval=parseInt(reqArray[0].interval*0.8)
        } else if (changed == false && reqArray[0].interval < 300000) {
            reqArray[0].interval=parseInt(reqArray[0].interval*1.2)
        }
    }
    return changed
}

function sendDatasourceDataUpdate (did) {
    if (datasourceStore._datasourceData.hasOwnProperty(did)) {
        PubSub.publish('datasourceDataUpdate-'+did,did)
    }
}

function requestDatasourceConfig (did) {
    $.ajax({
        url: '/etc/ds/'+did,
        dataType: 'json',
    })
    .done(function (data) {
        changed=storeDatasourceConfig(did, data);
        if (changed == true) {
            sendDatasourceConfigUpdate(did);
        }
    })
}

function storeDatasourceConfig (did, data) {
    doStore=false
    if (!datasourceStore._datasourceConfig.hasOwnProperty(did)) {
        datasourceStore._datasourceConfig[did]={}
        $.each(data, function (key,value) {
            datasourceStore._datasourceConfig[did][key]=value
        });
        doStore=true
    }
    else {
        $.each(data, function (key,value) {
            if (!(datasourceStore._datasourceConfig[did].hasOwnProperty(key) && datasourceStore._datasourceConfig[did][key]==value)) {
                doStore=true
            }
        });
        if (doStore) {
            datasourceStore._datasourceConfig[did]=data
        }
    }
    reqArray=$.grep(datasourceStore.registeredRequests, function (e) {return e.did == did && e.requestType == 'requestDatasourceConfig'})
    if (reqArray.length == 1) {
        reqArray[0].lastRequest=new Date();
        if (doStore == false && reqArray[0].interval<1800000) {
            reqArray[0].interval=parseInt(reqArray[0].interval*1.2)
        } else if (doStore == true && reqArray[0].interval>300000) {
            reqArray[0].interval=parseInt(reqArray[0].interval*0.8)
        }
    }
    return doStore;
}

function sendDatasourceConfigUpdate (did) {
    if (datasourceStore._datasourceConfig.hasOwnProperty(did)) {
        PubSub.publish('datasourceConfigUpdate-'+did,did)
    }
}

function processMsgLoadDatasourceSlide (data) {
    if (data.hasOwnProperty('did')) {
        did=data.did
        if (datasourceStore._datasourceConfig.hasOwnProperty(did)) {
            if (datasourceStore._datasourceConfig[did].hasOwnProperty('wid')) {
                PubSub.publish('loadSlide',{wid:datasourceStore._datasourceConfig[did].wid})
            }
        } else {
            $.ajax({
                url: '/etc/ds/'+did,
                dataType: 'json',
            })
            .done(function (data) {
                storeDatasourceConfig(did, data);
                if (data.hasOwnProperty('wid')) {
                    PubSub.publish('loadSlide',{wid:data.wid})
                }
            });
        }
    }
}

