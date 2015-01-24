from komfig import config, logger, options
from komlibs.general.validation import arguments
from komlibs.mail import connection
from komlibs.mail import types as mailtypes
from komlibs.mail import messages as mailmessages

def send_welcome_mail(usermail, code):
    if not arguments.is_valid_email(usermail) or not arguments.is_valid_code(code):
        return False
    mailargs={'to_address':usermail,
              'code':code,
              'domain':config.get(options.MAIL_DOMAIN)
             }
    mailmessage=mailmessages.get_message(mailtypes.NEW_USER,mailargs)
    if connection.mailer.send(mailmessage):
        return True
    else:
        return False
