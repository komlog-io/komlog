import ConfigParser
import os, getpass

config=None

class Config(ConfigParser.ConfigParser):
    def __init__(self, conf_file):
        ConfigParser.ConfigParser.__init__(self)
        self.conf_file = conf_file
        self.root_dir = os.path.split(conf_file)[0]
        try: self.readfp(open(self.conf_file), 'r')
        except IOError as Err:
            if Err.errno == 2: pass
            else: raise Err

    def set(self, section, option, value):
        ConfigParser.ConfigParser.set(self, section, option, str(value))
        
    def get(self, section, option):
        return ConfigParser.ConfigParser.get(self, section, option)
    
    def safe_set(self, section, option, value):
        if self.has_section(section):
            self.set(section, option, str(value))
        else:
            self.add_section(section)
            self.set(section, option, str(value))

    def safe_get(self, section, option):
        if self.has_option(section, option):
            return self.get(section, option)
        else:
            return None

def initialize_config(cfg_file):
    ''' This function return the handler to the configuration file.
    If this is the first execution of the agent, create from a template '''
    global config
    if os.path.isfile(cfg_file):
        config=Config(cfg_file)
        if config:
            return True
        else:
            return False
    else:
        return False

