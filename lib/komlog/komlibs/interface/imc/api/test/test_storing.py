import unittest
import uuid
import json
import time
import os
from komlog.komfig import logging
from komlog.komfs import api as fsapi
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.interface.imc import api as imcapi
from komlog.komlibs.interface.imc.api import storing
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status, exceptions
from komlog.komlibs.general.time import timeuuid


class InterfaceImcApiStoringTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.storing tests '''

    def test_process_message_STOSMP_success(self):
        ''' process_message_STOSMP should succeed if datasource does exist '''
        username='test_process_message_stosmp_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        ts=1000.5
        file_content=json.dumps({'did':did.hex, 'json_content':json.dumps({'content':'Datasource Content 1 2 3 4 5','ts':ts})})
        filename='/tmp/test_process_message_STOSMP_success.pspl'
        fsapi.create_sample(filename=filename, data=file_content)
        message=messages.StoreSampleMessage(sample_file=filename)
        response=storing.process_message_STOSMP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.unrouted_messages),4)
        self.assertEqual(response.routed_messages,{})
        expected_messages={
            messages.MAP_VARS_MESSAGE:1,
            messages.GENERATE_TEXT_SUMMARY_MESSAGE:1,
            messages.UPDATE_QUOTES_MESSAGE:1,
            messages.URIS_UPDATED_MESSAGE:1
        }
        retrieved_messages={}
        for msg in response.unrouted_messages:
            try:
                retrieved_messages[msg.type]+=1
            except KeyError:
                retrieved_messages[msg.type]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))
        os.remove(filename[:-5]+'.sspl')

    def test_process_message_STOSMP_failure_datasource_not_found(self):
        ''' process_message_STOSMP should fail if datasource does not exist '''
        did=uuid.uuid4()
        ts=1000.5
        file_content=json.dumps({'did':did.hex, 'json_content':json.dumps({'content':'Datasource Content 1 2 3 4 5','ts':ts})})
        filename='/tmp/test_process_message_STOSMP_failure_datasource_not_found.pspl'
        fsapi.create_sample(filename=filename, data=file_content)
        message=messages.StoreSampleMessage(sample_file=filename)
        response=storing.process_message_STOSMP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.unrouted_messages,[])
        self.assertEqual(response.routed_messages,{})
        os.remove(filename[:-5]+'.wspl')

    def test_process_message_STOSMP_failure_invalid_filename(self):
        ''' process_message_STOSMP should fail if filename is not a string '''
        filenames=[None, 23423, 23423.23423, {'a':'dict'}, ['a','list'],('a','tuple'),uuid.uuid4()]
        for filename in filenames:
            self.assertRaises(exceptions.BadParametersException, messages.StoreSampleMessage, sample_file=filename)

    def test_process_message_STOSMP_failure_non_existent_filename(self):
        ''' process_message_STOSMP should fail if filename does not exist '''
        filename='/xxxx/yyyy/zzzz'
        message=messages.StoreSampleMessage(sample_file=filename)
        response=storing.process_message_STOSMP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_INTERNAL_ERROR)
        self.assertEqual(response.unrouted_messages,[])
        self.assertEqual(response.routed_messages,{})

    def test_process_message_STOSMP_failure_empty_file(self):
        ''' process_message_STOSMP should fail if file is empty '''
        did=uuid.uuid4()
        file_content=''
        filename='/tmp/test_process_message_STOSMP_failure_empty_file.pspl'
        fd=open(filename,'w')
        fd.write(file_content)
        fd.close()
        message=messages.StoreSampleMessage(sample_file=filename)
        response=storing.process_message_STOSMP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_INTERNAL_ERROR)
        self.assertEqual(response.unrouted_messages,[])
        self.assertEqual(response.routed_messages,{})
        os.remove(filename[:-5]+'.xspl')

    def test_process_message_STOSMP_failure_invalid_json_dict_content(self):
        ''' process_message_STOSMP should fail if file has no valid json content '''
        did=uuid.uuid4()
        file_contents=['a string with no json content', json.dumps(['a','list'])]
        filename='/tmp/test_process_message_STOSMP_failure_invalid_json_content.pspl'
        for file_content in file_contents:
            fsapi.create_sample(filename=filename, data=file_content)
            message=messages.StoreSampleMessage(sample_file=filename)
            response=storing.process_message_STOSMP(message=message)
            self.assertEqual(response.status, status.IMC_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.unrouted_messages,[])
            self.assertEqual(response.routed_messages,{})
            os.remove(filename[:-5]+'.xspl')

    def test_process_message_STOSMP_failure_no_did_info(self):
        ''' process_message_STOSMP should fail if file content does not have did info '''
        file_content=json.dumps({'json_content':json.dumps({'content':'Datasource Content 1 2 3 4 5','ts':time.time()})})
        filename='/tmp/test_process_message_STOSMP_failure_no_did_info.pspl'
        fsapi.create_sample(filename=filename, data=file_content)
        message=messages.StoreSampleMessage(sample_file=filename)
        response=storing.process_message_STOSMP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.unrouted_messages,[])
        self.assertEqual(response.routed_messages,{})
        os.remove(filename[:-5]+'.xspl')

    def test_process_message_STOSMP_failure_no_content(self):
        ''' process_message_STOSMP should fail if file content does not have content field '''
        did=uuid.uuid4()
        file_content=json.dumps({'did':did.hex, 'json_content':json.dumps({'ts':time.time()})})
        filename='/tmp/test_process_message_STOSMP_failure_no_content.pspl'
        fsapi.create_sample(filename=filename, data=file_content)
        message=messages.StoreSampleMessage(sample_file=filename)
        response=storing.process_message_STOSMP(message=message)
        self.assertEqual(response.unrouted_messages,[])
        self.assertEqual(response.routed_messages,{})
        self.assertEqual(response.status, status.IMC_STATUS_BAD_PARAMETERS)
        os.remove(filename[:-5]+'.xspl')

    def test_process_message_STOSMP_failure_no_timestamp(self):
        ''' process_message_STOSMP should fail if file content does not have timestamp '''
        did=uuid.uuid4()
        file_content=json.dumps({'did':did.hex, 'json_content':json.dumps({'ts':time.time()})})
        filename='/tmp/test_process_message_STOSMP_failure_no_timestamp.pspl'
        fsapi.create_sample(filename=filename, data=file_content)
        message=messages.StoreSampleMessage(sample_file=filename)
        response=storing.process_message_STOSMP(message=message)
        self.assertEqual(response.unrouted_messages,[])
        self.assertEqual(response.routed_messages,{})
        self.assertEqual(response.status, status.IMC_STATUS_BAD_PARAMETERS)
        os.remove(filename[:-5]+'.xspl')

    def test_process_message_STOSMP_failure_no_timestamp_nor_content(self):
        ''' process_message_STOSMP should fail if file content does not have timestamp '''
        did=uuid.uuid4()
        file_content=json.dumps({'did':did.hex, 'json_content':json.dumps('')})
        filename='/tmp/test_process_message_STOSMP_failure_no_timestamp_nor_content.pspl'
        fsapi.create_sample(filename=filename, data=file_content)
        message=messages.StoreSampleMessage(sample_file=filename)
        response=storing.process_message_STOSMP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.unrouted_messages,[])
        self.assertEqual(response.routed_messages,{})
        os.remove(filename[:-5]+'.xspl')

