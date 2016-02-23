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
    componentDidUpdate: function () {
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
        bid = this.props.bid
        slides = this.state.slides.map( function (slide) {
            return React.createElement(Slide, {key:slide.shortcut, bid:bid, lid:slide.lid, tid:slide.tid, shortcut:slide.shortcut, type:slide.type, isPinned:slide.isPinned});
        });
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
                 //React.createElement(DashboardHeader, {bid:this.props.bid, dashboardname:this.state.dashboardname, closeCallback:this.closeDashboard}),
                 //React.createElement('div', null, 
                   //React.createElement(ReactCSSTransitionGroup, {transitionName:'list-item', transitionEnterTimeout:500, transitionLeaveTimeout:300}, 
                     //slides
                     //)
                   //)
                 React.createElement(DashboardGrid, {children:slides})
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

var DashboardGrid=React.createClass({
    getInitialState: function () {
        return {
            columns: 0,
            width: 0,
            cellWidth: 0,
            cells: {},
            colDim:{},
       }
    },
    componentDidMount: function () {
        var width=ReactDOM.findDOMNode(this).offsetWidth
        var height=ReactDOM.findDOMNode(this).offsetHeight
        var minCellWidth = 450;
        var columns = parseInt(width / minCellWidth);
        var cellWidth= parseInt(width / columns);
        var colDim={}
        for (var i = 0; i< columns; i++) {
            colDim[i]={x:i*cellWidth,y:0}
        }
        this.setState({cellWidth:cellWidth, columns: columns, colDim:colDim})
    },
    componentDidUpdate: function () {
        var shouldUpdate = false;
        var cells = this.state.cells
        var colDim = this.state.colDim
        var cellsLayout = {}
        // update cells dims
        for (var lid in this.refs) {
            var curX = this.refs[lid].offsetLeft
            var curY = this.refs[lid].offsetTop
            var curWidth = this.refs[lid].offsetWidth
            var curHeight = this.refs[lid].offsetHeight
            if (cells.hasOwnProperty(lid)) {
                var curCell = cells[lid]
                if (curCell.x != curX || curCell.y != curY || curCell.width != curWidth || curCell.height != curHeight ) {
                    shouldUpdate = true;
                    curCell.x = curX
                    curCell.y = curY
                    curCell.width = curWidth
                    curCell.height = curHeight
                }
            } else {
                shouldUpdate = true;
                cells[lid]={x:curX, y:curY, width:curWidth, height:curHeight}
            }
            for (var colNum in colDim) {
                if (curX == colDim[colNum].x && (parseInt(curY)+parseInt(curHeight)>colDim[colNum].y)) {
                    shouldUpdate = true;
                    colDim[colNum].y=parseInt(curY)+parseInt(curHeight)
                }
            }
        }
        //nos quedamos con las cells que existen actualmente
        for (var oldLid in cells) {
            var hasIt = false;
            for (var newLid in this.refs) {
                if (oldLid == newLid) {
                    hasIt = true;
                    break;
                }
            }
            if (hasIt == false) {
                shouldUpdate = true;
                delete cells[oldLid]
            } else {
                if (!cellsLayout.hasOwnProperty(cells[newLid].x)) {
                    cellsLayout[cells[newLid].x]=[]
                }
                cellsLayout[cells[newLid].x].push({y:cells[newLid].y, height:cells[newLid].height, ref:newLid})
            }
        }
        // ahora tenemos que agrupar las cells si hay huecos o separarlas si hay solapes
        var newY = 0
        var ref = null;
        for (var col in cellsLayout) {
            cellsLayout[col].sort(function (a,b) {return a.y - b.y})
            newY=0;
            for (var i=0;i<cellsLayout[col].length;i++) {
                ref = cellsLayout[col][i].ref
                cells[ref].y = newY
                cellsLayout[col][i].y = newY // lo necesitaremos en el siguiente paso
                newY += cells[ref].height
                if (i == cellsLayout[col].length-1) {
                    for (var colNum in colDim) {
                        if (col == colDim[colNum].x) {
                            colDim[colNum].y=cellsLayout[col][i].y+cellsLayout[col][i].height
                        }
                    }
                }
            }
        }
        // por ultimo, debemos ver si alguna columna tiene demasiadas cells y hay que moverlas a otras columnas
        var relocated = false
        for (var col in cellsLayout) {
            cellsLayout[col].sort(function (a,b) {return b.y - a.y}) //descendente
            for (var i=0;i<cellsLayout[col].length;i++) {
                ref = cellsLayout[col][i].ref
                for (var colNum in colDim) {
                    if (col != colDim[colNum].x && colDim[colNum].y < cellsLayout[col][i].y) {
                        relocated = true;
                        cells[ref].x = colDim[colNum].x
                        cells[ref].y = colDim[colNum].y
                        colDim[colNum].y= cells[ref].y+cells[ref].height
                        break;
                    }
                    relocated = false;
                }
                if (!relocated) {
                    break;
                }
            }
        }
        
        if (shouldUpdate) {
            this.setState({cells:cells, colDim:colDim})
        }
    },
    getGrid: function () {
        var grid=[]
        if (this.state.columns == 0) {
            return grid
        } else {
            var cells = this.state.cells
            var colDim = this.state.colDim
            var cellWidth = this.state.cellWidth
            grid = React.Children.map( this.props.children, function (child, i) {
                if (child.props.lid in cells) {
                    var x = cells[child.props.lid].x
                    var y = cells[child.props.lid].y
                    var width = cells[child.props.lid].width
                } else {
                    var x = colDim[0].x;
                    var y = colDim[0].y;
                    var width = cellWidth
                    for (var col in colDim) {
                        if (colDim[col].y < y ) {
                            x = colDim[col].x;
                            y = colDim[col].y;
                        }
                    }
                }
                var cellStyle={left:x, top:y, width: width}
                return React.createElement('div',{className:'grid-element', key:child.props.lid, ref:child.props.lid, style:cellStyle},
                    child
                )
            });
            return grid
        }
    },
    render: function () {
        grid = this.getGrid();
        return React.createElement('div',null,
            grid
        );
    },
});

