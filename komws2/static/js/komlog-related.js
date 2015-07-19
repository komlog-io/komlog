var RelatedSlides = React.createClass({
    getInitialState: function () {
        return {slides:[]}
    },
    subscriptionTokens: [],
    componentWillMount: function () {
        this.subscriptionTokens.push({token:PubSub.subscribe('showSlidesRelated', this.subscriptionHandler),msg:'showSlidesRelated'});
    },
    componentDidMount: function () {
        this.refreshSlides()
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens, function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
    },
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case 'showSlidesRelated':
                this.refreshSlides(data.lid)
                break;
        }
    },
    handleClick: function (wid) {
        PubSub.publish('loadSlide',{wid:wid})
    },
    refreshSlides: function (lid) {
        if (typeof lid != "undefined") {
            newSlides=getSlidesRelated(lid)
            for (var i=0; i<this.state.slides.length;i++) {
                addSlide=true
                for (var j=newSlides.length;j>0;j--) {
                    if (this.state.slides[i].wid==newSlides[j-1].wid) {
                        addSlide=false
                        break;
                    }
                }
                if (addSlide) {
                    slide=$.grep(slideStore._slidesLoaded, function (e) {return e.lid == this.state.slides[i].wid}.bind(this))
                    if (slide.length==0) {
                        newSlides.push(this.state.slides[i])
                    }
                }
            }
            this.setState({slides:newSlides})
        }
    },
    render: function () {
        related = $.map(this.state.slides, function (d,i) {
            return (
                      <li key={d.wid} onClick={this.handleClick.bind(null,d.wid)}>
                        <div className="sliderelated-panel">{d.widgetname}</div>
                        <div className="sliderelated-badge">
                          <i className={d.className} />
                        </div>
                      </li>
                   )
        }.bind(this));
        return (<ul className="sliderelated">
                { related }
                </ul>);
    }
});

React.render(
    <RelatedSlides />
    ,
    document.getElementById('related-slides')
);

