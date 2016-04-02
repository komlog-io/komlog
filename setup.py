from setuptools import setup, find_packages
import sys
import os
from pathlib import Path

if sys.version_info < (3, 5):
    sys.exit("Sorry, Python 3.5 or greater required.")

komws2_data_paths = ('./lib/komlog/komws2/static/','./lib/komlog/komws2/templates/')
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

setup(name='komlog',
    version='0.0.1',
    description='Komlog',
    author='Komlog Crew',
    author_email='dev@komlog.org',
    url='http://komlog.org',
    license='LICENSE.txt',
    install_requires=[
        'setuptools',
        'cryptography',
        'cassandra-driver',
        'redis',
        'Mako',
        'nltk',
        'scikit-learn',
        'scipy',
        'numpy',
        'tornado'
    ],
    package_dir={ '': 'lib' },
    packages= find_packages('lib'),
    package_data = {
        'komlog.komws2':komws2_data,
        'komlog.komlibs.mail':mail_data
    },
    scripts=[
       'bin/komlog',
       'bin/komlog-test',
    ]
)

