'''
Created on 27/02/2015

@author: komlog crew
'''

from komlog.komcass.model.orm import graph as ormgraph
from komlog.komcass.model.statement import graph as stmtgraph
from komlog.komcass import connection, exceptions

@exceptions.ExceptionHandler
def get_uri_in_relations(idd):
    relations=[]
    row=connection.session.execute(stmtgraph.S_A_GRURIIN_B_IDD,(idd,))
    if row:
        for r in row:
            relations.append(ormgraph.UriRelation(**r))
    return relations

@exceptions.ExceptionHandler
def get_uri_out_relations(ido):
    relations=[]
    row=connection.session.execute(stmtgraph.S_A_GRURIOUT_B_IDO,(ido,))
    if row:
        for r in row:
            relations.append(ormgraph.UriRelation(**r))
    return relations

@exceptions.ExceptionHandler
def get_uri_in_vertices(idd):
    vertices=[]
    row=connection.session.execute(stmtgraph.S_IDO_GRURIIN_B_IDD,(idd,))
    if row:
        for r in row:
            vertices.append(r['ido'])
    return vertices

@exceptions.ExceptionHandler
def get_uri_out_vertices(ido):
    vertices=[]
    row=connection.session.execute(stmtgraph.S_IDD_GRURIOUT_B_IDO,(ido,))
    if row:
        for r in row:
            vertices.append(r['idd'])
    return vertices

@exceptions.ExceptionHandler
def get_uri_in_relation(idd, ido):
    row=connection.session.execute(stmtgraph.S_A_GRURIIN_B_IDD_IDO,(idd,ido))
    return ormgraph.UriRelation(**row[0]) if row else None

@exceptions.ExceptionHandler
def get_uri_out_relation(ido, idd):
    row=connection.session.execute(stmtgraph.S_A_GRURIOUT_B_IDO_IDD,(ido,idd))
    return ormgraph.UriRelation(**row[0]) if row else None

@exceptions.ExceptionHandler
def delete_uri_in_relation(idd, ido):
    row=connection.session.execute(stmtgraph.D_A_GRURIIN_B_IDD_IDO,(idd,ido))
    return True

@exceptions.ExceptionHandler
def delete_uri_out_relation(ido, idd):
    row=connection.session.execute(stmtgraph.D_A_GRURIOUT_B_IDO_IDD,(ido,idd))
    return True

@exceptions.ExceptionHandler
def insert_uri_in_relation(relation):
    if not isinstance(relation, ormgraph.UriRelation):
        return False
    connection.session.execute(stmtgraph.I_A_GRURIIN,(relation.idd,relation.ido,relation.type,relation.creation_date,relation.uri))
    return True

@exceptions.ExceptionHandler
def insert_uri_out_relation(relation):
    if not isinstance(relation, ormgraph.UriRelation):
        return False
    connection.session.execute(stmtgraph.I_A_GRURIOUT,(relation.ido,relation.idd,relation.type,relation.creation_date,relation.uri))
    return True

# KIN RELATIONS

@exceptions.ExceptionHandler
def get_kin_in_relations(idd):
    relations=[]
    row=connection.session.execute(stmtgraph.S_A_GRKININ_B_IDD,(idd,))
    if row:
        for r in row:
            relations.append(ormgraph.KinRelation(**r))
    return relations

@exceptions.ExceptionHandler
def get_kin_out_relations(ido):
    relations=[]
    row=connection.session.execute(stmtgraph.S_A_GRKINOUT_B_IDO,(ido,))
    if row:
        for r in row:
            relations.append(ormgraph.KinRelation(**r))
    return relations

@exceptions.ExceptionHandler
def get_kin_in_vertices(idd):
    vertices=[]
    row=connection.session.execute(stmtgraph.S_IDO_GRKININ_B_IDD,(idd,))
    if row:
        for r in row:
            vertices.append(r['ido'])
    return vertices

@exceptions.ExceptionHandler
def get_kin_out_vertices(ido):
    vertices=[]
    row=connection.session.execute(stmtgraph.S_IDD_GRKINOUT_B_IDO,(ido,))
    if row:
        for r in row:
            vertices.append(r['idd'])
    return vertices

@exceptions.ExceptionHandler
def get_kin_in_relation(idd, ido):
    row=connection.session.execute(stmtgraph.S_A_GRKININ_B_IDD_IDO,(idd,ido))
    return ormgraph.KinRelation(**row[0]) if row else None

@exceptions.ExceptionHandler
def get_kin_out_relation(ido, idd):
    row=connection.session.execute(stmtgraph.S_A_GRKINOUT_B_IDO_IDD,(ido,idd))
    return ormgraph.KinRelation(**row[0]) if row else None

@exceptions.ExceptionHandler
def insert_kin_in_relation(relation):
    if not isinstance(relation, ormgraph.KinRelation):
        return False
    connection.session.execute(stmtgraph.I_A_GRKININ,(relation.idd,relation.ido,relation.type,relation.creation_date,relation.params))
    return True

@exceptions.ExceptionHandler
def insert_kin_out_relation(relation):
    if not isinstance(relation, ormgraph.KinRelation):
        return False
    connection.session.execute(stmtgraph.I_A_GRKINOUT,(relation.ido,relation.idd,relation.type,relation.creation_date,relation.params))
    return True

@exceptions.ExceptionHandler
def delete_kin_in_relation(idd, ido):
    row=connection.session.execute(stmtgraph.D_A_GRKININ_B_IDD_IDO,(idd,ido))
    return True

@exceptions.ExceptionHandler
def delete_kin_out_relation(ido, idd):
    row=connection.session.execute(stmtgraph.D_A_GRKINOUT_B_IDO_IDD,(ido,idd))
    return True

