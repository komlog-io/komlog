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
        return React.createElement(ReactBootstrap.Navbar, {staticTop:true, fluid:true},
                 React.createElement(ReactBootstrap.Nav, {pullRight:true},
                   React.createElement(ReactBootstrap.NavDropdown, {id:"dropdown",noCaret:true, pullRight:true, title:this.state.username},
                     React.createElement(ReactBootstrap.MenuItem, {key:1, href:"/config"},
                       React.createElement('span', null,
                         React.createElement(ReactBootstrap.Glyphicon, {glyph:"cog"}),
                         " Configuration" 
                       )
                     ),
                     React.createElement(ReactBootstrap.MenuItem, {divider:true}),
                     React.createElement(ReactBootstrap.MenuItem, {key:2, href:"/logout"},
                       React.createElement('span', null,
                         React.createElement(ReactBootstrap.Glyphicon, {glyph:"log-out"}),
                         " Log Out"
                       )
                     )
                   )
                 )
               );
    },
});

ReactDOM.render(
    React.createElement(UserHeader, null)
    ,
    document.getElementById('user-header')
);

