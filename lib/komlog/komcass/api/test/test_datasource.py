import unittest
import time
import uuid
import json
import pickle
import zlib
from komlog.komlibs.general.time import timeuuid
from komlog.komcass.api import datasource as datasourceapi
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komfig import logging


class KomcassApiDatasourceTest(unittest.TestCase):
    ''' komlog.komcass.api.datasource tests '''

    def setUp(self):
        did1=uuid.uuid4()
        did2=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        name='test_komlog.komcass.api.datasource_datasource1'
        creation_date=timeuuid.uuid1()
        self.datasource1=ormdatasource.Datasource(did=did1, uid=uid, aid=aid, datasourcename=name, creation_date=creation_date)
        self.datasource2=ormdatasource.Datasource(did=did2, uid=uid, aid=aid, datasourcename=name, creation_date=creation_date)
        datasourceapi.insert_datasource(self.datasource1)
        datasourceapi.insert_datasource(self.datasource2)

    def test_get_datasource_existing_did(self):
        ''' get_datasource should succeed if we pass an existing did '''
        did=self.datasource1.did
        datasource=datasourceapi.get_datasource(did=did)
        self.assertEqual(datasource.did, self.datasource1.did)
        self.assertEqual(datasource.aid, self.datasource1.aid)
        self.assertEqual(datasource.uid, self.datasource1.uid)
        self.assertEqual(datasource.datasourcename, self.datasource1.datasourcename)

    def test_get_datasource_non_existing_did(self):
        ''' get_datasource should return None if we pass a non existing did '''
        did=uuid.uuid4()
        self.assertIsNone(datasourceapi.get_datasource(did=did))

    def test_get_datasources_existing_aid(self):
        ''' get_datasources should succeed if we pass an existing uid '''
        aid=self.datasource1.aid
        datasources=datasourceapi.get_datasources(aid=aid)
        self.assertEqual(len(datasources),2)
        for datasource in datasources:
            self.assertTrue(isinstance(datasource, ormdatasource.Datasource))

    def test_get_datasources_existing_uid(self):
        ''' get_datasources should succeed if we pass an existing uid '''
        uid=self.datasource1.uid
        datasources=datasourceapi.get_datasources(uid=uid)
        self.assertEqual(len(datasources),2)
        for datasource in datasources:
            self.assertTrue(isinstance(datasource, ormdatasource.Datasource))

    def test_get_datasources_non_existing_aid(self):
        ''' get_datasources should return an empty array if we pass a non existing aid '''
        aid=uuid.uuid4()
        datasources=datasourceapi.get_datasources(aid=aid)
        self.assertTrue(isinstance(datasources,list))
        self.assertEqual(len(datasources),0)

    def test_get_datasources_non_existing_uid(self):
        ''' get_datasources should return an empty array if we pass a non existing uid '''
        uid=uuid.uuid4()
        datasources=datasourceapi.get_datasources(uid=uid)
        self.assertTrue(isinstance(datasources,list))
        self.assertEqual(len(datasources),0)

    def test_get_datasources_dids_existing_aid(self):
        ''' get_datasources_dids should return a list with dids belonging to an aid '''
        aid=self.datasource1.aid
        dids=datasourceapi.get_datasources_dids(aid=aid)
        self.assertTrue(isinstance(dids, list))
        self.assertEqual(len(dids),2)
        for did in dids:
            self.assertTrue(isinstance(did,uuid.UUID))

    def test_get_datasources_dids_existing_uid(self):
        ''' get_datasources_dids should return a list with dids belonging to an uid '''
        uid=self.datasource1.uid
        dids=datasourceapi.get_datasources_dids(uid=uid)
        self.assertTrue(isinstance(dids, list))
        self.assertEqual(len(dids),2)
        for did in dids:
            self.assertTrue(isinstance(did,uuid.UUID))

    def test_get_datasources_dids_non_existing_uid(self):
        ''' get_datasources_dids should return an empty list if uid does not exist '''
        uid=uuid.uuid4()
        dids=datasourceapi.get_datasources_dids(uid=uid)
        self.assertTrue(isinstance(dids, list))
        self.assertEqual(len(dids),0)

    def test_get_datasources_dids_non_existing_aid(self):
        ''' get_datasources_dids should return an empty list if aid does not exist '''
        aid=uuid.uuid4()
        dids=datasourceapi.get_datasources_dids(aid=aid)
        self.assertTrue(isinstance(dids, list))
        self.assertEqual(len(dids),0)

    def test_get_number_of_datasources_by_aid_success(self):
        ''' get_number_of_datasources_by_aid should return the number of datasources belonging to an aid '''
        aid=self.datasource1.aid
        num_datasources=datasourceapi.get_number_of_datasources_by_aid(aid)
        self.assertEqual(num_datasources, 2)

    def test_get_number_of_datasources_by_aid_no_datasources(self):
        ''' get_number_of_datasources_by_aid should return the number of datasources belonging to an aid '''
        aid=uuid.uuid4()
        num_datasources=datasourceapi.get_number_of_datasources_by_aid(aid)
        self.assertEqual(num_datasources, 0)

    def test_insert_datasource_success(self):
        ''' insert_datasource should succeed if datasource object is passed '''
        did=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        name='test_insert_datasource_success_datasourcename'
        date=timeuuid.uuid1()
        datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=name, creation_date=date)
        self.assertTrue(datasourceapi.insert_datasource(datasource))
        datasource_db=datasourceapi.get_datasource(did=datasource.did)
        self.assertTrue(isinstance(datasource_db, ormdatasource.Datasource))
        self.assertEqual(datasource.did, datasource_db.did)
        self.assertEqual(datasource.aid, datasource_db.aid)
        self.assertEqual(datasource.uid, datasource_db.uid)
        self.assertEqual(datasource.datasourcename, datasource_db.datasourcename)

    def test_insert_datasource_no_datasource_object(self):
        ''' insert_datasource should return False if argument passed is not a datasource object '''
        datasources=[None, 23423423,'234232342',{'a':'dict'},['a','dict']]
        for datasource in datasources:
            self.assertFalse(datasourceapi.insert_datasource(datasource))

    def test_delete_datasource_success(self):
        ''' delete_datasource should succeed if datasource exists '''
        did=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        name='test_insert_datasource_success_datasourcename'
        date=timeuuid.uuid1()
        datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=name, creation_date=date)
        self.assertTrue(datasourceapi.insert_datasource(datasource))
        datasource_db=datasourceapi.get_datasource(did=datasource.did)
        self.assertTrue(isinstance(datasource_db, ormdatasource.Datasource))
        self.assertTrue(datasourceapi.delete_datasource(datasource.did))
        datasource_db2=datasourceapi.get_datasource(did=datasource.did)
        self.assertIsNone(datasource_db2)

    def test_delete_datasource_success_non_existent_datasource(self):
        ''' delete_datasource should succeed even if datasource does not exist '''
        did=uuid.uuid4()
        self.assertTrue(datasourceapi.delete_datasource(did))

    def test_get_datasource_stats_existing_did(self):
        ''' get_datasource_stats should succeed if we pass an existing did '''
        did=self.datasource1.did
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.set_last_received(did=did, last_received=date))
        datasource_stats=datasourceapi.get_datasource_stats(did=did)
        self.assertTrue(isinstance(datasource_stats,ormdatasource.DatasourceStats))
        self.assertEqual(datasource_stats.did, self.datasource1.did)

    def test_get_datasource_stats_non_existing_did(self):
        ''' get_datasource_stats should return None if we pass a non existing did '''
        did=uuid.uuid4()
        self.assertIsNone(datasourceapi.get_datasource_stats(did=did))

    def test_set_last_received_success(self):
        ''' set_last_received should succeed '''
        did=uuid.uuid4()
        last_received=timeuuid.uuid1()
        self.assertTrue(datasourceapi.set_last_received(did=did, last_received=last_received))

    def test_set_last_mapped_success(self):
        ''' set_last_mapped should succeed '''
        did=uuid.uuid4()
        last_mapped=timeuuid.uuid1()
        self.assertTrue(datasourceapi.set_last_mapped(did=did, last_mapped=last_mapped))

    def test_delete_datasource_stats_success(self):
        ''' delete_datasource_stats should delete the associated entry of the did '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.set_last_received(did=did, last_received=date))
        datasource_stats=datasourceapi.get_datasource_stats(did=did)
        self.assertTrue(isinstance(datasource_stats,ormdatasource.DatasourceStats))
        self.assertEqual(datasource_stats.did, did)
        self.assertTrue(datasourceapi.delete_datasource_stats(did=did))
        self.assertIsNone(datasourceapi.get_datasource_stats(did=did))

    def test_get_datasource_data_at_non_existing_did(self):
        ''' get_datasource_data_at should return None if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(datasourceapi.get_datasource_data_at(did=did, date=date))

    def test_get_datasource_data_at_existing_did_but_no_data_at_this_date(self):
        ''' get_datasource_data_at should return None if there is no data at this date '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='TEST_GET_DATASOURCE_DATA_AT_EXISTING_DID_BUT_NO_DATA_AT_THIS_DATE'
        dsdata=ormdatasource.DatasourceData(did=did, date=date, content=content)
        datasourceapi.insert_datasource_data(dsdobj=dsdata)
        date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-600)
        self.assertIsNone(datasourceapi.get_datasource_data_at(did=did, date=date))

    def test_get_datasource_data_at_success(self):
        ''' get_datasource_data_at should return DatapointData structure with the data '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='TEST_GET_DATASOURCE_DATA_AT_SUCCESS'
        dsdata=ormdatasource.DatasourceData(did=did, date=date, content=content)
        datasourceapi.insert_datasource_data(dsdobj=dsdata)
        data=datasourceapi.get_datasource_data_at(did=did, date=date)
        self.assertTrue(isinstance(data, ormdatasource.DatasourceData))
        self.assertEqual(data.content,content)
        self.assertEqual(data.did, did)

    def test_get_datasource_data_no_did(self):
        did=uuid.uuid4()
        fromdate=timeuuid.uuid1()
        todate=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(fromdate)+30)
        data=datasourceapi.get_datasource_data(did=did, fromdate=fromdate, todate=todate)
        self.assertTrue(isinstance(data,list))
        self.assertEqual(data,[])

    def test_get_datasource_data_success_did_passed(self):
        did=uuid.uuid4()
        init_interval=100
        end_interval=1000
        init_subinterval=250
        end_subinterval=750
        for i in range(init_interval, end_interval):
            data=ormdatasource.DatasourceData(did=did, date=timeuuid.uuid1(seconds=i), content=str(i))
            self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=data))
        data=datasourceapi.get_datasource_data(did=did)
        self.assertEqual(len(data),end_interval-init_interval)

    def test_get_datasource_data_success_did_and_count_passed(self):
        did=uuid.uuid4()
        init_interval=100
        end_interval=1000
        init_subinterval=250
        end_subinterval=750
        for i in range(init_interval, end_interval):
            data=ormdatasource.DatasourceData(did=did, date=timeuuid.uuid1(seconds=i), content=str(i))
            self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=data))
        count=100
        data=datasourceapi.get_datasource_data(did=did, count=count)
        self.assertEqual(len(data),count)
        min_date=timeuuid.min_uuid_from_time(end_interval-count)
        for item in data:
            self.assertTrue(item.date.time>=min_date.time)

    def test_get_datasource_data_success_did_and_fromdate_passed(self):
        did=uuid.uuid4()
        init_interval=1
        end_interval=10
        for i in range(init_interval, end_interval):
            data=ormdatasource.DatasourceData(did=did, date=timeuuid.uuid1(seconds=i), content=str(i))
            self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=data))
        count=5
        fromdate=timeuuid.min_uuid_from_time(end_interval-count)
        data=datasourceapi.get_datasource_data(did=did, fromdate=fromdate)
        self.assertEqual(len(data),count)
        min_date=fromdate
        for item in data:
            self.assertTrue(item.date.time>=min_date.time)

    def test_get_datasource_data_success_did_and_fromdate_and_count_passed(self):
        did=uuid.uuid4()
        init_interval=1
        end_interval=10
        for i in range(init_interval, end_interval):
            data=ormdatasource.DatasourceData(did=did, date=timeuuid.uuid1(seconds=i), content=str(i))
            self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=data))
        count=2
        fromdate=timeuuid.min_uuid_from_time(end_interval-5)
        data=datasourceapi.get_datasource_data(did=did, fromdate=fromdate, count=count)
        self.assertEqual(len(data),count)
        min_date=timeuuid.min_uuid_from_time(end_interval-count)
        for item in data:
            self.assertTrue(item.date.time>=min_date.time)

    def test_get_datasource_data_success_did_and_todate_passed(self):
        did=uuid.uuid4()
        init_interval=1
        end_interval=10
        for i in range(init_interval, end_interval):
            data=ormdatasource.DatasourceData(did=did, date=timeuuid.uuid1(seconds=i), content=str(i))
            self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=data))
        count=5
        todate=timeuuid.max_uuid_from_time(init_interval+count-1)
        data=datasourceapi.get_datasource_data(did=did, todate=todate)
        self.assertEqual(len(data),count)
        max_date=todate
        for item in data:
            self.assertTrue(item.date.time<=max_date.time)

    def test_get_datasource_data_success_did_and_todate_and_count_passed(self):
        did=uuid.uuid4()
        init_interval=1
        end_interval=10
        for i in range(init_interval, end_interval):
            data=ormdatasource.DatasourceData(did=did, date=timeuuid.uuid1(seconds=i), content=str(i))
            self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=data))
        count=3
        todate=timeuuid.max_uuid_from_time(end_interval-count)
        data=datasourceapi.get_datasource_data(did=did, todate=todate, count=count)
        self.assertEqual(len(data),count)
        min_date=timeuuid.min_uuid_from_time(end_interval-count-count)
        for item in data:
            self.assertTrue(item.date.time>=min_date.time)

    def test_get_datasource_data_success_did_and_fromdate_todate_and_count_passed(self):
        did=uuid.uuid4()
        init_interval=1
        end_interval=10
        for i in range(init_interval, end_interval):
            data=ormdatasource.DatasourceData(did=did, date=timeuuid.uuid1(seconds=i), content=str(i))
            self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=data))
        count=1
        todate=timeuuid.max_uuid_from_time(end_interval-1)
        fromdate=timeuuid.max_uuid_from_time(end_interval-5)
        data=datasourceapi.get_datasource_data(did=did,fromdate=fromdate,todate=todate,count=count)
        self.assertEqual(len(data),count)
        min_date=timeuuid.min_uuid_from_time(end_interval-2)
        max_date=todate
        for item in data:
            self.assertTrue(item.date.time>=min_date.time)
            self.assertTrue(item.date.time<=max_date.time)

    def test_get_datasource_data_success_did_and_fromdate_todate_passed(self):
        did=uuid.uuid4()
        init_interval=1
        end_interval=10
        for i in range(init_interval, end_interval):
            data=ormdatasource.DatasourceData(did=did, date=timeuuid.uuid1(seconds=i), content=str(i))
            self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=data))
        count=7
        todate=timeuuid.max_uuid_from_time(end_interval)
        fromdate=timeuuid.min_uuid_from_time(end_interval-count)
        data=datasourceapi.get_datasource_data(did=did,fromdate=fromdate,todate=todate)
        self.assertEqual(len(data),count)
        min_date=fromdate
        max_date=todate
        for item in data:
            self.assertTrue(item.date.time>=min_date.time)
            self.assertTrue(item.date.time<=max_date.time)

    def test_get_datasource_data_success_same_fromdate_and_todate_passed(self):
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='content'
        data=ormdatasource.DatasourceData(did=did, date=date, content=content)
        self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=data))
        todate=date
        fromdate=date
        data=datasourceapi.get_datasource_data(did=did,fromdate=fromdate,todate=todate)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0].date,date)
        self.assertEqual(data[0].did,did)
        self.assertEqual(data[0].content,content)
        date=timeuuid.min_uuid_from_time(1)
        data=ormdatasource.DatasourceData(did=did, date=date, content=content)
        self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=data))
        todate=date
        fromdate=date
        data=datasourceapi.get_datasource_data(did=did,fromdate=fromdate,todate=todate)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0].date,date)
        self.assertEqual(data[0].did,did)
        self.assertEqual(data[0].content,content)
        date=timeuuid.max_uuid_from_time(50)
        data=ormdatasource.DatasourceData(did=did, date=date, content=content)
        self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=data))
        todate=date
        fromdate=date
        data=datasourceapi.get_datasource_data(did=did,fromdate=fromdate,todate=todate)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0].date,date)
        self.assertEqual(data[0].did,did)
        self.assertEqual(data[0].content,content)

    def test_get_datasource_data_success_testing_interval_limits(self):
        did=uuid.uuid4()
        init_interval=100
        end_interval=1000
        init_subinterval=250
        end_subinterval=750
        for i in range(init_interval, end_interval):
            data=ormdatasource.DatasourceData(did=did, date=timeuuid.uuid1(seconds=i), content=str(i))
            self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=data))
        data=datasourceapi.get_datasource_data(did=did, fromdate=timeuuid.uuid1(seconds=init_subinterval), todate=timeuuid.uuid1(seconds=end_subinterval))
        self.assertTrue(isinstance(data, list))
        #The min/maxTimeuuid example selects all rows where the timeuuid column, t, 
        #is strictly later than 2013-01-01 00:05+0000 but strictly earlier than 
        #2013-02-02 10:00+0000. The t >= maxTimeuuid('2013-01-01 00:05+0000') 
        #does not select a timeuuid generated exactly at 2013-01-01 00:05+0000 
        #and is essentially equivalent to t > maxTimeuuid('2013-01-01 00:05+0000').
        self.assertTrue(len(data)>=end_subinterval-init_subinterval-1)
        self.assertTrue(timeuuid.get_unix_timestamp(data[0].date)>=end_subinterval-1)
        self.assertTrue(timeuuid.get_unix_timestamp(data[-1].date)<=init_subinterval+1)

    def test_insert_datasource_data_millisecond_precision_success(self):
        ''' insert_datasource_data must store data with the same date we pass in the DatasourceData object '''
        did=uuid.uuid4()
        for i in range(0,1000):
            base_sdate=time.time()+time.timezone
            content=str(base_sdate)
            date=timeuuid.uuid1(seconds=base_sdate)
            dsdobj=ormdatasource.DatasourceData(did=did, date=date, content=content)
            self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=dsdobj))
            db_data=datasourceapi.get_datasource_data_at(did=did, date=date)
            self.assertTrue(isinstance(db_data, ormdatasource.DatasourceData))
            self.assertEqual(db_data.did, did)
            self.assertEqual(db_data.content, content)
            self.assertEqual(timeuuid.get_unix_timestamp(db_data.date),timeuuid.get_unix_timestamp(date))

    def test_insert_datasource_data_millisecond_precision_success_2(self):
        ''' insert_datasource_data must retrieve the same data with the date stored in database '''
        did=uuid.uuid4()
        for i in range(0,1000):
            base_sdate=time.time()+time.timezone
            content=str(base_sdate)
            date=timeuuid.uuid1(seconds=base_sdate)
            dsdobj=ormdatasource.DatasourceData(did=did, date=date, content=content)
            self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=dsdobj))
            db_data=datasourceapi.get_datasource_data_at(did=did, date=date)
            db_data2=datasourceapi.get_datasource_data_at(did=did, date=db_data.date)
            self.assertTrue(isinstance(db_data, ormdatasource.DatasourceData))
            self.assertTrue(isinstance(db_data2, ormdatasource.DatasourceData))
            self.assertEqual(db_data.did, db_data2.did)
            self.assertEqual(db_data.content, db_data2.content)
            self.assertEqual(timeuuid.get_unix_timestamp(db_data.date),timeuuid.get_unix_timestamp(db_data2.date))

    def test_insert_datasource_data_success(self):
        ''' insert_datasource_data should succeed if a DatasourceData object is passed'''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='TEST_INSERT_DATASOURCE_DATA_SUCCESS'
        datasourcedata=ormdatasource.DatasourceData(did=did, date=date, content=content)
        self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=datasourcedata))

    def test_insert_datasource_data_non_datasource_data_object(self):
        ''' insert_datasource_data should fail if no DatasourceData object is passed '''
        datas=[None, 234234234, '23423423423', {'a':'dict'},['a','list']]
        for data in datas:
            self.assertFalse(datasourceapi.insert_datasource_data(data))

    def test_delete_datasource_data_at_non_existent_datasource(self):
        ''' delete_datasource_data_at should return True even if datasource does no exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.delete_datasource_data_at(did=did, date=date))

    def test_delete_datasource_data_at_success(self):
        ''' delete_datasource_data_at should return True if datasource exists '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='TEST_DELETE_DATASOURCE_DATA_AT_SUCCESS'
        dsdata=ormdatasource.DatasourceData(did=did, date=date, content=content)
        datasourceapi.insert_datasource_data(dsdobj=dsdata)
        data=datasourceapi.get_datasource_data_at(did=did, date=date)
        self.assertTrue(isinstance(data, ormdatasource.DatasourceData))
        self.assertTrue(datasourceapi.delete_datasource_data_at(did=did, date=date))
        self.assertIsNone(datasourceapi.get_datasource_data_at(did=did, date=date))

    def test_delete_datasource_data_success(self):
        ''' delete_datasource_data should delete all entries belonging to a did '''
        did=uuid.uuid4()
        for i in range(0,100):
            dsdobj=ormdatasource.DatasourceData(did=did, date=timeuuid.uuid1(),content=str(i))
            self.assertTrue(datasourceapi.insert_datasource_data(dsdobj=dsdobj))
        self.assertEqual(len(datasourceapi.get_datasource_data(did=did, fromdate=timeuuid.uuid1(seconds=1), todate=timeuuid.uuid1())),100)
        self.assertTrue(datasourceapi.delete_datasource_data(did=did))
        self.assertEqual(datasourceapi.get_datasource_data(did=did, fromdate=timeuuid.uuid1(seconds=1), todate=timeuuid.uuid1()),[])

    def test_insert_datasource_map_success(self):
        ''' insert_datasource_map should succeed if a DatasourceMap object is passed'''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcemap=ormdatasource.DatasourceMap(did=did, date=date, variables={})
        self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=datasourcemap))

    def test_insert_datasource_map_non_datasource_map_object(self):
        ''' insert_datasource_map should fail if no DatasourceMap object is passed '''
        datas=[None, 234234234, '23423423423', {'a':'dict'},['a','list']]
        for data in datas:
            self.assertFalse(datasourceapi.insert_datasource_map(data))

    def test_add_variable_to_datasource_map_success(self):
        ''' add_variable_to_datasource_map should succeed if all vars are passed and are correct '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=0
        length=1
        self.assertTrue(datasourceapi.add_variable_to_datasource_map(did=did, date=date, position=position, length=length))

    def test_add_datapoint_to_datasource_map_success(self):
        ''' add_datapoint_to_datasource_map should succeed if all vars are passed and are correct '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        pid=uuid.uuid4()
        position=0
        self.assertTrue(datasourceapi.add_datapoint_to_datasource_map(did=did, date=date, pid=pid, position=position))

    def test_delete_datapoint_from_datasource_map_success(self):
        ''' delete_datapoint_from_datasource_map should succeed if all vars are passed and are correct '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        pid=uuid.uuid4()
        self.assertTrue(datasourceapi.delete_datapoint_from_datasource_map(did=did, date=date, pid=pid))

    def test_get_datasource_map_non_existing_map(self):
        ''' get_datasource_data_at should return None if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(datasourceapi.get_datasource_map(did=did, date=date))

    def test_get_datasource_map_success(self):
        ''' get_datasource_map should return DatapointMap structure with the map '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        dsmap=ormdatasource.DatasourceMap(did=did, date=date, variables={1:1}, datapoints={uuid.uuid4():1})
        self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        dsmap_db=datasourceapi.get_datasource_map(did=did, date=date)
        self.assertTrue(isinstance(dsmap_db,ormdatasource.DatasourceMap))
        self.assertEqual(dsmap.did, dsmap_db.did)
        self.assertEqual(dsmap.variables, dsmap_db.variables)
        self.assertEqual(dsmap.datapoints, dsmap_db.datapoints)

    def test_get_datasource_maps_non_existing_maps(self):
        ''' get_datasource_maps should return an empty list if there are no maps '''
        did=uuid.uuid4()
        fromdate=timeuuid.uuid1()
        todate=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(fromdate)+1800)
        maps=datasourceapi.get_datasource_maps(did=did, fromdate=fromdate, todate=todate)
        self.assertTrue(isinstance(maps, list))
        self.assertEqual(len(maps),0)

    def test_get_datasource_maps_success(self):
        ''' get_datasource_maps should return a list with DatapointMap structures '''
        did=uuid.uuid4()
        fromdate=timeuuid.uuid1()
        dsmap=ormdatasource.DatasourceMap(did=did, date=fromdate, variables={})
        self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        todate=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(fromdate)+600)
        dsmap=ormdatasource.DatasourceMap(did=did, date=todate, variables={})
        self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        dsmaps_db=datasourceapi.get_datasource_maps(did=did, fromdate=fromdate, todate=todate)
        self.assertTrue(isinstance(dsmaps_db,list))
        self.assertEqual(len(dsmaps_db), 2)
        for amap in dsmaps_db:
            self.assertTrue(isinstance(amap,ormdatasource.DatasourceMap))
            self.assertEqual(amap.did, did)

    def test_get_datasource_maps_success_did_passed(self):
        did=uuid.uuid4()
        init_interval=100
        end_interval=1000
        init_subinterval=250
        end_subinterval=750
        for i in range(init_interval, end_interval):
            dsmap=ormdatasource.DatasourceMap(did=did, date=timeuuid.uuid1(seconds=i), variables={})
            self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        data=datasourceapi.get_datasource_maps(did=did)
        self.assertEqual(len(data),end_interval-init_interval)

    def test_get_datasource_maps_success_did_and_count_passed(self):
        did=uuid.uuid4()
        init_interval=100
        end_interval=1000
        init_subinterval=250
        end_subinterval=750
        for i in range(init_interval, end_interval):
            dsmap=ormdatasource.DatasourceMap(did=did, date=timeuuid.uuid1(seconds=i), variables={})
            self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        count=100
        data=datasourceapi.get_datasource_maps(did=did, count=count)
        self.assertEqual(len(data),count)
        min_date=timeuuid.min_uuid_from_time(end_interval-count)
        for item in data:
            self.assertTrue(item.date.time>=min_date.time)

    def test_get_datasource_maps_success_did_and_fromdate_passed(self):
        did=uuid.uuid4()
        init_interval=1
        end_interval=10
        for i in range(init_interval, end_interval):
            dsmap=ormdatasource.DatasourceMap(did=did, date=timeuuid.uuid1(seconds=i), variables={})
            self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        count=5
        fromdate=timeuuid.min_uuid_from_time(end_interval-count)
        data=datasourceapi.get_datasource_maps(did=did, fromdate=fromdate)
        self.assertEqual(len(data),count)
        min_date=fromdate
        for item in data:
            self.assertTrue(item.date.time>=min_date.time)

    def test_get_datasource_maps_success_did_and_fromdate_and_count_passed(self):
        did=uuid.uuid4()
        init_interval=1
        end_interval=10
        for i in range(init_interval, end_interval):
            dsmap=ormdatasource.DatasourceMap(did=did, date=timeuuid.uuid1(seconds=i), variables={})
            self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        count=2
        fromdate=timeuuid.min_uuid_from_time(end_interval-5)
        data=datasourceapi.get_datasource_maps(did=did, fromdate=fromdate, count=count)
        self.assertEqual(len(data),count)
        min_date=timeuuid.min_uuid_from_time(end_interval-count)
        for item in data:
            self.assertTrue(item.date.time>=min_date.time)

    def test_get_datasource_maps_success_did_and_todate_passed(self):
        did=uuid.uuid4()
        init_interval=1
        end_interval=10
        for i in range(init_interval, end_interval):
            dsmap=ormdatasource.DatasourceMap(did=did, date=timeuuid.uuid1(seconds=i), variables={})
            self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        count=5
        todate=timeuuid.max_uuid_from_time(init_interval+count-1)
        data=datasourceapi.get_datasource_maps(did=did, todate=todate)
        self.assertEqual(len(data),count)
        max_date=todate
        for item in data:
            self.assertTrue(item.date.time<=max_date.time)

    def test_get_datasource_maps_success_did_and_todate_and_count_passed(self):
        did=uuid.uuid4()
        init_interval=1
        end_interval=10
        for i in range(init_interval, end_interval):
            dsmap=ormdatasource.DatasourceMap(did=did, date=timeuuid.uuid1(seconds=i), variables={})
            self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        count=3
        todate=timeuuid.max_uuid_from_time(end_interval-count)
        data=datasourceapi.get_datasource_maps(did=did, todate=todate, count=count)
        self.assertEqual(len(data),count)
        min_date=timeuuid.min_uuid_from_time(end_interval-count-count)
        for item in data:
            self.assertTrue(item.date.time>=min_date.time)

    def test_get_datasource_maps_success_did_and_fromdate_todate_and_count_passed(self):
        did=uuid.uuid4()
        init_interval=1
        end_interval=10
        for i in range(init_interval, end_interval):
            dsmap=ormdatasource.DatasourceMap(did=did, date=timeuuid.uuid1(seconds=i), variables={})
            self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        count=1
        todate=timeuuid.max_uuid_from_time(end_interval-1)
        fromdate=timeuuid.max_uuid_from_time(end_interval-5)
        data=datasourceapi.get_datasource_maps(did=did,fromdate=fromdate,todate=todate,count=count)
        self.assertEqual(len(data),count)
        min_date=timeuuid.min_uuid_from_time(end_interval-2)
        max_date=todate
        for item in data:
            self.assertTrue(item.date.time>=min_date.time)
            self.assertTrue(item.date.time<=max_date.time)

    def test_get_datasource_maps_success_did_and_fromdate_todate_passed(self):
        did=uuid.uuid4()
        init_interval=1
        end_interval=10
        for i in range(init_interval, end_interval):
            dsmap=ormdatasource.DatasourceMap(did=did, date=timeuuid.uuid1(seconds=i), variables={})
            self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        count=7
        todate=timeuuid.max_uuid_from_time(end_interval)
        fromdate=timeuuid.min_uuid_from_time(end_interval-count)
        data=datasourceapi.get_datasource_maps(did=did,fromdate=fromdate,todate=todate)
        self.assertEqual(len(data),count)
        min_date=fromdate
        max_date=todate
        for item in data:
            self.assertTrue(item.date.time>=min_date.time)
            self.assertTrue(item.date.time<=max_date.time)

    def test_get_datasource_data_success_same_fromdate_and_todate_passed(self):
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        dsmap=ormdatasource.DatasourceMap(did=did, date=date, variables={})
        self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        todate=date
        fromdate=date
        data=datasourceapi.get_datasource_maps(did=did,fromdate=fromdate,todate=todate)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0].date,date)
        self.assertEqual(data[0].did,did)
        date=timeuuid.min_uuid_from_time(1)
        dsmap=ormdatasource.DatasourceMap(did=did, date=date, variables={})
        self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        todate=date
        fromdate=date
        data=datasourceapi.get_datasource_maps(did=did,fromdate=fromdate,todate=todate)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0].date,date)
        self.assertEqual(data[0].did,did)
        date=timeuuid.max_uuid_from_time(50)
        dsmap=ormdatasource.DatasourceMap(did=did, date=date, variables={})
        self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        todate=date
        fromdate=date
        data=datasourceapi.get_datasource_maps(did=did,fromdate=fromdate,todate=todate)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0].date,date)
        self.assertEqual(data[0].did,did)

    def test_get_datasource_map_success_testing_interval_limits(self):
        did=uuid.uuid4()
        init_interval=100
        end_interval=1000
        init_subinterval=250
        end_subinterval=750
        for i in range(init_interval, end_interval):
            data=ormdatasource.DatasourceMap(did=did, date=timeuuid.uuid1(seconds=i), variables={1:1})
            self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=data))
        data=datasourceapi.get_datasource_maps(did=did, fromdate=timeuuid.uuid1(seconds=init_subinterval), todate=timeuuid.uuid1(seconds=end_subinterval))
        self.assertTrue(isinstance(data, list))
        #The min/maxTimeuuid example selects all rows where the timeuuid column, t, 
        #is strictly later than 2013-01-01 00:05+0000 but strictly earlier than 
        #2013-02-02 10:00+0000. The t >= maxTimeuuid('2013-01-01 00:05+0000') 
        #does not select a timeuuid generated exactly at 2013-01-01 00:05+0000 
        #and is essentially equivalent to t > maxTimeuuid('2013-01-01 00:05+0000').
        self.assertTrue(len(data)>=end_subinterval-init_subinterval-1)
        self.assertTrue(timeuuid.get_unix_timestamp(data[0].date)>=end_subinterval-1)
        self.assertTrue(timeuuid.get_unix_timestamp(data[-1].date)<=init_subinterval+1)

    def test_get_datasource_map_dates_success(self):
        ''' get_datasource_map_dates should return the map dates between an interval '''
        did=uuid.uuid4()
        dates=[]
        for i in range(1,1000):
            date=timeuuid.uuid1(seconds=i)
            dates.append(date)
            data=ormdatasource.DatasourceMap(did=did, date=date, variables={})
            self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=data))
        data=datasourceapi.get_datasource_map_dates(did=did, fromdate=dates[250], todate=dates[499])
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data),250)
        for d in data:
            self.assertTrue(isinstance(d, uuid.UUID))


    def test_get_datasource_map_variables_success(self):
        ''' get_datasource_map_variables should return a dict with the variables '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=0
        length=1
        self.assertTrue(datasourceapi.add_variable_to_datasource_map(did=did, date=date, position=position, length=length))
        position=10
        length=1
        self.assertTrue(datasourceapi.add_variable_to_datasource_map(did=did, date=date, position=position, length=length))
        position=20
        length=1
        self.assertTrue(datasourceapi.add_variable_to_datasource_map(did=did, date=date, position=position, length=length))
        variables=datasourceapi.get_datasource_map_variables(did=did, date=date)
        self.assertEqual(variables,{0:1,10:1,20:1})

    def test_get_datasource_map_variables_no_variables(self):
        ''' get_datasource_map_variables should return None if no variables are found '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(datasourceapi.get_datasource_map_variables(did=did, date=date))

    def test_get_datasource_map_datapoints_success(self):
        ''' get_datasource_map_datapoints should return a dict with the datapoints '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=0
        pid1=uuid.uuid4()
        self.assertTrue(datasourceapi.add_datapoint_to_datasource_map(did=did, date=date, position=position, pid=pid1))
        position=0
        pid2=uuid.uuid4()
        self.assertTrue(datasourceapi.add_datapoint_to_datasource_map(did=did, date=date, position=position, pid=pid2))
        position=0
        pid3=uuid.uuid4()
        self.assertTrue(datasourceapi.add_datapoint_to_datasource_map(did=did, date=date, position=position, pid=pid3))
        datapoints=datasourceapi.get_datasource_map_datapoints(did=did, date=date)
        self.assertEqual(datapoints,{pid1:0,pid2:0,pid3:0})

    def test_get_datasource_map_datapoints_no_datapoints(self):
        ''' get_datasource_map_datapoints should return None if no datapoints are found '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(datasourceapi.get_datasource_map_datapoints(did=did, date=date))

    def test_delete_datasource_map_non_existent_map(self):
        ''' delete_datasource_map should return True even if map does no exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.delete_datasource_map(did=did, date=date))

    def test_delete_datasource_map_success(self):
        ''' delete_datasource_map should return True if map exists '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        datasourcemap=ormdatasource.DatasourceMap(did=did, date=date, variables={})
        self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=datasourcemap))
        data=datasourceapi.get_datasource_map(did=did, date=date)
        self.assertTrue(isinstance(data, ormdatasource.DatasourceMap))
        self.assertEqual(datasourcemap.did, data.did)
        self.assertEqual(datasourcemap.date, data.date)
        self.assertEqual(datasourcemap.variables, data.variables)
        self.assertEqual(datasourcemap.datapoints, data.datapoints)
        self.assertTrue(datasourceapi.delete_datasource_map(did=did, date=date))
        self.assertIsNone(datasourceapi.get_datasource_map(did=did, date=date))

    def test_delete_datasource_maps_sucess(self):
        ''' delete_datasource_maps should delete all map entries of a did '''
        did=uuid.uuid4()
        for i in range(0,100):
            date=timeuuid.uuid1()
            datasourcemap=ormdatasource.DatasourceMap(did=did, date=date, variables={})
            self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=datasourcemap))
            data=datasourceapi.get_datasource_map(did=did, date=date)
            self.assertTrue(isinstance(data, ormdatasource.DatasourceMap))
        self.assertTrue(datasourceapi.delete_datasource_maps(did=did))
        self.assertEqual(datasourceapi.get_datasource_maps(did=did, fromdate=timeuuid.uuid1(seconds=1), todate=timeuuid.uuid1()),[])

    def test_get_datasource_hash_non_existent_datasource_hash(self):
        ''' get_datasource_hash should return None if no datasource hash is found'''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(datasourceapi.get_datasource_hash(did=did, date=date))

    def test_get_datasource_hash_existent_datasource_hash(self):
        ''' get_datasource_hash should return the DatasourceHash object '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content=json.dumps({'key1':'value1','key2':{'key3':'value3','key4':4}})
        obj=ormdatasource.DatasourceHash(did=did, date=date, content=content)
        self.assertTrue(datasourceapi.insert_datasource_hash(obj=obj))
        db_obj=datasourceapi.get_datasource_hash(did=did, date=date)
        self.assertIsNotNone(db_obj)
        self.assertEqual(db_obj.did, did)
        self.assertEqual(db_obj.date, date)
        self.assertEqual(db_obj.content, content)

    def test_get_datasource_hashes_non_existent_hashes(self):
        ''' get_datasource_hashes should return an empty list if no datasource hash is found '''
        did=uuid.uuid4()
        fromdate=timeuuid.uuid1(seconds=1)
        todate=timeuuid.uuid1(seconds=1000)
        self.assertEqual(datasourceapi.get_datasource_hashes(did=did, fromdate=fromdate, todate=todate), [])

    def test_get_datasource_hashes_existent_hashes(self):
        ''' get_datasource_hashes should return the hashes found in the interval '''
        did=uuid.uuid4()
        for i in range(1,1000):
            content=json.dumps({'key1':i,'key2':{'key3':'value3','key4':4}})
            date=timeuuid.uuid1(seconds=i)
            obj=ormdatasource.DatasourceHash(did=did, date=date, content=content)
            self.assertTrue(datasourceapi.insert_datasource_hash(obj=obj))
        fromdate=timeuuid.uuid1(seconds=250.5)
        todate=timeuuid.uuid1(seconds=500.5)
        db_hashes=datasourceapi.get_datasource_hashes(did=did, fromdate=fromdate, todate=todate)
        self.assertEqual(len(db_hashes),250)

    def test_insert_datasource_hash_failure_invalid_object(self):
        ''' insert_datasource_hash should fail if obj is not a DatasourceHash object'''
        objs=[1,1.1,['a','list'],{'a':'dict'},('a','tuple'),{'set'},'text',uuid.uuid4(), timeuuid.uuid1()]
        for obj in objs:
            self.assertFalse(datasourceapi.insert_datasource_hash(obj))

    def test_insert_datasource_hash_success(self):
        ''' insert_datasource_hash should succeed '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content=json.dumps({'key1':'value1','key2':{'key3':'value3','key4':4}})
        obj=ormdatasource.DatasourceHash(did=did, date=date, content=content)
        self.assertTrue(datasourceapi.insert_datasource_hash(obj=obj))
        db_obj=datasourceapi.get_datasource_hash(did=did, date=date)
        self.assertIsNotNone(db_obj)
        self.assertEqual(db_obj.did, did)
        self.assertEqual(db_obj.date, date)
        self.assertEqual(db_obj.content, content)

    def test_delete_datasource_hash_success(self):
        ''' delete_datasource_hash should succeed '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content=json.dumps({'key1':'value1','key2':{'key3':'value3','key4':4}})
        obj=ormdatasource.DatasourceHash(did=did, date=date, content=content)
        self.assertTrue(datasourceapi.insert_datasource_hash(obj=obj))
        db_obj=datasourceapi.get_datasource_hash(did=did, date=date)
        self.assertIsNotNone(db_obj)
        self.assertEqual(db_obj.did, did)
        self.assertEqual(db_obj.date, date)
        self.assertEqual(db_obj.content, content)
        self.assertTrue(datasourceapi.delete_datasource_hash(did=did, date=date))
        self.assertIsNone(datasourceapi.get_datasource_hash(did=did, date=date))

    def test_delete_datasource_hashes_success(self):
        ''' delete_datasource_hashes should succeed '''
        did=uuid.uuid4()
        dates=[]
        for i in range(1,1001):
            date=timeuuid.uuid1()
            content=json.dumps({'key1':'value1','key2':{'key3':'value3','key4':4}})
            obj=ormdatasource.DatasourceHash(did=did, date=date, content=content)
            self.assertTrue(datasourceapi.insert_datasource_hash(obj=obj))
            dates.append(date)
        for date in dates:
            db_obj=datasourceapi.get_datasource_hash(did=did, date=date)
            self.assertIsNotNone(db_obj)
        self.assertTrue(datasourceapi.delete_datasource_hashes(did=did))
        for date in dates:
            db_obj=datasourceapi.get_datasource_hash(did=did, date=date)
            self.assertIsNone(db_obj)

    def test_get_datasource_metadata_none_found(self):
        ''' get_datasource_metadata should return an empty array if no data is found '''
        did=uuid.uuid4()
        init=timeuuid.uuid1(seconds=1)
        end=timeuuid.uuid1()
        self.assertEqual(datasourceapi.get_datasource_metadata(did=did,fromdate=init,todate=end),[])

    def get_datasource_metadata_success_some_data_found(self):
        ''' get_datasource_metadata should return an array with the metadata '''
        did=uuid.uuid4()
        for i in range(2,1000):
            date=timeuuid.uuid1(seconds=i)
            size=i
            obj=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
            self.assertTrue(datasourceapi.insert_datasource_metadata(obj=obj))
        init=timeuuid.uuid1(seconds=1)
        end=timeuuid.uuid1(seconds=1001)
        db_metadata=datasourceapi.get_datasource_metadata(did=did, fromdate=init, todate=end)
        self.assertEqual(len(db_metadata),998)
        for el in db_metadata:
            self.assertTrue(isinstance(el,ormdatasource.DatasourceMetadata))

    def test_get_datasource_metadata_at_none_found(self):
        ''' get_datasource_metadata_at should return None if none is found '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(datasourceapi.get_datasource_metadata_at(did=did, date=date))

    def test_get_datasource_metadata_at_found(self):
        ''' get_datasource_metadata_at should return the DatasourceMetadata object '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        size=100
        obj=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
        self.assertTrue(datasourceapi.insert_datasource_metadata(obj=obj))
        db_obj=datasourceapi.get_datasource_metadata_at(did=did, date=date)
        self.assertIsNotNone(db_obj)
        self.assertTrue(isinstance(db_obj,ormdatasource.DatasourceMetadata))
        self.assertEqual(did, db_obj.did)
        self.assertEqual(date, db_obj.date)
        self.assertEqual(size, db_obj.size)

    def test_get_datasource_metadata_size_at_none_found(self):
        ''' get_datasource_metadata_size_at should return None if none is found '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(datasourceapi.get_datasource_metadata_size_at(did=did, date=date))

    def test_get_datasource_metadata_size_at_found(self):
        ''' get_datasource_metadata_size_at should return the size value '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        size=100
        obj=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
        self.assertTrue(datasourceapi.insert_datasource_metadata(obj=obj))
        db_size=datasourceapi.get_datasource_metadata_size_at(did=did, date=date)
        self.assertEqual(size, db_size)

    def test_insert_datasource_metadata_failure_invalid_object(self):
        ''' insert_datasource_metadata should fail if argument is not a DatasourceMetadata object '''
        objs=[1,1.1,['a','list'],{'a':'dict'},('a','tuple'),{'set'},'text',uuid.uuid4(), timeuuid.uuid1()]
        for obj in objs:
            self.assertFalse(datasourceapi.insert_datasource_metadata(obj))

    def test_insert_datasource_metadata_success(self):
        ''' insert_datasource_metadata should succeed '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        size=100
        obj=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
        self.assertTrue(datasourceapi.insert_datasource_metadata(obj=obj))
        db_obj=datasourceapi.get_datasource_metadata_at(did=did, date=date)
        self.assertIsNotNone(db_obj)
        self.assertTrue(isinstance(db_obj,ormdatasource.DatasourceMetadata))
        self.assertEqual(did, db_obj.did)
        self.assertEqual(date, db_obj.date)
        self.assertEqual(size, db_obj.size)

    def delete_datasource_metadata_success_none_found(self):
        ''' delete_datasource_metadata should succeed even if no data exists '''
        did=uuid.uuid4()
        self.assertTrue(datasourceapi.delete_datasource_metadata(did=did))

    def delete_datasource_metadata_success_some_data_found(self):
        ''' delete_datasource_metadata should succeed and delete all did metadata '''
        did=uuid.uuid4()
        for i in range(1,1001):
            date=timeuuid.uuid1()
            size=i
            obj=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
            self.assertTrue(datasourceapi.insert_datasource_metadata(obj=obj))
        init=timeuuid.uuid1(seconds=1)
        end=timeuuid.uuid1()
        db_metadata=datasourceapi.get_datasource_metadata(did=did, fromdate=init, todate=end)
        self.assertEqual(len(db_metadata),1000)
        self.assertTrue(datasourceapi.delete_datasource_metadata(did=did))
        db_metadata=datasourceapi.get_datasource_metadata(did=did, fromdate=init, todate=end)
        self.assertEqual(len(db_metadata),0)

    def delete_datasource_metadata_at_success_none_found(self):
        ''' delete_datasource_metadata_at should succeed even if no data exists '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.delete_datasource_metadata_at(did=did, date=date))

    def delete_datasource_metadata_at_success_some_data_found(self):
        ''' delete_datasource_metadata_at should succeed and delete all did metadata '''
        did=uuid.uuid4()
        for i in range(1,1001):
            date=timeuuid.uuid1()
            size=i
            obj=ormdatasource.DatasourceMetadata(did=did, date=date, size=size)
            self.assertTrue(datasourceapi.insert_datasource_metadata(obj=obj))
        init=timeuuid.uuid1(seconds=1)
        end=timeuuid.uuid1()
        db_metadata=datasourceapi.get_datasource_metadata(did=did, fromdate=init, todate=end)
        self.assertEqual(len(db_metadata),1000)
        el=db_metadata[0]
        self.assertTrue(datasourceapi.delete_datasource_metadata_at(did=el.did, date=el.date))
        db_metadata=datasourceapi.get_datasource_metadata(did=did, fromdate=init, todate=end)
        self.assertEqual(len(db_metadata),999)

    def test_get_datasource_hooks_sids_none_found(self):
        ''' get_datasource_hooks should return an empty list if no sid is found '''
        did=uuid.uuid4()
        self.assertEqual(datasourceapi.get_datasource_hooks_sids(did=did),[])

    def test_get_datasource_hooks_sids_some_found(self):
        ''' get_datasource_hooks should return a sid list '''
        did=uuid.uuid4()
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        sids=datasourceapi.get_datasource_hooks_sids(did=did)
        self.assertEqual(len(sids),4)

    def test_insert_datasource_hook_success(self):
        ''' insert_datasource_hook should insert the did,sid data '''
        did=uuid.uuid4()
        sid=uuid.uuid4()
        self.assertEqual(datasourceapi.get_datasource_hooks_sids(did=did),[])
        self.assertTrue(datasourceapi.insert_datasource_hook(did,sid))
        self.assertEqual(datasourceapi.get_datasource_hooks_sids(did=did),[sid])

    def test_delete_datasource_hooks_some_found(self):
        ''' delete_datasource_hooks should delete the did hooks '''
        did=uuid.uuid4()
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        sids=datasourceapi.get_datasource_hooks_sids(did=did)
        self.assertEqual(len(sids),4)
        self.assertTrue(datasourceapi.delete_datasource_hooks(did=did))
        self.assertEqual(datasourceapi.get_datasource_hooks_sids(did=did),[])

    def test_delete_datasource_hooks_none_found(self):
        ''' delete_datasource_hooks should return True even if no sid is found '''
        did=uuid.uuid4()
        self.assertEqual(datasourceapi.get_datasource_hooks_sids(did=did),[])
        self.assertTrue(datasourceapi.delete_datasource_hooks(did=did))
        self.assertEqual(datasourceapi.get_datasource_hooks_sids(did=did),[])

    def test_delete_datasource_hook_found(self):
        ''' delete_datasource_hook should delete the hook '''
        did=uuid.uuid4()
        sid=uuid.uuid4()
        self.assertTrue(datasourceapi.insert_datasource_hook(did,sid))
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        sids=datasourceapi.get_datasource_hooks_sids(did=did)
        self.assertEqual(len(sids),4)
        self.assertTrue(datasourceapi.delete_datasource_hook(did=did,sid=sid))
        sids=datasourceapi.get_datasource_hooks_sids(did=did)
        self.assertEqual(len(sids),3)
        self.assertFalse(sid in sids)

    def test_delete_datasource_hook_not_found(self):
        ''' delete_datasource_hook should delete the hook if found. return True always '''
        did=uuid.uuid4()
        sid=uuid.uuid4()
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        self.assertTrue(datasourceapi.insert_datasource_hook(did,uuid.uuid4()))
        sids=datasourceapi.get_datasource_hooks_sids(did=did)
        self.assertEqual(len(sids),4)
        self.assertTrue(datasourceapi.delete_datasource_hook(did=did,sid=sid))
        sids=datasourceapi.get_datasource_hooks_sids(did=did)
        self.assertEqual(len(sids),4)
        self.assertFalse(sid in sids)

    def test_insert_datasource_supplies_success_some_supplies(self):
        ''' insert_datasource_supplies should insert the values successfully '''
        did = uuid.uuid4()
        date = timeuuid.uuid1()
        supplies = ['a','b','c','d']
        self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        supobj = datasourceapi.get_datasource_supplies_at(did, date)
        self.assertEqual(supobj.did, did)
        self.assertEqual(supobj.date, date)
        self.assertEqual(supobj.supplies, supplies)

    def test_insert_datasource_supplies_success_no_supplies(self):
        ''' insert_datasource_supplies should insert the values successfully '''
        did = uuid.uuid4()
        date = timeuuid.uuid1()
        supplies = []
        self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        supobj = datasourceapi.get_datasource_supplies_at(did, date)
        self.assertEqual(supobj.did, did)
        self.assertEqual(supobj.date, date)
        self.assertEqual(supobj.supplies, supplies)

    def test_insert_datasource_supplies_success_dup_supplies(self):
        ''' insert_datasource_supplies should insert the values successfully '''
        did = uuid.uuid4()
        date = timeuuid.uuid1()
        supplies = ['a','b','c','d','a']
        self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        supobj = datasourceapi.get_datasource_supplies_at(did, date)
        self.assertEqual(supobj.did, did)
        self.assertEqual(supobj.date, date)
        self.assertEqual(supobj.supplies, sorted(list(set(supplies))))

    def test_get_datasource_supplies_success_some_supplies(self):
        ''' get_datasource_supplies should return a list with the supplies entries found '''
        did = uuid.uuid4()
        supplies = ['a','b','c','d']
        for i in range(1,101):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        for i in range(200,300):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        suplist = datasourceapi.get_datasource_supplies(did, timeuuid.uuid1(199),timeuuid.uuid1(301))
        self.assertTrue(len(suplist),100)
        for item in suplist:
            self.assertEqual(item.did, did)
            self.assertEqual(item.supplies, supplies)

    def test_get_datasource_supplies_success_no_supplies(self):
        ''' get_datasource_supplies should return a list with the supplies entries found '''
        did = uuid.uuid4()
        supplies = ['a','b','c','d']
        for i in range(1,101):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        for i in range(200,300):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        suplist = datasourceapi.get_datasource_supplies(did, timeuuid.uuid1(1990),timeuuid.uuid1(20000))
        self.assertEqual(len(suplist),0)

    def test_get_datasource_supplies_at_success_supplies_exist(self):
        ''' get_datasource_supplies_at should return the supplies entry if exists '''
        did = uuid.uuid4()
        sel_supplies = ['a','b','c','d','e']
        sel_date = timeuuid.uuid1(250)
        self.assertTrue(datasourceapi.insert_datasource_supplies(did, sel_date, sel_supplies))
        supplies = ['a','b','c','d']
        for i in range(1,101):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        for i in range(200,300):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        supobj = datasourceapi.get_datasource_supplies_at(did, sel_date)
        self.assertEqual(supobj.did, did)
        self.assertEqual(supobj.date, sel_date)
        self.assertEqual(supobj.supplies, sel_supplies)

    def test_get_datasource_supplies_at_success_supplies_does_not_exist(self):
        ''' get_datasource_supplies_at should return None if the supplies entry does not exist '''
        did = uuid.uuid4()
        sel_date = timeuuid.uuid1(250)
        supplies = ['a','b','c','d']
        for i in range(1,101):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        for i in range(200,300):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        self.assertIsNone(datasourceapi.get_datasource_supplies_at(did, sel_date))

    def test_get_last_datasource_supplies_count_no_row_exist(self):
        ''' get_last_datasource_supplies_count should return an empty list if no row exists '''
        did = uuid.uuid4()
        self.assertEqual(datasourceapi.get_last_datasource_supplies_count(did),[])

    def test_get_last_datasource_supplies_count_exist(self):
        ''' get_last_datasource_supplies_count should return as many elements as requested if they exist '''
        did = uuid.uuid4()
        last_date = timeuuid.uuid1()
        supplies = ['a','b','c','d']
        for i in range(1,101):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        self.assertTrue(datasourceapi.insert_datasource_supplies(did, last_date, supplies))
        for i in range(200,300):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        suplist = datasourceapi.get_last_datasource_supplies_count(did)
        self.assertEqual(len(suplist),1)
        self.assertEqual(suplist[0].did, did)
        self.assertEqual(suplist[0].date, last_date)
        self.assertEqual(suplist[0].supplies, supplies)

    def test_delete_datasource_supplies_success_rows_deleted(self):
        ''' delete_datasource_supplies should delete all did supplies rows '''
        did = uuid.uuid4()
        supplies = ['a','b','c','d']
        for i in range(1,101):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        fromdate = timeuuid.uuid1(0)
        todate = timeuuid.uuid1()
        suplist = datasourceapi.get_datasource_supplies(did, fromdate, todate)
        self.assertEqual(len(suplist),100)
        self.assertTrue(datasourceapi.delete_datasource_supplies(did))
        suplist = datasourceapi.get_datasource_supplies(did, fromdate, todate)
        self.assertEqual(len(suplist),0)

    def test_delete_datasource_supplies_success_no_rows_deleted(self):
        ''' delete_datasource_supplies should delete all did supplies rows '''
        did = uuid.uuid4()
        fromdate = timeuuid.uuid1(0)
        todate = timeuuid.uuid1()
        suplist = datasourceapi.get_datasource_supplies(did, fromdate, todate)
        self.assertEqual(len(suplist),0)
        self.assertTrue(datasourceapi.delete_datasource_supplies(did))
        suplist = datasourceapi.get_datasource_supplies(did, fromdate, todate)
        self.assertEqual(len(suplist),0)

    def test_delete_datasource_supplies_at_success_row_deleted(self):
        ''' delete_datasource_supplies_at should delete the selected row if exists '''
        did = uuid.uuid4()
        sel_date = timeuuid.uuid1(50)
        supplies = ['a','b','c','d']
        for i in range(1,101):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        self.assertTrue(datasourceapi.insert_datasource_supplies(did, sel_date, supplies))
        fromdate = timeuuid.uuid1(0)
        todate = timeuuid.uuid1()
        suplist = datasourceapi.get_datasource_supplies(did, fromdate, todate)
        self.assertEqual(len(suplist),101)
        self.assertTrue(datasourceapi.delete_datasource_supplies_at(did, sel_date))
        suplist = datasourceapi.get_datasource_supplies(did, fromdate, todate)
        self.assertEqual(len(suplist),100)

    def test_delete_datasource_supplies_at_success_no_row_deleted(self):
        ''' delete_datasource_supplies_at should delete the selected row if exists '''
        did = uuid.uuid4()
        sel_date = timeuuid.uuid1(50)
        supplies = ['a','b','c','d']
        for i in range(1,101):
            date = timeuuid.uuid1(i)
            self.assertTrue(datasourceapi.insert_datasource_supplies(did, date, supplies))
        #self.assertTrue(datasourceapi.insert_datasource_supplies(did, sel_date, supplies))
        fromdate = timeuuid.uuid1(0)
        todate = timeuuid.uuid1()
        suplist = datasourceapi.get_datasource_supplies(did, fromdate, todate)
        self.assertEqual(len(suplist),100)
        self.assertTrue(datasourceapi.delete_datasource_supplies_at(did, sel_date))
        suplist = datasourceapi.get_datasource_supplies(did, fromdate, todate)
        self.assertEqual(len(suplist),100)

    def test_get_datapoint_classifier_dtree_no_data(self):
        ''' get_datapoint_classifier_dtree should return None if no data is found '''
        did = uuid.uuid4()
        self.assertIsNone(datasourceapi.get_datapoint_classifier_dtree(did))

    def test_get_datapoint_classifier_dtree_no_dtree(self):
        ''' get_datapoint_classifier_dtree should return None if no data is found '''
        did = uuid.uuid4()
        self.assertTrue(datasourceapi.insert_datapoint_classifier_dtree(did,None))
        self.assertIsNone(datasourceapi.get_datapoint_classifier_dtree(did))

    def test_get_datapoint_classifier_dtree_data_found(self):
        ''' get_datapoint_classifier_dtree should return None if no data is found '''
        did = uuid.uuid4()
        dtree = pickle.dumps('some data')
        self.assertTrue(datasourceapi.insert_datapoint_classifier_dtree(did,dtree))
        dbtree = datasourceapi.get_datapoint_classifier_dtree(did)
        self.assertEqual(dtree, dbtree)

    def test_insert_datapoint_classifier_dtree_success(self):
        ''' set_last_received should succeed '''
        did = uuid.uuid4()
        dtree = pickle.dumps('some data')
        self.assertTrue(datasourceapi.insert_datapoint_classifier_dtree(did,dtree))
        dbtree = datasourceapi.get_datapoint_classifier_dtree(did)
        self.assertEqual(dtree, dbtree)

    def test_delete_datapoint_classifier_dtree_success(self):
        ''' delete_datapoint_classifier_dtree should delete the associated entry of the did '''
        did=uuid.uuid4()
        dtree = pickle.dumps('some data')
        self.assertTrue(datasourceapi.insert_datapoint_classifier_dtree(did,dtree))
        dbtree = datasourceapi.get_datapoint_classifier_dtree(did)
        self.assertEqual(dtree, dbtree)
        self.assertTrue(datasourceapi.delete_datapoint_classifier_dtree(did))
        self.assertIsNone(datasourceapi.get_datapoint_classifier_dtree(did))
        self.assertIsNone(datasourceapi.get_datapoint_classifier_dtree(did))

    def test_get_datasource_features_success_no_feature(self):
        ''' get_datasource_features should return None if no data is found '''
        did = uuid.uuid4()
        self.assertIsNone(datasourceapi.get_datasource_features(did))

    def test_get_datasource_features_success_features_found(self):
        ''' get_datasource_features should return a DatasourceFeatures object '''
        did = uuid.uuid4()
        date = timeuuid.uuid1()
        features = [1,2,3,4,5]
        self.assertTrue(datasourceapi.insert_datasource_features(did, date, features))
        obj = datasourceapi.get_datasource_features(did)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.features, sorted(features))

    def test_insert_datasource_features_success(self):
        ''' insert_datasource_features should insert data and return True '''
        did = uuid.uuid4()
        date = timeuuid.uuid1()
        features = [1,2,3,4,5]
        self.assertTrue(datasourceapi.insert_datasource_features(did, date, features))
        obj = datasourceapi.get_datasource_features(did)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.features, sorted(features))
        date2 = timeuuid.uuid1()
        features = [6,7,8,9]
        self.assertTrue(datasourceapi.insert_datasource_features(did, date2, features))
        obj = datasourceapi.get_datasource_features(did)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date2)
        self.assertEqual(obj.features, sorted(features))

    def test_insert_datasource_features_success_no_features(self):
        ''' insert_datasource_features should insert data and return True '''
        did = uuid.uuid4()
        date = timeuuid.uuid1()
        features = []
        self.assertTrue(datasourceapi.insert_datasource_features(did, date, features))
        obj = datasourceapi.get_datasource_features(did)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.features, [])
        features = [1,2,3,4,5]
        date2 = timeuuid.uuid1()
        self.assertTrue(datasourceapi.insert_datasource_features(did, date2, features))
        obj = datasourceapi.get_datasource_features(did)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date2)
        self.assertEqual(obj.features, sorted(features))

    def test_delete_datasource_features_success_no_features(self):
        ''' delete_datasource_features should return True even if datasource has no features '''
        did = uuid.uuid4()
        self.assertIsNone(datasourceapi.get_datasource_features(did))
        self.assertTrue(datasourceapi.delete_datasource_features(did))

    def test_delete_datasource_features_success_some_features(self):
        ''' delete_datasource_features should return True even if datasource has no features '''
        did = uuid.uuid4()
        date = timeuuid.uuid1()
        features = []
        self.assertTrue(datasourceapi.insert_datasource_features(did, date, features))
        obj = datasourceapi.get_datasource_features(did)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.features, [])
        self.assertTrue(datasourceapi.delete_datasource_features(did))
        self.assertIsNone(datasourceapi.get_datasource_features(did))
        date2 = timeuuid.uuid1()
        features = [1,2,3,4,5]
        self.assertTrue(datasourceapi.insert_datasource_features(did, date2, features))
        obj = datasourceapi.get_datasource_features(did)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date2)
        self.assertEqual(obj.features, sorted(features))
        self.assertTrue(datasourceapi.delete_datasource_features(did))
        self.assertIsNone(datasourceapi.get_datasource_features(did))

    def test_get_datasources_by_feature_success_no_data(self):
        ''' get_datasources_by_feature should return an empty list if no data is found '''
        feature = zlib.adler32(bytes('test_get_datasources_by_feature_success_no_data','utf-8'))
        self.assertEqual(datasourceapi.get_datasources_by_feature(feature), [])
        self.assertEqual(datasourceapi.get_datasources_by_feature(feature, count=100), [])

    def test_get_datasources_by_feature_success_some_datasources_found(self):
        ''' get_datasources_by_feature should return a did list with the data found '''
        feature = zlib.adler32(bytes('test_get_datasources_by_feature_success_some_datasources_found','utf-8'))
        for i in range(1,100):
            did = uuid.uuid4()
            weight = i/(i+1)
            self.assertTrue(datasourceapi.insert_datasource_by_feature(feature, did, weight))
        datasources = datasourceapi.get_datasources_by_feature(feature)
        self.assertEqual(len(datasources),1)
        datasources = datasourceapi.get_datasources_by_feature(feature, count=50)
        self.assertEqual(len(datasources),50)
        datasources = datasourceapi.get_datasources_by_feature(feature, count=1000)
        self.assertEqual(len(datasources),99)

    def test_insert_datasource_by_feature_success(self):
        ''' insert_datasource_by_feature should return True '''
        feature = zlib.adler32(bytes('test_insert_datasources_by_feature_success','utf-8'))
        for i in range(1,100):
            did = uuid.uuid4()
            weight = i/(i+1)
            self.assertTrue(datasourceapi.insert_datasource_by_feature(feature, did, weight))
        datasources = datasourceapi.get_datasources_by_feature(feature)
        self.assertEqual(len(datasources),1)
        datasources = datasourceapi.get_datasources_by_feature(feature, count=50)
        self.assertEqual(len(datasources),50)
        datasources = datasourceapi.get_datasources_by_feature(feature, count=1000)
        self.assertEqual(len(datasources),99)

    def test_insert_datasource_by_features_success_batch(self):
        ''' insert_datasource_by_features should return True '''
        did = uuid.uuid4()
        info = []
        for i in range(1,1000):
            feature = zlib.adler32(bytes('test_insert_datasource_by_features_success_batch'+str(i),'utf-8'))
            weight = i/(i+1)
            info.append({'feature':feature, 'weight':weight})
        self.assertTrue(datasourceapi.insert_datasource_by_features(did, info))
        for i in range(1,1000):
            feat = zlib.adler32(bytes('test_insert_datasource_by_features_success_batch'+str(i),'utf-8'))
            ds = datasourceapi.get_datasources_by_feature(feat, count=1)
            self.assertEqual(len(ds),1)
            self.assertEqual(ds[0].did,did)

    def test_delete_datasource_by_feature_success_no_previous_data(self):
        ''' delete_datasources_by_feature should return True and delete data if existed '''
        feature = zlib.adler32(bytes('test_delete_datasources_by_feature_success_no_previous_data','utf-8'))
        dids = datasourceapi.get_datasources_by_feature(feature)
        self.assertEqual(len(dids),0)
        for i in range(1,100):
            did = uuid.uuid4()
            self.assertTrue(datasourceapi.delete_datasource_by_feature(feature,did))
        dids = datasourceapi.get_datasources_by_feature(feature)
        self.assertEqual(len(dids),0)

    def test_delete_datasource_by_feature_success_previous_data_existed(self):
        ''' delete_datasources_by_feature should return True and delete data if existed '''
        feature = zlib.adler32(bytes('test_delete_datasources_by_feature_success_previous_data_existed','utf-8'))
        weight = 1
        dids = [uuid.uuid4() for i in range(1,100)]
        for did in dids:
            self.assertTrue(datasourceapi.insert_datasource_by_feature(feature,did, weight))
        dss = datasourceapi.get_datasources_by_feature(feature, count=1000)
        self.assertEqual(len(dss),99)
        for i,ds in enumerate(dss):
            self.assertTrue(datasourceapi.delete_datasource_by_feature(feature,ds.did))
            remaining = datasourceapi.get_datasources_by_feature(feature, count=1000)
            self.assertEqual(len(remaining),98-i)
            for r in remaining:
                self.assertNotEqual(r.did,ds.did)
        dss = datasourceapi.get_datasources_by_feature(feature)
        self.assertEqual(len(dss),0)

    def test_delete_datasource_by_features_success_batch(self):
        ''' delete_datasource_by_features should return True '''
        did = uuid.uuid4()
        info = []
        for i in range(1,1000):
            feature = zlib.adler32(bytes('test_delete_datasource_by_features_success_batch'+str(i),'utf-8'))
            weight = i/(i+1)
            info.append({'feature':feature, 'weight':weight})
        self.assertTrue(datasourceapi.insert_datasource_by_features(did, info))
        for i in range(1,1000):
            feat = zlib.adler32(bytes('test_delete_datasource_by_features_success_batch'+str(i),'utf-8'))
            the_ds = datasourceapi.get_datasources_by_feature(feat, count=1)
            self.assertEqual(len(the_ds),1)
            self.assertEqual(the_ds[0].did,did)
        self.assertTrue(datasourceapi.delete_datasource_by_features(did, [item['feature'] for item in info]))
        for i in range(1,1000):
            feat = zlib.adler32(bytes('test_delete_datasource_by_features_success_batch'+str(i),'utf-8'))
            the_ds = datasourceapi.get_datasources_by_feature(feat, count=1)
            self.assertEqual(len(the_ds),0)

