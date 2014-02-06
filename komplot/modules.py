#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os.path
import uuid
import sections, options
from datetime import datetime,timedelta
from komcass import api as cassapi
from komcass import connection as casscon
from komapp import modules
from komfig import komlogger
from komimc import bus,messages
from komimc import codes as msgcodes

class Plotter(modules.Module):
    def __init__(self, config, instance_number):
        super(Plotter,self).__init__(config, self.__class__.__name__, instance_number)
        self.params={}
        self.params['cass_keyspace'] = self.config.safe_get(sections.PLOTTER,options.CASS_KEYSPACE)
        self.params['cass_servlist'] = self.config.safe_get(sections.PLOTTER,options.CASS_SERVLIST).split(',')
        try:
            self.params['cass_poolsize'] = int(self.config.safe_get(sections.PLOTTER,options.CASS_POOLSIZE))
        except Exception:
            self.logger.error('Invalid '+options.CASS_POOLSIZE+'value: setting default (5)')
            self.params['cass_poolsize'] = 5
        self.params['broker'] = self.config.safe_get(sections.PLOTTER, options.MESSAGE_BROKER)
        if not self.params['broker']:
            self.params['broker'] = self.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)
        self.params['plot_dest_dir']=self.config.safe_get(sections.PLOTTER, options.PLOT_DEST_DIR)

    def start(self):
        self.logger = komlogger.getLogger(self.config.conf_file, self.name)
        self.logger.info('Plotter module started')
        if not self.params['cass_keyspace'] or not self.params['cass_poolsize'] or not self.params['cass_servlist']:
            self.logger.error('Cassandra connection configuration keys not found')
        elif not self.params['broker']:
            self.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        elif not self.params['plot_dest_dir']:
            self.logger.error('Key '+options.PLOT_DEST_DIR+' not found')
        else:
            self.cass_pool = casscon.Pool(keyspace=self.params['cass_keyspace'], server_list=self.params['cass_servlist'], pool_size=self.params['cass_poolsize'])
            self.cf = casscon.CF(self.cass_pool)
            self.message_bus = bus.MessageBus(self.params['broker'], self.name, self.instance_number, self.hostname, self.logger)
            self.__loop()
        self.logger.info('Plotter module exiting')
    
    def __loop(self):
        while True:
            message = self.message_bus.retrieveMessage(from_modaddr=True)
            self.message_bus.ackMessage()
            mtype=message.type
            try:
                msgresult=getattr(self,'process_msg_'+mtype)(message)
                messages.process_msg_result(msgresult,self.message_bus,self.logger)
            except AttributeError:
                self.logger.exception('Exception processing message: '+mtype)
            except Exception as e:
                self.logger.exception('Exception processing message: '+str(e))

    def process_msg_PLTSTO(self, message):
        '''
        Almacena un png con el plot del grafico.
        Los pasos son los siguientes:
        - Obtenemos la info del grafico
        - extraemos las variables que contiene, y los datos de un periodo determinado.
        - generamos la matriz de datos
        - generamos el plot
        - Almacenamos el contenido como png
        '''
        msgresult=messages.MessageResult(message)
        gid=message.gid
        init_date=message.init_date
        end_date=message.end_date
        graphinfo=cassapi.get_graphinfo(gid,self.cf)
        if not graphinfo:
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        if not end_date:
            end_date=datetime.utcnow()
        if not init_date:
            ''' por defecto traemos 12 horas '''
            init_date=end_date-timedelta(hours=12)
        graphdtp=graphinfo.get_datapoints()
        dates={}
        dtpinfo={}
        dtpdata={}
        for pid in graphdtp:
            dtpinfo[pid]=graphinfo.get_datapoint_info(pid)
            dtpdataarray=cassapi.get_datapointdata(pid,self.cf,fromdate=init_date,todate=end_date,reverse=True) 
            dtpdata[pid]={}
            for dtpdataobj in dtpdataarray:
                dates[dtpdataobj.date]=''
                dtpdata[pid][dtpdataobj.date]=dtpdataobj.content
        dates=dates.keys()
        dates.sort()
        pids=graphdtp
        pids.sort()
        legends=[]
        colors=[]
        for pid in pids:
            legends.append(dtpinfo[pid]['name'])
            colors.append(dtpinfo[pid]['color'])
        matrix=np.zeros((len(dates),len(pids)))
        matrix[:]=np.nan
        rows,cols=matrix.shape
        for row in range(rows):
            for col in range(cols):
                date=dates[row]
                pid=pids[col]
                try:
                    matrix[row][col]=dtpdata[pid][date]
                except KeyError:
                    pass
        dateFmt = mdates.DateFormatter('%H:%M')
        fig=plt.figure(figsize=(3.2, 0.9), dpi=100)
        fig.suptitle(graphinfo.name, fontsize=8, fontweight='bold')
        ax=fig.add_subplot(111)
        p1=ax.plot(dates,matrix,label=legends)
        for i,line in enumerate(p1):
            line.set_color(colors[i])
        ax.xaxis.set_major_formatter(dateFmt)
        plt.subplots_adjust(top=0.85)
        plt.setp(ax.get_xticklabels(), fontsize=5)
        plt.setp(ax.get_yticklabels(), fontsize=6)
        if len(legends)<4:
            leg=plt.legend(p1,legends,loc=2,prop={'size':6})
            leg.get_frame().set_alpha(0.5)
        plt.gcf().autofmt_xdate()
        plt.savefig(os.path.join(self.params['plot_dest_dir'],str(gid)))
        msgresult.retcode=msgcodes.SUCCESS
        return msgresult

