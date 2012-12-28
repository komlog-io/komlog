'''
Created on 26/12/2012

@author: jcazor
'''

import komapp
import os

def main():
    """ Program Init.
        
        Start program instance with its associated config file
    """
    HOME = os.getenv('HOME')
    cfg_file = '.komlog/komdc.cfg'
    app = komapp.Komapp(os.path.join(HOME,cfg_file))
    app.start()
    

if __name__ == "__main__": main() 
