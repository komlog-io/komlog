#coding: utf-8
'''

Storing message definitions

'''

import os
import json
import uuid
from komimc import messages
from komimc import codes as msgcodes
from komcass.api import datasource as cassapidatasource
from komcass.model.orm import datasource as ormdatasource
from komfig import config, logger, options
from komfs import api as fsapi
from komlibs.general.time import timeuuid

def process_message_STOSMP(message):
        msgresult=messages.MessageResult(message)
        f = message.sample_file
        try:
            os.rename(f,f[:-5]+'.wspl')
        except OSError:
        #other instance took it firts (it shouldn't because messages must be sent once)
            logger.logger.error('File already treated by other module instance: '+f)
            msgresult.retcode=msgcodes.NOOP
        else:
            filename = f[:-5]+'.wspl'
            logger.logger.debug('Storing '+filename)
            metainfo = json.loads(fsapi.get_file_content(filename))
            dsinfo=json.loads(metainfo['json_content'])
            did=uuid.UUID(metainfo['did'])
            ds_content=dsinfo['ds_content']
            ds_date=timeuuid.uuid1(seconds=dsinfo['ds_date'])
            dsdobj=ormdatasource.DatasourceData(did=did,date=ds_date,content=ds_content)
            try:
                if cassapidatasource.insert_datasource_data(dsdobj=dsdobj):
                    cassapidatasource.set_last_received(did=did, last_received=ds_date)
                    logger.logger.debug(filename+' stored successfully : '+str(did)+' '+str(ds_date))
                    fo = os.path.join(config.get(options.SAMPLES_STORED_PATH),os.path.basename(filename)[:-5]+'.sspl')
                    os.rename(filename,fo)
                    newmsg=messages.MapVarsMessage(did=did,date=ds_date)
                    msgresult.add_msg_originated(newmsg)
                    msgresult.retcode=msgcodes.SUCCESS
                else:
                    fo = filename[:-5]+'.xspl'
                    os.rename(filename,fo)
                    msgresult.retcode=msgcodes.ERROR
            except Exception as e:
                cassapidatasource.delete_datasource_data(did=did, date=ds_date)
                logger.logger.exception('Exception inserting sample: '+str(e))
                fo = filename[:-5]+'.xspl'
                os.rename(filename,fo)
                msgresult.retcode=msgcodes.ERROR
        return msgresult

