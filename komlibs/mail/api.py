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

def send_invitation_mail(to, inv_id):
    if not arguments.is_valid_email(to) or not arguments.is_valid_uuid(inv_id):
        return False
    mailargs={'to_address':to,
              'inv_id':inv_id.hex,
              'domain':config.get(options.MAIL_DOMAIN)
             }
    mailmessage=mailmessages.get_message(mailtypes.NEW_INVITATION,mailargs)
    if connection.mailer.send(mailmessage):
        return True
    else:
        return False

def send_forget_mail(to, code):
    if not arguments.is_valid_email(to) or not arguments.is_valid_uuid(code):
        return False
    mailargs={'to_address':to,
              'code':code.hex,
              'domain':config.get(options.MAIL_DOMAIN)
             }
    mailmessage=mailmessages.get_message(mailtypes.FORGET,mailargs)
    if connection.mailer.send(mailmessage):
        return True
    else:
        return False

