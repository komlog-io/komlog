#coding: utf-8

'''

This file contains funcions and classes related with email connections and its operations

2013/07/30


'''

import smtplib

class Mailer(object):
    """
    Represents an SMTP connection.

    Use login() to log in with a username and password.
    """

    def __init__(self, host="localhost"):
        self.host = u''+host
        self._usr = None
        self._pwd = None

    def login(self, usr, pwd):
        self._usr = usr
        self._pwd = pwd

    def send(self, msg):
        """
        Send one message or a sequence of messages.

        Every time you call send, the mailer creates a new
        connection, so if you have several emails to send, pass
        them as a list:
        mailer.send([msg1, msg2, msg3])
        """
        try:
            print 'Creando server'
            print self.host
            #server = smtplib.SMTP(self.host)
            server = smtplib.SMTP_SSL(self.host,465)
            print 'ehlo'
            server.ehlo()
            print 'starttls'
            #server.starttls()
            print 'ehlo'
            server.ehlo()

            if self._usr and self._pwd:
                print 'login'
                print self._usr
                print self._pwd
                server.login(self._usr, self._pwd)

            try:
                for m in msg:
                    print 'send'
                    self._send(server, m)
            except TypeError:
                self._send(server, msg)
            print 'OK'
            server.quit()
            return True
        except Exception as e:
            print str(e)
            return False

    def _send(self, server, msg):
        """
        Sends a single message using the server
        we created in send()
        """
        me = msg.From
        you = [x.strip() for x in msg.To.split(",")]
        server.sendmail(me, you, msg.as_string())
