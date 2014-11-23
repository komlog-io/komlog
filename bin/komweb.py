'''
Created on 01/11/2014

@author: jcazor
'''

from komapp import komapp
from komapp.modules import webserver
import os

def main():
    """ Program Init.
        
        Start program instance with its associated config file
    """
    HOME = os.getenv('HOME')
    cfg_file = '.komlogs/komws2.cfg'
    program_name = 'komws2App'
    app = komapp.Komapp(os.path.join(HOME,cfg_file), program_name)
    app.start()
    

if __name__ == "__main__": main() 
