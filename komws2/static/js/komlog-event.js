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
            if (d.type < 1000) {
                icon=React.createElement(ReactBootstrap.Glyphicon, {glyp:"info-sign"});
                //icon=(<ReactBootstrap.Glyphicon glyph="info-sign" />)
                className="userevents-panel "+d.priority
                if (d.type == 1) {
                    title=React.createElement('span', null, "New User");
                    //title=(<span>New User</span>)
                    message=React.createElement('div', null, "Welcome to Komlog, "+d.params.username+"!");
                    //message=(<div>Welcome to Komlog, {d.params.username}!</div>)
                } else if (d.type == 2) {
                    title=React.createElement('span', null, "New Agent");
                    //title=<span>New Agent</span>
                    message=React.createElement('div', null, "Agent "+d.params.agentname+" created.");
                    //message=(<div>Agent {d.params.agentname} was created.</div>)
                } else if (d.type == 3) {
                    title=React.createElement('span', null, "New Datasource");
                    //title=<span>New Datasource</span>
                    message=React.createElement('div', null,
                              "Datasource ",
                              React.createElement('a', {onClick:() => PubSub.publish('loadSlide',{did:d.params.did})}, d.params.datasourcename),
                              " created."
                            );
                    //message=(<div>Datasource <a onClick={() => PubSub.publish('loadSlide',{did:d.params.did})}>{d.params.datasourcename}</a> created.</div>)
                } else if (d.type == 4) {
                    title=React.createElement('span', null, "New Datapoint");
                    //title=<span>New Datapoint</span>
                    message=React.createElement('div', null,
                              "Datapoint ",
                              React.createElement('a', {onClick:() => PubSub.publish('loadSlide',{pid:d.params.pid})}, d.params.datapointname),
                              " created, associated to datasource ",
                              React.createElement('a', {onClick:() => PubSub.publish('loadSlide',{did:d.params.did})}, d.params.datasourcename)
                            );
                    //message=(<div>Datapoint <a onClick={() => PubSub.publish('loadSlide',{pid:d.params.pid})}>{d.params.datapointname}</a> created, associated to datasource <a onClick={() => PubSub.publish('loadSlide',{did:d.params.did})}>{d.params.datasourcename}</a>.</div>)
                } else if (d.type == 5) {
                    title=React.createElement('span', null, "New Graph");
                    //title=<span>New Graph</span>
                    message=React.createElement('div', null,
                              "Graph ",
                              React.createElement('a', {onClick:() => PubSub.publish('loadSlide',{wid:d.params.wid})}, d.params.widgetname),
                              " created."
                            );
                    //message=(<div>Graph <a onClick={() => PubSub.publish('loadSlide',{wid:d.params.wid})}>{d.params.widgetname}</a> created.</div>)
                } else if (d.type == 6) {
                    title=React.createElement('span', null, "New Dashboard");
                    //title=<span>New Dashboard</span>
                    message=React.createElement('div', null,
                              "Dashboard ",
                              React.createElement('a', {onClick:() => PubSub.publish('loadSlide',{bid:d.params.bid})}, d.params.dashboardname),
                              " created."
                            );
                    //message=(<div>Dashboard <a onClick={() => PubSub.publish('loadSlide',{bid:d.params.bid})}>{d.params.dashboardname}</a> created.</div>)
                } else if (d.type == 7) {
                    title=React.createElement('span', null, "New Circle");
                    //title=<span>New Circle</span>
                    message=React.createElement('div', null, "Circle "+d.params.circlename+" created.");
                    //message=(<div>Circle {d.params.circlename} created.</div>)
                } else if (d.type == 8) {
                    title=React.createElement('span', null, "New Snapshot Shared");
                    //title=<span>New Snapshot Shared</span>
                    message=React.createElement('div', null,
                              "New snapshot shared of ",
                              React.createElement('a', {onClick:() => PubSub.publish('loadSlide',{nid:d.params.nid})}, d.params.widgetname),
                              "."
                            );
                    //message=(<div>New snapshot shared of <a onClick={() => PubSub.publish('loadSlide',{nid:d.params.nid})}>{d.params.widgetname}</a>.</div>)
                } else if (d.type == 9) {
                    title=React.createElement('span', null, "New Snapshot Received");
                    //title=<span>New Snapshot Received</span>
                    message=React.createElement('div', null,
                              "User "+d.params.username+' shared a snapshot of ',
                              React.createElement('a', {onClick:() => PubSub.publish('loadSlide',{nid:d.params.nid, tid:d.params.tid})}, d.params.widgetname),
                              " with you."
                            );
                    //message=(<div>User {d.params.username} shared a snapshot of <a onClick={() => PubSub.publish('loadSlide',{nid:d.params.nid,tid:d.params.tid})}>{d.params.widgetname}</a> with you.</div>)
                } else {
                    title=React.createElement('span', null, "?");
                    //title=<span></span>
                    message=React.createElement('div', null, "Whats this?");
                    //message=(<div></div>)
                }
            } else if (d.type >= 1000 && d.type <10000) {
                icon=React.createElement(ReactBootstrap.Glyphicon, {glyp:"question-sign"});
                //icon=(<ReactBootstrap.Glyphicon glyph="question-sign" />)
                    title=React.createElement('span', null, "WTF");
                    //title=<span>New Snapshot Received</span>
                    message=React.createElement('div', null);
                    //message=(<div>Welcome to Komlog</div>)
            } else {
                icon=React.createElement(ReactBootstrap.Glyphicon, {glyp:"exclamation-sign"});
                //icon=(<ReactBootstrap.Glyphicon glyph="exclamation-sign" />)
                    title=React.createElement('span', null, "WTF");
                    //title=<span>New Snapshot Received</span>
                    message=React.createElement('div', null);
                    //message=(<div>Welcome to Komlog</div>)
            }
            return React.createElement('li', {key:d.seq, className:"userevents"},
                     React.createElement('div', {className:className},
                       React.createElement('div', {className:"userevents-bar"},
                         React.createElement('span', null,
                           React.createElement(ReactBootstrap.Glyphicon, {glyph:"time"}),
                             this.getDateStatement(d.ts)
                         ),
                         React.createElement('span', {onClick:this.disableEvent.bind(this,d.seq), className:"pull-right"},
                           React.createElement(ReactBootstrap.Glyphicon, {glyph:"remove"})
                         )
                       ),
                       React.createElement('div', {className:"userevents-title"},
                         icon,
                         " ",
                         title
                       ),
                       React.createElement('div', {className:"userevents-body"}, message)
                     )
                   );
            //return (<li key={d.seq} className="userevents">
                      //<div className={className}>
                        //<div className="userevents-bar">
                          //<span><ReactBootstrap.Glyphicon glyph="time" />
                          //&nbsp;{date}
                          //</span>
                          //<span onClick={this.disableEvent.bind(this,d.seq)} className="pull-right">
                            //<ReactBootstrap.Glyphicon glyph="remove" />
                          //</span>
                        //</div>
                        //<div className="userevents-title">
                          //{icon}&nbsp;
                          //{title}
                        //</div>
                        //<div className="userevents-body">
                          //{message}
                        //</div>
                      //</div>
                    //</li>
                    //);
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
                 React.createElement('ul', {className:"userevents"}, eventList)
               );
        //return (
                //<div>
                  //<div className="update-panel">
                    //<ReactBootstrap.Collapse in={this.state.newEvents}>
                      //<div>
                        //<ReactBootstrap.Well>
                          //<ReactBootstrap.Badge pullRight={true} >
                          //{this.state.numNewEvents}
                          //</ReactBootstrap.Badge>
                          //<ReactBootstrap.Glyphicon onClick={this.showNewEvents} glyph="refresh" />
                          //&nbsp;New Events
                        //</ReactBootstrap.Well>
                      //</div>
                    //</ReactBootstrap.Collapse>
                  //</div>
                  //<ul className="userevents">
                   //{eventList}
                  //</ul>
                //</div>
                //);
    }
});

ReactDOM.render(
    React.createElement(EventsSideBar, null)
    //<EventsSideBar />
    ,
    document.getElementById('events-sidebar')
);

