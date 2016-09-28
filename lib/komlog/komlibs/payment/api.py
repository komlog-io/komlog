import time
import stripe
import traceback
from komlog.komfig import logging, config, options
from komlog.komcass.api import user as cassapiuser


def create_customer(uid, token):
    ''' creates a payment profile for the specified uid '''
    if not cassapiuser.new_user_stripe_info(uid=uid, stripe_id=None):
        return None
    try:
        customer = stripe.Customer.create(
            metadata={'uid':uid.hex},
            source=token
        )
    except stripe.error.StripeError as e:
        cassapiuser.delete_user_stripe_info(uid=uid)
        ex_info=traceback.format_exc().splitlines()
        for line in ex_info:
            logging.logger.error(line)
        return None
    else:
        if customer is not None:
            if cassapiuser.insert_user_stripe_info(uid=uid, stripe_id = customer.id):
                return customer
            else:
                try:
                    cu = stripe.Customer.retrieve(customer.id)
                    cu.delete()
                except stripe.error.StripeError as e:
                    ex_info=traceback.format_exc().splitlines()
                    for line in ex_info:
                        logging.logger.error(line)
        cassapiuser.delete_user_stripe_info(uid=uid)
        return None

def delete_customer(uid):
    ''' delete customer profile '''
    stripe_info = cassapiuser.get_user_stripe_info(uid=uid)
    if stripe_info:
        try:
            cu = stripe.Customer.retrieve(stripe_info.stripe_id)
            cu.delete()
        except stripe.error.StripeError as e:
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
            return False
        else:
            if cu.deleted is True:
                cassapiuser.delete_user_stripe_info(uid=uid)
            else:
                return False
    return True

def get_customer(uid):
    ''' returns the customer information '''
    stripe_info = cassapiuser.get_user_stripe_info(uid=uid)
    if stripe_info != None:
        try:
            cu = stripe.Customer.retrieve(stripe_info.stripe_id)
        except stripe.error.StripeError as e:
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
        else:
            return cu
    return None

def update_customer(uid, token):
    ''' updates a customer profile '''
    stripe_info = cassapiuser.get_user_stripe_info(uid=uid)
    if stripe_info is None:
        return None
    try:
        cu = stripe.Customer.retrieve(stripe_info.stripe_id)
        cu.source = token
        cu.save()
    except stripe.error.StripeError as e:
        ex_info=traceback.format_exc().splitlines()
        for line in ex_info:
            logging.logger.error(line)
    else:
        return cu

def initialize_payment():
    key = config.get(options.STRIPE_API_KEY)
    if key is None:
        logging.logger.error('Stripe api key not found')
        return False
    stripe.api_key = key
    return True

def disable_payment():
    logging.logger.debug('Disabling Stripe key')
    stripe.api_key = None
    return True

