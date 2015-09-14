'''

Events templates

'''

from mako.template import Template
from komlibs.events.model import types

HTML_TPL_USER_EVENT_NOTIFICATION_NEW_USER=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">Welcome to Komlog, ${parameters['username']}!</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_USER_EVENT_NOTIFICATION_NEW_AGENT=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">New Agent</div>\
                <div class=\"userevents-body\">Agent ${parameters['agentname']} was created</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_USER_EVENT_NOTIFICATION_NEW_DATASOURCE=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">New Datasource</div>\
                <div class=\"userevents-body\">Datasource <a onclick=\"PubSub.publish('loadSlide',{did:'${parameters['did']}'})\">${parameters['datasourcename']}</a> created.</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_USER_EVENT_NOTIFICATION_NEW_DATAPOINT=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">New Datapoint</div>\
                <div class=\"userevents-body\">Datapoint <a onclick=\"PubSub.publish('loadSlide',{pid:'${parameters['pid']}'})\">${parameters['datapointname']}</a> created, \
                associated to datasource <a onclick=\"PubSub.publish('loadSlide',{did:'${parameters['did']}'})\">${parameters['datasourcename']}</a></div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_USER_EVENT_NOTIFICATION_NEW_WIDGET=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">New Widget</div>\
                <div class=\"userevents-body\">Widget <a onclick=\"PubSub.publish('loadSlide',{wid:'${parameters['wid']}'})\">${parameters['widgetname']}</a> created.</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_USER_EVENT_NOTIFICATION_NEW_DASHBOARD=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">New Dashboard</div>\
                <div class=\"userevents-body\">Dashboard <a onclick=\"PubSub.publish('loadSlide',{bid:'${parameters['bid']}'})\">${parameters['dashboardname']}</a> created.</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_USER_EVENT_NOTIFICATION_NEW_CIRCLE=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">New Circle</div>\
                <div class=\"userevents-body\">Circle ${parameters['circlename']} created.</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">Help needed identifying datapoints</div>\
                <div class=\"userevents-body\">Please, help us identifying datapoints on report ${parameters['did']}</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-exclamation-sign\"></i></div>"
             )



HTML_TEMPLATES={
    types.USER_EVENT_NOTIFICATION_NEW_USER:HTML_TPL_USER_EVENT_NOTIFICATION_NEW_USER,
    types.USER_EVENT_NOTIFICATION_NEW_AGENT:HTML_TPL_USER_EVENT_NOTIFICATION_NEW_AGENT,
    types.USER_EVENT_NOTIFICATION_NEW_DATASOURCE:HTML_TPL_USER_EVENT_NOTIFICATION_NEW_DATASOURCE,
    types.USER_EVENT_NOTIFICATION_NEW_DATAPOINT:HTML_TPL_USER_EVENT_NOTIFICATION_NEW_DATAPOINT,
    types.USER_EVENT_NOTIFICATION_NEW_WIDGET:HTML_TPL_USER_EVENT_NOTIFICATION_NEW_WIDGET,
    types.USER_EVENT_NOTIFICATION_NEW_DASHBOARD:HTML_TPL_USER_EVENT_NOTIFICATION_NEW_DASHBOARD,
    types.USER_EVENT_NOTIFICATION_NEW_CIRCLE:HTML_TPL_USER_EVENT_NOTIFICATION_NEW_CIRCLE,
    types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION: HTML_TPL_USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION,
}

