var ReactCSSTransitionGroup = React.addons.CSSTransitionGroup;

var Dashboard=React.createClass({
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
            return React.createElement(Slide, {key:slide.shortcut, bid:this.props.bid, lid:slide.lid, tid:slide.tid, shortcut:slide.shortcut, type:slide.type, isPinned:slide.isPinned});
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
        return React.createElement('div', {className:"workspace modal-container", style:{display:display}}, 
                 React.createElement(DashboardHeader, {bid:this.props.bid, dashboardname:this.state.dashboardname, closeCallback:this.closeDashboard}),
                 React.createElement('div', null, 
                   React.createElement(ReactCSSTransitionGroup, {transitionName:'list-item', transitionEnterTimeout:500, transitionLeaveTimeout:300}, 
                     slides
                     )
                   )
                 );
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
            return React.createElement('div', null, 
                     React.createElement('h3', {className:"dashboard-header"},
                       this.props.dashboardname
                       )
                     );
        } else {
            return React.createElement('div', null, 
                     React.createElement('h3', {className:"dashboard-header"},
                       this.props.dashboardname,
                       React.createElement('small', null,
                         React.createElement(ReactBootstrap.Glyphicon, {glyph:"remove", className:"pull-right", onClick:this.closeDashboard}," ")
                       ),
                       React.createElement('small', null,
                         React.createElement(ReactBootstrap.Glyphicon, {glyph:"cog", className:"pull-right", onClick:this.showConfig}," ")
                       )
                     ),
                     React.createElement(ReactBootstrap.Collapse, {in:this.state.showConfig}, 
                       React.createElement('div', null, 
                         React.createElement(ReactBootstrap.Well, null, 
                           React.createElement(ReactBootstrap.ListGroup, null,
                             React.createElement(ReactBootstrap.ListGroupItem, {bsSize:"small"},
                               React.createElement('form', {className:"form-horizontal"},
                                 React.createElement(ReactBootstrap.Input, {ref:"dashboardname", placeholder:this.props.dashboardname, bsSize:"small", type:"text", label:"Dashboard Name", labelClassName:"col-xs-3", wrapperClassName:"col-xs-6"}),
                                 React.createElement('div', {className:"text-right"}, 
                                   React.createElement(ReactBootstrap.Button, {bsSize:"small", bsStyle:"primary", onClick:this.updateConfig}, "Update")
                                 )
                               )
                             ),
                             React.createElement(ReactBootstrap.ListGroupItem, {bsSize:"small"},
                               React.createElement('strong', null, "Delete Dashboard"),
                               React.createElement('div', {className:"text-right"}, 
                                 React.createElement(ReactBootstrap.Button, {bsSize:"small", bsStyle:"danger", onClick:this.deleteDashboard}, "Delete")
                               )
                             )
                           )
                         ),
                         React.createElement(ReactBootstrap.Modal, {bsSize:"small", show:this.state.deleteModal, onHide:this.cancelDelete, container:this, "aria-labeledby":"contained-modal-title"},
                           React.createElement(ReactBootstrap.Modal.Header, {closeButton:true},
                             React.createElement(ReactBootstrap.Modal.Title, {id:"contained-modal-title"}, "Delete Dashboard")
                           ), 
                           React.createElement(ReactBootstrap.Modal.Body, null,
                             "Dashboard "+this.props.dashboardname+" will be deleted",
                             React.createElement('strong', null, "Are You Sure?")
                           ),
                           React.createElement(ReactBootstrap.Modal.Footer, null, 
                             React.createElement(ReactBootstrap.Button, {bsStyle:"default", onClick:this.cancelDelete}, "Cancel"),
                             React.createElement(ReactBootstrap.Button, {bsStyle:"primary", onClick:this.confirmDelete}, "Delete")
                           )
                         )
                       )
                     )
                   );
        }
    },
    render: function () {
        header=this.getDashboardHeader();
        if (header) {
            return React.createElement('div', null, header);
        } else {
            return null
        }
    },
});

