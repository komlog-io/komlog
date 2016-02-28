var SideMenu = React.createClass({
    getInitialState: function () {
        return {
            activeTab: 1
        }
    },
    componentDidMount: function () {
        console.log('el side menu está listo')
    },
    switchTab: function (eventKey) {
        if (eventKey != this.state.activeTab) {
            this.setState({activeTab:eventKey})
        }
    },
    render: function () {
        return React.createElement('div', null,
            React.createElement('div',{className:"brand"},"_< Komlog"),
            React.createElement(MenuToolBar,null),
            React.createElement(ReactBootstrap.Tabs, {activeKey:this.state.activeTab, onSelect: this.switchTab},
              React.createElement(ReactBootstrap.Tab, {eventKey:1, title:"Dashboards"}, React.createElement(DashboardList, null)),
              React.createElement(ReactBootstrap.Tab, {eventKey:2, title:"Data model"}, React.createElement(TreeItem, {uri:''}))
            ),
            React.createElement('div',{className:"side-footer"},
              "Made with ",
              React.createElement('span',{className:'glyphicon glyphicon-heart'}),
              " by ",
              React.createElement('span',{className:'side-footer-brand'},"Komlog")
            )
        );
    }
});

var DashboardList = React.createClass ({
    getInitialState: function () {
        return {
            activeBid: '0'
        }
    },
    subscriptionTokens: [],
    componentWillMount: function () {
        this.subscriptionTokens.push({token:PubSub.subscribe('dashboardConfigUpdate', this.subscriptionHandler),msg:'dashboardConfigUpdate'});

    },
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'dashboardConfigUpdate':
                this.forceUpdate();
                break;
        }
    },
    componentDidMount: function () {
        PubSub.publish('dashboardsConfigReq',{})
    },
    switchDashboard: function (bid, event) {
        event.preventDefault();
        PubSub.publish('showDashboard',{bid:bid})
        this.setState({activeBid:bid})
    },
    getDashboardList: function () {
        var dashboards=[]
        var activeBid = this.state.activeBid
        for (var bid in dashboardStore._dashboardConfig) {
            dashboards.push({bid:bid, dashboardname:dashboardStore._dashboardConfig[bid].dashboardname})
        }
        dashboards.sort(function (a,b) {
            return a.dashboardname-b.dashboardname
        });
        var listItems=$.map(dashboards, function (e,i) {
            var className=activeBid == e.bid ? "list-item-active" : "list-item"
            return React.createElement('li', {key:i+1, className:className, onClick:this.switchDashboard.bind(this, e.bid)},e.dashboardname);
        }.bind(this))
        var className=activeBid == 0 ? "list-item-active" : "list-item"
        return React.createElement('ul', {className:"menu-list"},
                 React.createElement('li', {key:0, className:className, onClick:this.switchDashboard.bind(this,'0')},"Home"),
                 listItems
               );
    },
    render: function () {
        var dashboardList = this.getDashboardList()
        return dashboardList
    }
});


var MenuToolBar= React.createClass({
    getInitialState: function () {
        return {inputName:'',
                inputStyle:null,
                inputPlaceholder:'Name'}
    },
    subscriptionTokens: [],
    subscriptionHandler: function (msg,data) {
        if (/dashboardConfigUpdate/.test(msg)) {
            this.updateDashboardList()
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens.push({token:PubSub.subscribe('dashboardConfigUpdate', this.subscriptionHandler),msg:'dashboardConfigUpdate'});
    },
    componentDidMount: function () {
        PubSub.publish('dashboardsConfigReq',{})
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens, function (d) {
            PubSub.unsubscribe(d.token)
            });
    },
    handleChange: function () {
        name=this.refs.inputName.getValue();
        this.setState({inputName:name,inputStyle:null})
    },
    newGraph: function () {
        name=this.refs.inputName.getValue();
        if (name.length==0) {
            this.setState({inputStyle:'error'})
        } else {
            data={type:'mp',widgetname:name}
            PubSub.publish('newWidget',data)
            this.setState({inputName:'',inputStyle:''})
        }
    },
    newDashboard: function () {
        name=this.refs.inputName.getValue();
        if (name.length==0) {
            this.setState({inputStyle:'error'})
        } else {
            console.log('new dashboard',name)
            data={dashboardname:name}
            PubSub.publish('newDashboard',data)
            this.setState({inputName:'',inputStyle:''})
        }
        
    },
    switchDb: function (bid,e) {
        console.log('switch db')
        e.preventDefault();
        PubSub.publish('showDashboard',{bid:bid})
    },
    getDashboardList: function () {
        dashboards=$.map(dashboardStore._dashboardConfig, function (e,i) {
            return React.createElement(ReactBootstrap.MenuItem, {key:i+1, onSelect:this.switchDb.bind(this, e.bid)},e.dashboardname);
        }.bind(this))
        return React.createElement(ReactBootstrap.Dropdown.Menu, null,
                 React.createElement(ReactBootstrap.MenuItem, {key:0, onSelect:this.switchDb.bind(this,'0')},"Main"),
                 dashboards
               );
    },
    updateDashboardList: function () {
        console.log('actualizando menu dashboard')
        this.forceUpdate();
    },
    render: function () {
        inputOptions=React.createElement(ReactBootstrap.Dropdown, {id:"menu"},
                       React.createElement(ReactBootstrap.Dropdown.Toggle, {noCaret:true},
                         React.createElement(ReactBootstrap.Glyphicon, {glyph:"plus"})
                       ),
                       React.createElement(ReactBootstrap.Dropdown.Menu, null,
                         React.createElement(ReactBootstrap.MenuItem, {ref:"newGraph", onSelect:this.newGraph},
                           React.createElement('span', null,
                             React.createElement(ReactBootstrap.Glyphicon, {glyph:"equalizer"}),
                             " New graph"
                           )
                         ),
                         React.createElement(ReactBootstrap.MenuItem, {ref:"newDashboard", onSelect:this.newDashboard},
                           React.createElement('span', null,
                             React.createElement(ReactBootstrap.Glyphicon, {glyph:"th-large"}),
                             " New dashboard"
                           )
                         )
                       )
                     );
        return React.createElement(ReactBootstrap.ButtonGroup, null,
                 React.createElement(ReactBootstrap.Input, {onChange:this.handleChange, placeholder:this.state.inputPlaceholder, value:this.state.inputName, bsStyle:this.state.inputStyle, ref:"inputName", type:"text", buttonBefore:inputOptions})
               );
    }
});

ReactDOM.render(
    React.createElement(SideMenu,null)
    ,
    document.getElementById('side-menu')
);

