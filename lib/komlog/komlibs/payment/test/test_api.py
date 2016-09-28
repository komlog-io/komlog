import unittest
import uuid
import os
import stripe
from komlog.komlibs.general.time import timeuuid
from komlog.komcass.api import user as cassapiuser
from komlog.komlibs.payment import api as paymentapi


class KomlibsPaymentApiTest(unittest.TestCase):
    ''' komlog.komlibs.payment.api tests '''

    def test_create_customer_failure_stripe_info_already_exists(self):
        ''' create_customer should return None if stripe_info already exists '''
        uid = uuid.uuid4()
        token = 'whatever'
        self.assertTrue(cassapiuser.new_user_stripe_info(uid=uid, stripe_id=None))
        self.assertIsNone(paymentapi.create_customer(uid=uid, token=token))

    def test_create_customer_failure_invalid_token(self):
        ''' create_customer should return None token is invalid '''
        uid = uuid.uuid4()
        token = 'whatever'
        self.assertIsNone(paymentapi.create_customer(uid=uid, token=token))
        self.assertIsNone(cassapiuser.get_user_stripe_info(uid=uid))

    def test_create_customer_failure_invalid_api_key(self):
        ''' create_customer should return None if api_key is invalid '''
        uid = uuid.uuid4()
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        api_key_bck=stripe.api_key
        stripe.api_key = 'whatever'
        self.assertIsNone(paymentapi.create_customer(uid=uid, token=token.id))
        stripe.api_key = api_key_bck
        self.assertIsNone(cassapiuser.get_user_stripe_info(uid=uid))

    def test_create_customer_success(self):
        ''' create_customer should return the recently created customer '''
        uid = uuid.uuid4()
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        customer = paymentapi.create_customer(uid=uid, token=token.id)
        stripe_info = cassapiuser.get_user_stripe_info(uid=uid)
        self.assertEqual(stripe_info.uid, uid)
        self.assertEqual(stripe_info.stripe_id, customer.id)
        stripe_cus = paymentapi.get_customer(uid=uid)
        self.assertEqual(stripe_cus.id, customer.id)
        self.assertEqual(stripe_cus.metadata['uid'], uid.hex)

    def test_delete_customer_failure_invalid_stripe_id(self):
        ''' delete_customer should fail if stripe id is not found in stripe systems '''
        uid = uuid.uuid4()
        stripe_id = 'some_wrong_id'
        self.assertTrue(cassapiuser.insert_user_stripe_info(uid=uid, stripe_id = stripe_id))
        self.assertFalse(paymentapi.delete_customer(uid=uid))

    def test_delete_customer_success_no_stripe_info_found(self):
        ''' delete_customer should succeed if no stripe info is found '''
        uid = uuid.uuid4()
        self.assertTrue(paymentapi.delete_customer(uid=uid))

    def test_delete_customer_success(self):
        ''' delete_customer should succeed and delete the customer '''
        uid = uuid.uuid4()
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        customer = paymentapi.create_customer(uid=uid, token=token.id)
        stripe_info = cassapiuser.get_user_stripe_info(uid=uid)
        self.assertEqual(stripe_info.uid, uid)
        self.assertEqual(stripe_info.stripe_id, customer.id)
        self.assertTrue(paymentapi.delete_customer(uid=uid))
        stripe_customer = stripe.Customer.retrieve(customer.id)
        self.assertTrue(stripe_customer.deleted)

    def test_get_customer_non_existent(self):
        ''' get_customer should return None if customer does not exist '''
        uid = uuid.uuid4()
        self.assertIsNone(paymentapi.get_customer(uid=uid))

    def test_get_customer_success(self):
        ''' get_customer should succeed and return the customer object '''
        uid = uuid.uuid4()
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        customer = paymentapi.create_customer(uid=uid, token=token.id)
        stripe_info = cassapiuser.get_user_stripe_info(uid=uid)
        self.assertEqual(stripe_info.uid, uid)
        self.assertEqual(stripe_info.stripe_id, customer.id)
        stripe_customer = stripe.Customer.retrieve(customer.id)
        self.assertEqual(stripe_customer.id, customer.id)
        self.assertEqual(stripe_customer.metadata['uid'], uid.hex)

    def test_update_customer_failure_non_existent_customer(self):
        ''' update_customer should return None if customer does not exist '''
        uid = uuid.uuid4()
        token = 'token'
        self.assertIsNone(paymentapi.update_customer(uid=uid, token=token))

    def test_update_customer_success(self):
        ''' update_customer should return the recently updated customer '''
        uid = uuid.uuid4()
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        customer = paymentapi.create_customer(uid=uid, token=token.id)
        stripe_info = cassapiuser.get_user_stripe_info(uid=uid)
        self.assertEqual(stripe_info.uid, uid)
        self.assertEqual(stripe_info.stripe_id, customer.id)
        stripe_cus = paymentapi.get_customer(uid=uid)
        self.assertEqual(stripe_cus.id, customer.id)
        self.assertEqual(stripe_cus.metadata['uid'], uid.hex)
        new_token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        updated_customer = paymentapi.update_customer(uid=uid, token=new_token.id)
        self.assertIsNotNone(updated_customer)

    def test_update_customer_failure_invalid_token(self):
        ''' update_customer should fail if token is invalid '''
        uid = uuid.uuid4()
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        customer = paymentapi.create_customer(uid=uid, token=token.id)
        stripe_info = cassapiuser.get_user_stripe_info(uid=uid)
        self.assertEqual(stripe_info.uid, uid)
        self.assertEqual(stripe_info.stripe_id, customer.id)
        stripe_cus = paymentapi.get_customer(uid=uid)
        self.assertEqual(stripe_cus.id, customer.id)
        self.assertEqual(stripe_cus.metadata['uid'], uid.hex)
        new_token = 'token'
        self.assertIsNone(paymentapi.update_customer(uid=uid, token=new_token))

    def test_update_customer_failure_token_reused(self):
        ''' update_customer should fail if token is reused'''
        uid = uuid.uuid4()
        token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        customer = paymentapi.create_customer(uid=uid, token=token.id)
        stripe_info = cassapiuser.get_user_stripe_info(uid=uid)
        self.assertEqual(stripe_info.uid, uid)
        self.assertEqual(stripe_info.stripe_id, customer.id)
        stripe_cus = paymentapi.get_customer(uid=uid)
        self.assertEqual(stripe_cus.id, customer.id)
        self.assertEqual(stripe_cus.metadata['uid'], uid.hex)
        new_token = stripe.Token.create(
            card={
                "number": '4242424242424242',
                "exp_month": 12,
                "exp_year": 2017,
                "cvc": '123'
            },
        )
        updated_customer = paymentapi.update_customer(uid=uid, token=new_token.id)
        self.assertIsNotNone(updated_customer)
        self.assertIsNone(paymentapi.update_customer(uid=uid, token=new_token.id))

