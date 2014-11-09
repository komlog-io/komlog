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

def get(option, section=None):
    global config
    params=option.split(':')
    if len(params)==2 and config.has_option(params[0], params[1]):
        return config.get(params[0], params[1])
    elif not section is None and config.has_option(section, option):
        return config.get(section, option)
    else:
        return None

