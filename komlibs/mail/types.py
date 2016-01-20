'''

this file enumerate the multiple email types we will send

2013/07/30

'''


NEW_USER=0
NEW_INVITATION=1
FORGET=2


texttemplates={
    0:'/home/komlog/komlogs/komlibs/mail/templates/text/new_user_body.tpl',
    1:'/home/komlog/komlogs/komlibs/mail/templates/text/new_invitation_body.tpl',
    2:'/home/komlog/komlogs/komlibs/mail/templates/text/forget_body.tpl',
}

htmltemplates={
    0:'/home/komlog/komlogs/komlibs/mail/templates/html/new_user_body.tpl',
    1:'/home/komlog/komlogs/komlibs/mail/templates/html/new_invitation_body.tpl',
    2:'/home/komlog/komlogs/komlibs/mail/templates/html/forget_body.tpl',
}

subjects={
    0:'Welcome to Komlog!',
    1:'Join Komlog now!',
    2:'Password reset requested',
}

fromaddress={
    0:'jcazor@gmail.com',
    1:'jcazor@gmail.com',
    2:'jcazor@gmail.com',
}

toaddress={
    0:'${to_address}',
    1:'${to_address}',
    2:'${to_address}',
}

