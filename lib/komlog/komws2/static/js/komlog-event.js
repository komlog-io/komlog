var EventSummary = React.createClass ({
    componentDidMount: function () {
        var el = ReactDOM.findDOMNode(this)
        if (this.props.data.type == 'dp') {
            d3SummaryLinegraph.create(el, this.props.data.datapoints, this.props.data.its, this.props.data.ets)
        } else if (this.props.data.type == 'mp') {
            d3SummaryLinegraph.create(el, this.props.data.datapoints, this.props.data.its, this.props.data.ets)
        } else if (this.props.data.type == 'ds') {
            d3SummaryDatasource.create(el, this.props.data.datasource, this.props.data.ts)
        }
    },
    render: function () {
        return React.createElement('div', {className: 'user-event-summary'});
    }
});

var EventsSideBar = React.createClass({
    getInitialState: function () {
        return {events:[],
                newEvents: false,
                numNewEvents: undefined,
                lastSeq: undefined,
               }
    },
    subscriptionTokens: [],
    componentWillMount: function () {
        this.subscriptionTokens.push({token:PubSub.subscribe('newEvents', this.subscriptionHandler),msg:'newEvents'});
    },
    componentDidMount: function () {
        this.refreshEvents()
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens, function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
    },
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'newEvents':
                this.refreshEvents()
                break;
        }
    },
    disableEvent: function (seq,e) {
        PubSub.publish('deleteEvent',{seq:seq})
        newEvents=this.state.events.filter( function (el) {
            return el.seq !== seq;
        });
        this.setState({events:newEvents})
    },
    refreshEvents: function () {
        if (this.state.lastSeq == undefined || $('#events-sidebar').position().top==0) {
            this.showNewEvents()
        } else {
            numNewEvents=getNumEventsNewerThan(this.state.lastSeq)
            if (numNewEvents>0) {
                this.setState({newEvents:true,numNewEvents:numNewEvents})
            } else {
                this.setState({newEvents:false,numNewEvents:0})
            }
        }
    },
    showNewEvents: function () {
        events=getEventList(this.state.numNewEvents,this.state.lastSeq)
        if (this.state.events.length > 0) {
            for (var i=0;i<this.state.events.length;i++) {
                events.push(this.state.events[i])
            }
        }
        if (events.length>0) {
            lastSeq=events[0].seq
            numNewEvents=0
        } else {
            lastSeq = undefined
            numNewEvents=undefined
        }
        this.setState({events:events,lastSeq:lastSeq,newEvents:false,numNewEvents:numNewEvents})
    },
    getDateStatement: function (timestamp) {
        if (typeof timestamp === 'number') {
            var date = new Date(timestamp*1000);
            var now = new Date();
            diff = now.getTime()/1000 - timestamp;
            if (diff<0) {
                return React.createElement('span',{title:date.toString()}, ' right now');
            } else {
                if (diff<60) {
                    when=" right now"
                } else if (diff<3600) {
                    when=" "+(diff/60 | 0)+" min"+(diff/60>=2 ? "s":"")+" ago";
                } else if (diff<86400) {
                    when=" "+(diff/3600 | 0)+" hour"+(diff/3600>=2 ? "s":"")+" ago";
                } else if (diff<2678400) {
                    when=" "+(diff/86400 | 0)+" day"+(diff/86400>=2 ? "s":"")+" ago";
                } else {
                    when=" "+(diff/2678400 | 0)+" month"+(diff/2678400>=2 ? "s":"")+" ago";
                }
                return React.createElement('span',{title:date.toString()}, when);
            }
        } else {
            return null
        }
    },
    getEventList: function () {
        eventList = $.map(this.state.events, function (d,i) {
            icon=React.createElement(ReactBootstrap.Glyphicon, {glyph:"info-sign", className:"user-event-id-icon"});
            event_title={__html:d.html.title}
            event_body={__html:d.html.body}
            title=React.createElement('div', {dangerouslySetInnerHTML:event_title});
            body=React.createElement('div', {dangerouslySetInnerHTML:event_body});
            if ('summary' in d && d.summary!=null) {
                summary=React.createElement(EventSummary, {data:d.summary})
            } else {
                summary=null
            }
            return React.createElement('li', {key:d.seq, className:"user-event"},
                     icon,
                     React.createElement('div', {className:"user-event-title"},
                       title
                     ),
                     React.createElement('div', {className:"user-event-subtitle"},
                       this.getDateStatement(d.ts)
                     ),
                     React.createElement('div', {className:"user-event-body"}, body),
                     summary
                   );
        }.bind(this));
        return eventList
    },
    render: function () {
        eventList = this.getEventList();
        return React.createElement('div', null,
                 React.createElement('div', {className:"update-panel"},
                   React.createElement(ReactBootstrap.Collapse, {in:this.state.newEvents},
                     React.createElement('div', null,
                       React.createElement(ReactBootstrap.Well, null,
                         React.createElement(ReactBootstrap.Badge, {pullRight:true}, this.state.numNewEvents),
                         React.createElement(ReactBootstrap.Glyphicon, {onClick:this.showNewEvents, glyph:"refresh"}),
                         " New Events"
                       )
                     )
                   )
                 ),
                 React.createElement('ul', {className:"user-events"}, eventList)
               );
    }
});

ReactDOM.render(
    React.createElement(EventsSideBar, null)
    ,
    document.getElementById('events-sidebar')
);

