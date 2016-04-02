#!/usr/bin/python3
'''
Created on 03/08/2015

@author: jcazor
'''

from komlog.komapp import komapp
from komlog.komapp.modules import anomalies
import os

def main():
    """ Program Init.
        
        Start program instance with its associated config file
    """
    HOME = os.getenv('HOME')
    cfg_file = '.komlogs/komanom.cfg'
    program_name = 'komanomApp'
    app = komapp.Komapp(os.path.join(HOME,cfg_file), program_name)
    app.start()

if __name__ == "__main__": main() 
