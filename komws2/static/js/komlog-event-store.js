function EventStore () {
    this._events = [];
    this.activeLoop = true;
}

EventStore.prototype = {
    shouldRequest: function () {
        var now = new Date();
        if (typeof this.lastRequest === "undefined"){
            return true;
        } else {
            nextRequest=new Date(this.lastRequest.getTime()+60)
            if (nextRequest < now ) {
                return true;
            } else {
                return false;
            }
        }
    },
    requestLoop: function () {
        now=new Date().getTime()/1000;
        if (this.shouldRequest()) {
            requestEvents()
        }
        if (this.activeLoop === true ) {
            setTimeout(this.requestLoop.bind(this),60000)
        }
    },
};

var eventStore = new EventStore();
eventStore.requestLoop()

function requestEvents () {
    parameters={}
    if (eventStore._events.length>0) {
        parameters.its=eventStore._events[eventStore._events.length-1].ts
    }
    $.ajax({
        url: '/var/usr/ev/',
        dataType: 'json',
        data: parameters,
    })
    .done(function (response) {
        storeEvents(response)
    })
}

function storeEvents (data) {
    newEvents=false;
    for (var i=data.length;i>0;i--) {
        if (eventStore._events.length==0) {
            eventStore._events.push(data[i-1])
            newEvents=true;
        } else {
            for (var j=eventStore._events.length;j>0;j--) {
                if (eventStore._events[j-1].ts<=data[i-1].ts && eventStore._events[j-1].seq!=data[i-1].seq && (j==eventStore._events.length || eventStore._events[j].ts>data[i-1].ts)) {
                    eventStore._events.splice(j,0,data[i-1])
                    newEvents=true
                }
            }
        }
    }
    if (newEvents == true) {
        sendNewEventsMessage()
    }
}

function sendNewEventsMessage () {
    PubSub.publish('newEvents',{})
}

function getEventList (numElem, lastSeq) {
    events=[]
    if (eventStore._events.length == 0) {
        return events
    } else if (typeof lastSeq === "undefined") {
        lastIndex=eventStore._events.length-1
    } else {
        for (var i=eventStore._events.length;i>=0;i--) {
            if (eventStore._events[i-1].seq == lastSeq) {
                lastIndex=i-1;
            }
        }
    }
    if (typeof lastIndex === "undefined" ) {
        lastIndex=eventStore._events.length-1;
    }
    firstIndex=lastIndex-numElem
    if (firstIndex <0) {
        firstIndex=0;
    }
    for (var j=lastIndex;j>=firstIndex;j--) {
        events.push(eventStore._events[j])
    }
    return events
}
