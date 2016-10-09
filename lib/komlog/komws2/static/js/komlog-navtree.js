var ReactCSSTransitionGroup = React.addons.CSSTransitionGroup;

var TreeItem = React.createClass({
    getInitialState: function () {
        return {
            collapse:true,
            draggable:false,
            children:[],
            collapseGlyph:'menu-right',
            typeGlyph:'unchecked',
            deleteNode: false
        }
    },
    subscriptionTokens: [],
    componentWillMount: function () {
        this.subscriptionTokens = new Array();
        this.subscriptionTokens.push({
            token:PubSub.subscribe('uriUpdate', this.subscriptionHandler),
            msg:'uriUpdate'
        });
        path=this.props.uri.split('.')
        paddingLeft=(path.length-1)*12
        label=path[path.length-1]
        this.setState({label:label,style:{paddingLeft:paddingLeft.toString()+'px'}})
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
        event.stopPropagation()
        if (this.state.draggable==true) {
            event.dataTransfer.setData('id',this.state.id)
        }
    },
    toggleCollapse: function (event) {
        event.stopPropagation();
        collapseGlyph= this.state.collapse ? 'menu-down' : 'menu-right'
        if (this.state.collapse == true) {
            PubSub.publish('uriReq',{uri:this.props.uri})
        }
        this.setState({collapse:!this.state.collapse, collapseGlyph:collapseGlyph})
    },
    requestAction: function (event) {
        event.stopPropagation();
        PubSub.publish('uriActionReq',{id:this.state.id});
    },
    refreshTree: function () {
        info=UriStore.getNodeInfoByUri(this.props.uri)
        console.log('la info que tengo es',info)
        if (info == null) {
            this.setState({deleteNode: true});
            return
        }
        var refresh=false
        if (this.state.children.length != info.children.length) {
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
            draggable=(info.type=='p'? true:false)
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
            console.log('repinto',this.props.uri)
            this.setState({children:orderedChildren,type:info.type,id:info.id,draggable:draggable,typeGlyph:typeGlyph,hasActions:hasActions})
        }
    },
    render: function () {
        if (this.state.deleteNode) {
            return null;
        } else if (this.props.uri == '') {
            var children=$.map(this.state.children, function (uri,i) {
                return React.createElement(TreeItem, {key:uri, uri:uri})
            });

            return React.createElement('div', null, 
                     React.createElement(ReactCSSTransitionGroup, {transitionName:"tree-item", transitionEnterTimeout:500, transitionLeaveTimeout:300}, children)
                     );
        } else {
            if (this.state.collapse == false) {
                if (this.state.children.length>0) {
                    var collapseIcon=React.createElement(ReactBootstrap.Glyphicon, {style:{width:'10px',fontSize:"8px"}, glyph:this.state.collapseGlyph});
                    var children=$.map(this.state.children, function (uri, i) {
                        return React.createElement(TreeItem, {key:uri, uri:uri});
                    });
                } else {
                    var collapseIcon=React.createElement('span', {style:{marginLeft:'10px'}});
                    var children=null
                }
            } else {
                var children=null
                if (this.state.children.length>0) {
                    var collapseIcon=React.createElement(ReactBootstrap.Glyphicon, {style:{width:'10px',fontSize:"8px"}, glyph:this.state.collapseGlyph});
                } else {
                    var collapseIcon=React.createElement('span', {style:{marginLeft:'10px'}});
                }
            }
            if (this.state.hasActions) {
                var action=React.createElement(ReactBootstrap.Glyphicon, {className:"action-icon", glyph:this.state.typeGlyph, onClick:this.requestAction})
            } else {
                action=null
            }
            return  React.createElement('div', null, 
            React.createElement('div', {className:'tree-item', draggable:this.state.draggable, onDragStart:this.onDragStart},
              action, 
              React.createElement('div', {style:this.state.style, onClick:this.toggleCollapse}, 
                collapseIcon,
                React.createElement('span', {style:{paddingLeft:'5px'}}, this.state.label)
              )
            ),
            React.createElement(ReactCSSTransitionGroup, {transitionName:'tree-item', transitionEnterTimeout:500, transitionLeaveTimeout:300}, children)
            );
        }
    },
});

