var Alert = React.createClass({
    propTypes: {
      type: React.PropTypes.string,
      message: React.PropTypes.string,
      autoCloseable: React.PropTypes.bool,
      messageTime: React.PropTypes.number
    },
    getDefaultProps: function () {
        return {
            closeLabel: "Close",
            autoCloseable: true,
        }
    },
    getInitialState: function () {
        return {
            type:this.props.type,
            message:this.props.message,
            messageTime:0
        }
    },
    componentWillUnmount: function () {
        clearTimeout(this.dismissTimer)
    },
    componentDidMount: function () {
        if (this.props.autoCloseable) {
            this.dismissTimer = setTimeout(this.dismiss, 3000);
        }
    },
    componentWillReceiveProps: function (nextProps) {
        if (nextProps.messageTime>this.state.messageTime) {
            clearTimeout(this.dismissTimer);
            if (nextProps.autoCloseable == true) {
                this.dismissTimer = setTimeout(this.dismiss, 3000);
            }
            this.setState({message:nextProps.message, type:nextProps.type, messageTime:nextProps.messageTime})
        }
    },
    dismiss: function () {
        clearTimeout(this.dismissTimer)
        this.setState({message:null,type:null})
    },
    render: function () {
        if (this.state.message != null) {
            var alertInstance = React.createElement(ReactBootstrap.Alert, { className:this.props.className, style:this.props.style, bsStyle:this.state.type},this.state.message);
        } else {
            var alertInstance = React.createElement('div', {className:this.props.className, style:this.props.style});
        }
        return alertInstance
    },
});

var AlertArea = React.createClass({
    propTypes: {
      address: React.PropTypes.string,
    },
    getDefaultProps: function () {
        return {
            address: null,
        }
    },
    getInitialState: function () {
        return {
            topic:this.props.address !== null ? 'barMessage.'+this.props.address : 'barMessage',
            message: null,
            type: null,
            messageTime: 0
        }
    },
    subscriptionTokens: {},
    subscriptionHandler: function (msg,data) {
        switch (msg) {
            case this.state.topic:
                this.barMessage(data)
                break;
        }
    },
    componentWillMount: function () {
        this.subscriptionTokens[this.state.topic]=[]
        this.subscriptionTokens[this.state.topic].push({token:PubSub.subscribe(this.state.topic, this.subscriptionHandler),msg:this.state.topic});
    },
    componentWillUnmount: function () {
        $.map(this.subscriptionTokens[this.state.topic], function (d) {
            PubSub.unsubscribe(d.token)
            }.bind(this));
        delete this.subscriptionTokens[this.state.topic];
    },
    barMessage: function (data) {
        if ('messageTime' in data) {
            console.log('estableciendo nuevo mensaje')
            this.setState({message:data.message.message, type:data.message.type, messageTime:data.messageTime});
        }
    },
    render: function () {
        message = this.state.message !== null ? React.createElement(Alert, {type:this.state.type,message:this.state.message, messageTime:this.state.messageTime}) : null;
        return React.createElement('div', {style:this.props.style, className:this.props.className}, message);
    },
});

ReactDOM.render(
    React.createElement(AlertArea, {className:'alert-area'})
    ,
    document.getElementById('alert-area')
);
