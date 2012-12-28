import ConfigParser
import os, getpass

DEFAULT_DIR = '/.komlog/'
DEFAULT_FILE = 'komlogd.cfg'
PASSWD_FILE = '/etc/passwd'

class Config(ConfigParser.ConfigParser):
    def __init__(self, conf_file):
        ConfigParser.ConfigParser.__init__(self)
        self.conf_file = conf_file
        try: self.readfp(open(self.conf_file), 'r')
        except IOError as Err:
            if Err.errno == 2: pass
            else: raise Err

    def set(self, section, option, value):
        ConfigParser.ConfigParser.set(self, section, option, str(value))
        
    def get(self, section, option):
        return ConfigParser.ConfigParser.get(self, section, option)
    
    def safe_set(self, section, option, value):
        print "safe_set"
        if self.has_section(section):
            print "has section"+str(section)
            print "set: "+str(option)+' - '+str(value)
            self.set(section, option, str(value))
        else:
            self.add_section(section)
            self.set(section, option, str(value))

    def safe_get(self, section, option):
        if self.has_option(section, option):
            return self.get(section, option)
        else:
            return None

    def save(self):
        self.write(open(self.conf_file, 'w'))
        

    def __del__(self):
        self.save()

def get_cfg_file():
    HOME = os.getenv('HOME')
    if not HOME:
        user = getpass.getuser()
        try:
            passwd_file = open(PASSWD_FILE,'r')
            for line in passwd_file:
                if line.split(':')[0] == user:
                    HOME = line.split(':')[5]
        except:
            print "Error searching $HOME directory"
            exit()
        else:
            if not HOME:
                print "Error: $HOME directory not found"
                exit()
    cfg_file = HOME+DEFAULT_DIR+DEFAULT_FILE 
    return cfg_file