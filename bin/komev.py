#!/usr/bin/python3
'''
Created on 12/07/2015

@author: jcazor
'''

from komapp import komapp
from komapp.modules import events
import os

def main():
    """ Program Init.
        
        Start program instance with its associated config file
    """
    HOME = os.getenv('HOME')
    cfg_file = '.komlogs/komev.cfg'
    program_name = 'komevApp'
    app = komapp.Komapp(os.path.join(HOME,cfg_file), program_name)
    app.start()
    

if __name__ == "__main__": main() 
