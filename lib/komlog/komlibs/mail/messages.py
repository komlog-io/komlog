#coding: utf-8

'''

This file defines a Mail Message object


2013/07/30

'''

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mako.template import Template
from komlog.komlibs.mail import types as mailtypes

# For guessing MIME type based on file name extension
import mimetypes

class Message(object):
    """
    Represents an email message.

    Set the To, From, Subject, and Body attributes as plain-text strings.
    Optionally, set the Html attribute to send an HTML email, or use the
    attach() method to attach files.

    Even when sending an HTML email, you have to set the Body
    attribute as the alternative text version.

    Send using the Mailer class.
    """

    def __init__(self):
        self.attachments = []
        self._to = None
        self.From = None
        self.Subject = None
        self.Body = None
        self.Html = None

    def _get_to(self):
        addrs = self._to.replace(";", ",").split(",")
        return ", ".join([x.strip()
                          for x in addrs])
    def _set_to(self, to):
        self._to = to

    To = property(_get_to, _set_to,
                  doc="""The recipient(s) of the email.
                  Separate multiple recipients with commas or semicolons""")

    def as_string(self):
        """Get the email as a string to send in the mailer"""

        if not self.attachments:
            return self._plaintext()
        else:
            return self._multipart()

    def _plaintext(self):
        """Plain text email with no attachments"""

        if not self.Html:
            msg = MIMEText(self.Body)
        else:
            msg  = self._with_html()

        self._set_info(msg)
        return msg.as_string()

    def _with_html(self):
        """There's an html part"""

        outer = MIMEMultipart('alternative')

        part1 = MIMEText(self.Body, 'plain')
        part2 = MIMEText(self.Html, 'html')

        outer.attach(part1)
        outer.attach(part2)

        return outer

    def _set_info(self, msg):
        msg['Subject'] = self.Subject
        msg['From'] = self.From
        msg['To'] = self.To

    def _multipart(self):
        """The email has attachments"""

        msg = MIMEMultipart()

        msg.attach(MIMEText(self.Body, 'plain'))

        self._set_info(msg)
        msg.preamble = self.Subject

        for filename in self.attachments:
            self._add_attachment(msg, filename)
        return msg.as_string()

    def _add_attachment(self, outer, filename):
        ctype, encoding = mimetypes.guess_type(filename)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        fp = open(filename, 'rb')
        if maintype == 'text':
            # Note: we should handle calculating the charset
            msg = MIMEText(fp.read(), _subtype=subtype)
        elif maintype == 'image':
            msg = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == 'audio':
            msg = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())
            # Encode the payload using Base64
            encoders.encode_base64(msg)
        fp.close()
        # Set the filename parameter
        msg.add_header('Content-Disposition',
                'attachment',
                filename=path.basename(filename))
        outer.attach(msg)

    def attach(self, filename):
        """
        Attach a file to the email. Specify the name of the file;
        Message will figure out the MIME type and load the file.
        """

        self.attachments.append(filename)

def get_message(mailtype,args):
    msg=Message()
    msg.Body=Template(filename=mailtypes.texttemplates[mailtype]).render(**args)
    msg.Html=Template(filename=mailtypes.htmltemplates[mailtype]).render(**args)
    msg.Subject = Template(mailtypes.subjects[mailtype]).render(**args)
    msg.From = Template(mailtypes.fromaddress[mailtype]).render(**args)
    msg._to = Template(mailtypes.toaddress[mailtype]).render(**args)
    return msg

