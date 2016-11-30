import unittest
from komlog.komfig import logging


MODULES = [
    'komlog.komlibs.textman.api.test.test_variables.TextmanApiVariablesTest',
    'komlog.komlibs.textman.api.test.test_summary.TextmanApiSummaryTest',
    'komlog.komlibs.textman.model.test.test_patterns.TextmanModelPatternsTest',
    'komlog.komlibs.events.api.test.test_user.EventsApiUserTest',
    'komlog.komlibs.events.api.test.test_user_responses.EventsApiUserResponsesTest',
    'komlog.komlibs.events.api.test.test_summary.EventsApiSummaryTest',
    'komlog.komlibs.general.validation.test.test_arguments.GeneralValidationArgumentsTest',
    'komlog.komlibs.general.time.test.test_timeuuid.GeneralTimeTimeuuidTest',
    'komlog.komlibs.graph.api.test.test_base.GraphApiBaseTest',
    'komlog.komlibs.graph.api.test.test_uri.GraphApiUriTest',
    'komlog.komlibs.graph.api.test.test_kin.GraphApiKinTest',
    'komlog.komlibs.gestaccount.user.test.test_userapi.GestaccountUserApiTest',
    'komlog.komlibs.gestaccount.agent.test.test_agentapi.GestaccountAgentApiTest',
    'komlog.komlibs.gestaccount.datasource.test.test_datasourceapi.GestaccountDatasourceApiTest',
    'komlog.komlibs.gestaccount.datapoint.test.test_datapointapi.GestaccountDatapointApiTest',
    'komlog.komlibs.gestaccount.widget.test.test_widgetapi.GestaccountWidgetApiTest',
    'komlog.komlibs.gestaccount.dashboard.test.test_dashboardapi.GestaccountDashboardApiTest',
    'komlog.komlibs.gestaccount.snapshot.test.test_snapshotapi.GestaccountSnapshotApiTest',
    'komlog.komlibs.gestaccount.circle.test.test_circleapi.GestaccountCircleApiTest',
    'komlog.komlibs.gestaccount.common.test.test_delete.GestaccountCommonDeleteTest',
    'komlog.komlibs.auth.test.test_authorization.AuthAuthorizationTest',
    'komlog.komlibs.auth.test.test_passport.AuthPassportTest',
    'komlog.komlibs.auth.test.test_session.AuthSessionTest',
    'komlog.komlibs.auth.quotes.test.test_authorization.AuthQuotesAuthorizationTest',
    'komlog.komlibs.auth.quotes.test.test_compare.AuthQuotesCompareTest',
    'komlog.komlibs.auth.quotes.test.test_update.AuthQuotesUpdateTest',
    'komlog.komlibs.auth.resources.test.test_authorization.AuthResourcesAuthorizationTest',
    'komlog.komlibs.auth.resources.test.test_update.AuthResourcesUpdateTest',
    'komlog.komlibs.auth.tickets.test.test_provision.AuthTicketsProvisionTest',
    'komlog.komlibs.auth.tickets.test.test_authorization.AuthTicketsAuthorizationTest',
    'komlog.komlibs.payment.test.test_api.KomlibsPaymentApiTest',
    'komlog.komfs.test.test_api.KomfsApiTest',
    'komlog.komcass.api.test.test_user.KomcassApiUserTest',
    'komlog.komcass.api.test.test_agent.KomcassApiAgentTest',
    'komlog.komcass.api.test.test_widget.KomcassApiWidgetTest',
    'komlog.komcass.api.test.test_dashboard.KomcassApiDashboardTest',
    'komlog.komcass.api.test.test_datapoint.KomcassApiDatapointTest',
    'komlog.komcass.api.test.test_datasource.KomcassApiDatasourceTest',
    'komlog.komcass.api.test.test_interface.KomcassApiInterfaceTest',
    'komlog.komcass.api.test.test_permission.KomcassApiPermissionTest',
    'komlog.komcass.api.test.test_quote.KomcassApiQuoteTest',
    'komlog.komcass.api.test.test_segment.KomcassApiSegmentTest',
    'komlog.komcass.api.test.test_snapshot.KomcassApiSnapshotTest',
    'komlog.komcass.api.test.test_graph.KomcassApiGraphTest',
    'komlog.komcass.api.test.test_circle.KomcassApiCircleTest',
    'komlog.komcass.api.test.test_events.KomcassApiEventsTest',
    'komlog.komcass.api.test.test_ticket.KomcassApiTicketTest',
    'komlog.komlibs.interface.imc.model.test.test_messages.InterfaceImcModelMessagesTest',
    'komlog.komlibs.interface.imc.api.test.test_gestconsole.InterfaceImcApiGestconsoleTest',
    'komlog.komlibs.interface.imc.api.test.test_rescontrol.InterfaceImcApiRescontrolTest',
    'komlog.komlibs.interface.imc.api.test.test_textmining.InterfaceImcApiTextminingTest',
    'komlog.komlibs.interface.imc.api.test.test_events.InterfaceImcApiEventsTest',
    'komlog.komlibs.interface.imc.api.test.test_anomalies.InterfaceImcApiAnomaliesTest',
    'komlog.komlibs.interface.imc.api.test.test_lambdas.InterfaceImcApiLambdasTest',
    'komlog.komlibs.interface.web.api.test.test_login.InterfaceWebApiLoginTest',
    'komlog.komlibs.interface.web.api.test.test_user.InterfaceWebApiUserTest',
    'komlog.komlibs.interface.web.api.test.test_agent.InterfaceWebApiAgentTest',
    'komlog.komlibs.interface.web.api.test.test_datasource.InterfaceWebApiDatasourceTest',
    'komlog.komlibs.interface.web.api.test.test_datapoint.InterfaceWebApiDatapointTest',
    'komlog.komlibs.interface.web.api.test.test_widget.InterfaceWebApiWidgetTest',
    'komlog.komlibs.interface.web.api.test.test_dashboard.InterfaceWebApiDashboardTest',
    'komlog.komlibs.interface.web.api.test.test_snapshot.InterfaceWebApiSnapshotTest',
    'komlog.komlibs.interface.web.api.test.test_circle.InterfaceWebApiCircleTest',
    'komlog.komlibs.interface.web.api.test.test_uri.InterfaceWebApiUriTest',
    'komlog.komlibs.interface.web.api.test.test_events.InterfaceWebApiEventsTest',
    'komlog.komlibs.interface.websocket.protocol.v1.model.test.test_message.InterfaceWebSocketProtocolV1ModelMessageTest',
    'komlog.komlibs.interface.websocket.protocol.v1.model.test.test_operation.InterfaceWebSocketProtocolV1ModelOperationTest',
    'komlog.komlibs.interface.websocket.protocol.v1.processing.test.test_operation.InterfaceWebSocketProtocolV1ProcessingOperationTest',
    'komlog.komlibs.interface.websocket.protocol.v1.processing.test.test_message.InterfaceWebSocketProtocolV1ProcessingMessageTest',
    'komlog.komlibs.interface.websocket.protocol.v1.test.test_api.InterfaceWebSocketProtocolV1ApiTest',
    'komlog.komlibs.interface.websocket.test.test_api.InterfaceWebSocketApiTest',
    'komlog.komlibs.interface.websocket.test.test_session.InterfaceWebSocketSessionTest',
    'komlog.komlibs.interface.websocket.model.test.test_response.InterfaceWebSocketModelResponseTest',
]

def run_tests():
    try:
        testsuite=unittest.defaultTestLoader.loadTestsFromNames(MODULES)
    except Exception as e:
        logging.logger.debug('Error loading TestSuite: '+str(e))
        return None
    if testsuite:
        logging.logger.debug('Executing tests...')
        results=unittest.TestResult()
        testsuite.run(results)
        logging.logger.debug(str(results))
        return results
    else:
        logging.logger.debug('No tests')
        return None

def send_report(results, email=False, logfile=False):
    if results and logfile:
        successes=results.testsRun
        logging.logger.debug('Tests Ran: '+str(results.testsRun))
        successes-=len(results.errors)
        logging.logger.debug('Error tests: '+str(len(results.errors)))
        for item in results.errors:
            logging.logger.debug('Test: '+str(item[0]))
            logging.logger.debug('Result: '+item[1])
        successes-=len(results.failures)
        logging.logger.debug('Failed tests: '+str(len(results.failures)))
        for item in results.failures:
            logging.logger.debug('Test: '+str(item[0]))
            logging.logger.debug('Result: '+item[1])
        logging.logger.debug('Skipped tests: '+str(len(results.skipped)))
        for item in results.skipped:
            logging.logger.debug('Test: '+str(item[0]))
            logging.logger.debug('Result: '+item[1])
        successes-=len(results.expectedFailures)
        logging.logger.debug('Expected failure tests: '+str(len(results.expectedFailures)))
        for item in results.expectedFailures:
            logging.logger.debug('Test: '+str(item[0]))
            logging.logger.debug('Result: '+item[1])
        successes-=len(results.unexpectedSuccesses)
        logging.logger.debug('Unexpected Success tests: '+str(len(results.unexpectedSuccesses)))
        for item in results.unexpectedSuccesses:
            logging.logger.debug('Test: '+str(item[0]))
            logging.logger.debug('Result: '+item[1])
        logging.logger.debug('Success tests: '+str(successes))


