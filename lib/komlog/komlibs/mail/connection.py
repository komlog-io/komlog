#coding: utf-8

'''

This file contains funcions and classes related with email connections and its operations

2013/07/30


'''

import smtplib
from komlog.komfig import logging, config, options

mailer=None

class Mailer(object):
    """
    Represents an SMTP connection.

    Use login() to log in with a username and password.
    """

    def __init__(self, user, password, server='localhost'):
        self.server = server
        self.user = user
        self.password = password

    def send(self, msg):
        """
        Send one message or a sequence of messages.

        Every time you call send, the mailer creates a new
        connection, so if you have several emails to send, pass
        them as a list:
        mailer.send([msg1, msg2, msg3])
        """
        try:
            logging.logger.debug('Creating SMTP Server to: '+self.server)
            server = smtplib.SMTP(self.server,587)
            logging.logger.debug('EHLO')
            server.ehlo()
            server.starttls()
            logging.logger.debug('SMTP LOGIN usr: '+self.user)
            server.login(self.user, self.password)
            try:
                for m in msg:
                    logging.logger.debug('SMTP sending message: '+m)
                    self._send(server, m)
            except TypeError:
                self._send(server, msg)
            server.close()
            logging.logger.debug('SMTP message sent OK')
            return True
        except Exception as e:
            logging.logger.debug('Exception: '+str(e))
            return False

    def _send(self, server, msg):
        """
        Sends a single message using the server
        we created in send()
        """
        me = msg.From
        you = [x.strip() for x in msg.To.split(",")]
        server.sendmail(me, you, msg.as_string())

def initialize_mailer():
    global mailer
    server=config.get(options.MAIL_SERVER)
    user=config.get(options.MAIL_USER)
    password=config.get(options.MAIL_PASSWORD)
    if not server or not user or not password:
        logging.logger.error('Error loading mail server parameters')
        return False
    mailer=Mailer(user=user, password=password, server=server)
    logging.logger.debug('Mail connection initialized successfully')
    return True

def terminate_mailer():
    global mailer
    if mailer:
        mailer=None

