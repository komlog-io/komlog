var NavigationGraph = React.createClass({
    render: function () {
        return <ResourceGraph />
    },
});

var ResourceGraph = React.createClass({
    getInitialState: function () {
        return {selectedUri:'',graphData:{}}
    },
    subscriptionTokens: [],
    componentWillMount: function () {
        this.subscriptionTokens.push({token:PubSub.subscribe('uriUpdate', this.subscriptionHandler),msg:'uriUpdate'});
    },
    focusUri: function (uri) {
        this.state.selectedUri=uri
        PubSub.publish('uriReq',{uri:uri})
    },
    segmentClicked: function (num) {
        uri=this.state.selectedUri.split('.').slice(0,num+1).join('.')
        this.focusUri(uri)
    },
    componentDidMount: function () {
        PubSub.publish('uriReq',{uri:this.state.selectedUri})
        var el = React.findDOMNode(this)
        d3ResourceGraph.create(el, this.state.graphData, this.focusUri)
    },
    componentDidUpdate: function () {
        var el = React.findDOMNode(this)
        d3ResourceGraph.update(el, this.state.graphData, this.focusUri)
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens, function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
    },
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'uriUpdate':
                if (data.uri == this.state.selectedUri) {
                    this.refreshGraph()
                }
                break;
        }
    },
    refreshGraph: function () {
        data=getUriGraph(this.state.selectedUri,50)
        this.setState({graphData:data})
    },
    render: function () {
        navbar = $.map(this.state.selectedUri.split('.'), function (d,i) {
            if (d.length>0) {
                uri=d
                return <span key={i}><a onClick={function (event){event.preventDefault();this.segmentClicked(i)}.bind(this)}>{'.'+d}</a></span>
            }
        }.bind(this));
        return (<div>
                 <div>
                    <span className="glyphicon glyphicon-home" onClick={function (event) {event.preventDefault();this.focusUri('')}.bind(this)}></span>
                     {navbar}
                 </div>
                 <svg/>
                </div>);
    }
});

React.render(
    <NavigationGraph />
    ,
    document.getElementById('navigation-graph-box')
);

