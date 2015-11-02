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
                tid=data.tid
                for (var i=0; i<this.state.slides.length;i++) {
                    if (this.state.slides[i].lid==lid) {
                        slideExists=true
                        break;
                    }
                }
                if (slideExists==false && lid) {
                    slide={lid:lid,tid:tid,shortcut:this.shortcutCounter++,type:type}
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
        slides = this.state.slides.map( function (slide) {
            return (<Slide key={slide.shortcut} lid={slide.lid} tid={slide.tid} shortcut={slide.shortcut} type={slide.type}/>)
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
        return {
                conf:{},
                shareCounter: 0,
                }
    },
    closeCallback: function() {
        PubSub.publish('closeSlide',{lid:this.props.lid})
    },
    getSlideEl: function () {
        switch (this.props.type) {
            case 'wid':
                return (
                  <Widget closeCallback={this.closeCallback} wid={this.props.lid}/>
                    );
                break;
            case 'nid':
                return (
                  <Snapshot closeCallback={this.closeCallback} nid={this.props.lid} tid={this.props.tid}/>
                    );
                break;
            default:
                return null;
                break;
        }
    },
    render: function() {
        slide=this.getSlideEl();
        return (
        <div className="Slide modal-container" style={this.styles.slidestyle} >
          {slide}
        </div>
        );
    },
});

React.render(
    <Workspace />
    ,
    document.getElementById('workspace-content')
);

