from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.auth.model.quotes import Quotes


operation_quotes = {
    Operations.NEW_USER: [
        Quotes.quo_user_total_agents,
        Quotes.quo_user_total_datasources,
        Quotes.quo_user_total_datapoints,
        Quotes.quo_user_total_widgets,
        Quotes.quo_user_total_dashboards,
        Quotes.quo_user_total_snapshots,
        Quotes.quo_user_total_circles,
    ],
    Operations.NEW_AGENT: [
        Quotes.quo_user_total_agents
    ],
    Operations.NEW_DATASOURCE: [
        Quotes.quo_agent_total_datasources,
        Quotes.quo_user_total_datasources
    ],
    Operations.NEW_DATASOURCE_DATAPOINT: [
        Quotes.quo_datasource_total_datapoints,
        Quotes.quo_agent_total_datapoints,
        Quotes.quo_user_total_datapoints
    ],
    Operations.NEW_USER_DATAPOINT: [
        Quotes.quo_agent_total_datapoints,
        Quotes.quo_user_total_datapoints
    ],
    Operations.NEW_WIDGET: [
        Quotes.quo_user_total_widgets
    ],
    Operations.NEW_DASHBOARD: [
        Quotes.quo_user_total_dashboards
    ],
    Operations.NEW_WIDGET_SYSTEM: [
        Quotes.quo_user_total_widgets
    ],
    Operations.NEW_SNAPSHOT: [
        Quotes.quo_user_total_snapshots
    ],
    Operations.NEW_CIRCLE: [
        Quotes.quo_user_total_circles,
        Quotes.quo_circle_total_members
    ],
    Operations.UPDATE_CIRCLE_MEMBERS: [
        Quotes.quo_circle_total_members
    ],
    Operations.DATASOURCE_DATA_STORED: [
        Quotes.quo_daily_datasource_occupation,
        Quotes.quo_daily_user_datasources_occupation,
        Quotes.quo_user_total_occupation,
    ],
    Operations.DELETE_AGENT: [
        Quotes.quo_user_total_agents
    ],
    Operations.DELETE_DATASOURCE: [
        Quotes.quo_agent_total_datasources,
        Quotes.quo_user_total_datasources
    ],
    Operations.DELETE_DATASOURCE_DATAPOINT: [
        Quotes.quo_datasource_total_datapoints,
        Quotes.quo_agent_total_datapoints,
        Quotes.quo_user_total_datapoints
    ],
    Operations.DELETE_USER_DATAPOINT: [
        Quotes.quo_user_total_datapoints
    ],
    Operations.DELETE_WIDGET: [
        Quotes.quo_user_total_widgets
    ],
    Operations.DELETE_DASHBOARD: [
        Quotes.quo_user_total_dashboards
    ],
    Operations.DELETE_SNAPSHOT: [
        Quotes.quo_user_total_snapshots
    ],
    Operations.DELETE_CIRCLE: [
        Quotes.quo_user_total_circles,
    ],
    Operations.DISSOCIATE_DATAPOINT_FROM_DATASOURCE: [
        Quotes.quo_datasource_total_datapoints,
    ],
}

