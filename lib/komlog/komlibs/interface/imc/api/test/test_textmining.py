import unittest
import uuid
from komlog.komfig import logging
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.imc.api import textmining
from komlog.komlibs.interface.imc.api import gestconsole
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status, exceptions
from komlog.komlibs.interface.imc.errors import Errors


class InterfaceImcApiTextminingTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.textmining tests '''

    def test_process_message_GDTREE_failure_non_existent_pid(self):
        ''' process_message_GDTREE should fail if pid does not exist '''
        pid=uuid.uuid4()
        message=messages.GenerateDTreeMessage(pid=pid)
        response=textmining.process_message_GDTREE(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.unrouted_messages,[])
        self.assertEqual(response.routed_messages,{})

    def test_process_message_MAPVARS_failure_non_existent_data(self):
        ''' process_message_MAPVARS should fail if data does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        message=messages.MapVarsMessage(did=did,date=date)
        response=textmining.process_message_MAPVARS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.unrouted_messages,[])
        self.assertEqual(response.routed_messages,{})

    def test_process_message_FILLDP_failure_non_existent_pid(self):
        ''' process_message_FILLDP should fail if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        message=messages.FillDatapointMessage(pid=pid,date=date)
        response=textmining.process_message_FILLDP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.unrouted_messages,[])
        self.assertEqual(response.routed_messages,{})

    def test_process_message_FILLDS_failure_non_existent_did(self):
        ''' process_message_FILLDS should fail if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        message=messages.FillDatasourceMessage(did=did,date=date)
        response=textmining.process_message_FILLDS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.unrouted_messages,[])
        self.assertEqual(response.routed_messages,{})

    def test_process_message_FILLDS_success_one_datapoint_found(self):
        ''' process_message_FILLDS should succeed and generate the UrisUpdatedMessage for the ds and datapoint found '''
        username='test_process_message_fillds_success_one_datapoint_found'
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
        ds_content='content: 23'
        ds_date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=ds_date))
        position=9
        length=2
        datapoint_uri='datapoint_uri'
        message=messages.MonitorVariableMessage(uid=uid, did=did, date=ds_date, position=position, length=length, datapointname=datapoint_uri)
        response=gestconsole.process_message_MONVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        message=messages.FillDatasourceMessage(did=did, date=ds_date)
        response=textmining.process_message_FILLDS(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.FILL_DATASOURCE_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertNotEqual(response.unrouted_messages, [])
        self.assertTrue(len(response.unrouted_messages) == 1)
        expected_messages={
            messages.URIS_UPDATED_MESSAGE:1,
        }
        retrieved_messages={}
        msgs=response.unrouted_messages
        for msg in msgs:
            try:
                retrieved_messages[msg.type]+=1
            except KeyError:
                retrieved_messages[msg.type]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))
        self.assertEqual(msgs[0].type,messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(msgs[0].date,ds_date)
        uris=[item['uri'] for item in msgs[0].uris]
        self.assertEqual(sorted(uris),sorted(['datasource_uri','datasource_uri.datapoint_uri']))

    def test_process_message_GENTEXTSUMMARY_failure_non_existent_pid(self):
        ''' process_message_GENTEXTSUMMARY should fail if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        message=messages.GenerateTextSummaryMessage(did=did,date=date)
        response=textmining.process_message_GENTEXTSUMMARY(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.unrouted_messages,[])
        self.assertEqual(response.routed_messages,{})

