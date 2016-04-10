import unittest
import uuid
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.general.validation import arguments

class GeneralValidationArgumentsTest(unittest.TestCase):
    ''' komlog.general.validation.arguments tests '''

    def test_is_valid_username_invalid(self):
        ''' is_valid_username should fail if username is not valid '''
        params=[None, 234234,'with spaces','withspecialcharacterslike\t','or\ncharacter',
                ' spacesatbeggining',
                'spacesatend ',
                'Capitals',
                'Two..consecutivepoints',
                '.beginswithpoint',
                'endswith.',
                'containsspecialchar$',
                'endswith\t',
                '\nbeginwithnewline',
                'endswith\n',
                '',
                ]
        for param in params:
            self.assertFalse(arguments.is_valid_username(param)) 

    def test_is_valid_username_valid(self):
        ''' is_valid_username should succeed if username is valid '''
        usernames=['test_user','user.with.dots','user_with_underscores','user-with-dash',
                   'userwithnumbers007']
        for username in usernames:
            self.assertTrue(arguments.is_valid_username(username)) 

    def test_is_valid_agentname_invalid(self):
        ''' is_valid_agentname should fail if agentname is not valid '''
        params=[None, 234234, 'Agentname with \t is not Valid','Agentname with \n neither',
               'cant end in \n',
               '\ncant begin with newline',
               '',
               ]
        for param in params:
            self.assertFalse(arguments.is_valid_agentname(param)) 

    def test_is_valid_agentname_valid(self):
        ''' is_valid_agentname should succeed if agentname is valid '''
        params=['test_agent', 'Agentname OK', 'Agentname @213 #23']
        for param in params:
            self.assertTrue(arguments.is_valid_agentname(param)) 

    def test_is_valid_datasourcename_invalid(self):
        ''' is_valid_datasourcename should fail if datasourcename is not valid '''
        params=[None, 234234, 'Datasource with \n is not valid', 'Datasource with \t not valid']
        for param in params:
            self.assertFalse(arguments.is_valid_datasourcename(param)) 

    def test_is_valid_datasourcename_valid(self):
        ''' is_valid_datasourcename should succeed if datasourcename is valid '''
        params=['Datasource Name','DatasourceName','234234','#1 Datasource','Datasource 234234','Con caracteres #@$%&+=_.- por ejemplo']
        for param in params:
            self.assertTrue(arguments.is_valid_datasourcename(param)) 

    def test_is_valid_datapointname_invalid(self):
        ''' is_valid_datapointname should fail if datapointname is not valid '''
        params=[None, 234234, 'Datapoints with \n are not valid', 'Datapoint with \t not valid']
        for param in params:
            self.assertFalse(arguments.is_valid_datapointname(param)) 

    def test_is_valid_datapointname_valid(self):
        ''' is_valid_datapointname should succeed if datapointname is valid '''
        params=['Datapoint Name','DatapointName','234234','#1 Datapoint','Datapoint 234234','Con caracteres #@$%&+=_.- por ejemplo']
        for param in params:
            self.assertTrue(arguments.is_valid_datapointname(param)) 

    def test_is_valid_datasource_content_invalid(self):
        ''' is_valid_datasource_content should fail if datasource_content is not valid '''
        params=[None, 234234]
        for param in params:
            self.assertFalse(arguments.is_valid_datasource_content(param)) 

    def test_is_valid_datasource_content_valid(self):
        ''' is_valid_datasource_content should succeed if datasource_content is valid '''
        params=['test_agent']
        for param in params:
            self.assertTrue(arguments.is_valid_datasource_content(param)) 

    def test_is_valid_password_invalid(self):
        ''' is_valid_password should fail if password is not valid '''
        params=[None, 234234,
               'six',
               'morethan256charsisnotvalid123456789101214161820222426283032343638404244464850525456586062646668707274767880828486889092949698100103106109112115118121124127130133136139142145148151154157160163166169172175178181184187190193196199202205208211214217220223226229232235238241244247250253256',
               ('a','tuple'),
               ['a','list'],
               {'a':'dict'},
               {'set'},
               uuid.uuid4()
               ]
        for param in params:
            self.assertFalse(arguments.is_valid_password(param)) 

    def test_is_valid_password_valid(self):
        ''' is_valid_password should succeed if password is valid '''
        params=['123123A#','12!password','ApasswordWithNumbers43343AndCAPITALSandsimbols+','cualquier cadena unicode æßðđ@# lo que ññ sea Pæ,']
        for param in params:
            self.assertTrue(arguments.is_valid_password(param)) 

    def test_is_valid_email_invalid(self):
        ''' is_valid_email should fail if email is not valid '''
        params=[None, 234234,'not_an_email','email.com','@domain.com','email@','email@domain@domain.com','español@domain.com', 'EMAIL@domain.com']
        for param in params:
            self.assertFalse(arguments.is_valid_email(param)) 

    def test_is_valid_email_valid(self):
        ''' is_valid_email should succeed if email is valid '''
        params=['my_email@domain.com','my.email@mydomain.es','thisemailisvalid@yahoo.com','info@subdomain.domain.com']
        for param in params:
            self.assertTrue(arguments.is_valid_email(param)) 

    def test_is_valid_code_invalid(self):
        ''' is_valid_code should fail if code is not valid '''
        params=[None, 234234,'Only ASCII ÑÑ',('tuple','notallowed'),{'set','notallowed'},{'dict':'notall'}, uuid.uuid4()]
        for param in params:
            self.assertFalse(arguments.is_valid_code(param)) 

    def test_is_valid_code_valid(self):
        ''' is_valid_code should succeed if code is valid '''
        params=['testcode']
        for param in params:
            self.assertTrue(arguments.is_valid_code(param)) 

    def test_is_valid_uri_invalid(self):
        ''' is_valid_code should fail if code is not valid '''
        params=[None,
            234234,
            'with spaces',
            'with_end_point.',
            'withspecialcharacterslike\t',
            'or\ncharacter',
            ' spacesatbeggining',
            'spacesatend ',
            'two..consecutivepoints',
            '.beginswithpoint',
            'endswith.',
            'containsspecialchar$',
            'endswith\t',
            '\nbeginwithnewline',
            'endswith\n',
            '',
        ]
        for param in params:
            self.assertFalse(arguments.is_valid_uri(param)) 

    def test_is_valid_uri_valid(self):
        ''' is_valid_uri should succeed if uri is valid '''
        params=['test_uri',
            'uri.with.dots',
            'uri_with_underscores',
            'uri-with-dash',
            'uriwithnumbers007',
            'Capitals',
            'all.together.0.a-b_.99'
        ]
        for param in params:
            self.assertTrue(arguments.is_valid_uri(param)) 

    def test_is_valid_relative_uri_invalid(self):
        ''' is_valid_relative_uri should fail if rel uri is not valid '''
        params=[None,
            234234,
            '..with_beginning_points',
            'with_end_point.',
            'with_end_points..',
            'with...three_points',
            'with spaces',
            'withspecialcharacterslike\t',
            'or\ncharacter',
            ' spacesatbeggining',
            'spacesatend ',
            '.beginswithpoint',
            'endswith.',
            'containsspecialchar$',
            'endswith\t',
            '\nbeginwithnewline',
            'endswith\n',
            '',
        ]
        for param in params:
            self.assertFalse(arguments.is_valid_relative_uri(param)) 

    def test_is_valid_relative_uri_valid(self):
        ''' is_valid_relative_uri should succeed if relative uri is valid '''
        params=['test_uri',
            'uri.with.dots',
            'uri.with..two.dots',
            'uri_with_underscores',
            'uri-with-dash',
            'uriwithnumbers007',
            'Capitals.and..two.dots',
            'all.togetheR.0..a-b_.99'
        ]
        for param in params:
            self.assertTrue(arguments.is_valid_relative_uri(param)) 

    def test_is_valid_pubkey_invalid(self):
        ''' is_valid_pubkey should fail if pubkey is not valid
            pubkeys should be at least 4096 bits long '''
        params=[None, 234234,'not ASCII ÑÑ','tabulators not allowed \t','semicolon not allowed ;',
            crypto.serialize_public_key(crypto.generate_rsa_key(key_size=1024).public_key()),
            crypto.serialize_private_key(crypto.generate_rsa_key()),
            ]
        for param in params:
            self.assertFalse(arguments.is_valid_pubkey(param)) 

    def test_is_valid_pubkey_valid(self):
        ''' is_valid_pubkey should succeed if pubkey is valid '''
        pubkeys=[crypto.serialize_public_key(crypto.generate_rsa_key().public_key()),
            crypto.serialize_public_key(crypto.generate_rsa_key(key_size=8192).public_key())
            ]
        for pubkey in pubkeys:
            self.assertTrue(arguments.is_valid_pubkey(pubkey))

    def test_is_valid_version_invalid(self):
        ''' is_valid_version should fail if version is not valid '''
        params=[None, 234234]
        for param in params:
            self.assertFalse(arguments.is_valid_version(param)) 

    def test_is_valid_version_valid(self):
        ''' is_valid_version should succeed if version is valid '''
        params=['version','version: 1.2','v2.0.0 codenamed: X']
        for param in params:
            self.assertTrue(arguments.is_valid_version(param)) 

    def test_is_valid_uuid_invalid(self):
        ''' is_valid_uuid should fail if uuid is not valid '''
        params=[None, 234234,'string','string with spaces','234234']
        for param in params:
            self.assertFalse(arguments.is_valid_uuid(param)) 

    def test_is_valid_uuid_valid(self):
        ''' is_valid_uuid should succeed if version is valid '''
        params=[uuid.uuid4()]
        for param in params:
            self.assertTrue(arguments.is_valid_uuid(param)) 

    def test_is_valid_hex_uuid_invalid(self):
        ''' is_valid_hex_uuid should fail if param is not valid uuid in hex format'''
        params=[None, 234234,'string','string with spaces','234234',uuid.uuid1(), uuid.uuid4(),timeuuid.uuid1()]
        for param in params:
            self.assertFalse(arguments.is_valid_hex_uuid(param)) 

    def test_is_valid_hex_uuid_valid(self):
        ''' is_valid_hex_uuid should succeed if param is a valid hex uuid '''
        params=[uuid.uuid4().hex]
        for param in params:
            self.assertTrue(arguments.is_valid_hex_uuid(param)) 

    def test_is_valid_dict_invalid(self):
        ''' is_valid_dict should fail if dict is not valid '''
        params=[None, 234234,'string','string with spaces','234234']
        for param in params:
            self.assertFalse(arguments.is_valid_dict(param)) 

    def test_is_valid_dict_valid(self):
        ''' is_valid_dict should succeed if dict is valid '''
        params=[{}, {'prueba':'value'}]
        for param in params:
            self.assertTrue(arguments.is_valid_dict(param)) 

    def test_is_valid_bool_invalid(self):
        ''' is_valid_bool should fail if bool is not valid '''
        params=[None, 234234,'string','string with spaces','234234']
        for param in params:
            self.assertFalse(arguments.is_valid_bool(param)) 

    def test_is_valid_bool_valid(self):
        ''' is_valid_bool should succeed if bool is valid '''
        params=[True,False]
        for param in params:
            self.assertTrue(arguments.is_valid_bool(param)) 

    def test_is_valid_string_int_invalid(self):
        ''' is_valid_string_int should fail if input is not valid '''
        params=[None, 234234,'string','string with spaces','#234234','234231000$','23422343€','234234.234234']
        for param in params:
            self.assertFalse(arguments.is_valid_string_int(param)) 

    def test_is_valid_string_int_valid(self):
        ''' is_valid_string_int should succeed if input is valid '''
        params=['1','000001','123123123123','0']
        for param in params:
            self.assertTrue(arguments.is_valid_string_int(param)) 

    def test_is_valid_date_invalid(self):
        ''' is_valid_date should fail if input is not valid date'''
        params=[None, 234234,'string','string with spaces','#234234','2014-12-10']
        for param in params:
            self.assertFalse(arguments.is_valid_date(param)) 

    def test_is_valid_date_valid(self):
        ''' is_valid_date should succeed if input is valid date'''
        params=[timeuuid.uuid1()]
        for param in params:
            self.assertTrue(arguments.is_valid_date(param)) 

    def test_is_valid_hexcolor_invalid(self):
        ''' is_valid_hexcolor should fail if input is not valid hex color (with #)'''
        params=[None, 234234,'string','string with spaces','23#4234','2014-12-10','332255','#FFGGFF','#0012HD','#ÑÑÑÑÑÑ','#0123vd']
        for param in params:
            self.assertFalse(arguments.is_valid_hexcolor(param)) 

    def test_is_valid_hexcolor_valid(self):
        ''' is_valid_hexcolor should succeed if input is valid hex color (with #)'''
        params=['#BBCCDD','#aa0033','#AA0033','#FFFFFF','#FFffff','#000000','#FF0000','#00FF00','#0000FF','#FF00FF','#FFFF00','#00FFFF','#AABBCC','#001234','#99807F','#4A5F6E']
        for param in params:
            self.assertTrue(arguments.is_valid_hexcolor(param)) 

