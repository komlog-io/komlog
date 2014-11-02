'''
Created on 01/11/2014

@author: jcazor
'''

from komapp import komapp
import os
import modules

def main():
    """ Program Init.
        
        Start program instance with its associated config file
    """
    HOME = os.getenv('HOME')
    cfg_file = '.komlogs/komws2.cfg'
    app = komapp.Komapp(os.path.join(HOME,cfg_file))
    app.start()
    

if __name__ == "__main__": main() 
