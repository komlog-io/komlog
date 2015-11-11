var Slide = React.createClass({
    styles: {
        slidestyle:  {
            padding: '1px',
            margin: '5px',
            backgroundColor: 'white',
            boxShadow: '1px 1px 5px 1px #ccc',
            borderRadius: '5px',
        },
    },
    getInitialState: function () {
        return {
                conf:{},
                shareCounter: 0,
                }
    },
    closeCallback: function() {
        PubSub.publish('closeSlide',{lid:this.props.lid})
    },
    getSlideEl: function () {
        switch (this.props.type) {
            case 'wid':
                return (
                  <Widget bid={this.props.bid} closeCallback={this.closeCallback} wid={this.props.lid} isPinned={this.props.isPinned} />
                    );
                break;
            case 'nid':
                return (
                  <Snapshot closeCallback={this.closeCallback} nid={this.props.lid} tid={this.props.tid}/>
                    );
                break;
            default:
                return null;
                break;
        }
    },
    render: function() {
        slide=this.getSlideEl();
        return (
        <div className="Slide modal-container" style={this.styles.slidestyle} >
          {slide}
        </div>
        );
    },
});


var Workspace= React.createClass({
    getInitialState: function () {
        return {
                dashboards: [{bid:'0'}],
                activeDashboard: '0',
               }
    },
    subscriptionTokens: [],
    subscriptionHandler: function(msg,data) {
        switch(msg){
            case 'showDashboard':
                this.switchActiveDashboard(data.bid)
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens.push({token:PubSub.subscribe('showDashboard', this.subscriptionHandler),msg:'showDashboard'});
    },
    componentWillUnmount: function () {
        this.subscriptionTokens.map(function (d) {
            PubSub.unsubscribe(d.token)
            });
    },
    switchActiveDashboard: function (bid) {
        console.log('switchActiveDashboard');
        if (this.state.activeDashboard.toString() == bid.toString()) {
            console.log('same Dashboard');
            return;
        } else {
            for (var i=0; i<this.state.dashboards.length; i++) {
                if (this.state.dashboards[i].bid.toString() == bid.toString()) {
                    this.setState({activeDashboard:bid.toString()});
                    return;
                }
            }
            dashboard=dashboardStore._dashboardConfig[bid.toString()];
            if (dashboard != undefined && dashboard.dashboardname != undefined) {
                dashboards=this.state.dashboards
                dashboards.push({bid:bid.toString()})
                this.setState({dashboards:dashboards,activeDashboard:bid.toString()})
            }
        }
    },
    closeDashboard: function (bid) {
        if (bid.toString() != '0') {
            dashboards=this.state.dashboards.filter(function (el) {
                return el.bid.toString() !== bid.toString();
            });
            this.setState({activeDashboard:'0',dashboards:dashboards})
        }
    },
    getDashboards: function () {
        dashboards=this.state.dashboards.map(function (el) {
            if (this.state.activeDashboard == el.bid) {
                active=true
            } else {
                active=false
            }
            return <Dashboard key={el.bid} bid={el.bid} active={active} closeCallback={this.closeDashboard}/>
        }.bind(this));
        return dashboards;
    },
    render: function () {
        dashboards = this.getDashboards()
        return (<div className="workspace">
                {dashboards}
                </div>);
    },
});

React.render(
    <Workspace />
    ,
    document.getElementById('workspace-content')
);

