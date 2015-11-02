function DatasourceStore () {
    this._datasourceData = [];
    this._datasourceConfig = [];
    this._snapshotDsData = [];
    this.subscriptionTokens = [];
    this.registeredRequests = [];
    this.activeLoop = true;

    this.subscriptionTokens.push({token:PubSub.subscribe('datasourceDataReq', this.subscriptionHandler.bind(this)),msg:'datasourceDataReq'});
    this.subscriptionTokens.push({token:PubSub.subscribe('datasourceConfigReq', this.subscriptionHandler.bind(this)),msg:'datasourceConfigReq'});
    this.subscriptionTokens.push({token:PubSub.subscribe('loadDatasourceSlide', this.subscriptionHandler.bind(this)),msg:'loadDatasourceSlide'});
    this.subscriptionTokens.push({token:PubSub.subscribe('snapshotDsDataReq', this.subscriptionHandler.bind(this)),msg:'snapshotDsDataReq'});
    this.subscriptionTokens.push({token:PubSub.subscribe('deleteDatasource', this.subscriptionHandler.bind(this)),msg:'deleteDatasource'});
    
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
            case 'snapshotDsDataReq':
                processMsgSnapshotDsDataReq(data)
                break;
            case 'deleteDatasource':
                processMsgDeleteDatasource(data)
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
    addLoopRequest: function (id,type,interval) {
        reqArray=$.grep(this.registeredRequests, function (e) {return e.did == id && e.requestType == type})
        if (reqArray.length == 0) {
            this.registeredRequests.push({requestType:type,did:id,interval:interval})
        }
    },
    deleteLoopRequest: function (id,type) {
        this.registeredRequests=this.registeredRequests.filter(function (el) {
            if (el.did==id && el.requestType==type) {
                return false
            } else {
                return true
            }
        });
    },
    slowDownRequest: function (id, type) {
        reqArray=$.grep(this.registeredRequests, function (e) {return e.did == id && e.requestType == type})
        if (reqArray.length == 1 && reqArray[0].interval<1800000) {
            reqArray[0].interval=parseInt(reqArray[0].interval*1.2)
            reqArray[0].lastRequest=new Date();
        }
    },
    speedUpRequest: function (id, type) {
        reqArray=$.grep(this.registeredRequests, function (e) {return e.did == id && e.requestType == type})
        if (reqArray.length == 1 && reqArray[0].interval>300000) {
            reqArray[0].interval=parseInt(reqArray[0].interval*0.8)
            reqArray[0].lastRequest=new Date();
        }
    },
    storeDatasourceData: function (did, data) {
        changed=false
        if (!this._datasourceData.hasOwnProperty(did)) {
            this._datasourceData[did]=data
            changed=true
        } else if (data.hasOwnProperty('ts') && data['ts']>this._datasourceData[did]['ts']) {
            this._datasourceData[did]=data
            changed=true
        }
        if (changed== false) {
            this.slowDownRequest(did,'requestDatasourceData')
        } else if (changed == true) {
            this.speedUpRequest(did,'requestDatasourceData')
        }
        return changed
    },
    storeDatasourceConfig: function (did, data) {
        doStore=false
        if (!this._datasourceConfig.hasOwnProperty(did)) {
            this._datasourceConfig[did]={}
            $.each(data, function (key,value) {
                this._datasourceConfig[did][key]=value
            }.bind(this));
            doStore=true
        }
        else {
            $.each(data, function (key,value) {
                if (!(this._datasourceConfig[did].hasOwnProperty(key) && this._datasourceConfig[did][key]==value)) {
                    doStore=true
                }
            }.bind(this));
            if (doStore) {
                this._datasourceConfig[did]=data
            }
        }
        if (doStore == false) {
            this.slowDownRequest(did,'requestDatasourceConfig')
        } else if (doStore == true) {
            this.speedUpRequest(did,'requestDatasourceConfig')
        }
        return doStore;
    },
    storeSnapshotDsData: function (did, data) {
        if (!this._snapshotDsData.hasOwnProperty(did)) {
            this._snapshotDsData[did]={}
        }
        if (!data.hasOwnProperty('seq')) {
            return false
        } else {
            this._snapshotDsData[did][data.seq]=data
            return true
        }
    }
};

var datasourceStore = new DatasourceStore();
datasourceStore.requestLoop()

function processMsgDatasourceDataReq (data) {
    if (data.hasOwnProperty('did')) {
        datasourceStore.addLoopRequest(data.did,'requestDatasourceData',60000)
        if (datasourceStore._datasourceData.hasOwnProperty(data.did)) {
            sendDatasourceDataUpdate(data.did)
        }
        requestDatasourceData(data.did)
    }
}

function processMsgDatasourceConfigReq (data) {
    if (data.hasOwnProperty('did')) {
        datasourceStore.addLoopRequest(data.did,'requestDatasourceConfig',120000)
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
        updated = datasourceStore.storeDatasourceData(did, data)
        if (updated) {
            sendDatasourceDataUpdate(did)
        }
    })
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
        changed=datasourceStore.storeDatasourceConfig(did, data);
        if (changed == true) {
            sendDatasourceConfigUpdate(did);
        }
    })
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
                datasourceStore.storeDatasourceConfig(did, data);
                if (data.hasOwnProperty('wid')) {
                    PubSub.publish('loadSlide',{wid:data.wid})
                }
            });
        }
    }
}

function processMsgSnapshotDsDataReq (data) {
    if (data.hasOwnProperty('did') && data.hasOwnProperty('tid') && data.hasOwnProperty('seq')) {
        if (datasourceStore._snapshotDsData.hasOwnProperty(data.did) && datasourceStore._snapshotDsData[data.did].hasOwnProperty(data.seq)) {
            sendSnapshotDsDataUpdate(data.did,data.seq)
        } else {
            requestSnapshotDsData(data.did,data.tid,data.seq)
        }
    }
}

function requestSnapshotDsData (did,tid,seq) {
    requestParams={t:tid,seq:seq}
    $.ajax({
        url: '/var/ds/'+did,
        dataType: 'json',
        data: requestParams,
    })
    .done(function (data) {
        if (datasourceStore.storeSnapshotDsData(did, data)) {
            sendSnapshotDsDataUpdate(did,seq)
        }
    })
}

function sendSnapshotDsDataUpdate (did,seq) {
    if (datasourceStore._snapshotDsData.hasOwnProperty(did) && datasourceStore._snapshotDsData[did].hasOwnProperty(seq)) {
        console.log('mandamos datos snapshot')
        PubSub.publish('snapshotDsDataUpdate-'+did,{seq:seq})
    } 
    console.log('salimos mandamos datos snapshot')
}

function processMsgDeleteDatasource(msgData) {
    if (msgData.hasOwnProperty('did')) {
        $.ajax({
                url: '/etc/ds/'+msgData.did,
                dataType: 'json',
                type: 'DELETE',
            })
            .then(function(data){
                datasourceStore.deleteLoopRequest(msgData.pid,'requestDatasourceConfig')
                datasourceStore.deleteLoopRequest(msgData.pid,'requestDatasourceData')
            }, function(data){
            });
    }
}

