var ReactCSSTransitionGroup = React.addons.CSSTransitionGroup;

var TreeItem = React.createClass({
    getInitialState: function () {
        return {collapse:true,draggable:'false',children:[], collapseGlyph:'menu-right', typeGlyph:'unchecked'}
    },
    subscriptionTokens: [],
    componentWillMount: function () {
        console.log('estoy vivo');
        this.subscriptionTokens.push({token:PubSub.subscribe('uriUpdate', this.subscriptionHandler),msg:'uriUpdate'});
        path=this.props.uri.split('.')
        paddingLeft=(path.length-1)*17
        name=path[path.length-1]
        this.setState({name:name,style:{paddingLeft:paddingLeft.toString()+'px'}})
    },
    componentDidMount: function () {
        PubSub.publish('uriReq',{uri:this.props.uri})
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens, function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
    },
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'uriUpdate':
                if (data.uri == this.props.uri) {
                    this.refreshTree()
                }
                break;
        }
    },
    onDragStart: function (event) {
        console.log('dragstart')
        event.stopPropagation()
        if (this.state.navDraggable=='true') {
            event.dataTransfer.setData('id',this.state.id)
        }
    },
    toggleCollapse: function (event) {
        event.stopPropagation();
        collapseGlyph= this.state.collapse ? 'menu-down' : 'menu-right'
        this.setState({collapse:!this.state.collapse, collapseGlyph:collapseGlyph})
    },
    requestAction: function (event) {
        event.stopPropagation();
        PubSub.publish('uriActionReq',{id:this.state.id});
    },
    refreshTree: function () {
        info=getNodeInfo(this.props.uri)
        refresh=false
        if ($(this.state.children).not(info.children).length === 0 && $(info.children).not(this.state.children).length === 0) {
            refresh=true
        }
        if (!refresh && info.type != this.state.type) {
            refresh=true
        }
        if (!refresh && info.id != this.state.id) {
            refresh=true
        }
        if (refresh) {
            orderedChildren=info.children.sort(function (a,b) {
                return a>b ? 1 : -1;
            });
            draggable=(info.type=='p'? 'true':'false')
            if (info.type=='p'){
                typeGlyph='stats'
                hasActions=true
            } else if (info.type =='d') {
                typeGlyph='file'
                hasActions=true
            } else {
                typeGlyph='unchecked'
                hasActions=false
            }
            this.setState({children:orderedChildren,type:info.type,id:info.id,draggable:draggable,typeGlyph:typeGlyph,hasActions:hasActions})
        }
    },
    render: function () {
        if (this.props.uri == '') {
            children=$.map(this.state.children, function (uri,i) {
                return React.createElement(TreeItem, {key:uri, uri:uri})
            });

            return React.createElement('div', null, 
                     React.createElement(ReactCSSTransitionGroup, {transitionName:"list-item", transitionEnterTimeout:500, transitionLeaveTimeout:300}, children)
                     );
        } else {
            if (this.state.collapse == false) {
                if (this.state.children.length>0) {
                    collapseIcon=React.createElement(ReactBootstrap.Glyphicon, {style:{width:'15px'}, glyph:this.state.collapseGlyph});
                    children=$.map(this.state.children, function (uri, i) {
                        return React.createElement(TreeItem, {key:uri, uri:uri});
                    });
                } else {
                    collapseIcon=React.createElement('span', {style:{marginLeft:'15px'}});
                    children=null
                }
            } else {
                children=null
                if (this.state.children.length>0) {
                    collapseIcon=React.createElement(ReactBootstrap.Glyphicon, {style:{width:'15px'}, glyph:this.state.collapseGlyph});
                } else {
                    collapseIcon=React.createElement('span', {style:{marginLeft:'15px'}});
                }
            }
            if (this.state.hasActions) {
                action=React.createElement('div', {style:{width:'15px', float:'right'}}, 
                         React.createElement(ReactBootstrap.Glyphicon, {style:{color:'#555',marginRight:'-10px'}, glyph:'triangle-right', onClick:this.requestAction})
                         );
            } else {
                action=null
            }
            return  React.createElement('div', null, 
                        React.createElement('div', {className:'tree-item', draggable:this.state.draggable, onDragStart:this.onDragStart},
                        action, 
                        React.createElement('div', {style:this.state.style, onClick:this.toggleCollapse}, 
                          collapseIcon,
                          React.createElement(ReactBootstrap.Glyphicon, {style:{width:'15px',paddingLeft:'2px'}, glyph:this.state.typeGlyph}),
                          React.createElement('span', {style:{paddingLeft:'5px'}}, this.state.name)
                          )
                        ),
                        React.createElement(ReactCSSTransitionGroup, {transitionName:'list-item', transitionEnterTimeout:500, transitionLeaveTimeout:300}, 
                          children)
                        );
        }
    },
});

ReactDOM.render(
    React.createElement(TreeItem, {uri:''})
    ,
    document.getElementById('navigation-tree')
);

