import connection
import schema


tablespace_relations = {'tbs_users':['users','user_types','user_states','user_capabilities'],
                        'tbs_agents':['agents','agent_types','agent_states','agent_capabilities'],
                        'tbs_datasources':['datasources','datasource_types','datasource_states','datasource_capabilities','datasource_config'],
                        'tbs_datapoints':['datapoints','datapoint_types','datapoint_states','datapoint_capabilities'],
                        'tbs_samples':['samples','sample_types','sample_states','sample_capabilities']}


def create_db():
    if schema.Base.metadata.create_all(connection.engine) == None:
        db = connection.Session()
        """ comprobamos que los tablespaces estan creados """
        tablespaces = db.execute("""select spcname from pg_tablespace""")
        existing_tss = tablespaces.fetchall()
        needed_tss = tablespace_relations.keys()
        create_tss=needed_tss[:]
        for needed_ts in needed_tss:
            for existing_ts in existing_tss:
                if existing_ts[0] == needed_ts:
                    """alter a las tablas correspondientes"""
                    for table in tablespace_relations[needed_ts]:
                        query='ALTER TABLE '+table+' SET TABLESPACE '+needed_ts
                        db.execute(query)
                    """eliminamos el needed_ts de la lista"""
                    create_tss.remove(needed_ts)
                    break
        if len(create_tss) > 0:
            for create_ts in create_tss:
                print "El tablespace "+create_ts+" no existe, es necesario su creacion"
    db.close()
    return True

def configure_db():
    """ This function loads the configuration to the db"""
    return True

