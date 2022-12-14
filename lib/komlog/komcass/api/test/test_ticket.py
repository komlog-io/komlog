import unittest
import time
import uuid
import random
from komlog.komlibs.general.time import timeuuid
from komlog.komcass.api import ticket as ticketapi
from komlog.komcass.model.orm import ticket as ormticket
from komlog.komcass.model.statement import ticket as stmtticket
from komlog.komcass import connection
from komlog.komfig import logging


class KomcassApiTicketTest(unittest.TestCase):
    ''' komlog.komcass.api.ticket tests '''

    def setUp(self):
        pass

    def test_get_ticket_non_existing_tid(self):
        ''' get_ticket should return None if tid does not exist '''
        tid=uuid.uuid4()
        self.assertIsNone(ticketapi.get_ticket(tid=tid))

    def test_get_ticket_success(self):
        ''' get_ticket should return a Ticket object '''
        tid=uuid.uuid4()
        date=uuid.uuid1()
        uid=uuid.uuid4()
        expires=uuid.uuid1()
        allowed_uids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        allowed_cids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        resources={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        permissions={uuid.uuid4():0,uuid.uuid4():3,uuid.uuid4():6}
        interval_init=uuid.uuid1()
        interval_end=uuid.uuid1()
        ticket=ormticket.Ticket(tid=tid,date=date,uid=uid,expires=expires,allowed_uids=allowed_uids,allowed_cids=allowed_cids,resources=resources,permissions=permissions,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(ticketapi.insert_ticket(ticket=ticket))
        db_ticket=ticketapi.get_ticket(tid=tid)
        self.assertEqual(db_ticket.tid,ticket.tid)
        self.assertEqual(db_ticket.date,ticket.date)
        self.assertEqual(db_ticket.uid,ticket.uid)
        self.assertEqual(db_ticket.expires,ticket.expires)
        self.assertEqual(db_ticket.allowed_uids,ticket.allowed_uids)
        self.assertEqual(db_ticket.allowed_cids,ticket.allowed_cids)
        self.assertEqual(db_ticket.resources,ticket.resources)
        self.assertEqual(db_ticket.permissions,ticket.permissions)
        self.assertEqual(db_ticket.interval_init,ticket.interval_init)
        self.assertEqual(db_ticket.interval_end,ticket.interval_end)

    def test_get_tickets_by_uid_non_existing_tickets(self):
        ''' get_tickets_by_uid should return an empty array if no tickets exist '''
        uid=uuid.uuid4()
        self.assertEqual(ticketapi.get_tickets_by_uid(uid=uid),[])

    def test_get_tickets_by_uid_success(self):
        ''' get_tickets_by_uid should return an array with the Ticket objects '''
        uid=uuid.uuid4()
        for i in range(1,100):
            tid=uuid.uuid4()
            date=uuid.uuid1()
            expires=uuid.uuid1()
            allowed_uids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
            allowed_cids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
            resources={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
            permissions={uuid.uuid4():0,uuid.uuid4():3,uuid.uuid4():6}
            interval_init=uuid.uuid1()
            interval_end=uuid.uuid1()
            ticket=ormticket.Ticket(tid=tid,date=date,uid=uid,expires=expires,allowed_uids=allowed_uids,allowed_cids=allowed_cids,resources=resources,permissions=permissions,interval_init=interval_init,interval_end=interval_end)
            self.assertTrue(ticketapi.insert_ticket(ticket=ticket))
        db_tickets=ticketapi.get_tickets_by_uid(uid=uid)
        self.assertEqual(len(db_tickets),99)

    def test_get_expired_ticket_non_existing_tid(self):
        ''' get_expired_ticket should return None if tid does not exist '''
        tid=uuid.uuid4()
        self.assertIsNone(ticketapi.get_expired_ticket(tid=tid))

    def test_get_expired_ticket_success(self):
        ''' get_expired_ticket should return a Ticket object '''
        tid=uuid.uuid4()
        date=uuid.uuid1()
        uid=uuid.uuid4()
        expires=uuid.uuid1()
        allowed_uids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        allowed_cids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        resources={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        permissions={uuid.uuid4():0,uuid.uuid4():3,uuid.uuid4():6}
        interval_init=uuid.uuid1()
        interval_end=uuid.uuid1()
        ticket=ormticket.Ticket(tid=tid,date=date,uid=uid,expires=expires,allowed_uids=allowed_uids,allowed_cids=allowed_cids,resources=resources,permissions=permissions,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(ticketapi.insert_expired_ticket(ticket=ticket))
        db_ticket=ticketapi.get_expired_ticket(tid=tid)
        self.assertEqual(db_ticket.tid,ticket.tid)
        self.assertEqual(db_ticket.date,ticket.date)
        self.assertEqual(db_ticket.uid,ticket.uid)
        self.assertEqual(db_ticket.expires,ticket.expires)
        self.assertEqual(db_ticket.allowed_uids,ticket.allowed_uids)
        self.assertEqual(db_ticket.allowed_cids,ticket.allowed_cids)
        self.assertEqual(db_ticket.resources,ticket.resources)
        self.assertEqual(db_ticket.permissions,ticket.permissions)
        self.assertEqual(db_ticket.interval_init,ticket.interval_init)
        self.assertEqual(db_ticket.interval_end,ticket.interval_end)

    def test_get_expired_tickets_by_uid_non_existing_tickets(self):
        ''' get_expired_tickets_by_uid should return an empty array if no tickets exist '''
        uid=uuid.uuid4()
        self.assertEqual(ticketapi.get_expired_tickets_by_uid(uid=uid),[])

    def test_get_expired_tickets_by_uid_success(self):
        ''' get_tickets_by_uid should return an array with the Ticket objects '''
        uid=uuid.uuid4()
        for i in range(1,100):
            tid=uuid.uuid4()
            date=uuid.uuid1()
            expires=uuid.uuid1()
            allowed_uids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
            allowed_cids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
            resources={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
            permissions={uuid.uuid4():0,uuid.uuid4():3,uuid.uuid4():6}
            interval_init=uuid.uuid1()
            interval_end=uuid.uuid1()
            ticket=ormticket.Ticket(tid=tid,date=date,uid=uid,expires=expires,allowed_uids=allowed_uids,allowed_cids=allowed_cids,resources=resources,permissions=permissions,interval_init=interval_init,interval_end=interval_end)
            self.assertTrue(ticketapi.insert_expired_ticket(ticket=ticket))
        db_tickets=ticketapi.get_expired_tickets_by_uid(uid=uid)
        self.assertEqual(len(db_tickets),99)

    def test_new_ticket_failure_no_ticket_object(self):
        ''' new_ticket should return False if argument is not a Ticket object '''
        tickets=[23,'23423',2342.2342, {'a':'dict'},('a','tuple'),{'set'},['a','list'],uuid.uuid4(), uuid.uuid1()]
        for ticket in tickets:
            self.assertFalse(ticketapi.new_ticket(ticket=ticket))

    def test_new_ticket_success(self):
        ''' new_ticket should succeed '''
        tid=uuid.uuid4()
        date=uuid.uuid1()
        uid=uuid.uuid4()
        expires=uuid.uuid1()
        allowed_uids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        allowed_cids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        resources={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        permissions={uuid.uuid4():0,uuid.uuid4():3,uuid.uuid4():6}
        interval_init=uuid.uuid1()
        interval_end=uuid.uuid1()
        ticket=ormticket.Ticket(tid=tid,date=date,uid=uid,expires=expires,allowed_uids=allowed_uids,allowed_cids=allowed_cids,resources=resources,permissions=permissions,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(ticketapi.new_ticket(ticket=ticket))
        db_ticket=ticketapi.get_ticket(tid=tid)
        self.assertEqual(db_ticket.tid,ticket.tid)
        self.assertEqual(db_ticket.date,ticket.date)
        self.assertEqual(db_ticket.uid,ticket.uid)
        self.assertEqual(db_ticket.expires,ticket.expires)
        self.assertEqual(db_ticket.allowed_uids,ticket.allowed_uids)
        self.assertEqual(db_ticket.allowed_cids,ticket.allowed_cids)
        self.assertEqual(db_ticket.resources,ticket.resources)
        self.assertEqual(db_ticket.permissions,ticket.permissions)
        self.assertEqual(db_ticket.interval_init,ticket.interval_init)
        self.assertEqual(db_ticket.interval_end,ticket.interval_end)

    def test_new_ticket_failure_already_exists(self):
        ''' new_ticket should fail if already exists a ticket with the same tid '''
        tid=uuid.uuid4()
        date=uuid.uuid1()
        uid=uuid.uuid4()
        expires=uuid.uuid1()
        allowed_uids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        allowed_cids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        resources={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        permissions={uuid.uuid4():0,uuid.uuid4():3,uuid.uuid4():6}
        interval_init=uuid.uuid1()
        interval_end=uuid.uuid1()
        ticket=ormticket.Ticket(tid=tid,date=date,uid=uid,expires=expires,allowed_uids=allowed_uids,allowed_cids=allowed_cids,resources=resources,permissions=permissions,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(ticketapi.new_ticket(ticket=ticket))
        db_ticket=ticketapi.get_ticket(tid=tid)
        self.assertEqual(db_ticket.tid,ticket.tid)
        self.assertEqual(db_ticket.date,ticket.date)
        self.assertEqual(db_ticket.uid,ticket.uid)
        self.assertEqual(db_ticket.expires,ticket.expires)
        self.assertEqual(db_ticket.allowed_uids,ticket.allowed_uids)
        self.assertEqual(db_ticket.allowed_cids,ticket.allowed_cids)
        self.assertEqual(db_ticket.resources,ticket.resources)
        self.assertEqual(db_ticket.permissions,ticket.permissions)
        self.assertEqual(db_ticket.interval_init,ticket.interval_init)
        self.assertEqual(db_ticket.interval_end,ticket.interval_end)
        self.assertFalse(ticketapi.new_ticket(ticket=ticket))

    def test_insert_ticket_failure_no_ticket_object(self):
        ''' insert_ticket should return False if argument is not a Ticket object '''
        tickets=[23,'23423',2342.2342, {'a':'dict'},('a','tuple'),{'set'},['a','list'],uuid.uuid4(), uuid.uuid1()]
        for ticket in tickets:
            self.assertFalse(ticketapi.insert_ticket(ticket=ticket))

    def test_insert_ticket_success(self):
        ''' insert_ticket should succeed '''
        tid=uuid.uuid4()
        date=uuid.uuid1()
        uid=uuid.uuid4()
        expires=uuid.uuid1()
        allowed_uids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        allowed_cids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        resources={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        permissions={uuid.uuid4():0,uuid.uuid4():3,uuid.uuid4():6}
        interval_init=uuid.uuid1()
        interval_end=uuid.uuid1()
        ticket=ormticket.Ticket(tid=tid,date=date,uid=uid,expires=expires,allowed_uids=allowed_uids,allowed_cids=allowed_cids,resources=resources,permissions=permissions,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(ticketapi.insert_ticket(ticket=ticket))
        db_ticket=ticketapi.get_ticket(tid=tid)
        self.assertEqual(db_ticket.tid,ticket.tid)
        self.assertEqual(db_ticket.date,ticket.date)
        self.assertEqual(db_ticket.uid,ticket.uid)
        self.assertEqual(db_ticket.expires,ticket.expires)
        self.assertEqual(db_ticket.allowed_uids,ticket.allowed_uids)
        self.assertEqual(db_ticket.allowed_cids,ticket.allowed_cids)
        self.assertEqual(db_ticket.resources,ticket.resources)
        self.assertEqual(db_ticket.permissions,ticket.permissions)
        self.assertEqual(db_ticket.interval_init,ticket.interval_init)
        self.assertEqual(db_ticket.interval_end,ticket.interval_end)

    def test_insert_expired_ticket_failure_no_ticket_object(self):
        ''' insert_ticket should return False if argument is not a Ticket object '''
        tickets=[23,'23423',2342.2342, {'a':'dict'},('a','tuple'),{'set'},['a','list'],uuid.uuid4(), uuid.uuid1()]
        for ticket in tickets:
            self.assertFalse(ticketapi.insert_expired_ticket(ticket=ticket))

    def test_insert_expired_ticket_success(self):
        ''' insert_ticket should succeed '''
        tid=uuid.uuid4()
        date=uuid.uuid1()
        uid=uuid.uuid4()
        expires=uuid.uuid1()
        allowed_uids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        allowed_cids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        resources={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        permissions={uuid.uuid4():0,uuid.uuid4():3,uuid.uuid4():6}
        interval_init=uuid.uuid1()
        interval_end=uuid.uuid1()
        ticket=ormticket.Ticket(tid=tid,date=date,uid=uid,expires=expires,allowed_uids=allowed_uids,allowed_cids=allowed_cids,resources=resources,permissions=permissions,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(ticketapi.insert_expired_ticket(ticket=ticket))
        db_ticket=ticketapi.get_expired_ticket(tid=tid)
        self.assertEqual(db_ticket.tid,ticket.tid)
        self.assertEqual(db_ticket.date,ticket.date)
        self.assertEqual(db_ticket.uid,ticket.uid)
        self.assertEqual(db_ticket.expires,ticket.expires)
        self.assertEqual(db_ticket.allowed_uids,ticket.allowed_uids)
        self.assertEqual(db_ticket.allowed_cids,ticket.allowed_cids)
        self.assertEqual(db_ticket.resources,ticket.resources)
        self.assertEqual(db_ticket.permissions,ticket.permissions)
        self.assertEqual(db_ticket.interval_init,ticket.interval_init)
        self.assertEqual(db_ticket.interval_end,ticket.interval_end)

    def test_delete_ticket_no_existing_tid(self):
        ''' delete_ticket should return True even if tid does not exist'''
        tid=uuid.uuid4()
        self.assertTrue(ticketapi.delete_ticket(tid=tid))

    def test_delete_ticket_success(self):
        ''' delete_ticket should succeed '''
        tid=uuid.uuid4()
        date=uuid.uuid1()
        uid=uuid.uuid4()
        expires=uuid.uuid1()
        allowed_uids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        allowed_cids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        resources={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        permissions={uuid.uuid4():0,uuid.uuid4():3,uuid.uuid4():6}
        interval_init=uuid.uuid1()
        interval_end=uuid.uuid1()
        ticket=ormticket.Ticket(tid=tid,date=date,uid=uid,expires=expires,allowed_uids=allowed_uids,allowed_cids=allowed_cids,resources=resources,permissions=permissions,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(ticketapi.insert_ticket(ticket=ticket))
        db_ticket=ticketapi.get_ticket(tid=tid)
        self.assertEqual(db_ticket.tid,ticket.tid)
        self.assertEqual(db_ticket.date,ticket.date)
        self.assertEqual(db_ticket.uid,ticket.uid)
        self.assertEqual(db_ticket.expires,ticket.expires)
        self.assertEqual(db_ticket.allowed_uids,ticket.allowed_uids)
        self.assertEqual(db_ticket.allowed_cids,ticket.allowed_cids)
        self.assertEqual(db_ticket.resources,ticket.resources)
        self.assertEqual(db_ticket.permissions,ticket.permissions)
        self.assertEqual(db_ticket.interval_init,ticket.interval_init)
        self.assertEqual(db_ticket.interval_end,ticket.interval_end)
        self.assertTrue(ticketapi.delete_ticket(tid=tid))
        self.assertIsNone(ticketapi.get_ticket(tid=tid))

    def test_delete_expired_ticket_no_existing_tid(self):
        ''' delete_expired_ticket should return True even if tid does not exist'''
        tid=uuid.uuid4()
        self.assertTrue(ticketapi.delete_expired_ticket(tid=tid))

    def test_delete_expired_ticket_success(self):
        ''' delete_expired_ticket should succeed '''
        tid=uuid.uuid4()
        date=uuid.uuid1()
        uid=uuid.uuid4()
        expires=uuid.uuid1()
        allowed_uids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        allowed_cids={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        resources={uuid.uuid4(),uuid.uuid4(),uuid.uuid4()}
        permissions={uuid.uuid4():0,uuid.uuid4():3,uuid.uuid4():6}
        interval_init=uuid.uuid1()
        interval_end=uuid.uuid1()
        ticket=ormticket.Ticket(tid=tid,date=date,uid=uid,expires=expires,allowed_uids=allowed_uids,allowed_cids=allowed_cids,resources=resources,permissions=permissions,interval_init=interval_init,interval_end=interval_end)
        self.assertTrue(ticketapi.insert_expired_ticket(ticket=ticket))
        db_ticket=ticketapi.get_expired_ticket(tid=tid)
        self.assertEqual(db_ticket.tid,ticket.tid)
        self.assertEqual(db_ticket.date,ticket.date)
        self.assertEqual(db_ticket.uid,ticket.uid)
        self.assertEqual(db_ticket.expires,ticket.expires)
        self.assertEqual(db_ticket.allowed_uids,ticket.allowed_uids)
        self.assertEqual(db_ticket.allowed_cids,ticket.allowed_cids)
        self.assertEqual(db_ticket.resources,ticket.resources)
        self.assertEqual(db_ticket.permissions,ticket.permissions)
        self.assertEqual(db_ticket.interval_init,ticket.interval_init)
        self.assertEqual(db_ticket.interval_end,ticket.interval_end)
        self.assertTrue(ticketapi.delete_expired_ticket(tid=tid))
        self.assertIsNone(ticketapi.get_expired_ticket(tid=tid))

