'''
Default values for komlogs configuration parameters

'''

CONFIG_DIR = '.komlogs'
PASSWD_FILE = '/etc/passwd'
LOG_DIRNAME='log/'
LOG_LEVEL='DEBUG'
LOG_ROTATION=True
LOG_MAX_BYTES=10000
LOG_BACKUP_COUNT=3
LOG_FORMAT='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
COUNTERS_LOG_FORMAT='%(processName)s %(message)s'
COUNTERS_LOG_HOST='localhost'
COUNTERS_LOG_PORT=514
COUNTERS_LOG_FACILITY='local7'
