import unittest
import time
import uuid
from komlibs.general.time import timeuuid
from komcass.api import datasource as datasourceapi
from komcass.model.orm import datasource as ormdatasource
from komfig import logger


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
        self.assertEqual(datasource.state, self.datasource1.state)

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
        state=0
        date=timeuuid.uuid1()
        datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=name, state=state, creation_date=date)
        self.assertTrue(datasourceapi.insert_datasource(datasource))
        datasource_db=datasourceapi.get_datasource(did=datasource.did)
        self.assertTrue(isinstance(datasource_db, ormdatasource.Datasource))
        self.assertEqual(datasource.did, datasource_db.did)
        self.assertEqual(datasource.aid, datasource_db.aid)
        self.assertEqual(datasource.uid, datasource_db.uid)
        self.assertEqual(datasource.datasourcename, datasource_db.datasourcename)
        self.assertEqual(datasource.state, datasource_db.state)

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
        state=0
        date=timeuuid.uuid1()
        datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=name, state=state, creation_date=date)
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

    def test_insert_datasource_map_success(self):
        ''' insert_datasource_map should succeed if a DatasourceMap object is passed'''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='TEST_INSERT_DATASOURCE_MAP_SUCCESS'
        datasourcemap=ormdatasource.DatasourceMap(did=did, date=date, content=content)
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
        ''' add_variable_to_datasource_map should succeed if all vars are passed and are correct '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        pid=uuid.uuid4()
        position=0
        self.assertTrue(datasourceapi.add_datapoint_to_datasource_map(did=did, date=date, pid=pid, position=position))

    def test_get_datasource_map_non_existing_map(self):
        ''' get_datasource_data_at should return None if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(datasourceapi.get_datasource_map(did=did, date=date))

    def test_get_datasource_map_success(self):
        ''' get_datasource_map should return DatapointMap structure with the map '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='TEST_GET_DATASOURCE_MAP_SUCCESS'
        dsmap=ormdatasource.DatasourceMap(did=did, date=date, content=content)
        self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        dsmap_db=datasourceapi.get_datasource_map(did=did, date=date)
        self.assertTrue(isinstance(dsmap_db,ormdatasource.DatasourceMap))
        self.assertEqual(dsmap.did, dsmap_db.did)
        self.assertEqual(dsmap.content, dsmap_db.content)
        self.assertEqual(dsmap.variables, dsmap_db.variables)
        self.assertEqual(dsmap.datapoints, dsmap_db.datapoints)

    def test_get_datasource_map_non_existing_maps(self):
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
        content='TEST_GET_DATASOURCE_MAPS_1_SUCCESS'
        dsmap=ormdatasource.DatasourceMap(did=did, date=fromdate, content=content)
        self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        todate=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(fromdate)+600)
        content='TEST_GET_DATASOURCE_MAPS_2_SUCCESS'
        dsmap=ormdatasource.DatasourceMap(did=did, date=todate, content=content)
        self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=dsmap))
        dsmaps_db=datasourceapi.get_datasource_maps(did=did, fromdate=fromdate, todate=todate)
        self.assertTrue(isinstance(dsmaps_db,list))
        self.assertEqual(len(dsmaps_db), 2)
        for amap in dsmaps_db:
            self.assertTrue(isinstance(amap,ormdatasource.DatasourceMap))
            self.assertEqual(amap.did, did)

    def test_get_datasource_map_success_testing_interval_limits(self):
        did=uuid.uuid4()
        init_interval=100
        end_interval=1000
        init_subinterval=250
        end_subinterval=750
        for i in range(init_interval, end_interval):
            data=ormdatasource.DatasourceMap(did=did, date=timeuuid.uuid1(seconds=i), content=str(i))
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
        self.assertTrue(isinstance(variables, dict))
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
        self.assertTrue(isinstance(datapoints, dict))
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
        content='TEST_DELETE_DATASOURCE_MAP_SUCCESS'
        datasourcemap=ormdatasource.DatasourceMap(did=did, date=date, content=content)
        self.assertTrue(datasourceapi.insert_datasource_map(dsmapobj=datasourcemap))
        data=datasourceapi.get_datasource_map(did=did, date=date)
        self.assertTrue(isinstance(data, ormdatasource.DatasourceMap))
        self.assertTrue(datasourceapi.delete_datasource_map(did=did, date=date))
        self.assertIsNone(datasourceapi.get_datasource_map(did=did, date=date))

