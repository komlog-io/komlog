var DesktopMenu = React.createClass({
    getInitialState: function () {
        return {inputName:'',
                inputStyle:'',
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
        this.setState({inputName:name,inputStyle:''})
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
            return (
                 <ReactBootstrap.MenuItem key={i+1} onSelect={this.switchDb.bind(this,e.bid)} >
                     {e.dashboardname}
                 </ReactBootstrap.MenuItem>
                 )
        }.bind(this))
        return ( <ReactBootstrap.Dropdown.Menu>
                   <ReactBootstrap.MenuItem key={0} onSelect={this.switchDb.bind(this,'0')} >
                     Main
                   </ReactBootstrap.MenuItem>
                   {dashboards}
                 </ReactBootstrap.Dropdown.Menu>
               );
    },
    updateDashboardList: function () {
        console.log('actualizando menu dashboard')
        this.forceUpdate();
    },
    render: function () {
        inputOptions=(
          <ReactBootstrap.Dropdown id="menu">
                 <ReactBootstrap.Dropdown.Toggle noCaret>
                   <ReactBootstrap.Glyphicon glyph="plus" />
                 </ReactBootstrap.Dropdown.Toggle>
                 <ReactBootstrap.Dropdown.Menu>
                   <ReactBootstrap.MenuItem ref="newGraph" onSelect={this.newGraph} >
                     <span><ReactBootstrap.Glyphicon glyph="equalizer" />
                     &nbsp;New Graph
                     </span>
                   </ReactBootstrap.MenuItem>
                   <ReactBootstrap.MenuItem ref="newDashboard" onSelect={this.newDashboard} >
                     <span><ReactBootstrap.Glyphicon glyph="th-large" />
                     &nbsp;New Dashboard
                     </span>
                   </ReactBootstrap.MenuItem>
                 </ReactBootstrap.Dropdown.Menu>
               </ReactBootstrap.Dropdown>
);
        dashboards=this.getDashboardList()
        return (
                   <ReactBootstrap.ButtonGroup>
                     <ReactBootstrap.Dropdown id="dashboards">
                       <ReactBootstrap.Dropdown.Toggle noCaret>
                         <ReactBootstrap.Glyphicon glyph="th-large" />
                       </ReactBootstrap.Dropdown.Toggle>
                       {dashboards}
                     </ReactBootstrap.Dropdown>
                     <ReactBootstrap.Input onChange={this.handleChange} placeholder={this.state.inputPlaceholder} value={this.state.inputName} bsStyle={this.state.inputStyle} ref="inputName" type="text" buttonBefore={inputOptions} />
                   </ReactBootstrap.ButtonGroup>
               );
    }
});

React.render(
    <DesktopMenu />
    ,
    document.getElementById('desktop-menu')
);

