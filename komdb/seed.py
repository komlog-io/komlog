from komdb import connection
from komdb import schema
from komdb.config import mappings
import imp, os


def create_db():
    if schema.Base.metadata.create_all(connection.engine) == None:
        db = connection.Session()
        """ comprobamos que los tablespaces estan creados """
        tablespaces = db.execute("""select spcname from pg_tablespace""")
        existing_tss = tablespaces.fetchall()
        needed_tss = mappings.MAPPING_TABLESPACES.keys()
        create_tss=needed_tss[:]
        for needed_ts in needed_tss:
            for existing_ts in existing_tss:
                if existing_ts[0] == needed_ts:
                    """alter a las tablas correspondientes"""
                    for table in mappings.MAPPING_TABLESPACES[needed_ts]:
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
    constants = []
    objects = []
    db = connection.Session()
    module_dir = os.path.dirname(mappings.__file__)
    for module_name in mappings.MAPPING_MODULES:
        fp, pathname, description = imp.find_module(module_dir+'/'+module_name)
        try:
            module = imp.load_module(module_name, fp, pathname, description)
        except:
            print "Module loading exception: "+str(module_name)
            break
        finally:
            if fp:
                fp.close()
        for variable in dir(module):
            if isinstance(getattr(module,variable),int) or isinstance(getattr(module,variable),str):
                constant = (variable,getattr(module,variable))
                constants.append(constant)
        
    entry_list = mappings.map_messages_to_objects(constants)
    
    for entry in entry_list:
        try:
            new_object = getattr(schema,entry[0])(*entry[1:])
            db.add(new_object)
            db.commit()
        except:
            pass
    db.close()
    return True

def main():
    """main funcion when seed.py called from console"""
    create_db()
    configure_db()

if __name__=='__main__':
    main()
