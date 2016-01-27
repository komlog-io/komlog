function UriStore () {
    this._nodes={}
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
        storeUriData(data)
        sendUriUpdate(uri)
    })
}

function storeUriData (data) {
    UriStore._data=data
    storeExpandedInfo(data)
}

function storeExpandedInfo(root) {
    if (root.hasOwnProperty('id')) {
        UriStore._nodes[root.id]={uri:root.name,type:root.type,id:root.id, children:[]}
        if (root.hasOwnProperty('children')) {
            for (var i=0;i<root.children.length;i++) {
                UriStore._nodes[root.id].children.push(root.children[i].name)
            }
            for (var i=0;i<root.children.length;i++) {
                storeExpandedInfo(root.children[i])
            }
        }
    }
}

function sendUriUpdate (uri) {
    data={'uri':uri}
    PubSub.publish('uriUpdate',data)
}

function getUriGraph (rootUri, numVertices) {
    return UriStore._data
}

function getNodeInfo (uri) {
    info={}
    for (var node in UriStore._nodes) {
        if (UriStore._nodes[node].uri == uri) {
            info=UriStore._nodes[node]
            break;
        }
    }
    return info
}

function processMsgUriActionReq (data) {
    if (UriStore._nodes.hasOwnProperty(data.id)) {
        node=UriStore._nodes[data.id]
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


