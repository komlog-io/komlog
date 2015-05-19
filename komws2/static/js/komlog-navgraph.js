var NavigationGraph = React.createClass({
    getInitialState: function () {
        return {items: []}
    },
    componentDidMount: function () {
        $.ajax({
            url: '/etc/wg/',
            dataType: 'json',
        })
        .done(function (data) {
            this.setState({items:data});
        }.bind(this))
    },
    loadSlide: function (wid,e) {
        e.preventDefault();
        PubSub.publish('loadSlide',{wid:wid})
    },
    render: function () {
        items = this.state.items.map( function (item) {
            element=<li key={item.wid} className="list-group-item"><a href="#" onClick={this.loadSlide.bind(null,item.wid)}>{item.widgetname}</a></li>
            return element
        }.bind(this));
        return(<div className="panel panel-default">
                 <div className="panel-heading">Reports</div>
                 <ul className="list-group">
                 {items}
                 </ul>
               </div>);
    },
});

React.render(
    <NavigationGraph />
    ,
    document.getElementById('navigation-graph-box')
);

