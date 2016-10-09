function UriStore () {
    this._uriIndex={}
    this._idIndex={}
    this.subscriptionTokens = [];
    this.subscriptionTokens.push({token:PubSub.subscribe('uriReq', this.subscriptionHandler.bind(this)),msg:'UriReq'});
    this.subscriptionTokens.push({token:PubSub.subscribe('uriActionReq', this.subscriptionHandler.bind(this)),msg:'UriActionReq'});
}

UriStore.prototype = {
    subscriptionHandler: function (msg, data) {
        switch (msg) {
            case 'uriReq':
                processMsgUriReq(data)
                break;
            case 'uriActionReq':
                processMsgUriActionReq(data)
                break;
        }
    },
    getNodeInfoByUri: function (uri) {
        if (uri == '') {
            return this._uriIndex['.']
        } else {
            return this._uriIndex[uri]
        }
    },
    getNodeInfoById: function (id) {
        return this._idIndex[id]
    },
    deleteNodeInfoByUri: function (uri) {
        if (uri == '') {
            var uriKey = '.';
            var parentKey = null
        } else {
            var uriKey = uri;
            var split = uri.split('.');
            var parentKey = split.slice(0,split.length-1).join('.')
            if (parentKey == '') {
                parentKey = '.';
            }
        }
        if (this._uriIndex.hasOwnProperty(uriKey)) {
            var info = this._uriIndex[uriKey];
            if (info.hasOwnProperty('id') && this._idIndex.hasOwnProperty(info.id)) {
                delete this._idIndex[info.id];
            }
            delete this._uriIndex[uriKey];
        }
        if (parentKey != null && this._uriIndex.hasOwnProperty(parentKey)) {
            var parentInfo = this._uriIndex[parentKey];
            var parentWithoutNode = this._uriIndex[parentKey].children.filter(function(value) { return value != uri });
            this._uriIndex[parentKey].children = parentWithoutNode;
            if (parentInfo.hasOwnProperty('id') && this._idIndex.hasOwnProperty(parentInfo.id)) {
                this._idIndex[parentInfo.id].children = parentWithoutNode;
            }
            console.log('Eliminando uri del padre',this._uriIndex[parentKey],this._idIndex[parentKey.id])
        }
    },
    storeData: function (data) {
        if (data.hasOwnProperty('name') && data.hasOwnProperty('id')) {
            if (data.name == '') {
                uriKey='.';
            } else {
                uriKey = data.name
            }
            this._uriIndex[uriKey]={uri:data.name,type:data.type,id:data.id,children:[]}
            this._idIndex[data.id]={uri:data.name,type:data.type,id:data.id,children:[]}
            if (data.hasOwnProperty('children')) {
                for (var i=0;i<data.children.length;i++) {
                    this._uriIndex[uriKey].children.push(data.children[i].name)
                    this._idIndex[data.id].children.push(data.children[i].id)
                }
                for (var i=0;i<data.children.length;i++) {
                    this.storeData(data.children[i])
                }
            }
        }
    }
};

var UriStore = new UriStore();

function processMsgUriReq (data) {
    uri=data.uri
    requestUri(uri)
}

function requestUri (uri) {
    parameters={'uri':uri}
    $.ajax({
        url: '/var/uri/',
        dataType: 'json',
        data: parameters,
    })
    .done(function (data) {
        UriStore.storeData(data)
        sendUriUpdate(uri)
    }).fail(function (jqXHR, textStatus) {
        UriStore.deleteNodeInfoByUri(uri)
        sendUriUpdate(uri)
    });
}

function sendUriUpdate (uri) {
    data={'uri':uri}
    PubSub.publish('uriUpdate',data)
}

function getUriGraph (rootUri, numVertices) {
    return UriStore._data
}


function processMsgUriActionReq (data) {
    node=UriStore.getNodeInfoById(data.id)
    if (node.hasOwnProperty('type')) {
        if (node.type=='p') {
            PubSub.publish('loadSlide',{pid:node.id})
        } else if (node.type=='d') {
            PubSub.publish('loadSlide',{did:node.id})
        } else if (node.type=='w') {
            PubSub.publish('loadSlide',{wid:node.id})
        } else if (node.type=='v') {
            PubSub.publish('uriReq',{uri:node.uri})
        }
    }
}

