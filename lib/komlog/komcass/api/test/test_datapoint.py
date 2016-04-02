import unittest
import uuid
import decimal
from komlog.komlibs.general.time import timeuuid
from komlog.komcass.api import datapoint as datapointapi
from komlog.komcass.model.orm import datapoint as ormdatapoint


class KomcassApiDatapointTest(unittest.TestCase):
    ''' komlog.komcass.api.datapoint tests '''

    def setUp(self):
        pid1=uuid.uuid4()
        pid2=uuid.uuid4()
        did=uuid.uuid4()
        datapointname='test_komlog.komcass.api.datapoint_datapoint1'
        datapointname='test_komlog.komcass.api.datapoint_datapoint2'
        creation_date=timeuuid.uuid1()
        self.datapoint1=ormdatapoint.Datapoint(pid=pid1, did=did, creation_date=creation_date, datapointname=datapointname)
        self.datapoint2=ormdatapoint.Datapoint(pid=pid2, did=did, creation_date=creation_date, datapointname=datapointname)
        datapointapi.insert_datapoint(self.datapoint1)
        datapointapi.insert_datapoint(self.datapoint2)
        datapointapi.set_datapoint_last_received(pid1,creation_date)
        datapointapi.set_datapoint_decimal_separator(pid1,',')

    def test_get_datapoint_existing_pid(self):
        ''' get_datapoint should succeed if we pass an existing pid '''
        pid=self.datapoint1.pid
        datapoint=datapointapi.get_datapoint(pid=pid)
        self.assertEqual(datapoint.pid, self.datapoint1.pid)
        self.assertEqual(datapoint.did, self.datapoint1.did)
        self.assertEqual(datapoint.datapointname, self.datapoint1.datapointname)

    def test_get_datapoint_non_existing_pid(self):
        ''' get_datapoint should return None if we pass a non existing pid '''
        pid=uuid.uuid4()
        self.assertIsNone(datapointapi.get_datapoint(pid=pid))

    def test_get_datapoints_existing_did(self):
        ''' get_datapoints should succeed if we pass an existing did '''
        did=self.datapoint1.did
        datapoints=datapointapi.get_datapoints(did=did)
        self.assertEqual(len(datapoints),2)
        for datapoint in datapoints:
            self.assertTrue(isinstance(datapoint, ormdatapoint.Datapoint))

    def test_get_datapoints_non_existing_did(self):
        ''' get_datapoints should return an empty array if we pass a non existing did '''
        did=uuid.uuid4()
        datapoints=datapointapi.get_datapoints(did=did)
        self.assertTrue(isinstance(datapoints,list))
        self.assertEqual(len(datapoints),0)

    def test_get_number_of_datapoints_by_did_success(self):
        ''' get_number_of_datapoints_by_did should return the number of datapoints belonging to a did '''
        did=self.datapoint1.did
        num_datapoints=datapointapi.get_number_of_datapoints_by_did(did)
        self.assertEqual(num_datapoints, 2)

    def test_get_number_of_datapoints_by_did_no_datapoints(self):
        ''' get_number_of_datapoints by did should return the number of datapoints belonging to a did '''
        did=uuid.uuid4()
        num_datapoints=datapointapi.get_number_of_datapoints_by_did(did)
        self.assertEqual(num_datapoints, 0)

    def test_get_datapoint_stats_existing_pid(self):
        ''' get_datapoint_stats should succeed if we pass an existing pid '''
        pid=self.datapoint1.pid
        datapoint_stats=datapointapi.get_datapoint_stats(pid=pid)
        self.assertTrue(isinstance(datapoint_stats,ormdatapoint.DatapointStats))
        self.assertEqual(datapoint_stats.pid, self.datapoint1.pid)

    def test_get_datapoint_stats_non_existing_pid(self):
        ''' get_datapoint_stats should return None if we pass a non existing pid '''
        pid=uuid.uuid4()
        self.assertIsNone(datapointapi.get_datapoint_stats(pid=pid))

    def test_get_datapoint_dtree_positives_existing_pid(self):
        ''' get_datapoint_dtree_positives should succeed if we pass an existing pid '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=0
        length=1
        datapointapi.set_datapoint_dtree_positive_at(pid=pid, date=date, position=position, length=length)
        date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-600)
        position=45
        length=1
        datapointapi.set_datapoint_dtree_positive_at(pid=pid, date=date, position=position, length=length)
        datapoint_dtree_positives=datapointapi.get_datapoint_dtree_positives(pid=pid)
        self.assertTrue(isinstance(datapoint_dtree_positives,list))
        self.assertEqual(len(datapoint_dtree_positives),2)
        for positive in datapoint_dtree_positives:
            self.assertTrue(isinstance(positive, ormdatapoint.DatapointDtreePositives))

    def test_get_datapoint_dtree_positives_non_existing_pid(self):
        ''' get_datapoint_dtree_positives should return an empty list if we pass a non existing pid '''
        pid=uuid.uuid4()
        datapoint_dtree_positives=datapointapi.get_datapoint_dtree_positives(pid=pid)
        self.assertTrue(isinstance(datapoint_dtree_positives,list))
        self.assertEqual(len(datapoint_dtree_positives),0)

    def test_get_datapoint_dtree_positives_at_existing_pid_one_positive(self):
        ''' get_datapoint_dtree_positives_at should succeed if we pass an existing pid '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=0
        length=1
        datapointapi.set_datapoint_dtree_positive_at(pid=pid, date=date, position=position, length=length)
        date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-600)
        position=45
        length=1
        datapointapi.set_datapoint_dtree_positive_at(pid=pid, date=date, position=position, length=length)
        datapoint_dtree_positives=datapointapi.get_datapoint_dtree_positives_at(pid=pid, date=date)
        self.assertTrue(isinstance(datapoint_dtree_positives,ormdatapoint.DatapointDtreePositives))
        self.assertEqual(datapoint_dtree_positives.pid, pid)

    def test_get_datapoint_dtree_positives_at_existing_pid_no_positive(self):
        ''' get_datapoint_dtree_positives_at should succeed if we pass an existing pid, but return None if no positive is found at that date'''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=0
        length=1
        datapointapi.set_datapoint_dtree_positive_at(pid=pid, date=date, position=position, length=length)
        date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-600)
        position=45
        length=1
        datapointapi.set_datapoint_dtree_positive_at(pid=pid, date=date, position=position, length=length)
        date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-1200)
        datapoint_dtree_positives=datapointapi.get_datapoint_dtree_positives_at(pid=pid, date=date)
        self.assertIsNone(datapoint_dtree_positives)

    def test_get_datapoint_dtree_positives_non_existing_pid(self):
        ''' get_datapoint_dtree_positives_at should return None if we pass a non existing pid '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        datapoint_dtree_positives=datapointapi.get_datapoint_dtree_positives_at(pid=pid, date=date)
        self.assertIsNone(datapoint_dtree_positives)

    def test_get_datapoint_dtree_negatives_existing_pid(self):
        ''' get_datapoint_dtree_negatives should succeed if we pass an existing pid '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=0
        length=1
        datapointapi.add_datapoint_dtree_negative_at(pid=pid, date=date, position=position, length=length)
        datapointapi.add_datapoint_dtree_negative_at(pid=pid, date=date, position=position+10, length=length)
        date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-600)
        position=45
        length=1
        datapointapi.add_datapoint_dtree_negative_at(pid=pid, date=date, position=position, length=length)
        datapoint_dtree_negatives=datapointapi.get_datapoint_dtree_negatives(pid=pid)
        self.assertTrue(isinstance(datapoint_dtree_negatives,list))
        self.assertEqual(len(datapoint_dtree_negatives),2)
        for negative in datapoint_dtree_negatives:
            self.assertTrue(isinstance(negative, ormdatapoint.DatapointDtreeNegatives))

    def test_get_datapoint_dtree_negatives_non_existing_pid(self):
        ''' get_datapoint_dtree_negatives should return an empty list if we pass a non existing pid '''
        pid=uuid.uuid4()
        datapoint_dtree_negatives=datapointapi.get_datapoint_dtree_negatives(pid=pid)
        self.assertTrue(isinstance(datapoint_dtree_negatives,list))
        self.assertEqual(len(datapoint_dtree_negatives),0)

    def test_get_datapoint_dtree_negatives_at_existing_pid_one_negative(self):
        ''' get_datapoint_dtree_negatives_at should succeed if we pass an existing pid '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=0
        length=1
        datapointapi.add_datapoint_dtree_negative_at(pid=pid, date=date, position=position, length=length)
        date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-600)
        position=45
        length=1
        datapointapi.add_datapoint_dtree_negative_at(pid=pid, date=date, position=position, length=length)
        datapointapi.add_datapoint_dtree_negative_at(pid=pid, date=date, position=position+4, length=length)
        datapoint_dtree_negatives=datapointapi.get_datapoint_dtree_negatives_at(pid=pid, date=date)
        self.assertTrue(isinstance(datapoint_dtree_negatives,ormdatapoint.DatapointDtreeNegatives))
        self.assertEqual(datapoint_dtree_negatives.pid, pid)
        self.assertEqual(datapoint_dtree_negatives.coordinates,{position:length,position+4:length})

    def test_get_datapoint_dtree_negatives_at_existing_pid_no_negatives(self):
        ''' get_datapoint_dtree_negatives_at should succeed if we pass an existing pid, but return None if no positive is found at that date'''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=0
        length=1
        datapointapi.add_datapoint_dtree_negative_at(pid=pid, date=date, position=position, length=length)
        date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-600)
        position=45
        length=1
        datapointapi.add_datapoint_dtree_negative_at(pid=pid, date=date, position=position, length=length)
        date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-1200)
        datapoint_dtree_negatives=datapointapi.get_datapoint_dtree_negatives_at(pid=pid, date=date)
        self.assertIsNone(datapoint_dtree_negatives)

    def test_get_datapoint_dtree_negatives_non_existing_pid(self):
        ''' get_datapoint_dtree_negatives_at should return None if we pass a non existing pid '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        datapoint_dtree_negatives=datapointapi.get_datapoint_dtree_negatives_at(pid=pid, date=date)
        self.assertIsNone(datapoint_dtree_negatives)

    def test_new_datapoint_no_datapoint_object(self):
        ''' new_datapoint should fail if no datapoint object is passed '''
        datapoints=[None, 234234, '12313514123', {'a':'dict'},['a','list']]
        for datapoint in datapoints:
            self.assertFalse(datapointapi.new_datapoint(datapoint))

    def test_new_datapoint_already_existing_pid(self):
        ''' new_datapoint should fail if pid already exists '''
        datapoint=self.datapoint1
        self.assertFalse(datapointapi.new_datapoint(datapoint))

    def test_new_datapoint_success(self):
        ''' new_datapoint should succeed if argument is a datapoint object and datapoint does not exist'''
        pid=uuid.uuid4()
        did=uuid.uuid4()
        datapointname='test_new_datapoint_success_datapoint'
        creation_date=timeuuid.uuid1()
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(datapointapi.new_datapoint(datapoint))
        datapoint_db=datapointapi.get_datapoint(pid=pid)
        self.assertTrue(isinstance(datapoint_db,ormdatapoint.Datapoint))
        self.assertEqual(datapoint.pid, datapoint_db.pid)
 
    def test_insert_datapoint_no_datapoint_object(self):
        ''' insert_datapoint should fail if no datapoint object is passed '''
        datapoints=[None, 234234, '12313514123', {'a':'dict'},['a','list']]
        for datapoint in datapoints:
            self.assertFalse(datapointapi.insert_datapoint(datapoint))

    def test_insert_datapoint_already_existing_pid(self):
        ''' insert_datapoint should succeed even if pid already exists '''
        datapoint=self.datapoint1
        self.assertTrue(datapointapi.insert_datapoint(datapoint))

    def test_insert_datapoint_success(self):
        ''' insert_datapoint should succeed if argument is a datapoint object and datapoint does not exist'''
        pid=uuid.uuid4()
        did=uuid.uuid4()
        datapointname='test_insert_datapoint_success_datapoint'
        creation_date=timeuuid.uuid1()
        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, creation_date=creation_date, datapointname=datapointname)
        self.assertTrue(datapointapi.insert_datapoint(datapoint))
        datapoint_db=datapointapi.get_datapoint(pid=pid)
        self.assertTrue(isinstance(datapoint_db,ormdatapoint.Datapoint))
        self.assertEqual(datapoint.pid, datapoint_db.pid)
 
    def test_insert_datapoint_data_success(self):
        ''' insert_datapoint_data should succeed '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        value=decimal.Decimal(234223.2342342)
        self.assertTrue(datapointapi.insert_datapoint_data(pid=pid, date=date, value=value))
        data=datapointapi.get_datapoint_data_at(pid=pid, date=date)
        self.assertEqual(data.date,date)
        self.assertEqual(data.value,value)
        self.assertEqual(data.pid,pid)
 
    def test_delete_datapoint_data_at_success_non_existent_data(self):
        ''' delete_datapoint_data_at should succeed even if data does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertTrue(datapointapi.delete_datapoint_data_at(pid=pid, date=date))

    def test_delete_datapoint_data_at_success_existent_data(self):
        ''' delete_datapoint_data_at should succeed even if data exists '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        value=decimal.Decimal(234223.2342342)
        self.assertTrue(datapointapi.insert_datapoint_data(pid=pid, date=date, value=value))
        data=datapointapi.get_datapoint_data_at(pid=pid, date=date)
        self.assertEqual(data.date,date)
        self.assertEqual(data.value,value)
        self.assertEqual(data.pid,pid)
        self.assertTrue(datapointapi.delete_datapoint_data_at(pid=pid, date=date))
        self.assertIsNone(datapointapi.get_datapoint_data_at(pid=pid, date=date))

    def test_delete_datapoint_data_success_non_existent_data(self):
        ''' delete_datapoint_data should succeed even if data does not exist '''
        pid=uuid.uuid4()
        self.assertTrue(datapointapi.delete_datapoint_data(pid=pid))

    def test_delete_datapoint_data_success_existent_data(self):
        ''' delete_datapoint_data should succeed even if data exists '''
        pid=uuid.uuid4()
        for i in range(0,100):
            date=timeuuid.uuid1()
            value=decimal.Decimal(i)
            self.assertTrue(datapointapi.insert_datapoint_data(pid=pid, date=date, value=value))
            data=datapointapi.get_datapoint_data_at(pid=pid, date=date)
            self.assertEqual(data.date,date)
            self.assertEqual(data.value,value)
            self.assertEqual(data.pid,pid)
        self.assertTrue(datapointapi.delete_datapoint_data(pid=pid))
        self.assertEqual(datapointapi.get_datapoint_data(pid=pid, fromdate=timeuuid.uuid1(seconds=1), todate=timeuuid.uuid1()),[])

    def test_set_datapoint_last_received_success(self):
        ''' set_datapoint_last_received should succeed '''
        pid=uuid.uuid4()
        last_received=timeuuid.uuid1()
        self.assertTrue(datapointapi.set_datapoint_last_received(pid=pid, last_received=last_received))
 
    def test_set_datapoint_dtree_success(self):
        ''' set_datapoint_dtree should succeed '''
        pid=uuid.uuid4()
        dtree='valid string'
        self.assertTrue(datapointapi.set_datapoint_dtree(pid=pid, dtree=dtree))
 
    def test_set_datapoint_decimal_separator_success(self):
        ''' set_datapoint_decimal_separator should succeed if decimal separator is , or . '''
        pid=uuid.uuid4()
        decimal_separators=[',','.']
        for d in decimal_separators:
            self.assertTrue(datapointapi.set_datapoint_decimal_separator(pid=pid, decimal_separator=d))

    def test_delete_datapoint_success_non_existent_pid(self):
        ''' delete_datapoint should succeed even if pid does not exist '''
        pid=uuid.uuid4()
        self.assertTrue(datapointapi.delete_datapoint(pid=pid))

    def test_delete_datapoint_success_existent_pid(self):
        ''' delete_datapoint should succeed even if pid does not exist '''
        datapoint=ormdatapoint.Datapoint(pid=uuid.uuid4(), did=uuid.uuid4())
        self.assertTrue(datapointapi.insert_datapoint(datapoint))
        self.assertIsNotNone(datapointapi.get_datapoint(pid=datapoint.pid))
        self.assertTrue(datapointapi.delete_datapoint(pid=datapoint.pid))
        self.assertIsNone(datapointapi.get_datapoint(pid=datapoint.pid))

    def test_set_datapoint_dtree_positive_at_success(self):
        ''' set_datapoint_dtree_positive_at should succeed even if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=0
        length=1
        self.assertTrue(datapointapi.set_datapoint_dtree_positive_at(pid=pid,date=date,position=position,length=length))

    def test_add_datapoint_dtree_negative_at_success(self):
        ''' add_datapoint_dtree_negative_at should succeed even if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=0
        length=1
        self.assertTrue(datapointapi.add_datapoint_dtree_negative_at(pid=pid,date=date,position=position,length=length))

    def test_delete_datapoint_dtree_positive_at_success(self):
        ''' delete_datapoint_dtree_positive_at should succeed even if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertTrue(datapointapi.delete_datapoint_dtree_positive_at(pid=pid,date=date))

    def test_delete_datapoint_dtree_negatives_at_success(self):
        ''' delete_datapoint_dtree_negatives_at should succeed even if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertTrue(datapointapi.delete_datapoint_dtree_negatives_at(pid=pid,date=date))

    def test_delete_datapoint_dtree_negative_at_success(self):
        ''' delete_datapoint_dtree_negative_at should succeed even if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=0
        self.assertTrue(datapointapi.delete_datapoint_dtree_negative_at(pid=pid,date=date,position=position))

    def test_delete_datapoint_stats_success_non_existent_pid(self):
        ''' delete_datapoint_stats should succeed even if pid does not exist '''
        pid=uuid.uuid4()
        self.assertTrue(datapointapi.delete_datapoint_stats(pid=pid))

    def test_delete_datapoint_stats_success_existent_pid(self):
        ''' delete_datapoint_stats should succeed if pid exists '''
        pid=uuid.uuid4()
        last_received=timeuuid.uuid1()
        self.assertTrue(datapointapi.set_datapoint_last_received(pid=pid, last_received=last_received))
        self.assertIsNotNone(datapointapi.get_datapoint_stats(pid=pid))
        self.assertTrue(datapointapi.delete_datapoint_stats(pid=pid))
        self.assertIsNone(datapointapi.get_datapoint_stats(pid=pid))

    def test_get_datapoint_data_at_non_existing_pid(self):
        ''' get_datapoint_data_at should return None if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(datapointapi.get_datapoint_data_at(pid=pid, date=date))

    def test_get_datapoint_data_at_existing_pid_but_no_data_at_this_date(self):
        ''' get_datapoint_data_at should return None if there is no data at this date '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        value=decimal.Decimal(12312.123123)
        datapointapi.insert_datapoint_data(pid=pid, date=date, value=value)
        date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-600)
        self.assertIsNone(datapointapi.get_datapoint_data_at(pid=pid, date=date))

    def test_get_datapoint_data_at_success(self):
        ''' get_datapoint_data_at should return DatapointData structure with the data '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        value=decimal.Decimal(12312.123123)
        datapointapi.insert_datapoint_data(pid=pid, date=date, value=value)
        data=datapointapi.get_datapoint_data_at(pid=pid, date=date)
        self.assertTrue(isinstance(data, ormdatapoint.DatapointData))
        self.assertEqual(data.value, value)
        self.assertEqual(data.pid, pid)

    def test_get_datapoint_data_non_existing_pid(self):
        ''' get_datapoint_data should return an empty list if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        fromdate=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-6000)
        data=datapointapi.get_datapoint_data(pid=pid, fromdate=fromdate, todate=date)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data),0)


    def test_get_datapoint_data_existing_pid_but_no_data_at_this_interval(self):
        ''' get_datapoint_data should return an empty list if there is no data at this date '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        value=decimal.Decimal(12312.123123)
        datapointapi.insert_datapoint_data(pid=pid, date=date, value=value)
        fromdate=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-6000)
        date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-600)
        data=datapointapi.get_datapoint_data(pid=pid, fromdate=fromdate, todate=date)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data),0)

    def test_get_datapoint_data_success(self):
        ''' get_datapoint_data should return a list with DatapointData structures '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        match_date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-300)
        value=decimal.Decimal('12312.123123')
        datapointapi.insert_datapoint_data(pid=pid, date=match_date, value=value)
        datapointapi.insert_datapoint_data(pid=pid, date=date, value=value)
        fromdate=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-6000)
        todate=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)-240)
        data=datapointapi.get_datapoint_data(pid=pid, fromdate=fromdate, todate=todate)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data),1)
        self.assertTrue('date' in data[0])
        self.assertTrue('value' in data[0])
        self.assertEqual(data[0]['date'],match_date)
        self.assertEqual(data[0]['value'],value)

