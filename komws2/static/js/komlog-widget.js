var Widget = React.createClass({
    getInitialState: function () {
        return {
                conf:{},
                shareCounter: 0,
                showConfig: false, 
                }
    },
    subscriptionTokens: {},
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'widgetConfigUpdate-'+this.props.wid:
                this.refreshConfig()
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens[this.props.wid]=[]
        this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('widgetConfigUpdate-'+this.props.wid, this.subscriptionHandler),msg:'widgetConfigUpdate-'+this.props.wid});
    },
    componentDidMount: function () {
        PubSub.publish('widgetConfigReq',{wid:this.props.wid})
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens[this.props.wid], function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.wid];
    },
    configCallback: function() {
        this.setState({showConfig:!this.state.showConfig})
    },
    shareCallback: function() {
        this.setState({shareCounter:this.state.shareCounter+1})
    },
    closeCallback: function() {
        this.props.closeCallback();
    },
    refreshConfig: function () {
        if (widgetStore._widgetConfig.hasOwnProperty(this.props.wid)) {
            widgetConfig=widgetStore._widgetConfig[this.props.wid]
            shouldUpdate=false
            $.each(widgetConfig, function (key,value) {
                if (!(this.state.conf.hasOwnProperty(key) && this.state.conf[key]==value)) {
                    shouldUpdate=true
                }
            }.bind(this));
            if (shouldUpdate) {
                this.setState({conf:widgetConfig})
            }
        }
    },
    getWidgetContentEl: function () {
        if ($.isEmptyObject(this.state.conf)) {
            return null
        } else {
            switch (this.state.conf.type) {
                case 'ds':
                    return React.createElement(WidgetDs, {wid:this.props.wid, did:this.state.conf.did, shareCounter:this.state.shareCounter});
                    //return (
                      //<WidgetDs wid={this.props.wid} did={this.state.conf.did} shareCounter={this.state.shareCounter}/>
                      //);
                    break;
                case 'dp':
                    return React.createElement(WidgetDp, {wid:this.props.wid, pid:this.state.conf.pid, shareCounter:this.state.shareCounter});
                    //return (
                      //<WidgetDp wid={this.props.wid} pid={this.state.conf.pid} shareCounter={this.state.shareCounter}/>
                      //);
                    break;
                case 'mp':
                    return React.createElement(WidgetMp, {wid:this.props.wid, datapoints:this.state.conf.datapoints, view:this.state.conf.view, shareCounter:this.state.shareCounter});
                    //return (
                      //<WidgetMp wid={this.props.wid} datapoints={this.state.conf.datapoints} view={this.state.conf.view} shareCounter={this.state.shareCounter}/>
                      //);
                    break;
                default:
                    return null;
                    break;
            }
        }
    },
    getWidgetConfigEl: function () {
        if ($.isEmptyObject(this.state.conf)) {
            return null
        } else {
            switch (this.state.conf.type) {
                case 'ds':
                    return React.createElement(WidgetConfigDs, {showConfig:this.state.showConfig, closeCallback:this.closeCallback, configCallback:this.configCallback, wid:this.props.wid, did:this.state.conf.did});
                    //return (
                          //<WidgetConfigDs showConfig={this.state.showConfig} closeCallback={this.closeCallback} configCallback={this.configCallback} wid={this.props.wid} did={this.state.conf.did} />
                      //);
                    break;
                case 'dp':
                    return React.createElement(WidgetConfigDp, {showConfig:this.state.showConfig, closeCallback:this.closeCallback, configCallback:this.configCallback, wid:this.props.wid, pid:this.state.conf.pid});
                    //return (
                          //<WidgetConfigDp showConfig={this.state.showConfig} closeCallback={this.closeCallback} configCallback={this.configCallback} wid={this.props.wid} pid={this.state.conf.pid} />
                      //);
                    break;
                case 'mp':
                    return React.createElement(WidgetConfigMp, {showConfig:this.state.showConfig, closeCallback:this.closeCallback, configCallback:this.configCallback, wid:this.props.wid, datapoints:this.state.conf.datapoints, widgetname:this.state.conf.widgetname});
                    //return (
                          //<WidgetConfigMp showConfig={this.state.showConfig} closeCallback={this.closeCallback} configCallback={this.configCallback} wid={this.props.wid} datapoints={this.state.conf.datapoints} widgetname={this.state.conf.widgetname} />
                      //);
                    break;
                default:
                    return null;
                    break;
            }
        }
    },
    render: function() {
        widget_content=this.getWidgetContentEl();
        widget_config=this.getWidgetConfigEl();
        if ($.isEmptyObject(this.state.conf)) {
            conf={widgetname: "Loading..."}
            widget=React.createElement('div', {className:"panel panel-default"},
                     React.createElement(WidgetBar, {bid:this.props.bid, wid:this.props.wid, conf:conf, closeCallback:this.closeCallback})
                   );
            //widget=(
            //<div className="panel panel-default">
              //<WidgetBar bid={this.props.bid} wid={this.props.wid} conf={conf} closeCallback={this.closeCallback}/>
            //</div>
            //);
        } else {
            widget=React.createElement('div', {className:"panel panel-default"},
                     React.createElement(WidgetBar, {bid:this.props.bid, wid:this.props.wid, conf:this.state.conf, shareCallback:this.shareCallback, closeCallback:this.closeCallback, configCallback:this.configCallback, isPinned:this.props.isPinned, configOpen:this.state.showConfig}),
                     widget_config,
                     widget_content
                   );
            //widget=(
            //<div className="panel panel-default">
                //<WidgetBar bid={this.props.bid} wid={this.props.wid} conf={this.state.conf} shareCallback={this.shareCallback} closeCallback={this.closeCallback} configCallback={this.configCallback} isPinned={this.props.isPinned} configOpen={this.state.showConfig} />
                //{widget_config}
                //{widget_content}
            //</div>
            //);
        }
        return widget
    },
});

var WidgetBar = React.createClass({
    getInitialState: function () {
        return {
                allowPin: false,
                isPinned: false,
               }
    },
    componentWillMount: function () {
        if (this.props.bid != '0') {
            this.setState({allowPin:true, isPinned: this.props.isPinned})
        }
    },
    componentWillReceiveProps: function (nextProps) {
        if (this.props.bid != '0') {
            if (nextProps.isPinned!=this.state.isPinned) {
                this.setState({isPinned:nextProps.isPinned})
            }
        }
    },
    configClick: function() {
        this.props.configCallback()
    },
    shareClick: function () {
        this.props.shareCallback()
    },
    closeClick: function () {
        this.props.closeCallback()
    },
    pinClick: function () {
        console.log('pin clicked')
        if (this.props.isPinned) {
            console.log('eliminando del dashboard')
            PubSub.publish('modifyDashboard',{bid:this.props.bid,delete_widgets:[this.props.wid]})
            this.setState({isPinned:false})
        } else {
            console.log('añadiendo al dashboard')
            PubSub.publish('modifyDashboard',{bid:this.props.bid,new_widgets:[this.props.wid]})
            this.setState({isPinned:true})
        }
    },
    styles: {
        barstyle: {
        },
        namestyle: {
            textAlign: 'left',
            width: '100%',
            fontWeight: 'bold',
        },
        righticonstylePushed: {
            textShadow: '2px 2px 5px 2px #ccc',
            align: 'right',
            float: 'right',
            height: '20px',
            padding: '5px',
            color: 'black',
        },
        righticonstyle: {
            textShadow: '1px 1px 5px 1px #ccc',
            align: 'right',
            float: 'right',
            height: '20px',
            padding: '5px',
            color: '#aaa',
        },
        lefticonstyle: {
            textShadow: '1px 1px 5px 1px #ccc',
            align: 'left',
            float: 'left',
            height: '20px',
            padding: '5px',
            color: '#aaa',
        },
    },
    render: function() {
        if (this.state.allowPin) {
            if (this.state.isPinned == true) {
                pinIcon=React.createElement('span', {className:"SlideBarIcon glyphicon glyphicon-pushpin", style:this.styles.righticonstylePushed, onClick:this.pinClick});
                //pinIcon=<span className="SlideBarIcon glyphicon glyphicon-pushpin" style={this.styles.righticonstylePushed} onClick={this.pinClick}></span>
            } else {
                pinIcon=React.createElement('span', {className:"SlideBarIcon glyphicon glyphicon-pushpin", style:this.styles.righticonstyle, onClick:this.pinClick});
                //pinIcon=<span className="SlideBarIcon glyphicon glyphicon-pushpin" style={this.styles.righticonstyle} onClick={this.pinClick}></span>
            }
        } else {
            pinIcon=null
        }
        if (this.props.configOpen) {
            configIcon=React.createElement('span', {className:"SlideBarIcon glyphicon glyphicon-chevron-down", style:this.styles.lefticonstyle, onClick:this.configClick});
            //configIcon=<span className="SlideBarIcon glyphicon glyphicon-chevron-down" style={this.styles.lefticonstyle} onClick={this.configClick}></span>
        } else {
            configIcon=React.createElement('span', {className:"SlideBarIcon glyphicon glyphicon-chevron-right", style:this.styles.lefticonstyle, onClick:this.configClick});
            //configIcon=<span className="SlideBarIcon glyphicon glyphicon-chevron-right" style={this.styles.lefticonstyle} onClick={this.configClick}></span>
        }
        return React.createElement('div', {className:"SlideBar panel-heading", style:this.styles.barstyle},
                 React.createElement('span', {className:"SlideBarIcon glyphicon glyphicon-remove", style:this.styles.righticonstyle, onClick:this.closeClick}),
                 React.createElement('span', {className:"SlideBarIcon glyphicon glyphicon-send", style:this.styles.righticonstyle, onClick:this.shareClick}),
                 pinIcon,
                 configIcon,
                 React.createElement('div', {className:"SlideBarName", style:this.styles.namestyle},
                   React.createElement('span', null, this.props.conf.widgetname)
                 )
               );
        //return (
            //<div className="SlideBar panel-heading" style={this.styles.barstyle}>
              //<span className="SlideBarIcon glyphicon glyphicon-remove" style={this.styles.righticonstyle} onClick={this.closeClick}></span>
              //<span className="SlideBarIcon glyphicon glyphicon-send" style={this.styles.righticonstyle} onClick={this.shareClick}></span>
              //{pinIcon}
              //{configIcon}
              //<div className="SlideBarName" style={this.styles.namestyle} >
                //<span>{this.props.conf.widgetname}</span>
              //</div>
            //</div>
        //);
    }
});

var WidgetConfigDs = React.createClass({
    getInitialState: function () {
        return {
                datasourcename: '',
                deleteModal: false,
                }
    },
    subscriptionTokens: {},
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'datasourceConfigUpdate-'+this.props.did:
                this.refreshConfig();
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens['cfg-'+this.props.wid]=[]
        this.subscriptionTokens['cfg-'+this.props.wid].push({token:PubSub.subscribe('datasourceConfigUpdate-'+this.props.did, this.subscriptionHandler),msg:'datasourceConfigUpdate-'+this.props.did});
    },
    componentDidMount: function () {
        PubSub.publish('datasourceConfigReq',{did:this.props.did})
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens['cfg-'+this.props.wid], function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens['cfg-'+this.props.wid];
    },
    refreshConfig: function () {
        datasourceConfig=datasourceStore._datasourceConfig[this.props.did]
        if (this.state.datasourcename != datasourceConfig.datasourcename) {
            this.setState({datasourcename:datasourceConfig.datasourcename})
        }
    },
    deleteWidget: function () {
        this.setState({deleteModal: true})
    },
    cancelDelete: function () {
        this.setState({deleteModal: false})
    },
    confirmDelete: function () {
        PubSub.publish('deleteDatasource',{did:this.props.did})
        this.setState({deleteModal: false})
        this.props.closeCallback()
    },
    render: function () {
        delete_modal=React.createElement(ReactBootstrap.Modal, {bsSize:"small", show:this.state.deleteModal, onHide:this.cancelDelete, container:this, "aria-labeledby":"contained-modal-title"},
                       React.createElement(ReactBootstrap.Modal.Header, {closeButton:true},
                         React.createElement(ReactBootstrap.Modal.Title, {id:"contained-modal-title"},"Delete Datasource")
                       ),
                       React.createElement(ReactBootstrap.Modal.Body, null,
                         "Datasource ",
                         React.createElement('strong', null, this.state.datasourcename),
                         " will be deleted, with all its datapoints. ",
                         React.createElement('strong', null, "Are You sure?")
                       ),
                       React.createElement(ReactBootstrap.Modal.Footer, null,
                         React.createElement(ReactBootstrap.Button, {bsStyle:"default", onClick:this.cancelDelete}, "Cancel"),
                         React.createElement(ReactBootstrap.Button, {bsStyle:"primary", onClick:this.confirmDelete}, "Delete")
                       )
                     );
        //delete_modal=(
            //<ReactBootstrap.Modal bsize="small" show={this.state.deleteModal} onHide={this.cancelDelete} container={this} aria-labelledby="contained-modal-title">
              //<ReactBootstrap.Modal.Header closeButton>
                //<ReactBootstrap.Modal.Title id="contained-modal-title">Delete Datasource</ReactBootstrap.Modal.Title>
              //</ReactBootstrap.Modal.Header>
              //<ReactBootstrap.Modal.Body>
                //Datasource <strong>{this.state.datasourcename}</strong> will be deleted, with all its datapoints.
                //<strong> Are You sure? </strong>
              //</ReactBootstrap.Modal.Body>
              //<ReactBootstrap.Modal.Footer>
                //<ReactBootstrap.Button bsStyle="default" onClick={this.cancelDelete}>Cancel</ReactBootstrap.Button>
                //<ReactBootstrap.Button bsStyle="primary" onClick={this.confirmDelete}>Delete</ReactBootstrap.Button>
              //</ReactBootstrap.Modal.Footer>
            //</ReactBootstrap.Modal>
        //);
        return React.createElement(ReactBootstrap.Collapse, {in:this.props.showConfig},
                 React.createElement('div', null,
                   React.createElement(ReactBootstrap.Well, null,
                     React.createElement(ReactBootstrap.ListGroup, null,
                       React.createElement(ReactBootstrap.ListGroupItem, {bsSize:"xsmall"},
                         React.createElement('strong', null, "Delete Datasource"),
                         React.createElement('div', {className:"text-right"},
                           React.createElement(ReactBootstrap.Button, {bsSize:"small", bsStyle:"danger", onClick:this.deleteWidget}, "Delete")
                         )
                       )
                     )
                   ),
                   delete_modal
                 )
               )
        //return (
              //<ReactBootstrap.Collapse in={this.props.showConfig}>
                //<div>
                  //<ReactBootstrap.Well>
                    //<ReactBootstrap.ListGroup >
                      //<ReactBootstrap.ListGroupItem bsSize="xsmall" >
                        //<strong>Delete Datasource</strong>
                        //<div className="text-right">
                          //<ReactBootstrap.Button bsSize="small" bsStyle="danger" onClick={this.deleteWidget}>Delete</ReactBootstrap.Button>
                        //</div>
                      //</ReactBootstrap.ListGroupItem>
                    //</ReactBootstrap.ListGroup>
                  //</ReactBootstrap.Well>
                  //{delete_modal}
                //</div>
              //</ReactBootstrap.Collapse>
              //);
    }
});

var WidgetConfigDp = React.createClass({
    getInitialState: function () {
        return {
                datapointname: '',
                color: '',
                boxColor: '',
                deleteModal: false,
                updateDisabled: true,
                }
    },
    subscriptionTokens: {},
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'datapointConfigUpdate-'+this.props.pid:
                this.refreshConfig();
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens['cfg-'+this.props.wid]=[]
        this.subscriptionTokens['cfg-'+this.props.wid].push({token:PubSub.subscribe('datapointConfigUpdate-'+this.props.pid, this.subscriptionHandler),msg:'datapointConfigUpdate-'+this.props.pid});
    },
    componentDidMount: function () {
        PubSub.publish('datapointConfigReq',{pid:this.props.pid})
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens['cfg-'+this.props.wid], function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens['cfg-'+this.props.wid];
    },
    handleChange: function () {
        color=this.refs.color.getValue()
        isOk  = /^#[0-9A-F]{6}$/i.test(color)
        newState={updateDisabled:!isOk}
        if (isOk) {
            newState.boxColor=color
        }
        this.setState(newState)
    },
    refreshConfig: function () {
        datapointConfig=datapointStore._datapointConfig[this.props.pid]
        if (this.state.datapointname != datapointConfig.datapointname) {
            this.setState({datapointname:datapointConfig.datapointname,color:datapointConfig.color,boxColor:datapointConfig.color})
        }
    },
    updateConfig: function () {
        color=this.refs.color.getValue().toUpperCase();
        if (color != this.state.color && /^#[0-9A-F]{6}$/i.test(color)) {
            PubSub.publish('modifyDatapoint',{pid:this.props.pid,color:color})
        }
        this.props.configCallback()
    },
    deleteWidget: function () {
        this.setState({deleteModal: true})
    },
    cancelDelete: function () {
        this.setState({deleteModal: false})
    },
    confirmDelete: function () {
        PubSub.publish('deleteDatapoint',{pid:this.props.pid})
        this.setState({deleteModal: false})
        this.props.closeCallback()
    },
    render: function () {
        delete_modal=React.createElement(ReactBootstrap.Modal, {bsSize:"small", show:this.state.deleteModal, onHide:this.cancelDelete, container:this, "aria-labeledby":"contained-modal-title"},
                       React.createElement(ReactBootstrap.Modal.Header, {closeButton:true},
                         React.createElement(ReactBootstrap.Modal.Title, {id:"contained-modal-title"},"Delete Datapoint")
                       ),
                       React.createElement(ReactBootstrap.Modal.Body, null,
                         "Datapoint ",
                         React.createElement('strong', null, this.state.datapointname),
                         " will be deleted. ",
                         React.createElement('strong', null, "Are You sure?")
                       ),
                       React.createElement(ReactBootstrap.Modal.Footer, null,
                         React.createElement(ReactBootstrap.Button, {bsStyle:"default", onClick:this.cancelDelete}, "Cancel"),
                         React.createElement(ReactBootstrap.Button, {bsStyle:"primary", onClick:this.confirmDelete}, "Delete")
                       )
                     );
        //delete_modal=(
            //<ReactBootstrap.Modal bsize="small" show={this.state.deleteModal} onHide={this.cancelDelete} container={this} aria-labelledby="contained-modal-title">
              //<ReactBootstrap.Modal.Header closeButton>
                //<ReactBootstrap.Modal.Title id="contained-modal-title">Delete Datapoint</ReactBootstrap.Modal.Title>
              //</ReactBootstrap.Modal.Header>
              //<ReactBootstrap.Modal.Body>
                //Datapoint <strong>{this.state.datapointname}</strong> will be deleted.
                //<strong> Are You sure? </strong>
              //</ReactBootstrap.Modal.Body>
              //<ReactBootstrap.Modal.Footer>
                //<ReactBootstrap.Button bsStyle="default" onClick={this.cancelDelete}>Cancel</ReactBootstrap.Button>
                //<ReactBootstrap.Button bsStyle="primary" onClick={this.confirmDelete}>Delete</ReactBootstrap.Button>
              //</ReactBootstrap.Modal.Footer>
            //</ReactBootstrap.Modal>
        //);
        //boxColor=<ReactBootstrap.Glyphicon glyph="unchecked" style={{'background-color':this.state.boxColor,'color':this.state.boxColor}} />
        boxColor=React.createElement(ReactBootstrap.Glyphicon, {glyph:"unchecked", style:{backgroundColor:this.state.boxColor, color:this.state.boxColor}});
        return React.createElement(ReactBootstrap.Collapse, {in:this.props.showConfig},
                 React.createElement('div', null,
                   React.createElement(ReactBootstrap.Well, null,
                     React.createElement(ReactBootstrap.ListGroup, null,
                       React.createElement(ReactBootstrap.ListGroupItem, {bsSize:"small"},
                         React.createElement('form', {className:"form-horizontal"},
                           React.createElement(ReactBootstrap.Input, {ref:"color", placeholder:this.state.color, bsSize:"small", type:"text", label:"Datapoint Color", labelClassName:"col-xs-3", wrapperClassName:"col-xs-3", onChange:this.handleChange, addonAfter:boxColor}),
                           React.createElement('div', {className:"text-right"},
                             React.createElement(ReactBootstrap.Button, {bsSize:"small", bsStyle:"primary", onClick:this.updateConfig, disabled:this.state.updateDisabled}, "Update")
                           )
                         )
                       ),
                       React.createElement(ReactBootstrap.ListGroupItem, {bsSize:"xsmall"},
                         React.createElement('strong', null, "Delete Datapoint"),
                         React.createElement('div', {className:"text-right"},
                           React.createElement(ReactBootstrap.Button, {bsSize:"small", bsStyle:"danger", onClick:this.deleteWidget}, "Delete")
                         )
                       )
                     )
                   ),
                   delete_modal
                 )
               )
        //return (
              //<ReactBootstrap.Collapse in={this.props.showConfig}>
                //<div>
                  //<ReactBootstrap.Well>
                    //<ReactBootstrap.ListGroup >
                      //<ReactBootstrap.ListGroupItem bsSize="small" >
                        //<form className="form-horizontal">
                          //<ReactBootstrap.Input ref="color" placeholder={this.state.color} bsSize="small" type="text" label="Datapoint Color" labelClassName="col-xs-3" wrapperClassName="col-xs-3" onChange={this.handleChange} addonAfter={boxColor}/>
                          //<div className="text-right">
                            //<ReactBootstrap.Button bsSize="small" bsStyle="primary" onClick={this.updateConfig} disabled={this.state.updateDisabled} >Update</ReactBootstrap.Button>
                          //</div>
                        //</form>
                      //</ReactBootstrap.ListGroupItem>
                      //<ReactBootstrap.ListGroupItem bsSize="xsmall" >
                        //<strong>Delete Datapoint</strong>
                        //<div className="text-right">
                          //<ReactBootstrap.Button bsSize="small" bsStyle="danger" onClick={this.deleteWidget}>Delete</ReactBootstrap.Button>
                        //</div>
                      //</ReactBootstrap.ListGroupItem>
                    //</ReactBootstrap.ListGroup>
                  //</ReactBootstrap.Well>
                  //{delete_modal}
                //</div>
              //</ReactBootstrap.Collapse>
              //);
    }
});

var WidgetConfigMp = React.createClass({
    getInitialState: function () {
        return {
                deleteModal: false,
                datapoints: [],
                }
    },
    subscriptionTokens: {},
    subscriptionHandler: function (msg,data) {
        msgType=msg.split('-')[0]
        switch (msgType) {
            case 'datapointConfigUpdate':
                pid=msg.split('-')[1]
                this.refreshConfig(pid);
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens['cfg-'+this.props.wid]=[]
        for (var i=0;i<this.props.datapoints.length;i++) {
            this.subscriptionTokens['cfg-'+this.props.wid].push({token:PubSub.subscribe('datapointConfigUpdate-'+this.props.datapoints[i], this.subscriptionHandler),msg:'datapointConfigUpdate-'+this.props.datapoints[i]});
        }
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens['cfg-'+this.props.wid], function (d) {
            PubSub.unsubscribe(d.token)
            });
        delete this.subscriptionTokens['cfg-'+this.props.wid];
    },
    componentDidMount: function () {
        for (var i=0;i<this.props.datapoints.length;i++) {
            PubSub.publish('datapointConfigReq',{pid:this.props.datapoints[i]})
        }
    },
    refreshConfig: function () {
        datapoints=[]
        for (var i=0;i<this.props.datapoints.length;i++) {
            if (datapointStore._datapointConfig.hasOwnProperty(this.props.datapoints[i])) {
                datapoint=datapointStore._datapointConfig[this.props.datapoints[i]]
                datapoints.push({pid:this.props.datapoints[i],color:datapoint.color,datapointname:datapoint.datapointname,lineThrough:false})
            }
        }
        this.setState({datapoints:datapoints})
    },
    updateConfig: function () {
        data={wid:this.props.wid}
        new_widgetname=this.refs.widgetname.getValue();
        if (new_widgetname.length>0 && new_widgetname!=this.props.widgetname) {
            data.new_widgetname=new_widgetname
        }
        for (var i=0;i<this.state.datapoints.length;i++) {
            deleteDatapoints=[]
            if (this.state.datapoints[i].lineThrough) {
                deleteDatapoints.push(this.state.datapoints[i].pid)
            }
            if (deleteDatapoints.length>0) {
                data.delete_datapoints=deleteDatapoints
            }
        }
        if (Object.keys(data).length>1) {
            PubSub.publish('modifyWidget',data)
        }
        this.props.configCallback()
    },
    markDatapoint: function (pid) {
        datapoints=this.state.datapoints
        render=false
        for (var i=0;i<datapoints.length;i++) {
            if (datapoints[i].pid == pid) {
                datapoints[i].lineThrough=!datapoints[i].lineThrough
                render=true
                break;
            }
        }
        if (render) {
            this.setState({datapoints:datapoints})
        }
    },
    deleteWidget: function () {
        this.setState({deleteModal: true})
    },
    cancelDelete: function () {
        this.setState({deleteModal: false})
    },
    confirmDelete: function () {
        PubSub.publish('deleteWidget',{wid:this.props.wid})
        this.setState({deleteModal: false})
        this.props.closeCallback()
    },
    renderDatapointList: function () {
        console.log('generando lista datapoints',this.state.datapoints)
        list=$.map(this.state.datapoints, function (el) {
            if (el.lineThrough) {
                style={'textDecoration':'line-through'}
                glyph="remove"
            } else {
                style={}
                glyph="ok"
            }
            return React.createElement('tr', {key:el.pid},
                     React.createElement('td', null,
                       React.createElement(ReactBootstrap.Glyphicon, {glyph:glyph, onClick:this.markDatapoint.bind(null, el.pid)})
                     ),
                     React.createElement('td', {style:style},
                       React.createElement('span', {style:{backgroundColor:el.color}},"   "),
                       React.createElement('span', null,el.datapointname)
                     )
                   );
            //return <tr key={el.pid}>
                    //<td><ReactBootstrap.Glyphicon glyph={glyph} onClick={this.markDatapoint.bind(null,el.pid)}/></td>
                    //<td style={style}><span style={{'backgroundColor':el.color}}>&nbsp;&nbsp;&nbsp;</span><span>&nbsp;{el.datapointname}</span></td>
                   //</tr>
        }.bind(this));
        return React.createElement(ReactBootstrap.Table, null, list);
        //return <ReactBootstrap.Table>
                 //{list}
               //</ReactBootstrap.Table>
    },
    render: function () {
        delete_modal=React.createElement(ReactBootstrap.Modal, {bsSize:"small", show:this.state.deleteModal, onHide:this.cancelDelete, container:this, "aria-labeledby":"contained-modal-title"},
                       React.createElement(ReactBootstrap.Modal.Header, {closeButton:true},
                         React.createElement(ReactBootstrap.Modal.Title, {id:"contained-modal-title"},"Delete Graph")
                       ),
                       React.createElement(ReactBootstrap.Modal.Body, null,
                         "Graph ",
                         React.createElement('strong', null, this.state.widgetname),
                         " will be deleted. ",
                         React.createElement('strong', null, "Are You sure?")
                       ),
                       React.createElement(ReactBootstrap.Modal.Footer, null,
                         React.createElement(ReactBootstrap.Button, {bsStyle:"default", onClick:this.cancelDelete}, "Cancel"),
                         React.createElement(ReactBootstrap.Button, {bsStyle:"primary", onClick:this.confirmDelete}, "Delete")
                       )
                     );
        //delete_modal=(
            //<ReactBootstrap.Modal bsize="small" show={this.state.deleteModal} onHide={this.cancelDelete} container={this} aria-labelledby="contained-modal-title">
              //<ReactBootstrap.Modal.Header closeButton>
                //<ReactBootstrap.Modal.Title id="contained-modal-title">Delete Graph</ReactBootstrap.Modal.Title>
              //</ReactBootstrap.Modal.Header>
              //<ReactBootstrap.Modal.Body>
                //Graph <strong>{this.props.widgetname}</strong> will be deleted,<strong> are You sure?</strong>
              //</ReactBootstrap.Modal.Body>
              //<ReactBootstrap.Modal.Footer>
                //<ReactBootstrap.Button bsStyle="default" onClick={this.cancelDelete}>Cancel</ReactBootstrap.Button>
                //<ReactBootstrap.Button bsStyle="primary" onClick={this.confirmDelete}>Delete</ReactBootstrap.Button>
              //</ReactBootstrap.Modal.Footer>
            //</ReactBootstrap.Modal>
        //);
        datapointList=this.renderDatapointList();
        return React.createElement(ReactBootstrap.Collapse, {in:this.props.showConfig},
                 React.createElement('div', null,
                   React.createElement(ReactBootstrap.Well, null,
                     React.createElement(ReactBootstrap.ListGroup, null,
                       React.createElement(ReactBootstrap.ListGroupItem, {bsSize:"small"},
                         React.createElement(ReactBootstrap.Table, {condensed:"true",responsive:"true"},
                           React.createElement('tr', null,
                             React.createElement('td',null,
                               React.createElement('strong',null,"Graph Name")
                             ),
                             React.createElement('td',null,
                               React.createElement(ReactBootstrap.Input, {ref:"widgetname", placeholder:this.props.widgetname, bsSize:"small", type:"text"})
                             )
                           ),
                           React.createElement('tr',null,
                             React.createElement('td', null,
                               React.createElement('strong',null,"Datapoints")
                             ),
                             React.createElement('td', null, datapointList)
                           ),
                           React.createElement('tr',null,
                             React.createElement('td',{colSpan:"2", className:"text-right"},
                               React.createElement(ReactBootstrap.Button, {bsSize:"small", bsStyle:"primary", onClick:this.updateConfig}, "Update")
                             )
                           )
                         )
                       ),
                       React.createElement(ReactBootstrap.ListGroupItem, {bsSize:"xsmall"},
                         React.createElement('strong', null, "Delete Graph"),
                         React.createElement('div', {className:"text-right"},
                           React.createElement(ReactBootstrap.Button, {bsSize:"small", bsStyle:"danger", onClick:this.deleteWidget}, "Delete")
                         )
                       )
                     )
                   ),
                   delete_modal
                 )
               )
        //return (
              //<ReactBootstrap.Collapse in={this.props.showConfig}>
                //<div>
                  //<ReactBootstrap.Well>
                    //<ReactBootstrap.ListGroup >
                    //<ReactBootstrap.ListGroupItem bsSize="small" >
                      //<ReactBootstrap.Table condensed="true" responsive="true">
                        //<tr>
                          //<td><strong>Graph Name</strong></td>
                          //<td><ReactBootstrap.Input ref="widgetname" placeholder={this.props.widgetname} bsSize="small" type="text"/></td>
                        //</tr>
                        //<tr>
                          //<td><strong>Datapoints</strong></td>
                          //<td>{datapointList}</td>
                        //</tr>
                        //<tr>
                          //<td colSpan="2" className="text-right">
                            //<ReactBootstrap.Button bsSize="small" bsStyle="primary" onClick={this.updateConfig}>Update</ReactBootstrap.Button>
                          //</td>
                        //</tr>
                      //</ReactBootstrap.Table>
                    //</ReactBootstrap.ListGroupItem>
                    //<ReactBootstrap.ListGroupItem bsSize="xsmall" >
                    //<strong>Delete Graph</strong>
                    //<div className="text-right">
                      //<ReactBootstrap.Button bsSize="small" bsStyle="danger" onClick={this.deleteWidget}>Delete</ReactBootstrap.Button>
                    //</div>
                    //</ReactBootstrap.ListGroupItem>
                    //</ReactBootstrap.ListGroup>
                  //</ReactBootstrap.Well>
                  //{delete_modal}
                //</div>
              //</ReactBootstrap.Collapse>
              //);
    }
});

var WidgetDs = React.createClass({
    styles: {
        infostyle: {
            float: 'right',
            color: '#aaa',
            padding: '3px 5px 0px 0px'
        },
    },
    getInitialState: function () {
        return {dsData: undefined,
                datasourcename: '',
                timestamp:0,
                seq:undefined,
                snapshotTimestamp:0,
                snapshotSeq:undefined,
                shareModal:false,
                shareCounter:this.props.shareCounter,
                }
    },
    subscriptionTokens: {},
    onClickDatapoint: function(pid,e) {
        e.preventDefault();
        PubSub.publish('loadSlide',{pid:pid})
    },
    onDragStartDatapoint: function (pid,e) {
        console.log('dragstartnavbar')
        e.stopPropagation()
        e.dataTransfer.setData('id',pid)
    },
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'datasourceDataUpdate-'+this.props.did:
                this.refreshData()
                break;
            case 'datasourceConfigUpdate-'+this.props.did:
                this.refreshConfig()
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens[this.props.wid]=[]
        this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('datasourceDataUpdate-'+this.props.did, this.subscriptionHandler),msg:'datasourceDataUpdate-'+this.props.did});
        this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('datasourceConfigUpdate-'+this.props.did, this.subscriptionHandler),msg:'datasourceConfigUpdate-'+this.props.did});
    },
    componentDidMount: function () {
        PubSub.publish('datasourceDataReq',{did:this.props.did})
        PubSub.publish('datasourceConfigReq',{did:this.props.did})
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens[this.props.wid], function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.wid];
    },
    componentWillReceiveProps: function (nextProps) {
        if (nextProps.shareCounter>this.state.shareCounter) {
            this.setState({shareModal:true,shareCounter:nextProps.shareCounter,snapshotTimestamp:this.state.timestamp,snapshotSeq:this.state.seq});
        }
    },
    refreshData: function () {
        if (datasourceStore._datasourceData.hasOwnProperty(this.props.did)) {
            datasourceData=datasourceStore._datasourceData[this.props.did]
            if (datasourceData.hasOwnProperty('datapoints')) {
                for (var i=0;i<datasourceData.datapoints.length;i++) {
                    pid=datasourceData.datapoints[i].pid
                    if (!datapointStore._datapointConfig.hasOwnProperty(pid)) {
                        PubSub.publish('datapointConfigReq',{pid:pid})
                    }
                }
            }
            if (!this.state.dsData) {
                this.setState({dsData:datasourceData, timestamp:datasourceData.ts,seq:datasourceData.seq})
            } else if (this.state.timestamp < datasourceData.ts) {
                this.setState({dsData:datasourceData, timestamp:datasourceData.ts,seq:datasourceData.seq})
            }
        }
    },
    refreshConfig: function () {
        if (datasourceStore._datasourceConfig.hasOwnProperty(this.props.did)) {
            datasourceConfig=datasourceStore._datasourceConfig[this.props.did]
            if (datasourceConfig.hasOwnProperty('pids')) {
                for (var i=0;i<datasourceConfig.pids.length;i++) {
                    pid=datasourceConfig.pids[i]
                    if (!datapointStore._datapointConfig.hasOwnProperty(pid)) {
                        PubSub.publish('datapointConfigReq',{pid:pid})
                    }
                }
            }
            shouldUpdate=false
            if (this.state.datasourcename != datasourceConfig.datasourcename) {
                shouldUpdate = true
            }
            if (shouldUpdate) {
                this.setState({datasourcename:datasourceConfig.datasourcename})
            }
        }
    },
    getDateStatement: function (timestamp) {
        if (typeof timestamp === 'number') {
            var date = new Date(timestamp*1000);
            var now = new Date();
            diff = now.getTime()/1000 - timestamp;
            if (diff<0) {
                return React.createElement('span',{title:date.toString()}, " right now");
            } else {
                if (diff<60) {
                    when=" right now"
                } else if (diff<3600) {
                    when=" "+(diff/60 | 0)+" min"+(diff/60>=2 ? "utes":"")+" ago";
                } else if (diff<86400) {
                    when=" "+(diff/3600 | 0)+" hour"+(diff/3600>=2 ? "s":"")+" ago";
                } else if (diff<2678400) {
                    when=" "+(diff/86400 | 0)+" day"+(diff/86400>=2 ? "s":"")+" ago";
                } else {
                    when=" "+(diff/2678400 | 0)+" month"+(diff/2678400>=2 ? "s":"")+" ago";
                }
                return React.createElement('span',{title:date.toString()}, when);
            }
        } else {
            return null
        }
    },
    generateDateString: function (timestamp) {
        if (typeof timestamp === 'number') {
            var date = new Date(timestamp*1000);
            var hours = date.getHours();
            var minutes = "0" + date.getMinutes();
            var seconds = "0" + date.getSeconds();
            return hours + ':' + minutes.substr(minutes.length-2) + ':' + seconds.substr(seconds.length-2);
        } else {
            return ''
        }
    },
    generateHtmlContent: function (dsData) {
        var elements=[]
        if (!dsData) {
            return elements
        }
        var numElement = 0
        var cursorPosition=0
        newLineRegex=/(?:\r\n|\r|\n)/g
        datasourcePids=[]
        if (datasourceStore._datasourceConfig.hasOwnProperty(this.props.did)) {
            datasourceConfig=datasourceStore._datasourceConfig[this.props.did]
            if (datasourceConfig.hasOwnProperty('pids')) {
                for (var i=0;i<datasourceConfig.pids.length;i++) {
                    if (datapointStore._datapointConfig.hasOwnProperty(datasourceConfig.pids[i])) {
                        datapointname=datapointStore._datapointConfig[datasourceConfig.pids[i]].datapointname
                        datasourcePids.push({pid:datasourceConfig.pids[i],datapointname:datapointname})
                    }
                }
            }
        }
        datasourcePids.sort( function (a,b) {
            nameA=a.datapointname.toLowerCase();
            nameB=b.datapointname.toLowerCase();
            return ((nameA < nameB) ? -1 : ((nameA > nameB) ? 1 : 0));
        });
        for (var i=0;i<dsData.variables.length;i++) {
            position=dsData.variables[i][0]
            length=dsData.variables[i][1]
            dsSubContent=dsData.content.substr(cursorPosition,position-cursorPosition)
            start=0
            while((match=newLineRegex.exec(dsSubContent)) != null) {
                text=dsSubContent.substr(start,match.index-start).replace(/ /g, '\u00a0');
                elements.push({ne:numElement++,type:'text',data:text});
                elements.push({ne:numElement++,type:'nl'});
                start=match.index+match.length-1
            }
            if (start<position) {
                text=dsSubContent.substr(start,position-start).replace(/ /g, '\u00a0');
                elements.push({ne:numElement++,type:'text',data:text});
            }
            datapointFound=false;
            for (var j=0;j<dsData.datapoints.length;j++) {
                if (dsData.datapoints[j].index == dsData.variables[i][0]) {
                    text=dsData.content.substr(position,length)
                    if (datapointStore._datapointConfig.hasOwnProperty(dsData.datapoints[j].pid)) {
                        color=datapointStore._datapointConfig[dsData.datapoints[j].pid].color
                        datapointname=datapointStore._datapointConfig[dsData.datapoints[j].pid].datapointname
                        classname='datapoint'
                    } else {
                        color='black'
                        datapointname=''
                        classname=''
                    }
                    elements.push({ne:numElement++,type:'datapoint',pid:dsData.datapoints[j].pid,p:position,l:length,style:{color:color},data:text,datapointname:datapointname,classname:classname})
                    datapointFound=true
                    break;
                }
            }
            if (datapointFound == false) {
                text=dsData.content.substr(position,length)
                elements.push({ne:numElement++, type:'variable',data:text,position:position,length:length,datapoints:datasourcePids})
            } else {
                datapointFound = false
            }
            cursorPosition=position+length
        }
        if (cursorPosition<dsData.content.length) {
            dsSubContent=dsData.content.substr(cursorPosition,dsData.content.length-cursorPosition)
            start=0
            while((match=newLineRegex.exec(dsSubContent)) != null) {
                text=dsSubContent.substr(start,match.index-start).replace(/ /g, '\u00a0');
                elements.push({ne:numElement++,type:'text',data:text});
                elements.push({ne:numElement++,type:'nl'});
                start=match.index+match.length-1
            }
            if (start<dsSubContent.length-1) {
                text=dsSubContent.substr(start,dsSubContent.length-1-start).replace(/ /g, '\u00a0');
                elements.push({ne:numElement++,type:'text',data:text});
            }
        }
        return elements
    },
    cancelSnapshot: function () {
        this.setState({shareModal:false})
    },
    shareSnapshot: function () {
        user_list=this.refs.users.getValue().split(/[\s,]+/);
        console.log('seq to share',this.state.snapshotSeq);
        console.log('user list',user_list);
        PubSub.publish('newWidgetDsSnapshot',{seq:this.state.snapshotSeq,user_list:user_list,wid:this.props.wid})
        this.setState({shareModal:false})
    },
    identifyVariable: function (position, length, datapointname) {
        console.log('quieren monitorizar ',position,length,datapointname)
        data={p:position,l:length,seq:this.state.seq,did:this.props.did,datapointname:datapointname}
        PubSub.publish('monitorDatapoint',data)
    },
    associateExistingDatapoint: function (position, length, pid) {
        data={p:position,l:length,seq:this.state.seq,pid:pid}
        PubSub.publish('markPositiveVar',data)
    },
    render: function () {
        elements=this.generateHtmlContent(this.state.dsData)
        var element_nodes=$.map(elements, function (element) {
            if (element.type == 'text') {
                return React.createElement('span', {key:element.ne},element.data);
                //return (<span key={element.ne}>{element.data}</span>);
            }else if (element.type == 'nl') {
                return React.createElement('br',{key:element.ne});
                //return (<br key={element.ne} />);
            }else if (element.type == 'datapoint') {
                if (element.classname=='datapoint') { 
                    tooltip=React.createElement(ReactBootstrap.Tooltip, null, element.datapointname);
                    //tooltip=(
                      //<ReactBootstrap.Tooltip>{element.datapointname}</ReactBootstrap.Tooltip>
                      //);
                    return React.createElement(ReactBootstrap.OverlayTrigger, {placement:"top", overlay:tooltip},
                             React.createElement('span',{key:element.ne, style:element.style, draggable:"true", onClick:this.onClickDatapoint.bind(null,element.pid), onDragStart:this.onDragStartDatapoint.bind(null,element.pid)}, element.data)
                           );
                    //return (
                        //<ReactBootstrap.OverlayTrigger placement="top" overlay={tooltip}>
                          //<span key={element.ne} style={element.style} draggable='true' onClick={this.onClickDatapoint.bind(null,element.pid)} onDragStart={this.onDragStartDatapoint.bind(null,element.pid)}>{element.data}</span>
                        //</ReactBootstrap.OverlayTrigger>
                      //);
                } else {
                    return React.createElement('span',{key:element.ne, style:element.style, draggable:"true", onClick:this.onClickDatapoint.bind(null,element.pid), onDragStart:this.onDragStartDatapoint.bind(null,element.pid)}, element.data);
                    //return (<span key={element.ne} style={element.style} draggable='true' onClick={this.onClickDatapoint.bind(null,element.pid)} onDragStart={this.onDragStartDatapoint.bind(null,element.pid)}>{element.data}</span>);
                }
            }else if (element.type == 'variable') {
                return React.createElement(WidgetDsVariable, {key:element.ne, content:element.data, position:element.position, length:element.length, identifyVariableCallback:this.identifyVariable, datapoints:element.datapoints, associateExistingDatapointCallback:this.associateExistingDatapoint});
                //return (<WidgetDsVariable key={element.ne} content={element.data} position={element.position} length={element.length} identifyVariableCallback={this.identifyVariable} datapoints={element.datapoints} associateExistingDatapointCallback={this.associateExistingDatapoint}/>
                    //);
            }
        }.bind(this));
        if (typeof this.state.timestamp === 'number') {
            info_node=React.createElement('div', {style:this.styles.infostyle},
                        React.createElement(ReactBootstrap.Glyphicon, {glyph:"time"}),
                        this.getDateStatement(this.state.timestamp)
                        //React.createElement('span', {style:this.styles.timestyle}, this.generateDateString(this.state.timestamp))
                      );
            //info_node=(
                //<div style={this.styles.infostyle}>
                //<ReactBootstrap.Glyphicon glyph="time" />
                //<span style={this.styles.timestyle}> {this.generateDateString(this.state.timestamp)}</span>
                //</div>
                //);
        } else {
            info_node=React.createElement('div', {style:this.styles.infostyle});
            //info_node=(
                //<div style={this.styles.infostyle} />
                //);
        }
        share_modal=React.createElement(ReactBootstrap.Modal, {bsSize:"small", show:this.state.shareModal, onHide:this.cancelSnapshot, container:this, "aria-labelledby":"contained-modal-title"},
                      React.createElement(ReactBootstrap.Modal.Header, {closeButton:true},
                        React.createElement(ReactBootstrap.Modal.Title, {id:"contained-modal-title"}, "Share datasource status at "+this.generateDateString(this.state.snapshotTimestamp))
                      ),
                      React.createElement(ReactBootstrap.Modal.Body, null,
                        React.createElement(ReactBootstrap.Input, {ref:"users", type:"textarea", label:"Select Users", placeholder:"type users separated by comma"})
                      ),
                      React.createElement(ReactBootstrap.Modal.Footer, null,
                        React.createElement(ReactBootstrap.Button, {bsStyle:"default", onClick:this.cancelSnapshot}, "Cancel"),
                        React.createElement(ReactBootstrap.Button, {bsStyle:"primary", onClick:this.shareSnapshot}, "Share")
                      )
                    );
        //share_modal=(
            //<ReactBootstrap.Modal bsize="small" show={this.state.shareModal} onHide={this.cancelSnapshot} container={this} aria-labelledby="contained-modal-title">
              //<ReactBootstrap.Modal.Header closeButton>
                //<ReactBootstrap.Modal.Title id="contained-modal-title">Share datasource status at {this.generateDateString(this.state.snapshotTimestamp)}</ReactBootstrap.Modal.Title>
              //</ReactBootstrap.Modal.Header>
              //<ReactBootstrap.Modal.Body>
                //<ReactBootstrap.Input ref="users" type="textarea" label="Select Users" placeholder="type users separated by comma" />
              //</ReactBootstrap.Modal.Body>
              //<ReactBootstrap.Modal.Footer>
                //<ReactBootstrap.Button bsStyle="default" onClick={this.cancelSnapshot}>Cancel</ReactBootstrap.Button>
                //<ReactBootstrap.Button bsStyle="primary" onClick={this.shareSnapshot}>Share</ReactBootstrap.Button>
              //</ReactBootstrap.Modal.Footer>
            //</ReactBootstrap.Modal>
        //);
        return React.createElement('div', null,
                 info_node,
                 React.createElement('div',null, element_nodes),
                 React.createElement('div',null, share_modal)
               );
        //return (<div>
                  //{info_node}
                  //<div>
                    //{element_nodes}
                  //</div>
                  //<div>
                    //{share_modal}
                  //</div>
                //</div>
                //);
    }
});

var WidgetDp = React.createClass({
    styles: {
    },
    getInitialState: function () {
        return {
                interval: {its:undefined,ets:undefined},
                color: '',
                datapointname: '',
                data: [],
                summary: {},
                live: true,
                shareModal:false,
                shareCounter:this.props.shareCounter,
                snapshotInterval: undefined,
                livePrevious: true,
        }
    },
    subscriptionTokens: {},
    componentWillMount: function () {
        this.subscriptionTokens[this.props.wid]=[]
        this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('intervalUpdate-'+this.props.wid, this.subscriptionHandler),msg:'intervalUpdate-'+this.props.wid});
        this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('datapointDataUpdate-'+this.props.pid, this.subscriptionHandler),msg:'datapointDataUpdate-'+this.props.pid});
        this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('datapointConfigUpdate-'+this.props.pid, this.subscriptionHandler),msg:'datapointConfigUpdate-'+this.props.pid});
    },
    componentDidMount: function () {
        PubSub.publish('datapointConfigReq',{pid:this.props.pid})
        PubSub.publish('datapointDataReq',{pid:this.props.pid})
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens[this.props.wid], function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.wid];
    },
    componentWillReceiveProps: function (nextProps) {
        if (nextProps.shareCounter>this.state.shareCounter) {
            this.setState({shareModal:true,shareCounter:nextProps.shareCounter, snapshotInterval:this.state.interval, livePrevious:this.state.live, live: false});
        }
    },
    newIntervalCallback: function (interval) {
        now=new Date().getTime()/1000;
        if (interval.hasOwnProperty('its') && interval.hasOwnProperty('ets')) {
            if (interval.its == interval.ets) {
                interval.its=interval.ets-3600
            }
            if (Math.abs(this.state.interval.ets-interval.ets)>1) {
                if (interval.ets < now-30) {
                    this.state.live = false;
                } else {
                    this.state.live = true;
                }
            }
            if (interval.ets > now) {
                interval.ets = now
            }
            PubSub.publish('datapointDataReq',{pid:this.props.pid,interval:interval})
            this.refreshData(interval);
        }
    },
    snapshotIntervalCallback: function (interval) {
        now=new Date().getTime()/1000;
        if (interval.hasOwnProperty('its') && interval.hasOwnProperty('ets')) {
            if (interval.its == interval.ets) {
                interval.its=interval.ets-3600
            }
            if (interval.ets > now) {
                interval.ets = now
            }
            this.setState({snapshotInterval:interval})
        }
    },
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'datapointDataUpdate-'+this.props.pid:
                if (this.state.interval.its == undefined || this.state.interval.ets == undefined) {
                    this.refreshData(data.interval);
                } else if (this.state.live == true && data.interval.ets > this.state.interval.ets) {
                        elapsedTs=data.interval.ets-this.state.interval.ets
                        newInterval={its:this.state.interval.its+elapsedTs, ets: data.interval.ets}
                        this.refreshData(newInterval)
                } else if ((this.state.interval.its <= data.interval.its && data.interval.its <= this.state.interval.ets) ||
                           (this.state.interval.its <= data.interval.ets && data.interval.ets <= this.state.interval.ets)) {
                    this.refreshData(this.state.interval)
                }
                break;
            case 'datapointConfigUpdate-'+this.props.pid:
                this.refreshConfig()
                break;
            case 'intervalUpdate-'+this.props.wid:
                this.newIntervalCallback(data.interval)
                break;
        }
    },
    refreshConfig: function () {
        if (datapointStore._datapointConfig.hasOwnProperty(this.props.pid)) {
            datapointConfig=datapointStore._datapointConfig[this.props.pid]
            shouldUpdate=false
            if (this.state.datapointname != datapointConfig.datapointname) {
                shouldUpdate = true
            }
            if (this.state.color != datapointConfig.color) {
                shouldUpdate = true
            }
            if (shouldUpdate) {
                this.setState({datapointname:datapointConfig.datapointname,color:datapointConfig.color})
            }
        }
    },
    refreshData: function (interval) {
        newData=getIntervalData(this.props.pid, interval)
        newSummary=this.getDataSummary(newData)
        this.setState({interval: interval, data: newData, summary:newSummary});
    },
    getDataSummary: function(data) {
        totalSamples=data.length;
        if (totalSamples>0) {
            maxValue=Math.max.apply(Math,data.map(function(o){return o.value;}));
            minValue=Math.min.apply(Math,data.map(function(o){return o.value;}));
            sumValues=0;
            meanValue=0;
            for (var j=0;j<data.length;j++) {
                sumValues+=data[j].value;
            }
            if (totalSamples>0) {
                meanValue=sumValues/totalSamples;
            }
            if ((maxValue % 1) != 0 || (minValue % 1) != 0) {
                if (typeof maxValue % 1 == 'number' && maxValue % 1 != 0) {
                    numDecimalsMaxValue=maxValue.toString().split('.')[1].length
                } else {
                    numDecimalsMaxValue=2
                }
                if (typeof minValue % 1 == 'number' && minValue % 1 != 0) {
                    numDecimalsMinValue=minValue.toString().split('.')[1].length
                } else {
                    numDecimalsMinValue=2
                }
                numDecimals=Math.max(numDecimalsMaxValue,numDecimalsMinValue)
            } else {
                numDecimals=2
            }
            meanValue=meanValue.toFixed(numDecimals)
            summary={'max':maxValue,'min':minValue,'datapointname':this.state.datapointname,'mean':meanValue}
        } else {
            summary={'max':0,'min':0,'datapointname':this.state.datapointname,'mean':0}
        }
        return summary
    },
    cancelSnapshot: function () {
        this.setState({shareModal:false, live: this.state.livePrevious})
    },
    shareSnapshot: function () {
        user_list=this.refs.users.getValue().split(/[\s,]+/);
        PubSub.publish('newWidgetDpSnapshot',{interval:this.state.snapshotInterval,user_list:user_list,wid:this.props.wid})
        this.setState({shareModal:false, live: this.state.livePrevious})
    },
    render: function () {
        if (this.state.summary.hasOwnProperty('datapointname')){
            summary=React.createElement('tr', null,
                      React.createElement('td', null, this.state.summary.datapointname),
                      React.createElement('td', null, this.state.summary.max),
                      React.createElement('td', null, this.state.summary.min),
                      React.createElement('td', null, this.state.summary.mean)
                    );
            //var summary=(<tr>
                            //<td>{this.state.summary.datapointname}</td>
                            //<td>{this.state.summary.max}</td>
                            //<td>{this.state.summary.min}</td>
                            //<td>{this.state.summary.mean}</td>
                        //</tr>
                        //);
        } else {
            summary=React.createElement('tr', null,
                      React.createElement('td', null),
                      React.createElement('td', null),
                      React.createElement('td', null),
                      React.createElement('td', null)
                    );
            //var summary=(<tr>
                            //<td/>
                            //<td/>
                            //<td/>
                            //<td/>
                        //</tr>
                        //);
        }
        var data=[{pid:this.props.pid,color:this.state.color,datapointname:this.state.datapointname,data:this.state.data}]
        share_modal=React.createElement(ReactBootstrap.Modal, {bsSize:"small", show:this.state.shareModal, onHide:this.cancelSnapshot, container:this, "aria-labelledby":"contained-modal-title"},
                      React.createElement(ReactBootstrap.Modal.Header, {closeButton:true},
                        React.createElement(ReactBootstrap.Modal.Title, {id:"contained-modal-title"}, "Share datapoint interval")
                      ),
                      React.createElement(ReactBootstrap.Modal.Body, null,
                        React.createElement('div', {className:"row"},
                          React.createElement('div', {className:"col-md-6"},
                            React.createElement(ReactBootstrap.Input, {ref:"users", type:"textarea", label:"Select Users", placeholder:"type users separated by comma"})
                          ),
                          React.createElement('div', {className:"col-md-6"},
                            React.createElement('strong', null, "Date Interval"),
                            React.createElement(TimeSlider, {interval:this.state.snapshotInterval, newIntervalCallback:this.snapshotIntervalCallback})
                          )
                        )
                      ),
                      React.createElement(ReactBootstrap.Modal.Footer, null,
                        React.createElement(ReactBootstrap.Button, {bsStyle:"default", onClick:this.cancelSnapshot}, "Cancel"),
                        React.createElement(ReactBootstrap.Button, {bsStyle:"primary", onClick:this.shareSnapshot}, "Share")
                      )
                    );
        //share_modal=(
            //<ReactBootstrap.Modal bsize="small" show={this.state.shareModal} onHide={this.cancelSnapshot} container={this} aria-labelledby="contained-modal-title">
              //<ReactBootstrap.Modal.Header closeButton>
                //<ReactBootstrap.Modal.Title id="contained-modal-title">Share datapoint interval</ReactBootstrap.Modal.Title>
              //</ReactBootstrap.Modal.Header>
              //<ReactBootstrap.Modal.Body>
                //<div className="row" >
                  //<div className="col-md-6">
                    //<ReactBootstrap.Input ref="users" type="textarea" label="Select Users" placeholder="type users separated by comma" />
                  //</div>
                  //<div className="col-md-6">
                    //<strong>Date Interval</strong>
                    //<TimeSlider interval={this.state.snapshotInterval} newIntervalCallback={this.snapshotIntervalCallback} />
                  //</div>
                //</div>
              //</ReactBootstrap.Modal.Body>
              //<ReactBootstrap.Modal.Footer>
                //<ReactBootstrap.Button bsStyle="default" onClick={this.cancelSnapshot}>Cancel</ReactBootstrap.Button>
                //<ReactBootstrap.Button bsStyle="primary" onClick={this.shareSnapshot}>Share</ReactBootstrap.Button>
              //</ReactBootstrap.Modal.Footer>
            //</ReactBootstrap.Modal>
        //);
        return React.createElement('div', null,
                 React.createElement('div', {className:"row"},
                   React.createElement('div', {className:"col-md-6"},
                     React.createElement('table', {className:"table table-condensed"},
                       React.createElement('tr', null,
                         React.createElement('th',null,"Name"),
                         React.createElement('th',null,"max"),
                         React.createElement('th',null,"min"),
                         React.createElement('th',null,"mean")
                       ),
                       summary
                     )
                   ),
                   React.createElement('div', {className:"col-md-6"},
                     React.createElement(TimeSlider, {interval:this.state.interval, newIntervalCallback:this.newIntervalCallback})
                   )
                 ),
                 React.createElement('div', {className:"row"},
                   React.createElement('div', {className:"col-md-6"},
                     React.createElement(ContentHistogram, {data:data})
                   ),
                   React.createElement('div', {className:"col-md-6"},
                     React.createElement(ContentLinegraph, {interval:this.state.interval, data:data})
                   )
                 ),
                 React.createElement('div', null,
                   share_modal
                 )
               );
        //return (<div>
                  //<div className="row">
                    //<div className="col-md-6">
                      //<table className="table table-condensed">
                        //<tr>
                          //<th>Name</th>
                          //<th>max</th>
                          //<th>min</th>
                          //<th>mean</th>
                        //</tr>
                        //{summary}
                      //</table>
                    //</div>
                    //<div className="col-md-6">
                      //<TimeSlider interval={this.state.interval} newIntervalCallback={this.newIntervalCallback} />
                    //</div>
                  //</div>
                  //<div className="row">
                    //<div className="col-md-6">
                      //<ContentHistogram data={data} />
                    //</div>
                    //<div className="col-md-6">
                      //<ContentLinegraph interval={this.state.interval} data={data} />
                    //</div>
                  //</div>
                  //<div>
                    //{share_modal}
                  //</div>
                //</div>
                //);
    }
});

var WidgetMp = React.createClass({
    styles: {
    },
    getInitialState: function () {
        return {
                interval: {its:undefined,ets:undefined},
                data: {},
                config: {},
                live: true,
                active_view: this.props.view,
                shareModal:false,
                shareCounter:this.props.shareCounter,
                snapshotInterval: undefined,
                livePrevious: true,
        }
    },
    subscriptionTokens: {},
    componentWillMount: function () {
        this.subscriptionTokens[this.props.wid]=[]
        this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('intervalUpdate-'+this.props.wid, this.subscriptionHandler),msg:'intervalUpdate-'+this.props.wid});
        for (var i=0;i<this.props.datapoints.length;i++) {
            this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('datapointDataUpdate-'+this.props.datapoints[i], this.subscriptionHandler),msg:'datapointDataUpdate-'+this.props.datapoints[i]});
            this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('datapointConfigUpdate-'+this.props.datapoints[i], this.subscriptionHandler),msg:'datapointConfigUpdate-'+this.props.datapoints[i]});
        }
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens[this.props.wid], function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.wid];
    },
    componentDidMount: function () {
        for (var i=0;i<this.props.datapoints.length;i++) {
            PubSub.publish('datapointConfigReq',{pid:this.props.datapoints[i]})
            PubSub.publish('datapointDataReq',{pid:this.props.datapoints[i]})
        }
    },
    componentWillReceiveProps: function (nextProps) {
        if (nextProps.shareCounter>this.state.shareCounter) {
            this.setState({shareModal:true,shareCounter:nextProps.shareCounter, snapshotInterval:this.state.interval, livePrevious:this.state.live, live: false});
        }
    },
    newIntervalCallback: function (interval) {
        now=new Date().getTime()/1000;
        if (interval.hasOwnProperty('its') && interval.hasOwnProperty('ets')) {
            if (Math.abs(this.state.interval.ets-interval.ets)>1) {
                if (interval.ets < now-30) {
                    this.state.live = false;
                } else {
                    this.state.live = true;
                }
            }
            if (interval.ets > now) {
                interval.ets = now
            }
            for (var i=0;i<this.props.datapoints.length;i++) {
                PubSub.publish('datapointDataReq',{pid:this.props.datapoints[i],interval:interval})
            }
            this.refreshData(interval);
        }
    },
    snapshotIntervalCallback: function (interval) {
        now=new Date().getTime()/1000;
        if (interval.hasOwnProperty('its') && interval.hasOwnProperty('ets')) {
            if (interval.its == interval.ets) {
                interval.its=interval.ets-3600
            }
            if (interval.ets > now) {
                interval.ets = now
            }
            this.setState({snapshotInterval:interval})
        }
    },
    subscriptionHandler: function (msg,data) {
        msgType=msg.split('-')[0]
        switch (msgType) {
            case 'datapointDataUpdate':
                pid=msg.split('-')[1]
                if (this.state.interval.its == undefined || this.state.interval.ets == undefined) {
                    this.refreshData(data.interval);
                } else if (this.state.live == true && data.interval.ets > this.state.interval.ets) {
                    elapsedTs=data.interval.ets-this.state.interval.ets
                    newInterval={its:this.state.interval.its+elapsedTs, ets: data.interval.ets}
                    this.refreshData(newInterval, pid)
                } else if ((this.state.interval.its <= data.interval.its && data.interval.its <= this.state.interval.ets) ||
                           (this.state.interval.its <= data.interval.ets && data.interval.ets <= this.state.interval.ets)) {
                    this.refreshData(this.state.interval, pid)
                }
                break;
            case 'datapointConfigUpdate':
                pid=msg.split('-')[1]
                this.refreshConfig(pid)
                break;
            case 'intervalUpdate':
                this.newIntervalCallback(data.interval)
                break;
        }
    },
    viewBtnClick: function (button) {
        console.log('button click',button)
        this.setState({active_view:button})
    },
    refreshConfig: function (pid) {
        if (datapointStore._datapointConfig.hasOwnProperty(pid)) {
            datapointConfig=datapointStore._datapointConfig[pid]
            shouldUpdate=false
            if (!this.state.config.hasOwnProperty(pid)) {
                shouldUpdate = true
            } else {
                if (this.state.config[pid].datapointname != datapointConfig.datapointname) {
                    shouldUpdate = true
                }
                if (this.state.config[pid].color != datapointConfig.color) {
                    shouldUpdate = true
                }
            }
            if (shouldUpdate) {
                config=this.state.config
                config[pid]=datapointConfig
                this.setState({config:config})
            }
        }
    },
    refreshData: function (interval, pid) {
        if (pid) {
            selectedPids=[pid]
        } else {
            selectedPids=this.props.datapoints
        }
        data=this.state.data
        for (var i=0;i<selectedPids.length;i++) {
            data[selectedPids[i]]=[];
            data[selectedPids[i]]=getIntervalData(selectedPids[i], interval)
        }
        this.setState({interval:interval,data:data})
    },
    onDrop: function (e) {
        console.log('onDrop ha llegado',e)
        console.log('id',e.dataTransfer.getData('id'))
        id=e.dataTransfer.getData('id')
        if (id.length==32){
            data={wid:this.props.wid, 'new_datapoints':[id]}
            PubSub.publish('modifyWidget',data)
        }
    },
    onDragEnter: function (e) {
        console.log('onDragEnter ha llegado',e)
        e.preventDefault();
    },
    onDragOver: function (e) {
        e.preventDefault();
    },
    cancelSnapshot: function () {
        this.setState({shareModal:false, live: this.state.livePrevious})
    },
    shareSnapshot: function () {
        user_list=this.refs.users.getValue().split(/[\s,]+/);
        PubSub.publish('newWidgetMpSnapshot',{interval:this.state.snapshotInterval,user_list:user_list,wid:this.props.wid})
        this.setState({shareModal:false, live: this.state.livePrevious})
    },
    render: function () {
        console.log('en el render del mp')
        var summary=$.map(this.state.data, function (element, key) {
                    if (this.state.config.hasOwnProperty(key)) {
                        summary=getDataSummary(element)
                        datapointStyle={backgroundColor: this.state.config[key].color, borderRadius: '10px'}
                        return React.createElement('tr', {key:key},
                                 React.createElement('td', null,
                                   React.createElement('span',{style:datapointStyle},"  "),
                                   React.createElement('span',null,"  "),
                                   this.state.config[key].datapointname
                                 ),
                                 React.createElement('td', null, summary.max),
                                 React.createElement('td', null, summary.min),
                                 React.createElement('td', null, summary.mean)
                               );
                        //return (<tr key={key}>
                            //<td><span style={datapointStyle}>&nbsp;&nbsp;</span><span>&nbsp;</span>{this.state.config[key].datapointname}</td>
                            //<td>{summary.max}</td>
                            //<td>{summary.min}</td>
                            //<td>{summary.mean}</td>
                        //</tr>
                        //);
                    }
        }.bind(this));
        var data=$.map(this.state.data, function (element, key) {
            if (this.state.config.hasOwnProperty(key)) {
                return {pid:key,color:this.state.config[key].color,datapointname:this.state.config[key].datapointname,data:element}
            }
        }.bind(this));
        switch (this.state.active_view){
            case 0:
                content=React.createElement(ContentLinegraph, {interval:this.state.interval, data:data});
                //content=<ContentLinegraph interval={this.state.interval} data={data} />
                break;
            case 1:
                content=React.createElement(ContentHistogram, {interval:this.state.interval, data:data});
                //content=<ContentHistogram interval={this.state.interval} data={data} />
                break;
            case 2:
                content=React.createElement(ContentTable, {interval:this.state.interval, data:data});
                //content=<ContentTable interval={this.state.interval} data={data} />
                break;
            default:
                content=React.createElement('div',null);
                //content=<div />
                break;
        }
        view_buttons=$.map([0,1,2], function (element) {
            if (this.state.active_view==element) {
                return React.createElement('button', {key:element, type:"button", className:"btn btn-default focus", onClick:function (event) {event.preventDefault(); this.viewBtnClick(element)}.bind(this)}, element);
                //return <button key={element} type="button" className="btn btn-default focus" onClick={function(event) {event.preventDefault(); this.viewBtnClick(element)}.bind(this)}>{element}</button>
            } else {
                return React.createElement('button', {key:element, type:"button", className:"btn btn-default", onClick:function (event) {event.preventDefault(); this.viewBtnClick(element)}.bind(this)}, element);
                //return <button key={element} type="button" className="btn btn-default" onClick={function(event) {event.preventDefault(); this.viewBtnClick(element)}.bind(this)} >{element}</button>
            }
        }.bind(this));
        share_modal=React.createElement(ReactBootstrap.Modal, {bsSize:"small", show:this.state.shareModal, onHide:this.cancelSnapshot, container:this, "aria-labelledby":"contained-modal-title"},
                      React.createElement(ReactBootstrap.Modal.Header, {closeButton:true},
                        React.createElement(ReactBootstrap.Modal.Title, {id:"contained-modal-title"}, "Share graph interval")
                      ),
                      React.createElement(ReactBootstrap.Modal.Body, null,
                        React.createElement('div', {className:"row"},
                          React.createElement('div', {className:"col-md-6"},
                            React.createElement(ReactBootstrap.Input, {ref:"users", type:"textarea", label:"Select Users", placeholder:"type users separated by comma"})
                          ),
                          React.createElement('div', {className:"col-md-6"},
                            React.createElement('strong', null, "Date Interval"),
                            React.createElement(TimeSlider, {interval:this.state.snapshotInterval, newIntervalCallback:this.snapshotIntervalCallback})
                          )
                        )
                      ),
                      React.createElement(ReactBootstrap.Modal.Footer, null,
                        React.createElement(ReactBootstrap.Button, {bsStyle:"default", onClick:this.cancelSnapshot}, "Cancel"),
                        React.createElement(ReactBootstrap.Button, {bsStyle:"primary", onClick:this.shareSnapshot}, "Share")
                      )
                    );
        //share_modal=(
            //<ReactBootstrap.Modal bsize="small" show={this.state.shareModal} onHide={this.cancelSnapshot} container={this} aria-labelledby="contained-modal-title">
              //<ReactBootstrap.Modal.Header closeButton>
                //<ReactBootstrap.Modal.Title id="contained-modal-title">Share Graph interval</ReactBootstrap.Modal.Title>
              //</ReactBootstrap.Modal.Header>
              //<ReactBootstrap.Modal.Body>
                //<div className="row" >
                  //<div className="col-md-6">
                    //<ReactBootstrap.Input ref="users" type="textarea" label="Select Users" placeholder="type users separated by comma" />
                  //</div>
                  //<div className="col-md-6">
                    //<strong>Date Interval</strong>
                    //<TimeSlider interval={this.state.snapshotInterval} newIntervalCallback={this.snapshotIntervalCallback} />
                  //</div>
                //</div>
              //</ReactBootstrap.Modal.Body>
              //<ReactBootstrap.Modal.Footer>
                //<ReactBootstrap.Button bsStyle="default" onClick={this.cancelSnapshot}>Cancel</ReactBootstrap.Button>
                //<ReactBootstrap.Button bsStyle="primary" onClick={this.shareSnapshot}>Share</ReactBootstrap.Button>
              //</ReactBootstrap.Modal.Footer>
            //</ReactBootstrap.Modal>
        //);
        return React.createElement('div', {onDrop:this.onDrop, onDragEnter:this.onDragEnter, onDragOver:this.onDragOver},
                 React.createElement('div', {className:"row"},
                   React.createElement('div', {className:"col-md-8"}, content),
                   React.createElement('div', {className:"col-md-4"},
                     React.createElement('div', {className:"row"},
                       React.createElement('div', {className:"col-md-12"},
                         React.createElement(TimeSlider, {interval:this.state.interval, newIntervalCallback:this.newIntervalCallback})
                       )
                     ),
                     React.createElement('div', {className:"row"},
                       React.createElement('div', {className:"col-md-12"},
                         React.createElement('div', {className:"btn-group", role:"group"}, view_buttons)
                       )
                     ),
                     React.createElement('div', {className:"row"},
                       React.createElement('div', {className:"col-md-12"},
                         React.createElement('table', {className:"table table-condensed"},
                           React.createElement('tr', null,
                             React.createElement('th', null, "Name"),
                             React.createElement('th', null, "max"),
                             React.createElement('th', null, "min"),
                             React.createElement('th', null, "mean")
                           ),
                           summary
                         )
                       )
                     )
                   )
                 ),
                 React.createElement('div', null, share_modal)
               );
        //return (<div onDrop={this.onDrop} onDragEnter={this.onDragEnter} onDragOver={this.onDragOver}>
                  //<div className="row" >
                    //<div className="col-md-8">
                      //{content}
                    //</div>
                    //<div className="col-md-4">
                      //<div className="row">
                        //<div className="col-md-12">
                          //<TimeSlider interval={this.state.interval} newIntervalCallback={this.newIntervalCallback} />
                        //</div>
                      //</div>
                      //<div className="row">
                        //<div className="col-md-12">
                          //<div className="btn-group" role="group">
                            //{view_buttons}
                          //</div>
                        //</div>
                      //</div>
                      //<div className="row">
                        //<div className="col-md-12">
                          //<table className="table table-condensed">
                            //<tr>
                              //<th>Name</th>
                              //<th>max</th>
                              //<th>min</th>
                              //<th>mean</th>
                            //</tr>
                            //{summary}
                          //</table>
                        //</div>
                      //</div>
                    //</div>
                  //</div>
                  //<div>
                    //{share_modal}
                  //</div>
                //</div>
                //);
    }
});

var TimeSlider = React.createClass({
    styles: {
    },
    notifyNewInterval: function(interval) {
        this.props.newIntervalCallback(interval);
    },
    componentDidMount: function () {
        var el = React.findDOMNode(this)
        d3TimeSlider.create(el, this.props.interval, this.notifyNewInterval)
    },
    componentDidUpdate: function () {
        var el = React.findDOMNode(this)
        d3TimeSlider.update(el, this.props.interval, this.notifyNewInterval)
    },
    render: function () {
        return React.createElement('div', null);
        //return (<div />);
    }
});

var ContentLinegraph = React.createClass({
    styles: {
    },
    componentDidMount: function () {
        var el = React.findDOMNode(this)
        d3Linegraph.create(el, this.props.data, this.props.interval)
    },
    componentDidUpdate: function () {
        var el = React.findDOMNode(this)
        d3Linegraph.update(el, this.props.data, this.props.interval)
    },
    render: function () {
        return React.createElement('div', null);
        //return (<div />);
    }
});

var ContentHistogram = React.createClass({
    styles: {
    },
    componentDidMount: function () {
        var el = React.findDOMNode(this)
        d3Histogram.create(el, this.props.data)
    },
    componentDidUpdate: function () {
        var el = React.findDOMNode(this)
        d3Histogram.update(el, this.props.data)
    },
    render: function () {
        return React.createElement('div', null);
        //return (<div />);
    }
});

var ContentTable = React.createClass({
    styles: {
    },
    componentDidMount: function () {
        var el = React.findDOMNode(this)
        d3Table.create(el, this.props.data)
    },
    componentDidUpdate: function () {
        var el = React.findDOMNode(this)
        d3Table.update(el, this.props.data)
    },
    render: function () {
        return React.createElement('div', null);
        //return (<div />);
    }
});

var WidgetDsVariable = React.createClass({
    getInitialState: function () {
        return {
                datapoints: this.props.datapoints,
        }
    },
    associateExistingDatapoint: function (event, pid) {
        event.preventDefault();
        console.log('associateExistingDatapoint',pid)
        this.refs.popover.hide()
        this.props.associateExistingDatapointCallback(this.props.position, this.props.length, pid)
    },
    identifyVariable: function () {
        console.log('el click ha llegado')
        datapointname=this.refs.datapointname.getValue();
        if (datapointname.length>1){ 
            this.refs.popover.hide()
            this.props.identifyVariableCallback(this.props.position, this.props.length, datapointname)
        }
    },
    render: function () {
        var already_monitored=$.map(this.state.datapoints, function (element,index) {
                            return React.createElement(ReactBootstrap.MenuItem, {key:index, eventKey:element.pid}, element.datapointname);
                            //return (
                            //<ReactBootstrap.MenuItem key={index} eventKey={element.pid}>
                              //{element.datapointname}
                            //</ReactBootstrap.MenuItem>
                            //);
        });
        if (already_monitored.length>0) {
            dropdown=React.createElement(ReactBootstrap.Nav, {onSelect:this.associateExistingDatapoint},
                       React.createElement(ReactBootstrap.NavDropdown, {bsSize:"xsmall", title:"This variable has been identified before", id:"nav-dropdown"},already_monitored)
                     );
            //dropdown=(<ReactBootstrap.Nav onSelect={this.associateExistingDatapoint}>
                       //<ReactBootstrap.NavDropdown bsSize="xsmall" title="This variable has been identified before" id="nav-dropdown">
                         //{already_monitored}
                       //</ReactBootstrap.NavDropdown>
                     //</ReactBootstrap.Nav>
                     //);
        } else {
            dropdown=null
        }
        return React.createElement(ReactBootstrap.OverlayTrigger, {ref:"popover", trigger:"click", rootClose:true, placement:"right", overlay:
                 React.createElement(ReactBootstrap.Popover, {title:"Identify Datapoint"},
                   React.createElement('div', null,
                     React.createElement('div', {className:"input-group"},
                       React.createElement(ReactBootstrap.Input, {ref:"datapointname", type:"text", className:"form-control", placeholder:"Datapoint name"}),
                       React.createElement('span', {className:"input-group-btn"},
                         React.createElement('button', {type:"submit", className:"btn btn-default", onClick:this.identifyVariable}, "Ok")
                       )
                     )
                   ),
                   dropdown
                 )},
                 React.createElement('span', null, this.props.content)
               );
        //return (
              //<ReactBootstrap.OverlayTrigger ref="popover" trigger="click" rootClose placement="right" overlay={<ReactBootstrap.Popover title="Identify Datapoint">
                  //<div>
                    //<div className="input-group">
                      //<ReactBootstrap.Input ref="datapointname" type="text" className="form-control" placeholder="Datapoint name" />
                      //<span className="input-group-btn">
                        //<button type="submit" className="btn btn-default" onClick={this.identifyVariable}>
                          //Ok
                        //</button>
                      //</span>
                    //</div>
                  //</div>
                  //{dropdown}
                //</ReactBootstrap.Popover>}>
                //<span>{this.props.content}</span>
              //</ReactBootstrap.OverlayTrigger>
                //);
    }
});

