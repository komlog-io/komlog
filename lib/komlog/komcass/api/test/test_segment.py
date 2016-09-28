import unittest
import uuid
import decimal
from komlog.komcass.api import segment as segmentapi
from komlog.komcass.model.orm import segment as ormsegment
from komlog.komlibs.general.time import timeuuid


class KomcassApiSegmentTest(unittest.TestCase):
    ''' komlog.komcass.api.segment tests '''

    def test_get_user_segment_non_found(self):
        ''' get_user_segment should return None if sid is not found '''
        self.assertIsNone(segmentapi.get_user_segment(sid=-1))

    def test_get_user_segment_found(self):
        ''' get_user_segment should return a UserSegment object with the segment '''
        sid=99999999
        description='Test segment'
        segment=ormsegment.UserSegment(sid=sid, description=description)
        self.assertTrue(segmentapi.insert_user_segment(segment))
        db_segment=segmentapi.get_user_segment(sid=sid)
        self.assertEqual(segment.sid, sid)
        self.assertEqual(segment.description, description)
        self.assertTrue(segmentapi.delete_user_segment(sid=sid))

    def test_insert_user_segment_failure(self):
        ''' insert_user_segment should fail if segment is not a UserSegment object '''
        sid=999999990
        description='Test segment'
        segment=ormsegment.UserSegment(sid=sid, description=description)
        self.assertTrue(segmentapi.insert_user_segment(segment))
        db_segment=segmentapi.get_user_segment(sid=sid)
        self.assertEqual(segment.sid, sid)
        self.assertEqual(segment.description, description)
        self.assertTrue(segmentapi.delete_user_segment(sid=sid))

    def test_insert_user_segment_success(self):
        ''' insert_user_segment should succeed and insert the object '''
        sid=999999990
        description='Test segment'
        segment=ormsegment.UserSegment(sid=sid, description=description)
        self.assertTrue(segmentapi.insert_user_segment(segment))
        db_segment=segmentapi.get_user_segment(sid=sid)
        self.assertEqual(segment.sid, sid)
        self.assertEqual(segment.description, description)
        self.assertTrue(segmentapi.delete_user_segment(sid=sid))

    def test_delete_user_segment_success_non_existent_segment(self):
        ''' delete_user_segment should return True even if segment does not exist '''
        sid=999999900
        self.assertIsNone(segmentapi.get_user_segment(sid=sid))
        self.assertTrue(segmentapi.delete_user_segment(sid=sid))

    def test_delete_user_segment_success_existent_segment(self):
        ''' delete_user_segment should succeed and delete the segment '''
        sid=999999890
        description='Test segment'
        segment=ormsegment.UserSegment(sid=sid, description=description)
        self.assertTrue(segmentapi.insert_user_segment(segment))
        db_segment=segmentapi.get_user_segment(sid=sid)
        self.assertEqual(segment.sid, sid)
        self.assertEqual(segment.description, description)
        self.assertTrue(segmentapi.delete_user_segment(sid=sid))
        self.assertIsNone(segmentapi.get_user_segment(sid=sid))

    def test_get_user_segment_quotes_non_existing_sid(self):
        ''' get_user_segment_quotes should return an empty array if sid does not exist '''
        sid=1000
        self.assertEqual(segmentapi.get_user_segment_quotes(sid=sid), [])

    def test_get_user_segment_quotes_existing_segment(self):
        ''' get_user_segment_quotes should return an array with UserSegmentQuo objects '''
        sid=1001
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        for quote,value in quotes.items():
            self.assertTrue(segmentapi.insert_user_segment_quote(sid,quote,value))
        quotes_db=segmentapi.get_user_segment_quotes(sid=sid)
        self.assertEqual(len(quotes_db),3)
        quotes_set=set(quotes.keys())
        for quote in quotes_db:
            self.assertTrue(isinstance(quote, ormsegment.UserSegmentQuo))
            self.assertEqual(quote.sid, sid)
            self.assertTrue(quote.quote in quotes_set)
            self.assertEqual(quote.value,quotes[quote.quote])
            quotes_set.remove(quote.quote)

    def test_get_user_segment_quote_existing_quote(self):
        ''' get_user_segment_quotes should return the UserSegmentQuo objects if quote exists '''
        sid=1002
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        for quote,value in quotes.items():
            self.assertTrue(segmentapi.insert_user_segment_quote(sid,quote,value))
        quote_db=segmentapi.get_user_segment_quote(sid=sid, quote='quote1')
        self.assertTrue(isinstance(quote_db, ormsegment.UserSegmentQuo))
        self.assertEqual(quote_db.sid, sid)
        self.assertEqual(quote_db.quote,'quote1')
        self.assertEqual(quote_db.value,quotes['quote1'])

    def test_get_user_segment_quote_non_existing_quote(self):
        ''' get_user_segment_quotes should return None if quote does not exist '''
        sid=1003
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        for quote,value in quotes.items():
            self.assertTrue(segmentapi.insert_user_segment_quote(sid,quote,value))
        quote_db=segmentapi.get_user_segment_quote(sid=sid, quote='quote4')
        self.assertIsNone(quote_db)

    def test_insert_user_segment_quote_non_previously_existing_quote(self):
        ''' insert_user_segment_quote should insert the quote if it did not exist previously '''
        sid=1004
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        self.assertEqual(segmentapi.get_user_segment_quotes(sid),[])
        for quote,value in quotes.items():
            self.assertTrue(segmentapi.insert_user_segment_quote(sid,quote,value))
        quote_db=segmentapi.get_user_segment_quote(sid=sid, quote='quote1')
        self.assertTrue(isinstance(quote_db, ormsegment.UserSegmentQuo))
        self.assertEqual(quote_db.sid, sid)
        self.assertEqual(quote_db.quote,'quote1')
        self.assertEqual(quote_db.value,quotes['quote1'])

    def test_insert_user_segment_quote_previously_existing_quote(self):
        ''' insert_user_segment_quote should update the quote if it did exist previously '''
        sid=1005
        quote='quote1'
        value=1
        self.assertEqual(segmentapi.get_user_segment_quotes(sid),[])
        self.assertTrue(segmentapi.insert_user_segment_quote(sid,quote,value))
        quote_db=segmentapi.get_user_segment_quote(sid=sid, quote=quote)
        self.assertTrue(isinstance(quote_db, ormsegment.UserSegmentQuo))
        self.assertEqual(quote_db.sid, sid)
        self.assertEqual(quote_db.quote,quote)
        self.assertEqual(quote_db.value,value)
        new_value=5
        self.assertTrue(segmentapi.insert_user_segment_quote(sid,quote,new_value))
        quote_db=segmentapi.get_user_segment_quote(sid=sid, quote=quote)
        self.assertTrue(isinstance(quote_db, ormsegment.UserSegmentQuo))
        self.assertEqual(quote_db.sid, sid)
        self.assertEqual(quote_db.quote,quote)
        self.assertEqual(quote_db.value,new_value)

    def test_delete_user_segment_quote_already_existing_quote(self):
        ''' delete_user_segment_quote should return True and delete the Segment quote if exists '''
        sid=1006
        quote='quote'
        value=1
        self.assertTrue(segmentapi.insert_user_segment_quote(sid,quote,value))
        quote_db=segmentapi.get_user_segment_quote(sid=sid, quote=quote)
        self.assertTrue(isinstance(quote_db, ormsegment.UserSegmentQuo))
        self.assertEqual(quote_db.sid, sid)
        self.assertEqual(quote_db.quote,quote)
        self.assertEqual(quote_db.value,value)
        self.assertTrue(segmentapi.delete_user_segment_quote(sid,quote))
        self.assertIsNone(segmentapi.get_user_segment_quote(sid, quote))

    def test_delete_user_segment_quote_non_existing_quote(self):
        ''' delete_user_segment_quote should return True even if quote does not exist '''
        sid=1007
        quote='quote'
        value=1
        self.assertTrue(segmentapi.insert_user_segment_quote(sid,quote,value))
        non_existing_quote='non_quote'
        self.assertIsNone(segmentapi.get_user_segment_quote(sid, non_existing_quote))
        self.assertTrue(segmentapi.delete_user_segment_quote(sid,non_existing_quote))
        self.assertIsNone(segmentapi.get_user_segment_quote(sid, non_existing_quote))
        db_quotes=segmentapi.get_user_segment_quotes(sid)
        self.assertEqual(len(db_quotes),1)
        self.assertEqual(db_quotes[0].sid,sid)
        self.assertEqual(db_quotes[0].quote,quote)
        self.assertEqual(db_quotes[0].value,value)

    def test_delete_user_segment_quote_non_existing_segment(self):
        ''' delete_user_segment_quote should return True '''
        sid=1008
        quote='quote'
        value=1
        self.assertEqual(segmentapi.get_user_segment_quotes(sid),[] )
        self.assertIsNone(segmentapi.get_user_segment_quote(sid, quote))
        self.assertTrue(segmentapi.delete_user_segment_quote(sid=sid,quote=quote))
        self.assertEqual(segmentapi.get_user_segment_quotes(sid),[] )

    def test_delete_user_segment_quotes_already_existing_quotes(self):
        ''' delete_user_segment_quotes should return True and delete the Segment quotes if exist '''
        sid=1009
        quotes={'quote1':1, 'quote2':2, 'quote3':3}
        for quote,value in quotes.items():
            self.assertTrue(segmentapi.insert_user_segment_quote(sid,quote,value))
        quotes_db=segmentapi.get_user_segment_quotes(sid=sid)
        self.assertEqual(len(quotes_db),3)
        self.assertTrue(segmentapi.delete_user_segment_quotes(sid))
        self.assertEqual(segmentapi.get_user_segment_quotes(sid),[])

    def test_delete_user_segment_quotes_non_existing_quotes(self):
        ''' delete_user_segment_quotes should return True and delete the Segment quotes if exist '''
        sid=1010
        self.assertEqual(segmentapi.get_user_segment_quotes(sid),[])
        self.assertTrue(segmentapi.delete_user_segment_quotes(sid))
        self.assertEqual(segmentapi.get_user_segment_quotes(sid),[])

    def test_get_user_segment_transition_non_existent(self):
        ''' get_user_segment_transition should return None if no transition exist '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertIsNone(segmentapi.get_user_segment_transition(uid=uid, date=date))

    def test_get_user_segment_transition_existent(self):
        ''' get_user_segment_transition should return  the UserSegmentTransition object '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        sid = 0
        previous_sid = None
        self.assertTrue(segmentapi.insert_user_segment_transition(uid=uid, date=date, sid=sid, previous_sid=previous_sid))
        transition=segmentapi.get_user_segment_transition(uid=uid, date=date)
        self.assertEqual(transition.uid, uid)
        self.assertEqual(transition.date, date)
        self.assertEqual(transition.sid, sid)
        self.assertEqual(transition.previous_sid, previous_sid)

    def test_get_user_segment_transitions_non_existent(self):
        ''' get_user_segment_transitions should return an empty array if no transition is found '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertEqual(segmentapi.get_user_segment_transitions(uid=uid),[])
        self.assertEqual(segmentapi.get_user_segment_transitions(uid=uid, init_date=timeuuid.uuid1()),[])
        self.assertEqual(segmentapi.get_user_segment_transitions(uid=uid, end_date=timeuuid.uuid1()),[])
        self.assertEqual(segmentapi.get_user_segment_transitions(uid=uid, init_date=timeuuid.uuid1(), end_date=timeuuid.uuid1()),[])

    def test_get_user_segment_transitions_existent(self):
        ''' get_user_segment_transitions should return an the transitions '''
        uid=uuid.uuid4()
        for i in range(1,10):
            date=timeuuid.uuid1(seconds=i)
            sid=i
            previous_sid = i-1
            self.assertTrue(segmentapi.insert_user_segment_transition(uid=uid, date=date, sid=sid, previous_sid=previous_sid))
        self.assertEqual(len(segmentapi.get_user_segment_transitions(uid=uid)),9)
        self.assertEqual(len(segmentapi.get_user_segment_transitions(uid=uid, init_date=timeuuid.min_uuid_from_time(5))),5)
        self.assertEqual(len(segmentapi.get_user_segment_transitions(uid=uid, end_date=timeuuid.max_uuid_from_time(5))),5)
        self.assertEqual(len(segmentapi.get_user_segment_transitions(uid=uid, init_date=timeuuid.min_uuid_from_time(5), end_date=timeuuid.max_uuid_from_time(5))),1)

    def test_insert_user_segment_transition(self):
        ''' insert_user_segment_transition should succeed and insert the values '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        sid=0
        previous_sid=0
        self.assertTrue(segmentapi.insert_user_segment_transition(uid=uid, date=date, sid=sid, previous_sid=previous_sid))
        transition = segmentapi.get_user_segment_transition(uid=uid, date=date)
        self.assertEqual(transition.uid, uid)
        self.assertEqual(transition.date, date)
        self.assertEqual(transition.sid, sid)
        self.assertEqual(transition.previous_sid, previous_sid)

    def test_delete_user_segment_transition_non_existent_transition(self):
        ''' delete_user_segment_transition should return true even if it does not exist '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertTrue(segmentapi.delete_user_segment_transition(uid=uid, date=date))

    def test_delete_user_segment_transition_existent_transition(self):
        ''' delete_user_segment_transition should delete and return True if transition exists '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        sid=0
        previous_sid=0
        self.assertTrue(segmentapi.insert_user_segment_transition(uid=uid, date=date, sid=sid, previous_sid=previous_sid))
        transition = segmentapi.get_user_segment_transition(uid=uid, date=date)
        self.assertEqual(transition.uid, uid)
        self.assertEqual(transition.date, date)
        self.assertEqual(transition.sid, sid)
        self.assertEqual(transition.previous_sid, previous_sid)
        self.assertTrue(segmentapi.delete_user_segment_transition(uid=uid, date=date))
        self.assertIsNone(segmentapi.get_user_segment_transition(uid=uid, date=date))

    def test_delete_user_segment_transitions(self):
        ''' get_user_segment_transitions should return an the transitions '''
        uid=uuid.uuid4()
        for i in range(1,10):
            date=timeuuid.uuid1(seconds=i)
            sid=i
            previous_sid = i-1
            self.assertTrue(segmentapi.insert_user_segment_transition(uid=uid, date=date, sid=sid, previous_sid=previous_sid))
        self.assertEqual(len(segmentapi.get_user_segment_transitions(uid=uid)),9)
        self.assertTrue(segmentapi.delete_user_segment_transitions(uid=uid, init_date=timeuuid.min_uuid_from_time(8)))
        self.assertEqual(len(segmentapi.get_user_segment_transitions(uid=uid)),7)
        self.assertEqual(len(segmentapi.get_user_segment_transitions(uid=uid, init_date=timeuuid.min_uuid_from_time(8))),0)
        self.assertTrue(segmentapi.delete_user_segment_transitions(uid=uid, end_date=timeuuid.max_uuid_from_time(2)))
        self.assertEqual(len(segmentapi.get_user_segment_transitions(uid=uid)),5)
        self.assertEqual(len(segmentapi.get_user_segment_transitions(uid=uid, end_date=timeuuid.max_uuid_from_time(2))),0)
        self.assertTrue(segmentapi.delete_user_segment_transitions(uid=uid, init_date=timeuuid.min_uuid_from_time(4), end_date=timeuuid.max_uuid_from_time(5)))
        self.assertEqual(len(segmentapi.get_user_segment_transitions(uid=uid)),3)
        self.assertEqual(len(segmentapi.get_user_segment_transitions(uid=uid, init_date = timeuuid.min_uuid_from_time(4), end_date=timeuuid.max_uuid_from_time(2))),0)
        self.assertTrue(segmentapi.delete_user_segment_transitions(uid=uid))
        self.assertEqual(len(segmentapi.get_user_segment_transitions(uid=uid)),0)

    def test_get_user_segment_allowed_transitions_non_existent(self):
        ''' get_user_segment_allowed_transitions should return None if no transition exist '''
        sid=999990
        self.assertIsNone(segmentapi.get_user_segment_allowed_transitions(sid=sid))

    def test_get_user_segment_allowed_transitions_existent(self):
        ''' get_user_segment_allowed_transitions should return  the UserSegmentAllowedTransition object '''
        sid=999999
        sids={23,43,2525,2423}
        self.assertTrue(segmentapi.insert_user_segment_allowed_transitions(sid=sid, sids=sids))
        transitions=segmentapi.get_user_segment_allowed_transitions(sid=sid)
        self.assertEqual(transitions.sid, sid)
        self.assertEqual(transitions.sids, sids)

    def test_insert_user_segment_allowed_transitions(self):
        ''' insert_user_segment_allowed_transition should succeed and insert the values '''
        sid=888888
        sids={43,52,12555,1432}
        self.assertTrue(segmentapi.insert_user_segment_allowed_transitions(sid=sid, sids=sids))
        transitions=segmentapi.get_user_segment_allowed_transitions(sid=sid)
        self.assertEqual(transitions.sid, sid)
        self.assertEqual(transitions.sids, sids)

    def test_delete_user_segment_allowed_transitions_non_existent_transition(self):
        ''' delete_user_segment_allowed_transitions should return true even if it does not exist '''
        sid=888880
        self.assertTrue(segmentapi.delete_user_segment_allowed_transitions(sid=sid))

    def test_delete_user_segment_allowed_transitions_existent_transition(self):
        ''' delete_user_segment_allowed_transitions should delete and return True if transition exists '''
        sid=888885
        sids={43,5,2212535,1432}
        self.assertTrue(segmentapi.insert_user_segment_allowed_transitions(sid=sid, sids=sids))
        transitions=segmentapi.get_user_segment_allowed_transitions(sid=sid)
        self.assertEqual(transitions.sid, sid)
        self.assertEqual(transitions.sids, sids)
        self.assertTrue(segmentapi.delete_user_segment_allowed_transitions(sid=sid))
        self.assertIsNone(segmentapi.get_user_segment_allowed_transitions(sid=sid))

    def test_get_user_segment_fare_non_existent(self):
        ''' get_user_segment_fare should return None if no entry exist '''
        sid=999990
        self.assertIsNone(segmentapi.get_user_segment_fare(sid=sid))

    def test_get_user_segment_fare_existent(self):
        ''' get_user_segment_fare should return  the UserSegmentAllowedTransition object '''
        sid=999999
        amount = decimal.Decimal('2234234')
        currency = 'USD'
        frequency = 'm'
        self.assertTrue(segmentapi.insert_user_segment_fare(sid=sid, amount=amount, currency=currency, frequency=frequency))
        fare=segmentapi.get_user_segment_fare(sid=sid)
        self.assertEqual(fare.sid, sid)
        self.assertEqual(fare.amount, amount)
        self.assertEqual(fare.currency, currency)
        self.assertEqual(fare.frequency, frequency)

    def test_insert_user_segment_fare(self):
        ''' insert_user_segment_allowed_transition should succeed and insert the values '''
        sid=888888
        amount = decimal.Decimal('22344')
        currency = 'USD'
        frequency = 'm'
        self.assertTrue(segmentapi.insert_user_segment_fare(sid=sid, amount=amount, currency=currency, frequency=frequency))
        fare=segmentapi.get_user_segment_fare(sid=sid)
        self.assertEqual(fare.sid, sid)
        self.assertEqual(fare.amount, amount)
        self.assertEqual(fare.currency, currency)
        self.assertEqual(fare.frequency, frequency)

    def test_delete_user_segment_fare_non_existent_fare(self):
        ''' delete_user_segment_fare should return true even if it does not exist '''
        sid=888880
        self.assertTrue(segmentapi.delete_user_segment_fare(sid=sid))

    def test_delete_user_segment_fare_existent_fare(self):
        ''' delete_user_segment_fare should delete and return True if fare exists '''
        sid=888885
        amount = decimal.Decimal('2.34')
        currency = 'EUR'
        frequency = 'm'
        self.assertTrue(segmentapi.insert_user_segment_fare(sid=sid, amount=amount, currency=currency, frequency=frequency))
        fare=segmentapi.get_user_segment_fare(sid=sid)
        self.assertEqual(fare.sid, sid)
        self.assertEqual(fare.amount, amount)
        self.assertEqual(fare.currency, currency)
        self.assertEqual(fare.frequency, frequency)
        self.assertTrue(segmentapi.delete_user_segment_fare(sid=sid))
        self.assertIsNone(segmentapi.get_user_segment_fare(sid=sid))

