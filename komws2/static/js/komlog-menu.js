var DesktopMenu = React.createClass({
    getInitialState: function () {
        return {inputName:'',
                inputStyle:'',
                inputPlaceholder:'Name'}
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
            this.setState({inputName:'',inputStyle:''})
        }
        
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
        return (
                <form>
                 <ReactBootstrap.Input onChange={this.handleChange} placeholder={this.state.inputPlaceholder} value={this.state.inputName} bsStyle={this.state.inputStyle} ref="inputName" type="text" buttonBefore={inputOptions} />
                </form>
               );
    }
});

React.render(
    <DesktopMenu />
    ,
    document.getElementById('desktop-menu')
);

