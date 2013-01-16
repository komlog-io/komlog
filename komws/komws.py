#!/usr/bin/env python
# coding: utf-8
'''
Created on 31/12/2012

@author: juan cañete <jcazor@komlog.org>
'''

from komapp import komapp
import os
import modules

def main():
    """ Program Init.
        
        Start program instance with its associated config file
    """
    HOME = os.getenv('HOME')
    cfg_file = '.komlog/komws.cfg'
    app = komapp.Komapp(os.path.join(HOME,cfg_file))
    app.start()
    
if __name__ == "__main__": main() 
