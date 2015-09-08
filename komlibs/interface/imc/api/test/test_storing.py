import unittest
import uuid
import json
import time
import os
from komfig import logger
from komfs import api as fsapi
from komlibs.interface.imc.api import storing
from komlibs.interface.imc.model import messages
from komlibs.interface.imc import status, exceptions


class InterfaceImcApiStoringTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.storing tests '''

    def test_process_message_STOSMP_success(self):
        ''' process_message_STOSMP should succeed because this message does not check if uid or aid exist '''
        did=uuid.uuid4()
        file_content=json.dumps({'did':did.hex, 'json_content':json.dumps({'content':'Datasource Content 1 2 3 4 5','ts':time.time()})})
        filename='/tmp/test_process_message_STOSMP_success.pspl'
        fsapi.create_sample(filename=filename, data=file_content)
        message=messages.StoreSampleMessage(sample_file=filename)
        response=storing.process_message_STOSMP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.get_msg_originated()),2)
        message_types=[messages.MAP_VARS_MESSAGE,messages.GENERATE_TEXT_SUMMARY_MESSAGE]
        self.assertTrue(response.get_msg_originated()[0].type in message_types)
        self.assertEqual(response.get_msg_originated()[0].did,did)
        message_types.remove(response.get_msg_originated()[0].type)
        self.assertTrue(response.get_msg_originated()[1].type in message_types)
        self.assertEqual(response.get_msg_originated()[1].did,did)
        os.remove(filename[:-5]+'.sspl')

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

    def test_process_message_STOSMP_failure_empty_file(self):
        ''' process_message_STOSMP should fail if file is empty '''
        did=uuid.uuid4()
        file_content=json.dumps('')
        filename='/tmp/test_process_message_STOSMP_failure_empty_file.pspl'
        fd=open(filename,'w')
        fd.write(file_content)
        message=messages.StoreSampleMessage(sample_file=filename)
        response=storing.process_message_STOSMP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_INTERNAL_ERROR)
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
            os.remove(filename[:-5]+'.xspl')

    def test_process_message_STOSMP_failure_no_did_info(self):
        ''' process_message_STOSMP should fail if file content does not have did info '''
        file_content=json.dumps({'json_content':json.dumps({'content':'Datasource Content 1 2 3 4 5','ts':time.time()})})
        filename='/tmp/test_process_message_STOSMP_failure_no_did_info.pspl'
        fsapi.create_sample(filename=filename, data=file_content)
        message=messages.StoreSampleMessage(sample_file=filename)
        response=storing.process_message_STOSMP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_BAD_PARAMETERS)
        os.remove(filename[:-5]+'.xspl')

    def test_process_message_STOSMP_failure_no_content(self):
        ''' process_message_STOSMP should fail if file content does not have content field '''
        did=uuid.uuid4()
        file_content=json.dumps({'did':did.hex, 'json_content':json.dumps({'ts':time.time()})})
        filename='/tmp/test_process_message_STOSMP_failure_no_content.pspl'
        fsapi.create_sample(filename=filename, data=file_content)
        message=messages.StoreSampleMessage(sample_file=filename)
        response=storing.process_message_STOSMP(message=message)
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
        os.remove(filename[:-5]+'.xspl')

