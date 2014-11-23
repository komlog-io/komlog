import unittest
from komfig import logger


MODULES = [
    'komlibs.gestaccount.user.test.test_userapi.GestaccountUserApiTest',
    ]

def run_tests():
    testsuite=unittest.defaultTestLoader.loadTestsFromNames(MODULES)
    if testsuite:
        logger.logger.debug('Executing tests...')
        results=unittest.TestResult()
        testsuite.run(results)
        logger.logger.debug(str(results))
        return results
    else:
        logger.logger.debug('No tests')
        return None
