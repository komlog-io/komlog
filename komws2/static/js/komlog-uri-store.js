function UriStore () {
    this._vertices = [];
    this._edges = [];
    this.subscriptionTokens = [];
    this.subscriptionTokens.push({token:PubSub.subscribe('uriReq', this.subscriptionHandler.bind(this)),msg:'UriReq'});
    this.subscriptionTokens.push({token:PubSub.subscribe('uriActionReq', this.subscriptionHandler.bind(this)),msg:'UriActionReq'});
}

UriStore.prototype = {
    subscriptionHandler: function (msg, data) {
        switch (msg) {
            case 'uriReq':
                console.log('uriReq recibido')
                processMsgUriReq(data)
                break;
            case 'uriActionReq':
                console.log('uriActionReq recibido')
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
    console.log('requesting uri: ',uri)
    parameters={'uri':uri}
    $.ajax({
        url: '/var/uri/',
        dataType: 'json',
        data: parameters,
    })
    .done(function (data) {
        console.log('data received',data)
        storeUriData(data)
        sendUriUpdate(uri)
    })
}

function storeUriData (data) {
    console.log('datos recibidos',data)
    UriStore._data=data
    storeExpandedInfo(data)
}

function storeExpandedInfo(root) {
    if (root.hasOwnProperty('id')) {
        UriStore._vertices[root.id]={uri:root.name,type:root.type,id:root.id}
    }
    if (root.hasOwnProperty('children')) {
        for (var i=0;i<root.children.length;i++) {
            storeExpandedInfo(root.children[i])
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

function processMsgUriActionReq (data) {
    console.log('processMsgUriActionReq',data,UriStore._vertices)
    if (UriStore._vertices.hasOwnProperty(data.id)) {
        vertex=UriStore._vertices[data.id]
        console.log('objecto uri seleccionado',vertex)
        if (vertex.type=='p') {
            PubSub.publish('loadSlide',{pid:vertex.id})
        } else if (vertex.type=='d') {
            console.log('loadSlide del datasource')
            PubSub.publish('loadSlide',{did:vertex.id})
        } else if (vertex.type=='w') {
            PubSub.publish('loadSlide',{wid:vertex.id})
        } else if (vertex.type=='v') {
            PubSub.publish('uriReq',{uri:vertex.uri})
        }
    }
}


