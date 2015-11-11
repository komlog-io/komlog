var Dashboard= React.createClass({
    getInitialState: function () {
        return {
                slides: [],
                dashboardname: '',
                wids: [],
               }
    },
    shortcutCounter: 1,
    subscriptionTokens: {},
    subscriptionHandler: function(msg,data) {
        switch(msg){
            case 'loadSlide':
                this.loadSlide(data)
                break;
            case 'closeSlide':
                this.closeSlide(data.lid)
                break;
            case 'dashboardConfigUpdate.'+this.props.bid:
                this.dashboardConfigUpdate()
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens[this.props.bid]=[]
        this.subscriptionTokens[this.props.bid].push({token:PubSub.subscribe('loadSlide', this.subscriptionHandler),msg:'loadSlide'});
        this.subscriptionTokens[this.props.bid].push({token:PubSub.subscribe('closeSlide', this.subscriptionHandler),msg:'closeSlide'});
        if (this.props.bid != '0') {
            this.subscriptionTokens[this.props.bid].push({token:PubSub.subscribe('dashboardConfigUpdate.'+this.props.bid, this.subscriptionHandler),msg:'dashboardConfigUpdate.'+this.props.bid});
        } else {
            this.setState({dashboardname:'Main Dashboard'})
        }
    },
    componentDidMount: function () {
        if (this.props.bid != '0') {
            PubSub.publish('dashboardConfigReq',{bid:this.props.bid})
        }
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens[this.props.bid], function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.bid];
    },
    dashboardConfigUpdate: function () {
        dashboard=dashboardStore._dashboardConfig[this.props.bid];
        if (dashboard != undefined) {
            state={}
            if (this.state.dashboardname != dashboard.dashboardname) {
                state.dashboardname=dashboard.dashboardname
            }
            if (dashboard.wids.length != this.state.wids.length) {
                state.wids=dashboard.wids
            } else {
                for (var i=0;i<dashboard.wids.length; i++) {
                    if (this.state.wids.indexOf(dashboard.wids[i])==-1) {
                        state.wids=wids
                        break;
                    }
                }
            }
            if (Object.keys(state).length > 0) {
                if (state.hasOwnProperty('wids')) {
                    slides=this.state.slides
                    for (var i=0;i<slides.length;i++) {
                        if (slides[i].isPinned == false && state.wids.indexOf(slides[i].lid)>-1 ) {
                            slides[i].isPinned=true;
                        } else if (slides[i].isPinned == true && state.wids.indexOf(slides[i].lid)==-1) {
                            slides[i].isPinned=false;
                        }
                    }
                    console.log('llego ')
                    for (var i=0;i<state.wids.length;i++) {
                        slide=slides.filter( function (el) {
                            return el.lid == state.wids[i]
                        });
                        if (slide.length == 0) {
                            slide={lid:state.wids[i],
                                   shortcut:this.shortcutCounter++,
                                   type:'wid',
                                   isPinned:true}
                            slides.push(slide)
                        }
                    }
                    state.slides=slides;
                }
                console.log('actualizo state',state,Object.keys(state).length)
                this.setState(state);
            }
        }
    },
    closeDashboard: function () {
        if (this.props.bid != '0') {
            this.props.closeCallback(this.props.bid)
        }
    },
    closeSlide: function (lid) {
        if (this.props.active == true ) {
            new_slides=this.state.slides.filter(function (el) {
                    return el.lid.toString()!==lid.toString();
                });
            this.setState({slides:new_slides});
        }
    },
    loadSlide: function (data) {
        if (this.props.active == true) {
            slideExists=false
            if (data.hasOwnProperty('wid')) {
                lid = data.wid
                type = 'wid'
            } else if (data.hasOwnProperty('nid')) {
                lid = data.nid
                type = 'nid'
            } else if (data.hasOwnProperty('pid')) {
                PubSub.publish('loadDatapointSlide',{pid:data.pid})
                return;
            } else if (data.hasOwnProperty('did')) {
                PubSub.publish('loadDatasourceSlide',{did:data.did})
                return;
            } else if (data.hasOwnProperty('bid')) {
                PubSub.publish('showDashboard',{bid:data.bid})
                return;
            } else {
                return;
            }
            tid=data.tid
            for (var i=0; i<this.state.slides.length;i++) {
                if (this.state.slides[i].lid==lid) {
                    slideExists=true
                    break;
                }
            }
            if (slideExists==false && lid) {
                if (type=='wid' && this.state.wids.indexOf(lid)>-1) {
                    isPinned=true
                } else {
                    isPinned=false
                }
                slide={lid:lid,tid:tid,shortcut:this.shortcutCounter++,type:type,isPinned:isPinned}
                new_slides=this.state.slides
                new_slides.push(slide)
                PubSub.publish('newSlideLoaded',{slide:slide})
                this.setState({slides:new_slides});
            }
        }
    },
    getSlideList: function () {
        slides = this.state.slides.map( function (slide) {
            return (<Slide key={slide.shortcut} bid={this.props.bid} lid={slide.lid} tid={slide.tid} shortcut={slide.shortcut} type={slide.type} isPinned={slide.isPinned} />)
        }.bind(this));
        return slides
    },
    render: function () {
        slides=this.getSlideList()
        if (this.props.active == true) {
            display='block'
        } else {
            display='none'
        }
        return (<div className="workspace modal-container" style={{'display':display}}> 
                  <DashboardHeader bid={this.props.bid} dashboardname={this.state.dashboardname} closeCallback={this.closeDashboard} />
                  <div>
                    {slides}
                  </div>
                </div>);
    },
});

var DashboardHeader= React.createClass({
    getInitialState: function () {
        return {
                showConfig: false,
                deleteModal: false,
               }
    },
    closeDashboard: function () {
        this.props.closeCallback()
    },
    showConfig: function () {
        this.setState({showConfig:!this.state.showConfig})
    },
    updateConfig: function () {
        new_dashboardname=this.refs.dashboardname.getValue();
        if (new_dashboardname.length>0 && new_dashboardname!=this.props.dashboardname && this.props.bid != '0') {
            PubSub.publish('modifyDashboard',{bid:this.props.bid, new_dashboardname:new_dashboardname})
            this.setState({showConfig:false})
        }
    },
    deleteDashboard: function () {
        this.setState({deleteModal:true})
    },
    confirmDelete: function () {
        PubSub.publish('deleteDashboard',{bid:this.props.bid})
        this.props.closeCallback()
    },
    cancelDelete: function () {
        this.setState({deleteModal:false})
    },
    getDashboardHeader: function () {
        if (this.props.bid == '0') {
            return (
                  <div>
                    <h3 className="dashboard-header">
                      {this.props.dashboardname}
                    </h3>
                  </div>
                );
        } else {
            return (
                    <div>
                      <h3 className="dashboard-header">
                        {this.props.dashboardname}
                        <small><ReactBootstrap.Glyphicon glyph="remove" className="pull-right" onClick={this.closeDashboard}>&nbsp;</ReactBootstrap.Glyphicon></small>
                        <small><ReactBootstrap.Glyphicon glyph="cog" className="pull-right"  onClick={this.showConfig}>&nbsp;</ReactBootstrap.Glyphicon></small>
                      </h3>
                      <ReactBootstrap.Collapse in={this.state.showConfig}>
                        <div>
                          <ReactBootstrap.Well>
                            <ReactBootstrap.ListGroup >
                              <ReactBootstrap.ListGroupItem bsSize="small" >
                                <form className="form-horizontal">
                                  <ReactBootstrap.Input ref="dashboardname" placeholder={this.props.dashboardname} bsSize="small" type="text" label="Dashboard Name" labelClassName="col-xs-3" wrapperClassName="col-xs-6" />
                                  <div className="text-right">
                                    <ReactBootstrap.Button bsSize="small" bsStyle="primary" onClick={this.updateConfig}>Update</ReactBootstrap.Button>
                                  </div>
                                </form>
                              </ReactBootstrap.ListGroupItem>
                              <ReactBootstrap.ListGroupItem bsSize="xsmall" >
                                <strong>Delete Dashboard</strong>
                                <div className="text-right">
                                  <ReactBootstrap.Button bsSize="small" bsStyle="danger" onClick={this.deleteDashboard}>Delete</ReactBootstrap.Button>
                                </div>
                              </ReactBootstrap.ListGroupItem>
                            </ReactBootstrap.ListGroup>
                          </ReactBootstrap.Well>
                          <ReactBootstrap.Modal bsize="small" show={this.state.deleteModal} onHide={this.cancelDelete} container={this} aria-labelledby="contained-modal-title">
                            <ReactBootstrap.Modal.Header closeButton>
                              <ReactBootstrap.Modal.Title id="contained-modal-title">Delete Dashboard</ReactBootstrap.Modal.Title>
                            </ReactBootstrap.Modal.Header>
                            <ReactBootstrap.Modal.Body>
                              Dashboard {this.props.dashboardname} will be deleted.
                              <strong> Are You sure? </strong>
                            </ReactBootstrap.Modal.Body>
                            <ReactBootstrap.Modal.Footer>
                              <ReactBootstrap.Button bsStyle="default" onClick={this.cancelDelete}>Cancel</ReactBootstrap.Button>
                              <ReactBootstrap.Button bsStyle="primary" onClick={this.confirmDelete}>Delete</ReactBootstrap.Button>
                            </ReactBootstrap.Modal.Footer>
                          </ReactBootstrap.Modal>
                        </div>
                      </ReactBootstrap.Collapse>
                    </div>
                );
        }
    },
    render: function () {
        header=this.getDashboardHeader();
        if (header) {
            return (
                  <div>
                    {header}
                  </div>
                  );
        } else {
            return null
        }
    },
});

