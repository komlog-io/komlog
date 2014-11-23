#!/usr/bin/python3
'''
Created on 26/12/2012

@author: jcazor
'''

from komapp import komapp
from komapp.modules import storing, validation
import os

def main():
    """ Program Init.
        
        Start program instance with its associated config file
    """
    HOME = os.getenv('HOME')
    cfg_file = '.komlogs/komdc.cfg'
    program_name = 'komdcApp'
    app = komapp.Komapp(os.path.join(HOME,cfg_file), program_name)
    app.start()
    

if __name__ == "__main__": main() 
