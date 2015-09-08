import unittest
from komfig import logger


MODULES = [
    'komlibs.textman.api.test.test_variables.TextmanApiVariablesTest',
    'komlibs.textman.api.test.test_summary.TextmanApiSummaryTest',
    'komlibs.textman.model.test.test_patterns.TextmanModelPatternsTest',
    'komlibs.events.api.test.test_user.EventsApiUserTest',
    'komlibs.general.validation.test.test_arguments.GeneralValidationArgumentsTest',
    'komlibs.graph.api.test.test_base.GraphApiBaseTest',
    'komlibs.graph.api.test.test_uri.GraphApiUriTest',
    'komlibs.graph.api.test.test_kin.GraphApiKinTest',
    'komlibs.gestaccount.user.test.test_userapi.GestaccountUserApiTest',
    'komlibs.gestaccount.agent.test.test_agentapi.GestaccountAgentApiTest',
    'komlibs.gestaccount.datasource.test.test_datasourceapi.GestaccountDatasourceApiTest',
    'komlibs.gestaccount.datapoint.test.test_datapointapi.GestaccountDatapointApiTest',
    'komlibs.gestaccount.widget.test.test_widgetapi.GestaccountWidgetApiTest',
    'komlibs.gestaccount.dashboard.test.test_dashboardapi.GestaccountDashboardApiTest',
    'komlibs.gestaccount.snapshot.test.test_snapshotapi.GestaccountSnapshotApiTest',
    'komlibs.gestaccount.circle.test.test_circleapi.GestaccountCircleApiTest',
    'komlibs.auth.test.test_authorization.AuthAuthorizationTest',
    'komlibs.auth.quotes.test.test_authorization.AuthQuotesAuthorizationTest',
    'komlibs.auth.quotes.test.test_deny.AuthQuotesDenyTest',
    'komlibs.auth.quotes.test.test_compare.AuthQuotesCompareTest',
    'komlibs.auth.quotes.test.test_update.AuthQuotesUpdateTest',
    'komlibs.auth.resources.test.test_authorization.AuthResourcesAuthorizationTest',
    'komlibs.auth.resources.test.test_update.AuthResourcesUpdateTest',
    'komlibs.auth.shared.test.test_authorization.AuthSharedAuthorizationTest',
    'komlibs.auth.shared.test.test_update.AuthSharedUpdateTest',
    'komlibs.auth.membership.test.test_update.AuthMembershipUpdateTest',
    'komfs.test.test_api.KomfsApiTest',
    'komcass.api.test.test_user.KomcassApiUserTest',
    'komcass.api.test.test_agent.KomcassApiAgentTest',
    'komcass.api.test.test_widget.KomcassApiWidgetTest',
    'komcass.api.test.test_dashboard.KomcassApiDashboardTest',
    'komcass.api.test.test_datapoint.KomcassApiDatapointTest',
    'komcass.api.test.test_datasource.KomcassApiDatasourceTest',
    'komcass.api.test.test_interface.KomcassApiInterfaceTest',
    'komcass.api.test.test_permission.KomcassApiPermissionTest',
    'komcass.api.test.test_quote.KomcassApiQuoteTest',
    'komcass.api.test.test_segment.KomcassApiSegmentTest',
    'komcass.api.test.test_snapshot.KomcassApiSnapshotTest',
    'komcass.api.test.test_graph.KomcassApiGraphTest',
    'komcass.api.test.test_circle.KomcassApiCircleTest',
    'komcass.api.test.test_events.KomcassApiEventsTest',
    'komlibs.interface.web.api.test.test_user.InterfaceWebApiUserTest',
    'komlibs.interface.web.api.test.test_agent.InterfaceWebApiAgentTest',
    'komlibs.interface.web.api.test.test_datasource.InterfaceWebApiDatasourceTest',
    'komlibs.interface.web.api.test.test_datapoint.InterfaceWebApiDatapointTest',
    'komlibs.interface.web.api.test.test_widget.InterfaceWebApiWidgetTest',
    'komlibs.interface.web.api.test.test_dashboard.InterfaceWebApiDashboardTest',
    'komlibs.interface.web.api.test.test_snapshot.InterfaceWebApiSnapshotTest',
    'komlibs.interface.web.api.test.test_circle.InterfaceWebApiCircleTest',
    'komlibs.interface.web.api.test.test_uri.InterfaceWebApiUriTest',
    'komlibs.interface.web.api.test.test_events.InterfaceWebApiEventsTest',
    'komlibs.interface.imc.model.test.test_messages.InterfaceImcModelMessagesTest',
    'komlibs.interface.imc.api.test.test_gestconsole.InterfaceImcApiGestconsoleTest',
    'komlibs.interface.imc.api.test.test_rescontrol.InterfaceImcApiRescontrolTest',
    'komlibs.interface.imc.api.test.test_storing.InterfaceImcApiStoringTest',
    'komlibs.interface.imc.api.test.test_textmining.InterfaceImcApiTextminingTest',
    'komlibs.interface.imc.api.test.test_events.InterfaceImcApiEventsTest',
    'komlibs.interface.imc.api.test.test_anomalies.InterfaceImcApiAnomaliesTest',
    ]

def run_tests():
    try:
        testsuite=unittest.defaultTestLoader.loadTestsFromNames(MODULES)
    except Exception as e:
        logger.logger.debug('Error loading TestSuite: '+str(e))
        return None
    if testsuite:
        logger.logger.debug('Executing tests...')
        results=unittest.TestResult()
        testsuite.run(results)
        logger.logger.debug(str(results))
        return results
    else:
        logger.logger.debug('No tests')
        return None

def send_report(results, email=False, logfile=False):
    if results and logfile:
        successes=results.testsRun
        logger.logger.debug('Tests Ran: '+str(results.testsRun))
        successes-=len(results.errors)
        logger.logger.debug('Error tests: '+str(len(results.errors)))
        for item in results.errors:
            logger.logger.debug('Test: '+str(item[0]))
            logger.logger.debug('Result: '+item[1])
        successes-=len(results.failures)
        logger.logger.debug('Failed tests: '+str(len(results.failures)))
        for item in results.failures:
            logger.logger.debug('Test: '+str(item[0]))
            logger.logger.debug('Result: '+item[1])
        logger.logger.debug('Skipped tests: '+str(len(results.skipped)))
        for item in results.skipped:
            logger.logger.debug('Test: '+str(item[0]))
            logger.logger.debug('Result: '+item[1])
        successes-=len(results.expectedFailures)
        logger.logger.debug('Expected failure tests: '+str(len(results.expectedFailures)))
        for item in results.expectedFailures:
            logger.logger.debug('Test: '+str(item[0]))
            logger.logger.debug('Result: '+item[1])
        successes-=len(results.unexpectedSuccesses)
        logger.logger.debug('Unexpected Success tests: '+str(len(results.unexpectedSuccesses)))
        for item in results.unexpectedSuccesses:
            logger.logger.debug('Test: '+str(item[0]))
            logger.logger.debug('Result: '+item[1])
        logger.logger.debug('Success tests: '+str(successes))


