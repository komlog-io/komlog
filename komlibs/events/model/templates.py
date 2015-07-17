'''

Events templates

'''

from mako.template import Template

HTML_TPL_NEW_USER=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">Welcome to Komlog, ${parameters['username']}!</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_NEW_AGENT=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">New Agent</div>\
                <div class=\"userevents-body\">Agent ${parameters['agentname']} was created</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_NEW_DATASOURCE=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">New Datasource</div>\
                <div class=\"userevents-body\">Datasource <a onclick=\"PubSub.publish('loadSlide',{did:'${parameters['did']}'})\">${parameters['datasourcename']}</a> created.</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_NEW_DATAPOINT=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">New Datapoint</div>\
                <div class=\"userevents-body\">Datapoint <a onclick=\"PubSub.publish('loadSlide',{pid:'${parameters['pid']}'})\">${parameters['datapointname']}</a> created, \
                associated to datasource <a onclick=\"PubSub.publish('loadSlide',{did:'${parameters['did']}'})\">${parameters['datasourcename']}</a></div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_NEW_WIDGET=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">New Widget</div>\
                <div class=\"userevents-body\">Widget <a onclick=\"PubSub.publish('loadSlide',{wid:'${parameters['wid']}'})\">${parameters['widgetname']}</a> created.</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_NEW_DASHBOARD=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">New Dashboard</div>\
                <div class=\"userevents-body\">Dashboard <a onclick=\"PubSub.publish('loadSlide',{bid:'${parameters['bid']}'})\">${parameters['dashboardname']}</a> created.</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

HTML_TPL_NEW_CIRCLE=Template(
              "<div class=\"userevents-panel\">\
                <div class=\"userevents-title\">New Circle</div>\
                <div class=\"userevents-body\">Circle ${parameters['circlename']} created.</div>\
              </div>\
              <div class=\"userevents-badge info\"><i class=\"glyphicon glyphicon-info-sign\"></i></div>"
             )

