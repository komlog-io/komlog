'''
Default values for komlogs configuration parameters

'''

CONFIG_DIR = '.komlogs'
PASSWD_FILE = '/etc/passwd'
LOG_DIRNAME='logs/'
LOG_LEVEL='DEBUG'
LOG_ROTATION=True
LOG_MAX_BYTES=10000
LOG_BACKUP_COUNT=3
LOG_FORMAT='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
