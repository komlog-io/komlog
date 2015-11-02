function SlideStore () {
    this._slidesRelated = {};
    this._slidesLoaded = []
    this.subscriptionTokens = [];

    this.subscriptionTokens.push({token:PubSub.subscribe('closeSlide', this.subscriptionHandler.bind(this)),msg:'closeSlide'});
    this.subscriptionTokens.push({token:PubSub.subscribe('newSlideLoaded', this.subscriptionHandler.bind(this)),msg:'newSlideLoaded'});
    
}

SlideStore.prototype = {
    subscriptionHandler: function (msg, data) {
        switch (msg) {
            case 'newSlideLoaded':
                processMsgNewSlideLoaded(data)
                break;
            case 'closeSlide':
                processMsgCloseSlide(data)
                break;
        }
    },
};

var slideStore = new SlideStore();

function processMsgCloseSlide(msgData) {
    new_slides=slideStore._slidesLoaded.filter(function (el) {
            return el.lid.toString()!==msgData.lid.toString();
        });
    slideStore._slidesLoaded=new_slides;
}

function processMsgNewSlideLoaded (data) {
    slide=$.grep(slideStore._slidesLoaded, function (e) {return e.shortcut == data.slide.shortcut})
    if (slide.length == 0) {
        slideStore._slidesLoaded.push(data.slide)
    }
    if (slideStore._slidesRelated.hasOwnProperty(data.slide.lid)) {
        sendShowSlidesRelated(data.slide.lid)
    } else if (data.slide.type=='wid')  {
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
                } else if (slideStore._slidesRelated[lid][i].type=='mp') {
                    className="glyphicon glyphicon-equalizer"
                } else {
                    className="glyphicon glyphicon-question"
                }
                slides.push({wid:slideStore._slidesRelated[lid][i].wid,widgetname:slideStore._slidesRelated[lid][i].widgetname,type:slideStore._slidesRelated[lid][i].type, className:className})
            }
        }
    }
    return slides
}

