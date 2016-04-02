function ShellStore () {
    this._shortcuts = [];
    this.subscriptionTokens = [];
    this.subscriptionTokens.push({token:PubSub.subscribe('processCommand', this.subscriptionHandler.bind(this)),msg:'processCommand'});
}

ShellStore.prototype = {
    subscriptionHandler: function (msg, data) {
        switch (msg) {
            case 'processCommand':
                this.processCommand(data.commandline)
                break;
        }
    },
    parse: function (commandLine) {
        commandArray=$.grep(commandLine.split(' '), function (e) {return e!=''})
        command={}
        lastOption=''
        for (var i=0;i<commandArray.length;i++) {
            if (i==0){
                command.command=commandArray[i]
            } else if (i==1) {
                command.subcommand=commandArray[i]
            } else {
                if (commandArray[i].charAt(0)=='-') {
                    if (commandArray[i].charAt(1)=='-'){
                        lastOption=commandArray[i].slice(2)
                        command[lastOption]=''
                    } else {
                        lastOption=commandArray[i].slice(1)
                        command[lastOption]=''
                    }
                }
                else {
                    if (lastOption!='') {
                        if (command[lastOption]=='') {
                        command[lastOption]=commandArray[i]
                        } else {
                            command[lastOption]+=' '+commandArray[i]
                        }
                    }
                }
            }
        }
        console.log(command)
        return command
    },
    processCommand: function (commandLine) {
        command = this.parse(commandLine)
        switch (command.command) {
            case 'slide':
                commandSlide(command)
                break;
            default:
                console.log('error',command)
                break;
        }
    },
}

var shellStore = new ShellStore();

function commandSlide(command) {
    console.log('command slide',command)
    switch(command.subcommand) {
        case 'new':
            commandSlideNew(command)
            break;
        case 'modify':
            commandSlideModify(command)
            break;
        case 'delete':
            commandSlideDelete(command)
            break;
        case 'close':
            commandSlideClose(command)
            break;
        case 'open':
            commandSlideOpen(command)
            break;
        case 'interval':
            commandSlideInterval(command)
            break;
        default:
            console.log('error',command)
            break;
    }
}

function commandSlideNew(command) {
    console.log('requesting new slide')
    ALLOWEDTYPES=['hg','lg','tb']
    if (command.hasOwnProperty('help')) {
        console.log('Help Menu: ....')
    } else if (!command.hasOwnProperty('type')) {
        console.log('errorMessage',{message:'missing mandatory "type" option. Type slide new --help for help'})
    } else if ($.inArray(command.type, ALLOWEDTYPES)==-1) {
        console.log('errorMessage',{message:'Invalid "type" option. Type slide new --help for help'})
    } else if (!command.hasOwnProperty('name')) {
        console.log('errorMessage',{message:'missing mandatory "name" option. Type slide new --help for help'})
    } else {
        PubSub.publish('newSlide',{type:command.type,widgetname:command.name})
    }
}

function commandSlideModify(command) {
    console.log('executing slide modify')
    msgData={}
    if (command.hasOwnProperty('help')) {
        console.log('Help Menu: ....')
        return
    }
    if (!command.hasOwnProperty('id')) {
        console.log('Missing mandatory "id" option. Type slide modify --help')
        return
    } else {
        msgData.lid=command.id
    }
    if (command.hasOwnProperty('name')) {
        msgData.new_widgetname=command.name
    }
    if (command.hasOwnProperty('add')) {
        new_datapoints=$.grep(command.add.split(','), function (e) {return e!=''}).map(function (d) {return d.replace(/^\s+|\s+$/g,'');})
        msgData.new_datapoints=new_datapoints
    }
    if (command.hasOwnProperty('delete')) {
        delete_datapoints=$.grep(command.delete.split(','), function (e) {return e!=''}).map(function (d) {return d.replace(/^\s+|\s+$/g,'');})
        msgData.delete_datapoints=delete_datapoints
    }
    if (!msgData.hasOwnProperty('new_widgetname') && !msgData.hasOwnProperty('new_datapoints') && !msgData.hasOwnProperty('delete_datapoints')) {
        console.log('command with no options. Type slide modify --help')
    } else {
        console.log('requesting modifySlide', msgData)
        PubSub.publish('modifySlide',msgData)
    }
}

function commandSlideDelete(command) {
    console.log('init slide delete...',command)
    if (command.hasOwnProperty('help')) {
        console.log('Help Menu....')
    } else if (command.hasOwnProperty('id')) {
        PubSub.publish('deleteSlide',{lid:command.id})
    } else {
        console.log('missing mandatory "id" parameter. Type slide delete --help')
    }
}

function commandSlideClose(command) {
    console.log('init slide close...',command)
    if (command.hasOwnProperty('help')) {
        console.log('Help Menu....')
    } else if (command.hasOwnProperty('id')) {
        PubSub.publish('closeSlide',{lid:command.id})
    } else {
        console.log('missing mandatory "id" parameter. Type slide hide --help')
    }
}

function commandSlideOpen(command) {
    console.log('init slide open...',command)
    if (command.hasOwnProperty('help')) {
        console.log('Help Menu....')
    } else if (command.hasOwnProperty('wid')) {
        PubSub.publish('loadSlide',{wid:command.wid})
    } else {
        console.log('missing mandatory "wid" parameter. Type slide show --help')
    }
}

function commandSlideInterval(command) {
    console.log('init slide interval...',command)
    if (command.hasOwnProperty('help')) {
        console.log('Help Menu....')
    } else if (command.hasOwnProperty('id')) {
        interval={its:undefined, ets:undefined}
        console.log('vamos a enviar','intervalUpdate-'+command.id)
        if (command.hasOwnProperty('its') || command.hasOwnProperty('ets')) {
            interval={its:command.its, ets:command.ets}
        } else if (command.hasOwnProperty('init') || command.hasOwnProperty('end')) {
            if (Date.parse(command.init)!=NaN) {
                interval.its=Date.parse(command.init)/1000
            }
            if (Date.parse(command.end)!=NaN) {
                interval.ets=Date.parse(command.end)/1000
            }
        } else if (command.hasOwnProperty('lh')) {
            interval.ets=new Date().getTime()/1000;
            if (!command.lh == '' && !isNaN(command.lh)) {
                console.log('es un numero',command.lh)
                interval.its=interval.ets-3600*command.lh
            } else {
                console.log('no es un numero')
                interval.its=interval.ets-3600
            }
            console.log(interval)
        } else if (command.hasOwnProperty('ld')) {
            interval.ets=new Date().getTime()/1000;
            if (!command.ld == '' && !isNaN(command.ld)) {
                console.log('es un numero',command.ld)
                interval.its=interval.ets-3600*24*command.ld
            } else {
                console.log('no es un numero')
                interval.its=interval.ets-3600*24
            }
            console.log(interval)
        } else if (command.hasOwnProperty('lw')) {
            interval.ets=new Date().getTime()/1000;
            if (!command.lw == '' && !isNaN(command.lw)) {
                interval.its=interval.ets-3600*24*7*command.lw
            } else {
                interval.its=interval.ets-3600*24*7
            }
        } else if (command.hasOwnProperty('lm')) {
            interval.ets=new Date().getTime()/1000;
            if (!command.lm == '' && !isNaN(command.lm)) {
                interval.its=interval.ets-3600*24*31*command.lm
            } else {
                interval.its=interval.ets-3600*24*31
            }
        } else if (command.hasOwnProperty('ly')) {
            interval.ets=new Date().getTime()/1000;
            if (!command.ly == '' && !isNaN(command.ly)) {
                interval.its=interval.ets-3600*24*356*command.ly
            } else {
                interval.its=interval.ets-3600*24*356
            }
        } else {
            console.log('bad parameters. type slide interval --help')
            return
        }
        PubSub.publish('intervalUpdate-'+command.id,{interval:{its:interval.its,ets:interval.ets}})
    } else {
        console.log('missing mandatory "id" parameter. Type slide interval --help')
    }
}

function commandSlideShare(command) {
}

