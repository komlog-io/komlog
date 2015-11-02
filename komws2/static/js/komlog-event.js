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
        console.log('disable',seq,e)
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
    generateDateString: function (timestamp) {
        if (typeof timestamp === 'number') {
            var date = new Date(timestamp*1000);
            var hours = date.getHours();
            var minutes = "0" + date.getMinutes();
            var seconds = "0" + date.getSeconds();
            return hours + ':' + minutes.substr(minutes.length-2) + ':' + seconds.substr(seconds.length-2);
        } else {
            return ''
        }
    },
    getEventList: function () {
        eventList = $.map(this.state.events, function (d,i) {
            date=this.generateDateString(d.ts)
            if (d.type < 1000) {
                icon=(<ReactBootstrap.Glyphicon glyph="info-sign" />)
                className="userevents-panel "+d.priority
                if (d.type == 1) {
                    title=(<span>New User</span>)
                    message=(<div>Welcome to Komlog, {d.params.username}!</div>)
                } else if (d.type == 2) {
                    title=<span>New Agent</span>
                    message=(<div>Agent {d.params.agentname} was created.</div>)
                } else if (d.type == 3) {
                    title=<span>New Datasource</span>
                    message=(<div>Datasource <a onClick={() => PubSub.publish('loadSlide',{did:d.params.did})}>{d.params.datasourcename}</a> created.</div>)
                } else if (d.type == 4) {
                    title=<span>New Datapoint</span>
                    message=(<div>Datapoint <a onClick={() => PubSub.publish('loadSlide',{pid:d.params.pid})}>{d.params.datapointname}</a> created, associated to datasource <a onClick={() => PubSub.publish('loadSlide',{did:d.params.did})}>{d.params.datasourcename}</a>.</div>)
                } else if (d.type == 5) {
                    title=<span>New Graph</span>
                    message=(<div>Graph <a onClick={() => PubSub.publish('loadSlide',{wid:d.params.wid})}>{d.params.widgetname}</a> created.</div>)
                } else if (d.type == 6) {
                    title=<span>New Dashboard</span>
                    message=(<div>Dashboard <a onClick={() => PubSub.publish('loadSlide',{bid:d.params.bid})}>{d.params.dashboardname}</a> created.</div>)
                } else if (d.type == 7) {
                    title=<span>New Circle</span>
                    message=(<div>Circle {d.params.circlename} created.</div>)
                    message=(<div>Welcome to Komlog</div>)
                } else if (d.type == 8) {
                    title=<span>New Snapshot Shared</span>
                    message=(<div>New snapshot shared of <a onClick={() => PubSub.publish('loadSlide',{nid:d.params.nid})}>{d.params.widgetname}</a>.</div>)
                } else if (d.type == 9) {
                    title=<span>New Snapshot Received</span>
                    message=(<div>User {d.params.username} shared a snapshot of <a onClick={() => PubSub.publish('loadSlide',{nid:d.params.nid,tid:d.params.tid})}>{d.params.widgetname}</a> with you.</div>)
                } else {
                    title=<span></span>
                    message=(<div></div>)
                }
            } else if (d.type >= 1000 && d.type <10000) {
                icon=(<ReactBootstrap.Glyphicon glyph="question-sign" />)
                    title=<span>New Snapshot Received</span>
                    message=(<div>Welcome to Komlog</div>)
            } else {
                icon=(<ReactBootstrap.Glyphicon glyph="exclamation-sign" />)
                    title=<span>New Snapshot Received</span>
                    message=(<div>Welcome to Komlog</div>)
            }
            return (<li key={d.seq} className="userevents">
                      <div className={className}>
                        <div className="userevents-bar">
                          <span><ReactBootstrap.Glyphicon glyph="time" />
                          &nbsp;{date}
                          </span>
                          <span onClick={this.disableEvent.bind(this,d.seq)} className="pull-right">
                            <ReactBootstrap.Glyphicon glyph="remove" />
                          </span>
                        </div>
                        <div className="userevents-title">
                          {icon}&nbsp;
                          {title}
                        </div>
                        <div className="userevents-body">
                          {message}
                        </div>
                      </div>
                    </li>
                    );
        }.bind(this));
        return eventList
    },
    render: function () {
        console.log('listado de eventos',this.state.events)
        console.log('el stado queda',this.state.numNewEvents,this.state.lastSeq)
        eventList = this.getEventList();
        return (
                <div>
                  <div className="update-panel">
                    <ReactBootstrap.Collapse in={this.state.newEvents}>
                      <div>
                        <ReactBootstrap.Well>
                          <ReactBootstrap.Badge pullRight={true} >
                          {this.state.numNewEvents}
                          </ReactBootstrap.Badge>
                          <ReactBootstrap.Glyphicon onClick={this.showNewEvents} glyph="refresh" />
                          &nbsp;New Events
                        </ReactBootstrap.Well>
                      </div>
                    </ReactBootstrap.Collapse>
                  </div>
                  <ul className="userevents">
                   {eventList}
                  </ul>
                </div>
                );
    }
});

React.render(
    <EventsSideBar />
    ,
    document.getElementById('events-sidebar')
);

