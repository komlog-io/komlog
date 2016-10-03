function SnapshotStore () {
    this._snapshotConfig = {};
    this.subscriptionTokens = [];

    this.subscriptionTokens.push({token:PubSub.subscribe('snapshotConfigReq', this.subscriptionHandler.bind(this)),msg:'snapshotConfigReq'});
    this.subscriptionTokens.push({token:PubSub.subscribe('deleteSnapshot', this.subscriptionHandler.bind(this)),msg:'deleteSnapshot'});

}

SnapshotStore.prototype = {
    subscriptionHandler: function (msg, data) {
        switch (msg) {
            case 'snapshotConfigReq':
                processMsgSnapshotConfigReq(data)
                break;
            case 'deleteSnapshot':
                processMsgDeleteSnapshot(data)
                break;
        }
    },
};

var snapshotStore = new SnapshotStore();


function processMsgDeleteSnapshot(msgData) {
    if (msgData.hasOwnProperty('nid')) {
        $.ajax({
            url: '/etc/sn/'+msgData.nid,
            dataType: 'json',
            type: 'DELETE',
        })
        .then(function(data){
            PubSub.publish('closeSlide',{lid:msgData.nid});
        }, function(data){
            PubSub.publish('barMessage',{message:{type:'danger',message:'Error deleting snapshot. Code: '+data.responseJSON.error},messageTime:(new Date).getTime()});
        });
    }
}

function processMsgSnapshotConfigReq (data) {
    if (data.hasOwnProperty('nid')) {
        if (snapshotStore._snapshotConfig.hasOwnProperty(data.nid)) {
            sendSnapshotConfigUpdate(data.nid)
        }
        requestSnapshotConfig(data.nid, data.tid)
    }
}

function requestSnapshotConfig (nid, tid) {
    if (tid) {
        parameters={t:tid}
    } else {
        parameters={}
    }
    $.ajax({
        url: '/etc/sn/'+nid,
        dataType: 'json',
        data: parameters,
    })
    .done(function (data) {
        changed=storeSnapshotConfig(nid, data);
        if (changed == true) {
            sendSnapshotConfigUpdate(nid);
        }
    })
}

function storeSnapshotConfig (nid, data) {
    doStore=false
    if (!snapshotStore._snapshotConfig.hasOwnProperty(nid)) {
        snapshotStore._snapshotConfig[nid]={}
        $.each(data, function (key,value) {
            snapshotStore._snapshotConfig[nid][key]=value
        });
        doStore=true
    }
    else {
        $.each(data, function (key,value) {
            if (!(snapshotStore._snapshotConfig[nid].hasOwnProperty(key) && snapshotStore._snapshotConfig[nid][key]==value)) {
                doStore=true
            }
        });
        if (doStore) {
            snapshotStore._snapshotConfig[nid]=data
        }
    }
    return doStore;
}

function sendSnapshotConfigUpdate (nid) {
    if (snapshotStore._snapshotConfig.hasOwnProperty(nid)) {
        PubSub.publish('snapshotConfigUpdate-'+nid,nid)
    }
}

