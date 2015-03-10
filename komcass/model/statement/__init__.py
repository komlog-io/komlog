STATEMENT_MODULES = ['user','agent','datasource','datapoint','widget','dashboard','interface','permission','quote','segment','snapshot','graph']

import sys

def get_statement(stmt):
    for i in STATEMENT_MODULES:
        try:
            query=sys.modules['komcass.model.statement.'+i].get_statement(stmt)
            if query:
                return query
        except KeyError:
            __import__('komcass.model.statement.'+i)
            query=sys.modules['komcass.model.statement.'+i].get_statement(stmt)
            if query:
                return query

    return None

