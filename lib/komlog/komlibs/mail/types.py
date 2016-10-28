'''

this file enumerate the multiple email types we will send

2013/07/30

'''

import os.path

NEW_USER=0
NEW_INVITATION=1
FORGET=2

CURRENT_PATH = os.path.dirname(__file__)
TEXT_TEMPLATES_PATH='templates/text'
HTML_TEMPLATES_PATH='templates/html'

texttemplates={
    0:os.path.join(CURRENT_PATH,TEXT_TEMPLATES_PATH,'new_user_body.tpl'),
    1:os.path.join(CURRENT_PATH,TEXT_TEMPLATES_PATH,'new_invitation_body.tpl'),
    2:os.path.join(CURRENT_PATH,TEXT_TEMPLATES_PATH,'forget_body.tpl'),
}

htmltemplates={
    0:os.path.join(CURRENT_PATH,HTML_TEMPLATES_PATH,'new_user_body.tpl'),
    1:os.path.join(CURRENT_PATH,HTML_TEMPLATES_PATH,'new_invitation_body.tpl'),
    2:os.path.join(CURRENT_PATH,HTML_TEMPLATES_PATH,'forget_body.tpl'),
}

subjects={
    0:'Welcome to Komlog!',
    1:'Join Komlog now!',
    2:'Password reset requested',
}

fromaddress={
    0:'no-reply@komlog.io',
    1:'no-reply@komlog.io',
    2:'no-reply@komlog.io',
}

toaddress={
    0:'${to_address}',
    1:'${to_address}',
    2:'${to_address}',
}

