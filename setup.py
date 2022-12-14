from setuptools import setup, find_packages
import unittest
import logging as log
import sys
import os.path
from pathlib import Path

if sys.version_info < (3, 5):
    sys.exit("Sorry, Python 3.5 or greater required.")

komws2_data_paths = ('./lib/komlog/komws2/templates/',)
komws2_data = []
for data_path in komws2_data_paths:
    for root, dirs, files in os.walk(data_path):
        for f in files:
            path = Path(os.path.join(root,f))
            komws2_data.append(str(path.relative_to('./lib/komlog/komws2/')))

mail_data_paths = ('./lib/komlog/komlibs/mail/templates/',)
mail_data = []
for data_path in mail_data_paths:
    for root, dirs, files in os.walk(data_path):
        for f in files:
            path = Path(os.path.join(root,f))
            mail_data.append(str(path.relative_to('./lib/komlog/komlibs/mail/')))

def get_test_suite():
    #initialize and load configuration before returning test_suite
    sys.path.insert(1, os.path.dirname(os.path.join(__file__,'lib/komlog')))
    from komlog.test.test import MODULES
    from komlog.komfig import config, options, logging
    from komlog.komapp.modules import tester
    from komlog.komcass.model.schema import creation
    HOME = os.path.expanduser('~')
    cfg_file = os.path.join(HOME,'.komlog/komlog-setup.py-test.cfg')
    config.initialize_config(cfg_file)
    logging.logger=log.getLogger('dummy')
    keyspace = config.get(options.CASSANDRA_KEYSPACE)
    cluster = config.get(options.CASSANDRA_CLUSTER)
    cluster = list(host for host in cluster.split(',') if len(host)>0) if cluster else None
    if not keyspace or not cluster:
        print ('ERROR: Keyspace and cluster not set in configuration')
        exit()
    else:
        print ('Dropping old keyspace before running tests')
        creation.drop_database(cluster,keyspace)
    test=tester.Tester(0)
    print ('Testing the following modules:')
    for mod in MODULES:
        print ('\t',mod)
    test.loop=lambda : None
    test.terminate=lambda : None
    test.start()
    #now load tests and return
    testsuite=unittest.defaultTestLoader.loadTestsFromNames(MODULES)
    return testsuite

setup(name='komlog',
    version='0.0.2',
    description='Komlog',
    author='Komlog Team',
    author_email='hello@komlog.io',
    url='http://www.komlog.io',
    license='LICENSE.txt',
    install_requires=[
        'setuptools',
        'cryptography',
        'pyjwt',
        'cassandra-driver',
        'aioredis',
        'hiredis',
        'Mako',
        'scikit-learn',
        'scipy',
        'numpy',
        'pandas',
        'tornado',
        'stripe'
    ],
    package_dir={ '': 'lib' },
    packages= find_packages('lib'),
    test_suite = 'setup.get_test_suite',
    package_data = {
        'komlog.komws2':komws2_data,
        'komlog.komlibs.mail':mail_data
    },
    scripts=[
       'bin/komlog-imc',
       'bin/komlog-web',
       'bin/komlog-websocket',
       'bin/komlog-test',
    ],
    data_files=[
        ('config',['etc/komlog-imc.cfg','etc/komlog-web.cfg','etc/komlog-websocket.cfg']),
        ('config/systemd',['etc/komlog-imc.service','etc/komlog-web.service','etc/komlog-websocket.service'])
    ]
)

