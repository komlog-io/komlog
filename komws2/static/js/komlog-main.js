var Workspace = React.createClass({
    getInitialState: function () {
        return {slides: []}
    },
    shortcutCounter: 1,
    subscriptionTokens: [],
    subscriptionHandler: function(msg,data) {
        switch(msg){
            case 'loadSlide':
                slideExists=false
                if (data.hasOwnProperty('wid')) {
                    lid = data.wid
                    type = 'wid'
                } else if (data.hasOwnProperty('nid')) {
                    lid = data.nid
                    type = 'nid'
                } else if (data.hasOwnProperty('pid')) {
                    PubSub.publish('loadDatapointSlide',{pid:data.pid})
                    break;
                } else if (data.hasOwnProperty('did')) {
                    PubSub.publish('loadDatasourceSlide',{did:data.did})
                    break;
                }
                for (var i=0; i<this.state.slides.length;i++) {
                    if (this.state.slides[i].lid==lid) {
                        slideExists=true
                        break;
                    }
                }
                if (slideExists==false && lid) {
                    slide={lid:lid,shortcut:this.shortcutCounter++,type:type}
                    new_slides=this.state.slides
                    new_slides.push(slide)
                    PubSub.publish('newSlideLoaded',{slide:slide})
                    this.setState({slides:new_slides});
                }
                break;
            case 'closeSlide':
                new_slides=this.state.slides.filter(function (el) {
                        return el.lid.toString()!==data.lid.toString();
                    });
                this.setState({slides:new_slides});
                break;
            case 'updateScroll':
                this.componentDidUpdate();
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens.push({token:PubSub.subscribe('loadSlide', this.subscriptionHandler),msg:'loadSlide'});
        this.subscriptionTokens.push({token:PubSub.subscribe('closeSlide', this.subscriptionHandler),msg:'closeSlide'});
        this.subscriptionTokens.push({token:PubSub.subscribe('updateScroll', this.subscriptionHandler),msg:'updateScroll'});
    },
    componentWillUnmount: function () {
        this.subscriptionTokens.map(function (d) {
            PubSub.unsubscribe(d.token)
            });
    },
    componentWillUpdate: function () {
        this.shouldScrollBottom = $('#workspace-content')[0].scrollTop + $('#workspace-content')[0].offsetHeight === $('#workspace-content')[0].scrollHeight;
    },
    componentDidUpdate: function () {
        if (this.lastScrollHeight != $('#workspace-content')[0].scrollHeight && this.shouldScrollBottom) {
            $('#workspace-content').scrollTop($('#workspace-content')[0].scrollHeight)
        }
        this.lastScrollHeight = $('#workspace-content')[0].scrollHeight;
    },
    render: function () {
        console.log('en el slide del workspace')
        slides = this.state.slides.map( function (slide) {
            return (<Slide key={slide.shortcut} lid={slide.lid} shortcut={slide.shortcut} type={slide.type}/>)
        });
        return (<div className="workspace"> 
                {slides}
                </div>);
    },
});

var Slide = React.createClass({
    styles: {
        slidestyle:  {
            padding: '1px',
            margin: '5px',
            backgroundColor: 'white',
            boxShadow: '1px 1px 5px 1px #ccc',
            borderRadius: '5px',
        },
    },
    getInitialState: function () {
        return {conf:{}}
    },
    subscriptionTokens: {},
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'slideConfigUpdate-'+this.props.lid:
                this.refreshConfig()
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens[this.props.lid]=[]
        this.subscriptionTokens[this.props.lid].push({token:PubSub.subscribe('slideConfigUpdate-'+this.props.lid, this.subscriptionHandler),msg:'slideConfigUpdate-'+this.props.lid});
    },
    componentDidMount: function () {
        PubSub.publish('slideConfigReq',{lid:this.props.lid, type:this.props.type})
        $.map(this.subscriptionTokens[this.props.lid], function (d) {
            console.log('me monte',this.props.lid,d.msg)
        }.bind(this))
    },
    componentWillUnmount: function () {
        console.log('me desmonto',this.subscriptionTokens)
        $.map(this.subscriptionTokens[this.props.lid], function (d) {
            console.log('me desmonto',this.props.lid,d.msg)
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.lid];
    },
    shareCallback: function() {
        //aqui puede que establezcamos una propiedad a true para que el contenido se recargue y él maneje el interfaz para compartir
    },
    closeCallback: function() {
        PubSub.publish('closeSlide',{lid:this.props.lid})
    },
    refreshConfig: function () {
        if (slideStore._slideConfig.hasOwnProperty(this.props.lid)) {
            slideConfig=slideStore._slideConfig[this.props.lid]
            shouldUpdate=false
            $.each(slideConfig, function (key,value) {
                if (!(this.state.conf.hasOwnProperty(key) && this.state.conf[key]==value)) {
                    shouldUpdate=true
                }
            }.bind(this));
            if (shouldUpdate) {
                this.setState({conf:slideConfig})
            }
        }
    },
    render: function() {
        if ($.isEmptyObject(this.state.conf)) {
            conf={widgetname: "Loading..."}
            slide=(
            <div className="Slide panel panel-default" style={this.styles.slidestyle}>
            <SlideBar shortcut={this.props.shortcut} conf={conf} closeCallback={this.closeCallback}/>
            </div>
            );
        } else {
            slide=(
            <div className="Slide panel panel-default" style={this.styles.slidestyle} >
            <SlideBar shortcut={this.props.shortcut} conf={this.state.conf} shareCallback={this.shareCallback} closeCallback={this.closeCallback}/>
            <SlideContent conf={this.state.conf}/>
            </div>
            );
        }
        return slide
    },
});

var SlideBar = React.createClass({
    moveClick: function() {
        alert('hola');
    },
    shareClick: function () {
        alert('me quieren compartir')
        this.props.shareCallback()
    },
    closeClick: function () {
        this.props.closeCallback()
    },
    styles: {
        barstyle: {
        },
        namestyle: {
            textAlign: 'left',
            width: '100%',
            fontWeight: 'bold',
        },
        barseparatorstyle: {
            color: '#bbb',
        },
        iconstyle: {
            textShadow: '1px 1px 5px 1px #ccc',
            align: 'right',
            valign: 'top',
            float: 'right',
            height: '20px',
        },
    },
    getInitialState: function() {
        return {};
    },
    render: function() {
        return (
            <div className="SlideBar panel-heading" style={this.styles.barstyle}>
                <div className="SlideBarIcons" style={this.styles.iconstyle}>
                    <span className="glyphicon glyphicon-send" onClick={this.shareClick}></span> 
                    <span> </span>
                    <span className="glyphicon glyphicon-remove" onClick={this.closeClick}></span>
                </div>
                <div className="SlideBarName" style={this.styles.namestyle} >
                    <span className="glyphicon glyphicon-option-vertical" style={this.styles.barseparatorstyle} onClick={this.moveClick}></span>
                    <span > </span>
                    <span>#{this.props.shortcut} {this.props.conf.widgetname}</span>
                </div>
            </div>
        );
    }
});

var SlideContent = React.createClass({
    styles: {
        contentstyle: {
            padding: '15px',
        }
    },
    renderDs: function() {
        return (
            <div className="SlideContent" style={this.styles.contentstyle}>
                <SlideDs wid={this.props.conf.wid} did={this.props.conf.did}/>
            </div>
        );
    },
    renderDp: function() {
        return (
            <div className="SlideContent" style={this.styles.contentstyle}>
                <SlideDp wid={this.props.conf.wid} pid={this.props.conf.pid}/>
            </div>
        );
    },
    renderLg: function() {
        return (
            <div className="SlideContent" style={this.styles.contentstyle}>
                <SlideLg wid={this.props.conf.wid} datapoints={this.props.conf.datapoints}/>
            </div>
        );
    },
    renderHg: function() {
        return (
            <div className="SlideContent" style={this.styles.contentstyle}>
                <SlideHg wid={this.props.conf.wid} datapoints={this.props.conf.datapoints}/>
            </div>
        );
    },
    renderTb: function() {
        return (
            <div className="SlideContent" style={this.styles.contentstyle}>
                <SlideTb wid={this.props.conf.wid} datapoints={this.props.conf.datapoints}/>
            </div>
        );
    },
    render: function() {
        if (this.props.conf.hasOwnProperty('wid')) {
            switch (this.props.conf.type) {
                case 'ds':
                    return this.renderDs();
                    break;
                case 'dp':
                    return this.renderDp();
                    break;
                case 'lg':
                    return this.renderLg();
                    break;
                case 'hg':
                    return this.renderHg();
                    break;
                case 'tb':
                    return this.renderTb();
                    break;
                default:
                    return (
                        <div className="SlideContent" style={this.styles.contentstyle}>
                        ...
                        </div>
                    );
                    break;
            }
        }
    }
});

var SlideDs = React.createClass({
    styles: {
        infostyle: {
            float: 'right',
        },
        timestyle: {
            color: 'green',
        }
    },
    getInitialState: function () {
        return {dsData: undefined,
                datasourcename: '',
                timestamp:0,
                }
    },
    subscriptionTokens: {},
    onClickDatapoint: function(pid,e) {
        e.preventDefault();
        PubSub.publish('loadSlide',{pid:pid})
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
        $.map(this.subscriptionTokens[this.props.wid], function (d) {
            console.log('me monte',this.props.wid,d.msg,d.token)
        }.bind(this))
    },
    componentWillUnmount: function () {
        console.log('me desmonto',this.subscriptionTokens)
        $.map(this.subscriptionTokens[this.props.wid], function (d) {
            console.log('me desmonto',this.props.wid,d.msg,d.token)
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.wid];
    },
    componentDidUpdate: function () {
        console.log('componentDidUpdate')
        $('.datapoint-tooltip').tooltip()
        $('.variable-popover').popover()
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
                this.setState({dsData:datasourceData, timestamp:datasourceData.ts})
            } else if (this.state.timestamp < datasourceData.ts) {
                this.setState({dsData:datasourceData, timestamp:datasourceData.ts})
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
                        classname='datapoint-tooltip'
                    } else {
                        color='black'
                        datapointname=''
                        classname=''
                    }
                    elements.push({ne:numElement++,type:'datapoint',pid:dsData.datapoints[j].pid,p:position,l:length,style:{color:color},data:text,onclick:this.onClickDatapoint,datapointname:datapointname,classname:classname})
                    datapointFound=true
                    break;
                }
            }
            if (datapointFound == false) {
                text=dsData.content.substr(position,length)
                classname='variable-popover'
                title='Monitor variable'
                popoverContent='<div>\
                                <div class="input-group">\
                                  <input type="text" class="form-control" placeholder="Datapoint name">\
                                  <span class="input-group-btn">\
                                    <button type="submit" class="btn btn-default" onclick="monitorVariable (event,'+position+','+length+',\''+dsData.seq+'\',\''+this.props.did+'\')">Ok</button>\
                                  </span>\
                                </div>'
                if (datasourcePids.length>0) {
                    datapointDropdown='<p/>\
                                       <a href="#" class="dropdown-toggle h6" data-toggle="dropdown" aria-haspopup="true" role="button" aria-expanded="false">\
                                       This variable has already been monitored\
                                       <span class="caret"></span>\
                                       </a>\
                                       <ul id="menu1" class="dropdown-menu" role="menu" >'
                    for (var k=0;k<datasourcePids.length;k++) {
                        datapointDropdown=datapointDropdown+'<li role="presentation"><a role="menuitem" tabindex="-1" href="#" onclick=markPositiveVar(event,"'+datasourcePids[k].pid+'",'+position+','+length+',\''+dsData.seq+'\')>'+datasourcePids[k].datapointname+'</a></li>'
                    }
                    datapointDropdown=datapointDropdown+'</ul></div>'
                } else {
                    datapointDropdown=''
                }
                popoverContent=popoverContent+datapointDropdown
                elements.push({ne:numElement++, type:'variable',data:text,title:title,classname:classname,popoverContent:popoverContent})
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
    render: function () {
        elements=this.generateHtmlContent(this.state.dsData)
        var element_nodes=$.map(elements, function (element) {
            if (element.type == 'text') {
                return (<span key={element.ne}>{element.data}</span>);
            }else if (element.type == 'nl') {
                return (<br key={element.ne} />);
            }else if (element.type == 'datapoint') {
                return (<span key={element.ne} style={element.style} className={element.classname} data-placement="top" title={element.datapointname} onClick={element.onclick.bind(null,element.pid)}>{element.data}</span>);
            }else if (element.type == 'variable') {
                return (<span key={element.ne} className={element.classname} data-placement="right" data-html="true" data-content={element.popoverContent} title={element.title}>{element.data}</span>);
            }
        });
        if (typeof this.state.timestamp === 'number') {
            info_node=(
                <div style={this.styles.infostyle}>
                last updated:
                <span style={this.styles.timestyle}> {this.generateDateString(this.state.timestamp)}</span>
                </div>
                );
        } else {
            info_node=(
                <div style={this.styles.infostyle} />
                );
        }
        return (<div>
                  {info_node}
                  <div>
                    {element_nodes}
                  </div>
                </div>
                );
    }
});

var SlideDp = React.createClass({
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
        $.map(this.subscriptionTokens[this.props.wid], function (d) {
            console.log('me monte',this.props.wid,d.msg,d.token)
        }.bind(this))
    },
    componentWillUnmount: function () {
        console.log('me desmonto',this.subscriptionTokens)
        $.map(this.subscriptionTokens[this.props.wid], function (d) {
            console.log('me desmonto',this.props.wid,d.msg,d.token)
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.wid];
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
            console.log('datapointDataReq',interval)
            PubSub.publish('datapointDataReq',{pid:this.props.pid,interval:interval})
            console.log('refreshdata',interval)
            this.refreshData(interval);
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
                console.log('intervalUpdate recibido',this.props.wid,data)
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
        console.log('refreshing data',newData,newSummary)
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
    render: function () {
        if (this.state.summary.hasOwnProperty('datapointname')){
            var summary=(<tr>
                            <td>{this.state.summary.datapointname}</td>
                            <td>{this.state.summary.max}</td>
                            <td>{this.state.summary.min}</td>
                            <td>{this.state.summary.mean}</td>
                        </tr>
                        );
        } else {
            var summary=(<tr>
                            <td/>
                            <td/>
                            <td/>
                            <td/>
                        </tr>
                        );
        }
        var data=[{pid:this.props.pid,color:this.state.color,datapointname:this.state.datapointname,data:this.state.data}]
        console.log('en el return del render')
        return (<div>
                  <div className="row">
                    <div className="col-md-6">
                      <table className="table table-condensed">
                        <tr>
                          <th>Name</th>
                          <th>max</th>
                          <th>min</th>
                          <th>mean</th>
                        </tr>
                        {summary}
                      </table>
                    </div>
                    <div className="col-md-6">
                      <TimeSlider interval={this.state.interval} newIntervalCallback={this.newIntervalCallback} />
                    </div>
                  </div>
                  <div className="row">
                    <div className="col-md-6">
                      <ContentHistogram data={data} />
                    </div>
                    <div className="col-md-6">
                      <ContentLinegraph interval={this.state.interval} data={data} />
                    </div>
                  </div>
                </div>
                );
    }
});

var SlideLg = React.createClass({
    styles: {
    },
    getInitialState: function () {
        return {
                interval: {its:undefined,ets:undefined},
                data: {},
                config: {},
                live: true,
        }
    },
    subscriptionTokens: {},
    componentWillMount: function () {
        this.subscriptionTokens[this.props.wid]=[]
        this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('intervalUpdate-'+this.props.wid, this.subscriptionHandler),msg:'intervalUpdate-'+this.props.wid});
        for (var i=0;i<this.props.datapoints.length;i++) {
            this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('datapointDataUpdate-'+this.props.datapoints[i].pid, this.subscriptionHandler),msg:'datapointDataUpdate-'+this.props.datapoints[i].pid});
            this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('datapointConfigUpdate-'+this.props.datapoints[i].pid, this.subscriptionHandler),msg:'datapointConfigUpdate-'+this.props.datapoints[i].pid});
        }
    },
    componentWillUnmount: function () {
        console.log('me desmonto',this.subscriptionTokens)
        $.map(this.subscriptionTokens[this.props.wid], function (d) {
            console.log('me desmonto',this.props.wid,d.msg,d.token)
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.wid];
    },
    componentDidMount: function () {
        for (var i=0;i<this.props.datapoints.length;i++) {
            PubSub.publish('datapointConfigReq',{pid:this.props.datapoints[i].pid})
            PubSub.publish('datapointDataReq',{pid:this.props.datapoints[i].pid})
        }
    },
    componentDidUpdate: function () {
        PubSub.publish('updateScroll',{})
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
                PubSub.publish('datapointDataReq',{pid:this.props.datapoints[i].pid,interval:interval})
            }
            this.refreshData(interval);
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
            selectedPids=$.map(this.props.datapoints, function (element) {
                return element.pid;
            });
        }
        data=this.state.data
        for (var i=0;i<selectedPids.length;i++) {
            data[selectedPids[i]]=[];
            data[selectedPids[i]]=getIntervalData(selectedPids[i], interval)
        }
        this.setState({interval:interval,data:data})
    },
    render: function () {
        var summary=$.map(this.state.data, function (element, key) {
                    if (this.state.config.hasOwnProperty(key)) {
                        summary=getDataSummary(element)
                        datapointStyle={backgroundColor: this.state.config[key].color, borderRadius: '10px'}
                        return (<tr key={key}>
                            <td><span style={datapointStyle}>&nbsp;&nbsp;</span><span>&nbsp;</span>{this.state.config[key].datapointname}</td>
                            <td>{summary.max}</td>
                            <td>{summary.min}</td>
                            <td>{summary.mean}</td>
                        </tr>
                        );
                    }
        }.bind(this));
        var data=$.map(this.state.data, function (element, key) {
            if (this.state.config.hasOwnProperty(key)) {
                return {pid:key,color:this.state.config[key].color,datapointname:this.state.config[key].datapointname,data:element}
            }
        }.bind(this));
        return (<div>
                  <div className="row">
                    <div className="col-md-8">
                      <ContentLinegraph interval={this.state.interval} data={data} />
                    </div>
                    <div className="col-md-4">
                      <div className="row">
                        <div className="col-md-12">
                          <TimeSlider interval={this.state.interval} newIntervalCallback={this.newIntervalCallback} />
                        </div>
                      </div>
                      <div className="row">
                        <div className="col-md-12">
                          <table className="table table-condensed">
                            <tr>
                              <th>Name</th>
                              <th>max</th>
                              <th>min</th>
                              <th>mean</th>
                            </tr>
                            {summary}
                          </table>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                );
    }
});

var SlideHg = React.createClass({
    styles: {
    },
    getInitialState: function () {
        return {
                interval: {its:undefined,ets:undefined},
                data: {},
                config: {},
                live: true,
        }
    },
    subscriptionTokens: {},
    componentWillMount: function () {
        this.subscriptionTokens[this.props.wid]=[]
        this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('intervalUpdate-'+this.props.wid, this.subscriptionHandler),msg:'intervalUpdate-'+this.props.wid});
        for (var i=0;i<this.props.datapoints.length;i++) {
            this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('datapointDataUpdate-'+this.props.datapoints[i].pid, this.subscriptionHandler),msg:'datapointDataUpdate-'+this.props.datapoints[i].pid});
            this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('datapointConfigUpdate-'+this.props.datapoints[i].pid, this.subscriptionHandler),msg:'datapointConfigUpdate-'+this.props.datapoints[i].pid});
        }
    },
    componentWillUnmount: function () {
        console.log('me desmonto',this.subscriptionTokens)
        $.map(this.subscriptionTokens[this.props.wid], function (d) {
            console.log('me desmonto',this.props.wid,d.msg,d.token)
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.wid];
    },
    componentDidMount: function () {
        for (var i=0;i<this.props.datapoints.length;i++) {
            PubSub.publish('datapointConfigReq',{pid:this.props.datapoints[i].pid})
            PubSub.publish('datapointDataReq',{pid:this.props.datapoints[i].pid})
        }
    },
    componentDidUpdate: function () {
        PubSub.publish('updateScroll',{})
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
                PubSub.publish('datapointDataReq',{pid:this.props.datapoints[i].pid,interval:interval})
            }
            this.refreshData(interval);
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
            selectedPids=$.map(this.props.datapoints, function (element) {
                return element.pid;
            });
        }
        data=this.state.data
        for (var i=0;i<selectedPids.length;i++) {
            data[selectedPids[i]]=[];
            data[selectedPids[i]]=getIntervalData(selectedPids[i], interval)
        }
        this.setState({interval:interval,data:data})
    },
    render: function () {
        var summary=$.map(this.state.data, function (element, key) {
                    if (this.state.config.hasOwnProperty(key)) {
                        summary=getDataSummary(element)
                        datapointStyle={backgroundColor: this.state.config[key].color, borderRadius: '10px'}
                        return (<tr key={key}>
                            <td><span style={datapointStyle}>&nbsp;&nbsp;</span><span>&nbsp;</span>{this.state.config[key].datapointname}</td>
                            <td>{summary.max}</td>
                            <td>{summary.min}</td>
                            <td>{summary.mean}</td>
                        </tr>
                        );
                    }
        }.bind(this));
        var data=$.map(this.state.data, function (element, key) {
            if (this.state.config.hasOwnProperty(key)) {
                return {pid:key,color:this.state.config[key].color,datapointname:this.state.config[key].datapointname,data:element}
            }
        }.bind(this));
        return (<div>
                  <div className="row">
                    <div className="col-md-8">
                      <ContentHistogram data={data} />
                    </div>
                    <div className="col-md-4">
                      <div className="row">
                        <div className="col-md-12">
                          <TimeSlider interval={this.state.interval} newIntervalCallback={this.newIntervalCallback} />
                        </div>
                      </div>
                      <div className="row">
                        <div className="col-md-12">
                          <table className="table table-condensed">
                            <tr>
                              <th>Name</th>
                              <th>max</th>
                              <th>min</th>
                              <th>mean</th>
                            </tr>
                            {summary}
                          </table>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                );
    }
});

var SlideTb = React.createClass({
    styles: {
    },
    getInitialState: function () {
        return {
                interval: {its:undefined,ets:undefined},
                data: {},
                config: {},
                live: true,
        }
    },
    subscriptionTokens: {},
    componentWillMount: function () {
        this.subscriptionTokens[this.props.wid]=[]
        this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('intervalUpdate-'+this.props.wid, this.subscriptionHandler),msg:'intervalUpdate-'+this.props.wid});
        for (var i=0;i<this.props.datapoints.length;i++) {
            this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('datapointDataUpdate-'+this.props.datapoints[i].pid, this.subscriptionHandler),msg:'datapointDataUpdate-'+this.props.datapoints[i].pid});
            this.subscriptionTokens[this.props.wid].push({token:PubSub.subscribe('datapointConfigUpdate-'+this.props.datapoints[i].pid, this.subscriptionHandler),msg:'datapointConfigUpdate-'+this.props.datapoints[i].pid});
        }
    },
    componentWillUnmount: function () {
        console.log('me desmonto',this.subscriptionTokens)
        $.map(this.subscriptionTokens[this.props.wid], function (d) {
            console.log('me desmonto',this.props.wid,d.msg,d.token)
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.wid];
    },
    componentDidMount: function () {
        for (var i=0;i<this.props.datapoints.length;i++) {
            PubSub.publish('datapointConfigReq',{pid:this.props.datapoints[i].pid})
            PubSub.publish('datapointDataReq',{pid:this.props.datapoints[i].pid})
        }
    },
    componentDidUpdate: function () {
        PubSub.publish('updateScroll',{})
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
                PubSub.publish('datapointDataReq',{pid:this.props.datapoints[i].pid,interval:interval})
            }
            this.refreshData(interval);
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
            selectedPids=$.map(this.props.datapoints, function (element) {
                return element.pid;
            });
        }
        data=this.state.data
        for (var i=0;i<selectedPids.length;i++) {
            data[selectedPids[i]]=[];
            data[selectedPids[i]]=getIntervalData(selectedPids[i], interval)
        }
        this.setState({interval:interval,data:data})
    },
    render: function () {
        var summary=$.map(this.state.data, function (element, key) {
                    if (this.state.config.hasOwnProperty(key)) {
                        summary=getDataSummary(element)
                        datapointStyle={backgroundColor: this.state.config[key].color, borderRadius: '10px'}
                        return (<tr key={key}>
                            <td><span style={datapointStyle}>&nbsp;&nbsp;</span><span>&nbsp;</span>{this.state.config[key].datapointname}</td>
                            <td>{summary.max}</td>
                            <td>{summary.min}</td>
                            <td>{summary.mean}</td>
                        </tr>
                        );
                    }
        }.bind(this));
        var data=$.map(this.state.data, function (element, key) {
            if (this.state.config.hasOwnProperty(key)) {
                return {pid:key,color:this.state.config[key].color,datapointname:this.state.config[key].datapointname,data:element}
            }
        }.bind(this));
        return (<div>
                  <div className="row">
                    <div className="col-md-8">
                      <ContentTable data={data} />
                    </div>
                    <div className="col-md-4">
                      <div className="row">
                        <div className="col-md-12">
                          <TimeSlider interval={this.state.interval} newIntervalCallback={this.newIntervalCallback} />
                        </div>
                      </div>
                      <div className="row">
                        <div className="col-md-12">
                          <table className="table table-condensed">
                            <tr>
                              <th>Name</th>
                              <th>max</th>
                              <th>min</th>
                              <th>mean</th>
                            </tr>
                            {summary}
                          </table>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                );
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
        return (<div />);
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
        return (<div />);
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
        return (<div />);
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
        return (<div />);
    }
});

React.render(
    <Workspace />
    ,
    document.getElementById('workspace-content')
);

function monitorVariable (event,position,length,seq,did) {
    event.preventDefault()
    var theName = $(event.target).parent().parent().find('input').val()
    var thePopover = $(event.target).parent().parent().parent().parent().parent()
    thePopover.popover('disable').popover('hide')
    thePopover.remove();
    console.log('monitor var received',position,length,seq,did,theName)
    data={p:position,l:length,seq:seq,did:did,datapointname:theName}
    PubSub.publish('monitorDatapoint',data)
}

function markPositiveVar(event,pid,position,length,seq) {
    event.preventDefault()
    console.log('markPositiveVar',pid,position,length,seq)
    var thePopover = $(event.target).parent().parent().parent().parent().parent()
    thePopover.popover('disable').popover('hide')
    thePopover.remove();
    data={p:position,l:length,seq:seq,pid:pid}
    PubSub.publish('markPositiveVar',data)
}
