#!/usr/bin/python3
'''
Created on 24/02/2012

@author: jcazor
'''

from komapp import komapp
from komapp.modules import textmining
import os

def main():
    """ Program Init.
        
        Start program instance with its associated config file
    """
    HOME = os.getenv('HOME')
    cfg_file = '.komlogs/komai.cfg'
    program_name = 'komaiApp'
    app = komapp.Komapp(os.path.join(HOME,cfg_file), program_name)
    app.start()
    

if __name__ == "__main__": main() 
