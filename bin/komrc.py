#!/usr/bin/python3
'''
Komlog Resource Control Daemon

Created on 30/09/2013

@author: jcazor
'''

from komlog.komapp import komapp
from komlog.komapp.modules import rescontrol
import os

def main():
    """ Program Init.
        
        Start program instance with its associated config file
    """
    HOME = os.getenv('HOME')
    cfg_file = '.komlogs/komrc.cfg'
    program_name = 'komrcApp'
    app = komapp.Komapp(os.path.join(HOME,cfg_file), program_name)
    app.start()

if __name__ == "__main__": main() 
