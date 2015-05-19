var Shell = React.createClass({
    getInitialState: function () {
        return {placeholder:'type help', value:''}
    },
    commandHandler: function (event) {
        event.preventDefault();
        cmdline=this.state.value.replace(/^\s+|\s+$/g,'');
        data={commandline:cmdline}
        if (cmdline.length>0) {
            PubSub.publish('processCommand',data)
        }
        this.setState({value:'', placeholder:''})
    },
    textUpdate: function (event) {
        this.setState({value:event.target.value,placeholder:''})
    },
    render: function () {
        return (<div>
                  <form className="form-inline">
                    <div className="form-group">
                      <label>[user@komlog] $&nbsp;</label>
                      <input ref="shellCommand" type="text" className="form-control shell" value={this.state.value} placeholder={this.state.placeholder} onChange={this.textUpdate}/>
                      <button className="btn btn-default" onClick={this.commandHandler}>&#9166;</button>
                    </div>
                  </form>
                </div>);
    }
});

React.render(
    <Shell />
    ,
    document.getElementById('komlog-shell')
);

