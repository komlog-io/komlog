var UserHeader= React.createClass({
    getInitialState: function () {
        return {username:'',uid:null,email:''}
    },
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'myUserConfigUpdate':
                this.refreshConfig(data)
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens=[];
        this.subscriptionTokens.push({token:PubSub.subscribe('myUserConfigUpdate', this.subscriptionHandler),msg:'myUserConfigUpdate'});
    },
    componentDidMount: function () {
        PubSub.publish('myUserConfigReq',{})
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens, function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        this.subscriptionTokens=[];
    },
    refreshConfig: function(uid) {
        refresh=false;
        if (this.state.uid==null) {
            refresh=true;
        } else if (this.state.uid == uid) {
            refresh=true;
        }
        if (refresh==true) {
            if (userStore._userConfig.hasOwnProperty(uid)) {
                userConfig=userStore._userConfig[uid]
                this.setState({'username':userConfig.username,
                               'uid':userConfig.uid,
                               'email':userConfig.email,
                });
            }
        }
    },
    render: function () {
        return (
    <ReactBootstrap.Navbar fixedTop fluid="True">
        <ReactBootstrap.Nav pullLeft>
            Komlog
        </ReactBootstrap.Nav>
        <ReactBootstrap.Nav pullRight >
            <ReactBootstrap.NavDropdown pullRight title={this.state.username}>
                <ReactBootstrap.MenuItem key={1}>
                <span><ReactBootstrap.Glyphicon glyph="cog" /> {this.state.email}</span>
                </ReactBootstrap.MenuItem>
                <ReactBootstrap.MenuItem divider />
                <ReactBootstrap.MenuItem key={2} href="/logout">
                    <span><ReactBootstrap.Glyphicon glyph="log-out" /> Log Out</span>
                </ReactBootstrap.MenuItem>
            </ReactBootstrap.NavDropdown>
        </ReactBootstrap.Nav>
    </ReactBootstrap.Navbar>
);
    },
});

React.render(
    <UserHeader />
    ,
    document.getElementById('user-header')
);

