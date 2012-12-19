'''
Created on 16/12/2012

@author: jcazor
'''

import os, sys
import glob
import time
import dateutil.parser
from komdb import api as dbapi
from komcass import api as cassapi


input_dir='/tmp/samples'

def loop():
    while True:
        files = filter(os.path.isfile,glob.glob(os.path.join(input_dir,'*pspl')))
        files.sort(key=lambda x: os.path.getmtime(x))
        if len(files)>0:
            for f in files:
                if validate(f):
                    if store(f):
                        os.rename(os.path.join(input_dir,f),os.path.join(input_dir,f[:-5]))                    
        else:
            time.sleep(5)

def validate(filename):
    '''This function should validate if data is correct:
       - Its format is clear text
       - Codification (?)
       By now, return True because we are sending validated data
    '''
    return True

def store(filename):
    print "Storing: "+filename
    datasourceid = filename.split('_')[1].split('.')[0]
    date = dateutil.parser.parse(os.path.basename(filename).split('_')[0])
    data = open(filename).read()
    # Register the sample
    sid = dbapi.create_sample(datasourceid, date)
    if sid > 0:
        sample = cassapi.Sample(str(sid), content=data)
        sample.insert()
        return True
    else:
        return False
        

def main():
    if not os.path.isdir(input_dir):
        sys.exit(-1)
    else:
        loop()
    


if __name__=='__main__':
    main()
    

