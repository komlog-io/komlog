var ConfigMenu = React.createClass({
    getInitialState: function () {
        return {
            activeTab: 1
        }
    },
    componentDidMount: function () {
    },
    switchTab: function (eventKey) {
        if (eventKey != this.state.activeTab) {
            if (eventKey === 2) {
                PubSub.publish('uriReq',{uri:''})
            }
            this.setState({activeTab:eventKey})
        }
    },
    render: function () {
        return React.createElement('div', null,
            React.createElement('div', {className: "side-config-menu"},
              React.createElement('a',{href:"/home"},
                React.createElement('div',{className:"brand"},"_< Komlog")
              ),
              React.createElement('ul',null,
                React.createElement('li',null,"Account"),
                React.createElement('li',null,"Agents"),
                React.createElement('li',null,"Billing")
              ),
              React.createElement('div',{className:"side-footer"},
                "Made with ",
                React.createElement('span',{className:'glyphicon glyphicon-heart'}),
                " by ",
                React.createElement('span',{className:'side-footer-brand'},"Komlog")
              )
            ),
            "ESTO ES EL CONTENIDO DE LA CONFIGURACION"
          );
    }
});

var AgentSubMenu = React.createClass({
    render: function () {
        return React.createElement('div', null,
            React.createElement('div', {className: "side-config-menu"},
              React.createElement('a',{href:"/home"},
                React.createElement('div',{className:"brand"},"_< Komlog")
              ),
              React.createElement('div',{className:"side-footer"},
                "Made with ",
                React.createElement('span',{className:'glyphicon glyphicon-heart'}),
                " by ",
                React.createElement('span',{className:'side-footer-brand'},"Komlog")
              )
            ),
            "ESTO ES EL CONTENIDO DE LA CONFIGURACION"
          );
    }
});

ReactDOM.render(
    React.createElement(ConfigMenu,null)
    ,
    document.getElementById('config-menu')
);

