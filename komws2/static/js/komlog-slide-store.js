function SlideStore () {
    this._slideConfig = {};
    this._slidesRelated = {};
    this._slidesLoaded = []
    this.subscriptionTokens = [];
    this.registeredRequests = [];
    this.activeLoop = true;

    this.subscriptionTokens.push({token:PubSub.subscribe('slideConfigReq', this.subscriptionHandler.bind(this)),msg:'slideConfigReq'});
    this.subscriptionTokens.push({token:PubSub.subscribe('newSlide', this.subscriptionHandler.bind(this)),msg:'newSlide'});
    this.subscriptionTokens.push({token:PubSub.subscribe('modifySlide', this.subscriptionHandler.bind(this)),msg:'modifySlide'});
    this.subscriptionTokens.push({token:PubSub.subscribe('deleteSlide', this.subscriptionHandler.bind(this)),msg:'deleteSlide'});
    this.subscriptionTokens.push({token:PubSub.subscribe('closeSlide', this.subscriptionHandler.bind(this)),msg:'closeSlide'});
    this.subscriptionTokens.push({token:PubSub.subscribe('newSlideLoaded', this.subscriptionHandler.bind(this)),msg:'newSlideLoaded'});
    
}

SlideStore.prototype = {
    subscriptionHandler: function (msg, data) {
        switch (msg) {
            case 'slideConfigReq':
                processMsgSlideConfigReq(data)
                break;
            case 'newSlideLoaded':
                processMsgNewSlideLoaded(data)
                break;
            case 'newSlide':
                processMsgNewSlide(data)
                break;
            case 'modifySlide':
                processMsgModifySlide(data)
                break;
            case 'deleteSlide':
                processMsgDeleteSlide(data)
                break;
            case 'closeSlide':
                processMsgCloseSlide(data)
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
                    case 'requestSlideConfig':
                        requestSlideConfig(request.lid)
                        break;
                }
            }
        }
        if (this.activeLoop === true ) {
            setTimeout(this.requestLoop.bind(this),15000)
        }
    },
};

var slideStore = new SlideStore();
slideStore.requestLoop()


function processMsgCloseSlide(msgData) {
    new_slides=slideStore._slidesLoaded.filter(function (el) {
            return el.lid.toString()!==msgData.lid.toString();
        });
    slideStore._slidesLoaded=new_slides;
}

function processMsgNewSlide(msgData) {
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
    })
}

function processMsgModifySlide(msgData) {
    var modifyWidgetname = function (widgetname) {
        requestData={widgetname:widgetname}
        return $.ajax({
            url: '/etc/wg/'+msgData.lid,
            dataType: 'json',
            type: 'PUT',
            data: JSON.stringify(requestData),
        })
    }
    var addDatapoint = function (pid) {
        return $.ajax({
            url: '/etc/wg/'+msgData.lid+'/dp/'+pid,
            dataType: 'json',
            type: 'POST',
        })
    }
    var deleteDatapoint = function (pid) {
        return $.ajax({
            url: '/etc/wg/'+msgData.lid+'/dp/'+pid,
            dataType: 'json',
            type: 'DELETE',
        })
    }
    var endModify = function () {
        PubSub.publish('slideConfigReq',{lid:msgData.lid})
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

function processMsgDeleteSlide(msgData) {
    if (msgData.hasOwnProperty('lid')) {
        $.ajax({
                url: '/etc/wg/'+msgData.lid,
                dataType: 'json',
                type: 'DELETE',
            })
            .then(function(data){
                PubSub.publish('closeSlide',{lid:msgData.lid});
            }, function(data){
                PubSub.publish('closeSlide',{lid:msgData.lid});
            });
    }
}

function processMsgSlideConfigReq (data) {
    if (data.hasOwnProperty('lid')) {
        reqArray=$.grep(slideStore.registeredRequests, function (e) {return e.lid == data.lid && e.requestType == 'requestSlideConfig'})
        if (reqArray.length == 0) {
            slideStore.registeredRequests.push({requestType:'requestSlideConfig',lid:data.lid,interval:120000})
        }
        if (slideStore._slideConfig.hasOwnProperty(data.lid)) {
            sendSlideConfigUpdate(data.lid)
        }
        requestSlideConfig(data.lid)
    }
}

function requestSlideConfig (lid) {
    $.ajax({
        url: '/etc/wg/'+lid,
        dataType: 'json',
    })
    .done(function (data) {
        changed=storeSlideConfig(lid, data);
        if (changed == true) {
            sendSlideConfigUpdate(lid);
        }
    })
}

function storeSlideConfig (lid, data) {
    doStore=false
    if (!slideStore._slideConfig.hasOwnProperty(lid)) {
        slideStore._slideConfig[lid]={}
        $.each(data, function (key,value) {
            slideStore._slideConfig[lid][key]=value
        });
        doStore=true
    }
    else {
        $.each(data, function (key,value) {
            if (!(slideStore._slideConfig[lid].hasOwnProperty(key) && slideStore._slideConfig[lid][key]==value)) {
                doStore=true
            }
        });
        if (doStore) {
            slideStore._slideConfig[lid]=data
        }
    }
    reqArray=$.grep(slideStore.registeredRequests, function (e) {return e.lid == lid && e.requestType == 'requestSlideConfig'})
    if (reqArray.length == 1) {
        if (doStore == false && reqArray[0].interval<1800000) {
            reqArray[0].interval=parseInt(reqArray[0].interval*1.2)
            reqArray[0].lastRequest=new Date();
        } else if (doStore == true && reqArray[0].interval>300000) {
            reqArray[0].interval=parseInt(reqArray[0].interval*0.8)
            reqArray[0].lastRequest=new Date();
        }
    }
    return doStore;
}

function sendSlideConfigUpdate (lid) {
    if (slideStore._slideConfig.hasOwnProperty(lid)) {
        PubSub.publish('slideConfigUpdate-'+lid,lid)
    }
}

function processMsgNewSlideLoaded (data) {
    slide=$.grep(slideStore._slidesLoaded, function (e) {return e.shortcut == data.slide.shortcut})
    if (slide.length == 0) {
        slideStore._slidesLoaded.push(data.slide)
    }
    if (slideStore._slidesRelated.hasOwnProperty(data.slide.lid)) {
        sendShowSlidesRelated(data.slide.lid)
    } else {
        requestSlidesRelated(data.slide.lid)
    }
}

function sendShowSlidesRelated (lid) {
    if (slideStore._slidesRelated.hasOwnProperty(lid)) {
        PubSub.publish('showSlidesRelated',{lid:lid})
    }
}

function requestSlidesRelated (lid) {
    $.ajax({
        url: '/etc/wg/'+lid+'/rel/',
        dataType: 'json',
    })
    .done(function (data) {
        storeSlidesRelated(lid, data);
        sendShowSlidesRelated(lid)
    })
}

function storeSlidesRelated (lid, data) {
    slideStore._slidesRelated[lid]=[]
    $.each(data, function (d,i) {
        slideStore._slidesRelated[lid].push(i)
    });
}

function getSlidesRelated (lid) {
    slides=[]
    if (slideStore._slidesRelated.hasOwnProperty(lid)) {
        for (var i=0;i<slideStore._slidesRelated[lid].length;i++) {
            slide=$.grep(slideStore._slidesLoaded, function (e) {return e.lid == slideStore._slidesRelated[lid][i].wid})
            if (slide.length == 0) {
                if (slideStore._slidesRelated[lid][i].type=='ds') {
                    className="glyphicon glyphicon-file"
                } else if (slideStore._slidesRelated[lid][i].type=='dp') {
                    className="glyphicon glyphicon-stats"
                } else {
                    className="glyphicon glyphicon-equalizer"
                }
                slides.push({wid:slideStore._slidesRelated[lid][i].wid,widgetname:slideStore._slidesRelated[lid][i].widgetname,type:slideStore._slidesRelated[lid][i].type, className:className})
            }
        }
    }
    return slides
}

