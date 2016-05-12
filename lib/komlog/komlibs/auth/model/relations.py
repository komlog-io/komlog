from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.auth.model.quotes import Quotes


operation_quotes = {
    Operations.NEW_AGENT: [
        Quotes.quo_static_user_total_agents
    ],
    Operations.NEW_DATASOURCE: [
        Quotes.quo_static_agent_total_datasources,
        Quotes.quo_static_user_total_datasources
    ],
    Operations.NEW_DATAPOINT: [
        Quotes.quo_static_datasource_total_datapoints,
        Quotes.quo_static_agent_total_datapoints,
        Quotes.quo_static_user_total_datapoints
    ],
    Operations.NEW_WIDGET: [
        Quotes.quo_static_user_total_widgets
    ],
    Operations.NEW_DASHBOARD: [
        Quotes.quo_static_user_total_dashboards
    ],
    Operations.NEW_WIDGET_SYSTEM: [
        Quotes.quo_static_user_total_widgets
    ],
    Operations.NEW_SNAPSHOT: [
        Quotes.quo_static_user_total_snapshots
    ],
    Operations.NEW_CIRCLE: [
        Quotes.quo_static_user_total_circles,
        Quotes.quo_static_circle_total_members
    ],
    Operations.UPDATE_CIRCLE_MEMBERS: [
        Quotes.quo_static_circle_total_members
    ],
    Operations.DATASOURCE_DATA_STORED: [
        Quotes.quo_daily_datasource_occupation,
        Quotes.quo_daily_user_datasources_occupation
    ]
}

