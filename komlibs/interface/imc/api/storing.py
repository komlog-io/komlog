#coding: utf-8
'''

Storing message definitions

'''

import os
import json
import uuid
from komfig import config, logger, options
from komfs import api as fsapi
from komlibs.general.time import timeuuid
from komlibs.general.validation import arguments as args
from komlibs.gestaccount.datasource import api as datasourceapi
from komlibs.gestaccount.widget import types as widgettypes
from komlibs.interface.imc.model import messages, responses
from komlibs.interface.imc import status, exceptions
from komlibs.mail import api as mailapi
from komlibs.interface.web.operations import weboperations


@exceptions.ExceptionHandler
def process_message_STOSMP(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    f = message.sample_file
    try:
        os.rename(f,f[:-5]+'.wspl')
    except OSError:
        logger.logger.error('Error renaming file before starting to process it: '+f)
        response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        filename = f[:-5]+'.wspl'
        file_content=fsapi.get_file_content(filename)
        if not file_content:
            logger.logger.error('Error loading file content. File is empty: '+f)
            try:
                os.rename(filename[:-5]+'.wspl',filename[:-5]+'.xspl')
            except Exception as e:
                logger.logger.debug('Error renaming file after failing loading its content: '+str(e))
            response.status=status.IMC_STATUS_INTERNAL_ERROR
            return response
        try:
            metainfo = json.loads(file_content)
            if not isinstance(metainfo,dict):
                raise TypeError
        except Exception as e:
            logger.logger.error('Error loading json content from file: '+f+' '+str(e))
            try:
                os.rename(filename[:-5]+'.wspl',filename[:-5]+'.xspl')
            except Exception as e:
                logger.logger.debug('Error renaming file after failing loading json content: '+str(e))
            response.status=status.IMC_STATUS_BAD_PARAMETERS
            return response
        str_did=metainfo['did'] if 'did' in metainfo else None
        sampledata=json.loads(metainfo['json_content']) if 'json_content' in metainfo else None
        content=sampledata['content'] if 'content' in sampledata else None
        timestamp=sampledata['ts'] if 'ts' in sampledata else None
        if not args.is_valid_datasource_content(content) or not args.is_valid_timestamp(timestamp) or not args.is_valid_hex_uuid(str_did):
            logger.logger.debug('Error validating file content ('+filename+'): content('+str(args.is_valid_datasource_content(content))+\
            '), timestamp('+str(args.is_valid_timestamp(timestamp))+'), did('+str(args.is_valid_hex_uuid(str_did))+')')
            try:
                os.rename(filename[:-5]+'.wspl',filename[:-5]+'.xspl')
            except Exception as e:
                logger.logger.debug('Error renaming file after failing checking its content: '+str(e))
            response.status=status.IMC_STATUS_BAD_PARAMETERS
            return response
        did=uuid.UUID(str_did)
        date=timeuuid.uuid1(seconds=timestamp)
        result=datasourceapi.store_datasource_data(did=did, date=date, content=content)
        if result:
            stored_path=config.get(options.SAMPLES_STORED_PATH)
            if not stored_path:
                logger.logger.debug('Error. SAMPLES_STORED_PATH configuration key not set.')
                stored_path=os.path.dirname(filename)
            fo = os.path.join(stored_path,os.path.basename(filename)[:-5]+'.sspl')
            try:
                os.rename(filename,fo)
            except Exception as e:
                logger.logger.debug('Error moving processed file to stored path: '+str(e))
            response.add_msg_originated(messages.GenerateTextSummaryMessage(did=did,date=date))
            response.add_msg_originated(messages.MapVarsMessage(did=did,date=date))
            response.status=status.IMC_STATUS_OK
        else:
            logger.logger.debug('Error storing sample. did: '+did.hex+' date:'+ds_date.hex)
            fo = filename[:-5]+'.xspl'
            try:
                os.rename(filename,fo)
            except Exception as e:
                logger.logger.debug('Error renaming file after failing proccessing it: '+str(e))
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    return response

