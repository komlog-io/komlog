var EventsSideBar = React.createClass({
    getInitialState: function () {
        return {events:[]}
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
    refreshEvents: function () {
        events=getEventList(15)
        if (this.state.events.length > 0) {
            lastSeq=this.state.events[this.state.events.length-1].seq
        } else {
            lastSeq=undefined
        }
        this.setState({events:events,lastSeq:lastSeq})
    },
    render: function () {
        eventList = $.map(this.state.events, function (d,i) {
            return <li draggable='true' className="userevents-inverted" key={d.seq} dangerouslySetInnerHTML={{__html: d.html}} />
        }.bind(this));
        return (<ul className="userevents">
                 {eventList}
                </ul>);
    }
});

React.render(
    <EventsSideBar />
    ,
    document.getElementById('events-sidebar')
);

