'''

Events templates

'''

from mako.template import Template
from komlibs.events.model import types

HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_USER=Template(
              "<div>Welcome to Komlog, <strong>${parameters['username']}!</strong></div>"
             )

HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_USER=Template(
              "<div />"
             )

HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_AGENT=Template(
              "<div>New agent joined</div>"
             )

HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_AGENT=Template(
              "<div>Agent ${parameters['agentname']} joined the system</div>"
             )

HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_DATASOURCE=Template(
              "<div>New Datasource</div>"
             )

HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_DATASOURCE=Template(
              "<div>Datasource <a onclick=\"PubSub.publish('loadSlide',{did:'${parameters['did']}'})\">${parameters['datasourcename']}</a> created.</div>"
             )

HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_DATAPOINT=Template(
              "<div>New Datapoint</div>"
             )

HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_DATAPOINT=Template(
              "<div>Datapoint <a onclick=\"PubSub.publish('loadSlide',{pid:'${parameters['pid']}'})\">${parameters['datapointname']}</a> created, \
                associated to datasource <a onclick=\"PubSub.publish('loadSlide',{did:'${parameters['did']}'})\">${parameters['datasourcename']}</a></div>"
             )

HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_WIDGET=Template(
              "<div>New Widget</div>"
             )

HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_WIDGET=Template(
              "<div>Widget <a onclick=\"PubSub.publish('loadSlide',{wid:'${parameters['wid']}'})\">${parameters['widgetname']}</a> created.</div>"
             )

HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_DASHBOARD=Template(
              "<div>New Dashboard</div>"
             )

HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_DASHBOARD=Template(
              "<div>Dashboard <a onclick=\"PubSub.publish('loadSlide',{bid:'${parameters['bid']}'})\">${parameters['dashboardname']}</a> created.</div>"
             )

HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_CIRCLE=Template(
              "<div>New Circle</div>"
             )

HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_CIRCLE=Template(
              "<div>Circle <strong>${parameters['circlename']}</strong> created.</div>"
             )

HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED=Template(
              "<div>New Snapshot Shared</div>"
             )

HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED=Template(
              "<div>New snapshot shared of <a onclick=\"PubSub.publish('loadSlide',{nid:'${parameters['nid']}'})\">${parameters['widgetname']}</a></div>"
             )

HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME=Template(
              "<div>New Snapshot Received</div>"
             )

HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME=Template(
              "<div>User <strong>${parameters['username']}</strong> shared a snapshot of <strong><a onclick=\"PubSub.publish('loadSlide',{nid:'${parameters['nid']}',tid:'${parameters['tid']}'})\">${parameters['widgetname']}</a></strong> with you.</div>"
             )

HTML_TITLE_TPL_USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION=Template(
              "<div>Can you help us identifying datapoints?</div>"
             )



HTML_BODY_TPL_USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION=Template(
              "<div>Please, help us identifying datapoints on report <strong>${parameters['did']}</strong></div>"
             )



HTML_TEMPLATES=[
    types.USER_EVENT_NOTIFICATION_NEW_USER,
    types.USER_EVENT_NOTIFICATION_NEW_AGENT,
    types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE,
    types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT,
    types.USER_EVENT_NOTIFICATION_NEW_WIDGET,
    types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD,
    types.USER_EVENT_NOTIFICATION_NEW_CIRCLE,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME,
    types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION,
]

HTML_BODY_TEMPLATES={
    types.USER_EVENT_NOTIFICATION_NEW_USER:HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_USER,
    types.USER_EVENT_NOTIFICATION_NEW_AGENT:HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_AGENT,
    types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_DATASOURCE,
    types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_DATAPOINT,
    types.USER_EVENT_NOTIFICATION_NEW_WIDGET:HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_WIDGET,
    types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_DASHBOARD,
    types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_CIRCLE,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED:HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME:HTML_BODY_TPL_USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME,
    types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION: HTML_BODY_TPL_USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION,
}

HTML_TITLE_TEMPLATES={
    types.USER_EVENT_NOTIFICATION_NEW_USER:HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_USER,
    types.USER_EVENT_NOTIFICATION_NEW_AGENT:HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_AGENT,
    types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_DATASOURCE,
    types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_DATAPOINT,
    types.USER_EVENT_NOTIFICATION_NEW_WIDGET:HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_WIDGET,
    types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_DASHBOARD,
    types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_CIRCLE,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED:HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED,
    types.USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME:HTML_TITLE_TPL_USER_EVENT_NOTIFICATION_NEW_SNAPSHOT_SHARED_WITH_ME,
    types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION: HTML_TITLE_TPL_USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION,
}

