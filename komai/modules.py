import sections, options
import re
import json
from komcass import api as cassapi
from komcass import connection as casscon
from komapp import modules
from komfig import komlogger
from komimc import bus,messages
        

FLOAT_REGEXP=u'[-+]?[0-9]*[\.,]?[0-9]+'
VAR_SEPARATORS=(u' ',u';',u'\n',u'\t')
VAR_SUFIX=(u'%')

class Textmining(modules.Module):
    def __init__(self, config, instance_number):
        super(Textmining,self).__init__(config, self.__class__.__name__, instance_number)
        self.cass_keyspace = self.config.safe_get(sections.TEXTMINING,options.CASS_KEYSPACE)
        self.cass_servlist = self.config.safe_get(sections.TEXTMINING,options.CASS_SERVLIST).split(',')
        try:
            self.cass_poolsize = int(self.config.safe_get(sections.TEXTMINING,options.CASS_POOLSIZE))
        except Exception:
            self.logger.error('Invalid '+options.CASS_POOLSIZE+'value: setting default (5)')
            self.cass_poolsize = 5
        self.broker = self.config.safe_get(sections.TEXTMINING, options.MESSAGE_BROKER)
        if not self.broker:
            self.broker = self.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)

    def start(self):
        self.logger = komlogger.getLogger(self.config.conf_file, self.name)
        self.logger.info('Textmining module started')
        if not self.cass_keyspace or not self.cass_poolsize or not self.cass_servlist:
            self.logger.error('Cassandra connection configuration keys not found')
        elif not self.broker:
            self.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        else:
            self.cass_pool = casscon.Pool(keyspace=self.cass_keyspace, server_list=self.cass_servlist, pool_size=self.cass_poolsize)
            self.samples_cf = casscon.SamplesCF(self.cass_pool.connection_pool)
            self.samplemap_cf = casscon.SampleMapCF(self.cass_pool.connection_pool)
            self.message_bus = bus.MessageBus(self.broker, self.name, self.instance_number, self.hostname, self.logger)
            self.__loop()
        self.logger.info('Textmining module exiting')
    
    def __loop(self):
        while True:
            message = self.message_bus.retrieveMessage(from_modaddr=True)
            self.message_bus.ackMessage()
            mtype=message.type
            if mtype==messages.MAP_VARS_MESSAGE:
                if self.process_MAP_VARS_MESSAGE(message):
                    self.logger.debug('Mesage completed successfully: '+mtype)
                    pass
            else:
                self.logger.error('Message Type not supported: '+mtype)
                self.message_bus.sendMessage(message)
    
    def process_MAP_VARS_MESSAGE(self, message):
        sid=message.sid
        varlist=[]
        sample=cassapi.get_sample(sid, self.samples_cf)
        if not sample==None:
            sample_content=sample.content
            varlist = getVarList(sample_content)
            calculateVarMatrix(varlist,sample_content)
            vardict={}
            for var in varlist:
                key=str(var.start)+':'+str(var.length)
                content=var.__dict__
                content.pop('start')
                content.pop('length')
                vardict[key]=json.dumps(content)
            try:
                cassapi.create_sample_map(sid, vardict, self.samplemap_cf)
                self.logger.debug('SampleMap create for sid: '+str(sid))
                return True
            except Exception as e:
                #rollback
                self.logger.exception('Exception creating SampleMap for sid '+str(sid)+' '+str(e))
                try:
                    cassapi.remove_sample_map(sid, self.samplemap_cf)
                except NotFoundException:
                    return False
                except Exception as e:
                    self.logger.exception('Exception in Rollback creating SampleMap for sid '+str(sid)+': '+str(e))
                    return False
                else:
                    return False
        else:
            self.logger.error('Sample not found: '+str(sid))
            return False

class SampleVar:
    def __init__(self, start,length,content):
        self.start=start
        self.length=length
        self.content=content
        self.hashes={}
        self.max_depth=0

    def sethash(self,offset,length,left_hash, right_hash):
        self.hashes[str(offset)+':'+str(length)]=(left_hash,right_hash)

    def __eq__(self, other):
        mykeys=self.hashes.keys()
        yourkeys=other.hashes.keys()
        common=list(set(mykeys)&set(yourkeys))
        try:
            for key in common:
                if not self.hashes[key]==other.hashes[key]:
                    return False
        except KeyError:
            return False
        return True

    def __repr__(self):
        return "{'start':"+str(self.start)+", 'content':"+self.content+", 'hashes': "+str(self.hashes)+"}"

def getVarList(sample_content):
    varlist=[]
    templist=[]
    p=re.compile(FLOAT_REGEXP)
    for m in p.finditer(sample_content):
        templist.append(m)
    for var in templist:
        try:
            if (sample_content[var.start()-1] in VAR_SEPARATORS) and (sample_content[var.start()+len(var.group())] in VAR_SEPARATORS):
                varlist.append(SampleVar(start=var.start(),length=len(var.group()), content=var.group()))
            elif (sample_content[var.start()-1] in VAR_SEPARATORS) and (sample_content[var.start()+len(var.group())] in VAR_SUFIX):
                varlist.append(SampleVar(start=var.start(),length=len(var.group()), content=var.group()))
        except IndexError:
            # out of bounds.... mmm store it:
            varlist.append(SampleVar(start=var.start(),length=len(var.group()), content=var.group()))
    return varlist

def calculateVarMatrix(varlist,sample_content):
    offset=0
    to_increase_depth=range(len(varlist))
    while len(to_increase_depth)>0:
        for i in to_increase_depth:
            left_string=getstring(offset=offset,start=varlist[i].start,content=sample_content,before=True)
            right_string=getstring(offset=offset,start=varlist[i].start+varlist[i].length-1,content=sample_content,before=False)
            left_hash=hash(left_string)
            right_hash=hash(right_string)
            varlist[i].sethash(offset,5,left_hash,right_hash)
        offset+=10
        to_increase_depth=[]
        for i,var_1 in enumerate(varlist):
           for j,var_2 in enumerate(varlist):
               if i != j:
                   if var_1==var_2:
                       to_increase_depth.append(i)
                       break
        to_increase_depth=list(set(to_increase_depth))

def getstring(offset,start,content,before):
    string=['' for i in range(5)]
    clean=False
    if before:
        start-=offset
        start-=1
        length=5
        while start>=0 and length>0:
            c=content[start]
            if c in (u'0',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9'):
                clean=True
                start-=1
            elif (c in (u',',u'.')) or (content[start+1] in (u'0',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9')):
                clean=True
                start-=1
            elif (c == u' ') and (content[start+1] == u' ') and not clean:
                clean=False
                start-=1
            else:
                start-=1
                length-=1
                clean=False
                string[length]=c
    else:
        start+=1
        start+=offset
        length=5
        pos=0
        while pos<length and start<len(content):
            c=content[start]
            if c in (u'0',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9'):
                clean=True
                start+=1
            elif (c in (u',',u'.')) and (content[start-1] in (u'0',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9')):
                clean=True
                start+=1
            elif (c == u' ') and (content[start-1] == u' ') and not clean:
                clean=False
                start+=1
            else:
                start+=1
                string[pos]=c
                clean=False
                pos+=1
    return ''.join(string)

