#!/usr/bin/python3
'''
Created on 29/02/2016

@author: jcazor
'''

from komapp import komapp
from komapp.modules import websocketserver
import os

def main():
    """ Program Init.
        
        Start program instance with its associated config file
    """
    HOME = os.getenv('HOME')
    cfg_file = '.komlogs/komwebagent.cfg'
    program_name = 'komwebagentApp'
    app = komapp.Komapp(os.path.join(HOME,cfg_file), program_name)
    app.start()
    

if __name__ == "__main__": main() 
