function EventStore () {
    this._events = [];
    this.subscriptionTokens = [];
    this.activeLoop = true;

    this.subscriptionTokens.push({token:PubSub.subscribe('deleteEvent', this.subscriptionHandler.bind(this)),msg:'deleteEvent'});

}

EventStore.prototype = {
    subscriptionHandler: function (msg, data) {
        switch (msg) {
            case 'deleteEvent':
                processMsgDeleteEvent(data)
                break;
        }
    },
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
    deleteEvent: function (seq) {
        events=this._events.filter( function (el) {
            return el.seq !== seq
        });
        this._events=events
    }
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
        console.log('asi queda el store',eventStore._events)
        sendNewEventsMessage()
    }
}

function sendNewEventsMessage () {
    PubSub.publish('newEvents',{})
}

function getEventList (numElem, lastSeq) {
    console.log('getEventList',numElem,lastSeq)
    events=[]
    if (eventStore._events.length == 0) {
        console.log('getEventList: no hay eventos',events)
        return events
    } else if (typeof lastSeq === "undefined") {
        lastIndex=0
        console.log('getEventList: lastIndex',lastIndex)
    } else {
        for (var i=eventStore._events.length;i>0;i--) {
            if (eventStore._events[i-1].seq == lastSeq) {
                lastIndex=i;
                break;
            }
        }
        console.log('getEventList: lastIndex',lastIndex)
    }
    if (typeof lastIndex === "undefined" ) {
        lastIndex=0
        console.log('getEventList: lastIndex',lastIndex)
    }
    firstIndex=lastIndex+numElem
    if (firstIndex>eventStore._events.length-1|| isNaN(firstIndex) ) {
        firstIndex=eventStore._events.length-1;
    }
    console.log('getEventList: firstIndex',firstIndex)
    for (var j=firstIndex;j>=lastIndex;j--) {
        events.push(eventStore._events[j])
    }
    console.log('getEventList: return',events)
    return events
}

function getNumEventsNewerThan (lastSeq) {
    console.log('getNumEventsNewerThan',lastSeq)
    if (eventStore._events.length == 0) {
        console.log('getNumEventsNewerThan: no hay eventos',0)
        return 0
    } else if (typeof lastSeq === "undefined") {
        console.log('getNumEventsNewerThan: undefined',0)
        return 0
    } else {
        for (var i=eventStore._events.length;i>=0;i--) {
            if (eventStore._events[i-1].seq == lastSeq) {
                console.log('getNumEventsNewerThan. coincide',eventStore._events.length,i)
                numEvents=eventStore._events.length-i
                break;
            }
        }
    }
    console.log('getNumEventsNewerThan',numEvents)
    return numEvents
}

function processMsgDeleteEvent(msgData) {
    if (msgData.hasOwnProperty('seq')) {
        $.ajax({
                url: '/var/usr/ev/'+msgData.seq,
                dataType: 'json',
                type: 'DELETE',
            })
            .then(function(data){
                eventStore.deleteEvent(msgData.seq)
            }, function(data){
                console.log('server Delete Event error',data)
            });
    }
}

