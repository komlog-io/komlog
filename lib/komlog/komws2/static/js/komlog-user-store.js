function UserStore () {
    this._userConfig = {};
    this.subscriptionTokens = [];
    this.registeredRequests = [];
    this.activeLoop = true;

    this.subscriptionTokens.push({token:PubSub.subscribe('myUserConfigReq', this.subscriptionHandler.bind(this)),msg:'myUserConfigReq'});
    
}

UserStore.prototype = {
    subscriptionHandler: function (msg, data) {
        switch (msg) {
            case 'myUserConfigReq':
                processMsgMyUserConfigReq(data);
                break;
        }
    },
    storeConfig: function (data) {
        storeNew=false
        uid=data.uid
        if (!this._userConfig.hasOwnProperty(uid)) {
            this._userConfig[uid]={}
            $.each(data, function (key,value) {
                this._userConfig[uid][key]=value
            }.bind(this));
            storeNew=true
        }
        else {
            $.each(data, function (key,value) {
                if (!(this._userConfig[uid].hasOwnProperty(key) && this._userConfig[uid][key]==value)) {
                    storeNew=true
                }
            }.bind(this));
            if (storeNew) {
                this._userConfig[uid]=data
            }
        }
        return storeNew;
    }
};

var userStore = new UserStore();

function processMsgMyUserConfigReq (data) {
    requestMyUserConfig()
}

function requestMyUserConfig () {
    url='/etc/usr/'
    $.ajax({
        url: url,
        dataType: 'json',
    })
    .done(function (data) {
        changed=userStore.storeConfig(data);
        if (changed == true ) {
            sendMyUserConfigUpdate(data.uid);
        }
    })
}

function sendMyUserConfigUpdate (uid) {
    if (userStore._userConfig.hasOwnProperty(uid)) {
        PubSub.publish('myUserConfigUpdate',uid)
    }
}

