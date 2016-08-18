import unittest
from komlog.komcass.api import segment as segmentapi
from komlog.komcass.model.orm import segment as ormsegment


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

