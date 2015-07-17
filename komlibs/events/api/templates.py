'''

api for getting event templates

'''

from komlibs.events.model import types, priorities, templates

HTML_TEMPLATES={types.NEW_USER:templates.HTML_TPL_NEW_USER,
                types.NEW_AGENT:templates.HTML_TPL_NEW_AGENT,
                types.NEW_DATASOURCE:templates.HTML_TPL_NEW_DATASOURCE,
                types.NEW_DATAPOINT:templates.HTML_TPL_NEW_DATAPOINT,
                types.NEW_WIDGET:templates.HTML_TPL_NEW_WIDGET,
                types.NEW_DASHBOARD:templates.HTML_TPL_NEW_DASHBOARD,
                types.NEW_CIRCLE:templates.HTML_TPL_NEW_CIRCLE,
}

def get_html_template(event_type, parameters):
    if event_type in HTML_TEMPLATES:
        return HTML_TEMPLATES[event_type].render(parameters=parameters)
    else:
        return ''


