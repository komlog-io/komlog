var Snapshot = React.createClass({
    getInitialState: function () {
        return {
                conf:{},
                shareCounter: 0,
                downloadCounter: 0,
                barMessageTime: 0,
                }
    },
    subscriptionTokens: {},
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'snapshotConfigUpdate-'+this.props.nid:
                this.refreshConfig()
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens[this.props.nid]=[]
        this.subscriptionTokens[this.props.nid].push({token:PubSub.subscribe('snapshotConfigUpdate-'+this.props.nid, this.subscriptionHandler),msg:'snapshotConfigUpdate-'+this.props.nid});
    },
    componentDidMount: function () {
        PubSub.publish('snapshotConfigReq',{nid:this.props.nid,tid:this.props.tid})
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens[this.props.nid], function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.nid];
    },
    shareCallback: function() {
        this.setState({shareCounter:this.state.shareCounter+1})
    },
    closeCallback: function() {
        this.props.closeCallback();
    },
    downloadCallback: function() {
        this.setState({downloadCounter:this.state.downloadCounter+1})
    },
    barMessage: function (data) {
        if ('messageTime' in data && data.messageTime > this.state.barMessageTime) {
            this.setState({barMessage:data.message, barMessageTime:data.messageTime});
        }
    },
    refreshConfig: function () {
        if (snapshotStore._snapshotConfig.hasOwnProperty(this.props.nid)) {
            snapshotConfig=snapshotStore._snapshotConfig[this.props.nid]
            shouldUpdate=false
            $.each(snapshotConfig, function (key,value) {
                if (!(this.state.conf.hasOwnProperty(key) && this.state.conf[key]==value)) {
                    shouldUpdate=true
                }
            }.bind(this));
            if (shouldUpdate) {
                this.setState({conf:snapshotConfig})
            }
        }
    },
    getSnapshotContentEl: function () {
        if ($.isEmptyObject(this.state.conf)) {
            return null
        } else {
            switch (this.state.conf.type) {
                case 'ds':
                    return React.createElement(SnapshotDs, {nid:this.props.nid, tid:this.props.tid, datasource:this.state.conf.datasource, datapoints:this.state.conf.datapoints, its:this.state.conf.its, seq:this.state.conf.seq, downloadCounter:this.state.downloadCounter});
                    break;
                case 'dp':
                    return React.createElement(SnapshotDp, {nid:this.props.nid, tid:this.props.tid, datapoint:this.state.conf.datapoint, its:this.state.conf.its, ets:this.state.conf.ets, downloadCounter:this.state.downloadCounter, barMessageCallback:this.barMessage});
                    break;
                case 'mp':
                    return React.createElement(SnapshotMp, {nid:this.props.nid, tid:this.props.tid, view:this.state.conf.view, datapoints:this.state.conf.datapoints, its:this.state.conf.its, ets:this.state.conf.ets, downloadCounter:this.state.downloadCounter, widgetname:this.state.conf.widgetname, barMessageCallback:this.barMessage});
                    break;
                default:
                    return null;
                    break;
            }
        }
    },
    render: function() {
        snapshot_content=this.getSnapshotContentEl();
        if ($.isEmptyObject(this.state.conf)) {
            snapshot=React.createElement('div', null,
                       React.createElement(SnapshotBar, {conf:this.state.conf, closeCallback:this.closeCallback})
                     );
        } else {
            snapshot=React.createElement('div', null,
                       React.createElement(SnapshotBar, {conf:this.state.conf, shareCallback:this.shareCallback, closeCallback:this.closeCallback, downloadCallback:this.downloadCallback, message:this.state.barMessage, messageTime:this.state.barMessageTime}),
                       snapshot_content
                     );
        }
        return snapshot
    },
});

var SnapshotBar = React.createClass({
    getInitialState: function() {
        return {
            message:{type:'info',message:'Loading'},
            messageTime:0,
        };
    },
    componentWillReceiveProps: function (nextProps) {
        if (!('widgetname' in this.props.conf) && 'widgetname' in nextProps.conf) {
            this.setState({message:{type:null,message:null},messageTime:(new Date).getTime()});
        }
        if (nextProps.messageTime>this.state.messageTime) {
            this.setState({message:nextProps.message, messageTime:nextProps.messageTime});
        }
    },
    moveClick: function() {
        alert('hola');
    },
    closeClick: function () {
        this.props.closeCallback()
    },
    downloadClick: function () {
        this.props.downloadCallback()
    },
    styles: {
        barstyle: {
        },
        namestyle: {
            textAlign: 'left',
            width: '100%',
            fontWeight: 'bold',
        },
        righticonstyle: {
            textShadow: '1px 1px 5px 1px #ccc',
            float: 'right',
            height: '20px',
            padding: '0px 5px 0px',
            color: '#aaa',
        },
        lefticonstyle: {
            textShadow: '1px 1px 5px 1px #ccc',
            float: 'left',
            height: '20px',
            padding: '0px 5px 0px',
        },
        messagestyle: {
            float: 'right',
            height: '25%',
            padding: '0px 10px 0px',
            marginBottom: '0px',
        },
    },
    render: function() {
        message=React.createElement(Alert, {style:this.styles.messagestyle,type:this.state.message.type,message:this.state.message.message,messageTime:this.state.messageTime,autoCloseable: ('widgetname' in this.props.conf) ? true : false})
        return React.createElement('div', {className:"SlideBar panel-heading", style:this.styles.barstyle},
                 React.createElement(ReactBootstrap.Glyphicon, {className:"SlideBarIcon", glyph:"remove", onClick:this.closeClick, style:this.styles.righticonstyle}),
                 React.createElement(ReactBootstrap.Glyphicon, {className:"SlideBarIcon", glyph:"download", onClick:this.downloadClick, style:this.styles.righticonstyle}),
                 message,
                 React.createElement(ReactBootstrap.Glyphicon, {glyph:"camera", style:this.styles.lefticonstyle}),
                 React.createElement('div', {className:"SlideBarName", style:this.styles.namestyle},this.props.conf.widgetname ? this.props.conf.widgetname : '')
               );
    }
});

var SnapshotDs = React.createClass({
    getInitialState: function () {
        return {dsData: undefined,
                timestamp: undefined,
                downloadCounter:this.props.downloadCounter,
                }
    },
    subscriptionTokens: {},
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'snapshotDsDataUpdate-'+this.props.datasource.did:
                if (data.hasOwnProperty('seq') && data.seq==this.props.seq) {
                    this.refreshData()
                }
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens[this.props.nid]=[]
        this.subscriptionTokens[this.props.nid].push({token:PubSub.subscribe('snapshotDsDataUpdate-'+this.props.datasource.did, this.subscriptionHandler),msg:'snapshotDsDataUpdate-'+this.props.datasource.did});
    },
    componentDidMount: function () {
        PubSub.publish('snapshotDsDataReq',{did:this.props.datasource.did,tid:this.props.tid,seq:this.props.seq})
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens[this.props.nid], function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.nid];
    },
    componentWillReceiveProps: function (nextProps) {
        if (nextProps.downloadCounter>this.state.downloadCounter) {
            this.downloadContent();
            this.setState({downloadCounter:nextProps.downloadCounter});
        }
    },
    refreshData: function () {
        if (datasourceStore._snapshotDsData.hasOwnProperty(this.props.datasource.did)) {
            datasourceData=datasourceStore._snapshotDsData[this.props.datasource.did]
            if (!this.state.dsData && datasourceData.hasOwnProperty(this.props.seq)) {
                this.setState({dsData:datasourceData[this.props.seq],timestamp:datasourceData[this.props.seq].ts})
            }
        }
    },
    downloadContent: function () {
        if (this.state.dsData.content && this.state.dsData.content.length>0) {
            downloadFile(this.props.datasource.datasourcename+'.txt',this.state.dsData.content,'text/plain')
        }
    },
    getDsInfo: function (timestamp) {
        if (typeof timestamp === 'number') {
            var dateFormat = d3.time.format("%Y/%m/%d - %H:%M:%S")
            var date = new Date(timestamp*1000);
            dateText=dateFormat(date)
            return React.createElement('div', {className: "ds-info"}, dateText);
        } else {
            return null
        }
    },
    generateHtmlContent: function (dsData) {
        var elements=[]
        if (!dsData) {
            return elements
        }
        var numElement = 0
        var cursorPosition=0
        var newLineRegex=/(?:\r\n|\r|\n)/g
        for (var i=0;i<dsData.variables.length;i++) {
            var position=dsData.variables[i][0]
            var length=dsData.variables[i][1]
            var dsSubContent=dsData.content.substr(cursorPosition,position-cursorPosition)
            var start=0
            while((match=newLineRegex.exec(dsSubContent)) != null) {
                var text=dsSubContent.substr(start,match.index-start).replace(/ /g, '\u00a0');
                elements.push({ne:numElement++,type:'text',data:text});
                elements.push({ne:numElement++,type:'nl'});
                start=match.index+match.length-1
            }
            if (start<position) {
                text=dsSubContent.substr(start,position-start).replace(/ /g, '\u00a0');
                elements.push({ne:numElement++,type:'text',data:text});
            }
            var datapointFound=false;
            for (var j=0;j<dsData.datapoints.length;j++) {
                if (dsData.datapoints[j].index == dsData.variables[i][0]) {
                    datapointFound=true
                    text=dsData.content.substr(position,length)
                    var color='black'
                    var datapointname=''
                    for (var k=0;k<this.props.datapoints.length;k++) {
                        if (this.props.datapoints[k].pid == dsData.datapoints[j].pid) {
                            datapointname=this.props.datapoints[k].datapointname
                            color=this.props.datapoints[k].color
                            break;
                        }
                    }
                    elements.push({ne:numElement++,type:'datapoint',pid:dsData.datapoints[j].pid,p:position,l:length,style:{color:color},data:text,datapointname:datapointname})
                    break;
                }
            }
            if (datapointFound == false) {
                text=dsData.content.substr(position,length)
                elements.push({ne:numElement++,type:'text',data:text});
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
        console.log('datos del snapshot',this.state.dsData)
        console.log('datos de props',this.props.datapoints)
        elements=this.generateHtmlContent(this.state.dsData)
        var element_nodes=$.map(elements, function (element) {
            if (element.type == 'text') {
                return React.createElement('span', {key:element.ne},element.data);
            }else if (element.type == 'nl') {
                return React.createElement('br', {key:element.ne});
            }else if (element.type == 'datapoint') {
                tooltip=React.createElement(ReactBootstrap.Tooltip, {id:'datapoint'}, element.datapointname);
                return React.createElement(ReactBootstrap.OverlayTrigger, {placement:"top", overlay:tooltip},
                         React.createElement('span', {key:element.ne, style:element.style}, element.data)
                       );
            }
        }.bind(this));
        info_node=this.getDsInfo(this.state.timestamp)
        return React.createElement('div', null,
                 info_node,
                 React.createElement('div',{className: 'ds-content'}, element_nodes)
               );
    }
});

var SnapshotDp = React.createClass({
    getInitialState: function () {
        return {
                interval: {its:this.props.its,ets:this.props.ets},
                data: [],
                summary: {},
                downloadCounter:this.props.downloadCounter,
                activeVis: 0,
            }
    },
    subscriptionTokens: {},
    componentWillMount: function () {
        this.subscriptionTokens[this.props.nid]=[]
        this.subscriptionTokens[this.props.nid].push({token:PubSub.subscribe('datapointDataUpdate-'+this.props.datapoint.pid, this.subscriptionHandler),msg:'datapointDataUpdate-'+this.props.datapoint.pid});
    },
    componentDidMount: function () {
        PubSub.publish('datapointDataReq',{pid:this.props.datapoint.pid, interval:this.state.interval, tid:this.props.tid})
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens[this.props.nid], function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.nid];
    },
    componentWillReceiveProps: function (nextProps) {
        if (nextProps.downloadCounter>this.state.downloadCounter) {
            this.downloadContent();
            this.setState({downloadCounter:nextProps.downloadCounter});
        }
    },
    selectVis: function (event) {
        event.preventDefault();
        buttonId=parseInt(event.target.id)
        if (this.state.activeVis != buttonId) {
            this.setState({activeVis:buttonId})
        }
    },
    downloadContent: function () {
        if (this.state.data.length>0) {
            csv="date,"+this.props.datapoint.datapointname+"\n"
            $.map(this.state.data, function (r,i) {
                csv+=new Date(r.ts*1000).toISOString()+','+r.value+"\n"
            });
            downloadFile(this.props.datapoint.datapointname+'.csv',csv,'text/csv')
        } else {
            this.props.barMessageCallback({message:{type:'info',message:'No data in selected interval'},messageTime:(new Date).getTime()});
        }
    },
    newIntervalCallback: function (interval) {
        if (interval.hasOwnProperty('its') && interval.hasOwnProperty('ets')) {
            if (interval.its<this.props.its) {
                interval.its=this.props.its
            }
            if (interval.ets>this.props.ets) {
                interval.ets=this.props.ets
            }
            if (interval.its == interval.ets) {
                interval.its=interval.ets-3600
            }
            PubSub.publish('datapointDataReq',{pid:this.props.datapoint.pid,interval:interval,tid:this.props.tid})
            this.refreshData(interval);
        }
    },
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'datapointDataUpdate-'+this.props.datapoint.pid:
                if ((this.state.interval.its <= data.interval.its && data.interval.its <= this.state.interval.ets) ||
                           (this.state.interval.its <= data.interval.ets && data.interval.ets <= this.state.interval.ets)) {
                    this.refreshData(this.state.interval)
                }
                break;
        }
    },
    refreshData: function (interval) {
        newData=getIntervalData(this.props.datapoint.pid, interval)
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
            summary={'max':d3.format(",")(maxValue),'min':d3.format(",")(minValue),'datapointname':this.props.datapoint.datapointname,'mean':d3.format(",")(meanValue),'color':this.props.datapoint.color}
        } else {
            summary={'max':0,'min':0,'datapointname':this.props.datapoint.datapointname,'mean':0}
        }
        return summary
    },
    render: function () {
        if (this.state.summary.hasOwnProperty('datapointname')){
            var summary=React.createElement('tr', null,
                React.createElement('td', null,
                  React.createElement('span', {style:{backgroundColor: this.state.summary.color, borderRadius: '5px'}}, '\u00a0\u00a0\u00a0'),
                  React.createElement('span', null, '\u00a0\u00a0'),
                  React.createElement('span', null,this.state.summary.datapointname)
                ),
                React.createElement('td', null, this.state.summary.max),
                React.createElement('td', null, this.state.summary.min),
                React.createElement('td', null, this.state.summary.mean)
            );
        } else {
            var summary=React.createElement('tr', null,
                React.createElement('td', null),
                React.createElement('td', null),
                React.createElement('td', null),
                React.createElement('td', null)
            );
        }
        var data=[{pid:this.props.datapoint.pid,color:this.props.datapoint.color,datapointname:this.props.datapoint.datapointname,data:this.state.data}]
        var visContent=this.state.activeVis == 0 ?  React.createElement(ContentLinegraph, {interval:this.state.interval, data:data, newIntervalCallback:this.newIntervalCallback}) : 
            this.state.activeVis == 1 ? React.createElement(ContentHistogram, {data:data}) :
            null;
        return React.createElement('div', null,
            React.createElement('div', {className:"dp-stats"},
              React.createElement('table', {className:"table-condensed"},
                React.createElement('tbody', null,
                  React.createElement('tr', null,
                    React.createElement('th',null,""),
                    React.createElement('th',null,"max"),
                    React.createElement('th',null,"min"),
                    React.createElement('th',null,"mean")
                  ),
                  summary
                )
              )
            ),
            React.createElement('div', {className:"row visual-bar"},
              React.createElement('div', {className:"col-md-5 text-center"},
                React.createElement(ReactBootstrap.ButtonGroup, {bsSize:"xsmall"},
                  React.createElement(ReactBootstrap.Button, {id:"0", active:this.state.activeVis == 0 ? true : false, onClick: this.selectVis },"chart"),
                  React.createElement(ReactBootstrap.Button, {id:"1", active:this.state.activeVis == 1 ? true : false, onClick: this.selectVis },"histogram")
                )
              ),
              React.createElement('div', {className:"col-md-7"},
                React.createElement(TimeSlider, {interval:this.state.interval, newIntervalCallback:this.newIntervalCallback})
              )
            ),
            React.createElement('div', {className:"row"},
              React.createElement('div', {className:"col-md-12"}, visContent)
            )
        );
    }
});

var SnapshotMp = React.createClass({
    getInitialState: function () {
        return {
                interval: {its:this.props.its,ets:this.props.ets},
                data: {},
                config: {},
                activeVis: this.props.view,
                downloadCounter: this.props.downloadCounter,
        }
    },
    subscriptionTokens: {},
    componentWillMount: function () {
        this.subscriptionTokens[this.props.nid]=[]
        for (var i=0;i<this.props.datapoints.length;i++) {
            this.subscriptionTokens[this.props.nid].push({token:PubSub.subscribe('datapointDataUpdate-'+this.props.datapoints[i].pid, this.subscriptionHandler),msg:'datapointDataUpdate-'+this.props.datapoints[i].pid});
        }
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens[this.props.nid], function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.props.nid];
    },
    componentDidMount: function () {
        for (var i=0;i<this.props.datapoints.length;i++) {
            PubSub.publish('datapointDataReq',{pid:this.props.datapoints[i].pid,interval:this.state.interval,tid:this.props.tid})
        }
    },
    componentWillReceiveProps: function (nextProps) {
        if (nextProps.downloadCounter>this.state.downloadCounter) {
            this.downloadContent();
            this.setState({downloadCounter:nextProps.downloadCounter});
        }
    },
    selectVis: function (event) {
        event.preventDefault();
        buttonId=parseInt(event.target.id)
        if (this.state.activeVis != buttonId) {
            this.setState({activeVis:buttonId})
        }
    },
    downloadContent: function () {
        if (Object.keys(this.state.data).length>0) {
            x={}
            x_final=[]
            y_final=[]
            for (var i=0;i<this.props.datapoints.length;i++) {
                pid=this.props.datapoints[i].pid
                y={}
                if (pid in this.state.data) {
                    for (var j=0;j<this.state.data[pid].length;j++) {
                        x[this.state.data[pid][j].ts]=0
                        y[this.state.data[pid][j].ts]=this.state.data[pid][j].value
                    }
                    y_final.push(y)
                }
            }
            for (var prop in x) {
                x_final.push(prop)
            }
            x_final.sort(function (a,b) {return a-b})
            if (x_final.length>0) {
                csv="date"
                for (var i=0;i<this.props.datapoints.length;i++) {
                    csv+=","+this.props.datapoints[i].datapointname
                }
                csv+="\n"
                for (var i=0;i<x_final.length;i++) {
                    line=new Date(x_final[i]*1000).toISOString();
                    for (var j=0;j<y_final.length;j++) {
                        value=( x_final[i] in y_final[j]) ? y_final[j][x_final[i]] : null
                        line+=value != null ? ","+value : ","
                    }
                    csv+=line+"\n"
                }
                downloadFile(this.props.widgetname+'.csv',csv,'text/csv')
            } else {
                this.props.barMessageCallback({message:{type:'info',message:'No data in selected interval'},messageTime:(new Date).getTime()});
            }
        } else {
            this.props.barMessageCallback({message:{type:'danger',message:'No datapoints in graph'},messageTime:(new Date).getTime()});
        }
    },
    newIntervalCallback: function (interval) {
        if (interval.hasOwnProperty('its') && interval.hasOwnProperty('ets')) {
            if (interval.its<this.props.its) {
                interval.its=this.props.its
            }
            if (interval.ets>this.props.ets) {
                interval.ets=this.props.ets
            }
            if (interval.its == interval.ets) {
                interval.its=interval.ets-3600
            }
            for (var i=0;i<this.props.datapoints.length;i++) {
                PubSub.publish('datapointDataReq',{pid:this.props.datapoints[i].pid,interval:interval,tid:this.props.tid})
            }
            this.refreshData(interval);
        }
    },
    subscriptionHandler: function (msg,data) {
        msgType=msg.split('-')[0]
        switch (msgType) {
            case 'datapointDataUpdate':
                pid=msg.split('-')[1]
                if ((this.state.interval.its <= data.interval.its && data.interval.its <= this.state.interval.ets) ||
                           (this.state.interval.its <= data.interval.ets && data.interval.ets <= this.state.interval.ets)) {
                    this.refreshData(this.state.interval, pid)
                }
                break;
        }
    },
    refreshData: function (interval, pid) {
        if (pid) {
            selectedPids=[pid]
        } else {
            selectedPids=$.map(this.props.datapoints, function (d) {return d.pid})
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
            var color=null;
            var datapointname=null;
            for (var i=0;i<this.props.datapoints.length;i++) {
                if (this.props.datapoints[i].pid==key) {
                    color=this.props.datapoints[i].color;
                    datapointname=this.props.datapoints[i].datapointname;
                    break;
                }
            }
            if (datapointname !== null) {
                var dpSummary=getDataSummary(element)
                var datapointStyle={backgroundColor: color, borderRadius: '5px'}
                return React.createElement('tr', {key:key},
                         React.createElement('td', null,
                           React.createElement('span',{style:datapointStyle},"\u00a0\u00a0\u00a0"),
                           React.createElement('span',null,"\u00a0\u00a0"),
                           React.createElement('span', null, datapointname)
                         ),
                         React.createElement('td', null, dpSummary.max),
                         React.createElement('td', null, dpSummary.min),
                         React.createElement('td', null, dpSummary.mean)
                       );
            }
        }.bind(this));
        var data=$.map(this.state.data, function (element, key) {
            color=null;
            datapointname=null;
            for (var i=0;i<this.props.datapoints.length;i++) {
                if (this.props.datapoints[i].pid==key) {
                    color=this.props.datapoints[i].color;
                    datapointname=this.props.datapoints[i].datapointname;
                    break;
                }
            }
            if (datapointname !== null) {
                return {pid:key,color:color,datapointname:datapointname,data:element}
            }
        }.bind(this));
        var visContent=this.state.activeVis == 0 ?  React.createElement(ContentLinegraph, {interval:this.state.interval, data:data, newIntervalCallback:this.newIntervalCallback}) : 
            this.state.activeVis == 1 ? React.createElement(ContentHistogram, {data:data}) :
            null;
        return React.createElement('div', null,
            React.createElement('div', {className:"dp-stats"},
              React.createElement('table', {className:"table-condensed"},
                React.createElement('tbody', null,
                  React.createElement('tr', null,
                    React.createElement('th',null,""),
                    React.createElement('th',null,"max"),
                    React.createElement('th',null,"min"),
                    React.createElement('th',null,"mean")
                  ),
                  summary
                )
              )
            ),
            React.createElement('div', {className:"row visual-bar"},
              React.createElement('div', {className:"col-md-5 text-center"},
                React.createElement(ReactBootstrap.ButtonGroup, {bsSize:"xsmall"},
                  React.createElement(ReactBootstrap.Button, {id:"0", active:this.state.activeVis == 0 ? true : false, onClick: this.selectVis },"chart"),
                  React.createElement(ReactBootstrap.Button, {id:"1", active:this.state.activeVis == 1 ? true : false, onClick: this.selectVis },"histogram")
                )
              ),
              React.createElement('div', {className:"col-md-7"},
                React.createElement(TimeSlider, {interval:this.state.interval, newIntervalCallback:this.newIntervalCallback})
              )
            ),
            React.createElement('div', {className:"row"},
              React.createElement('div', {className:"col-md-12"}, visContent)
            )
       );
    }
});

