'''
Created on 27/02/2015

@author: komlog crew
'''

from komcass.model.orm import graph as ormgraph
from komcass.model.statement import graph as stmtgraph
from komcass import exceptions, connection

def get_member_in_relations(idd):
    relations=[]
    row=connection.session.execute(stmtgraph.S_A_GRMEMBERIN_B_IDD,(idd,))
    if row:
        for r in row:
            relations.append(ormgraph.MemberRelation(**r))
    return relations

def get_member_out_relations(ido):
    relations=[]
    row=connection.session.execute(stmtgraph.S_A_GRMEMBEROUT_B_IDO,(ido,))
    if row:
        for r in row:
            relations.append(ormgraph.MemberRelation(**r))
    return relations

def get_member_in_vertices(idd):
    vertices=[]
    row=connection.session.execute(stmtgraph.S_IDO_GRMEMBERIN_B_IDD,(idd,))
    if row:
        for r in row:
            vertices.append(r['ido'])
    return vertices

def get_member_out_vertices(ido):
    vertices=[]
    row=connection.session.execute(stmtgraph.S_IDD_GRMEMBEROUT_B_IDO,(ido,))
    if row:
        for r in row:
            vertices.append(r['idd'])
    return vertices

def get_member_in_relation(idd, ido):
    row=connection.session.execute(stmtgraph.S_A_GRMEMBERIN_B_IDD_IDO,(idd,ido))
    return ormgraph.MemberRelation(**row[0]) if row else None

def get_member_out_relation(ido, idd):
    row=connection.session.execute(stmtgraph.S_A_GRMEMBEROUT_B_IDO_IDD,(ido,idd))
    return ormgraph.MemberRelation(**row[0]) if row else None

def get_bounded_share_in_relations(idd):
    relations=[]
    row=connection.session.execute(stmtgraph.S_A_GRBOUNDEDSHAREIN_B_IDD,(idd,))
    if row:
        for r in row:
            relations.append(ormgraph.BoundedShareRelation(**r))
    return relations

def get_bounded_share_out_relations(ido):
    relations=[]
    row=connection.session.execute(stmtgraph.S_A_GRBOUNDEDSHAREOUT_B_IDO,(ido,))
    if row:
        for r in row:
            relations.append(ormgraph.BoundedShareRelation(**r))
    return relations

def get_bounded_share_in_vertices(idd):
    vertices=[]
    row=connection.session.execute(stmtgraph.S_IDO_GRBOUNDEDSHAREIN_B_IDD,(idd,))
    if row:
        for r in row:
            vertices.append(r['ido'])
    return vertices

def get_bounded_share_out_vertices(ido):
    vertices=[]
    row=connection.session.execute(stmtgraph.S_IDD_GRBOUNDEDSHAREOUT_B_IDO,(ido,))
    if row:
        for r in row:
            vertices.append(r['idd'])
    return vertices

def get_bounded_share_in_relation(idd, ido):
    row=connection.session.execute(stmtgraph.S_A_GRBOUNDEDSHAREIN_B_IDD_IDO,(idd,ido))
    return ormgraph.BoundedShareRelation(**row[0]) if row else None

def get_bounded_share_out_relation(ido, idd):
    row=connection.session.execute(stmtgraph.S_A_GRBOUNDEDSHAREOUT_B_IDO_IDD,(ido,idd))
    return ormgraph.BoundedShareRelation(**row[0]) if row else None

def get_uri_in_relations(idd):
    relations=[]
    row=connection.session.execute(stmtgraph.S_A_GRURIIN_B_IDD,(idd,))
    if row:
        for r in row:
            relations.append(ormgraph.UriRelation(**r))
    return relations

def get_uri_out_relations(ido):
    relations=[]
    row=connection.session.execute(stmtgraph.S_A_GRURIOUT_B_IDO,(ido,))
    if row:
        for r in row:
            relations.append(ormgraph.UriRelation(**r))
    return relations

def get_uri_in_vertices(idd):
    vertices=[]
    row=connection.session.execute(stmtgraph.S_IDO_GRURIIN_B_IDD,(idd,))
    if row:
        for r in row:
            vertices.append(r['ido'])
    return vertices

def get_uri_out_vertices(ido):
    vertices=[]
    row=connection.session.execute(stmtgraph.S_IDD_GRURIOUT_B_IDO,(ido,))
    if row:
        for r in row:
            vertices.append(r['idd'])
    return vertices

def get_uri_in_relation(idd, ido):
    row=connection.session.execute(stmtgraph.S_A_GRURIIN_B_IDD_IDO,(idd,ido))
    return ormgraph.UriRelation(**row[0]) if row else None

def get_uri_out_relation(ido, idd):
    row=connection.session.execute(stmtgraph.S_A_GRURIOUT_B_IDO_IDD,(ido,idd))
    return ormgraph.UriRelation(**row[0]) if row else None

def delete_member_in_relation(idd, ido):
    row=connection.session.execute(stmtgraph.D_A_GRMEMBERIN_B_IDD_IDO,(idd,ido))
    return True

def delete_member_out_relation(ido, idd):
    row=connection.session.execute(stmtgraph.D_A_GRMEMBEROUT_B_IDO_IDD,(ido,idd))
    return True

def delete_bounded_share_in_relation(idd, ido):
    row=connection.session.execute(stmtgraph.D_A_GRBOUNDEDSHAREIN_B_IDD_IDO,(idd,ido))
    return True

def delete_bounded_share_out_relation(ido, idd):
    row=connection.session.execute(stmtgraph.D_A_GRBOUNDEDSHAREOUT_B_IDO_IDD,(ido,idd))
    return True

def delete_uri_in_relation(idd, ido):
    row=connection.session.execute(stmtgraph.D_A_GRURIIN_B_IDD_IDO,(idd,ido))
    return True

def delete_uri_out_relation(ido, idd):
    row=connection.session.execute(stmtgraph.D_A_GRURIOUT_B_IDO_IDD,(ido,idd))
    return True

def insert_member_in_relation(relation):
    if not isinstance(relation, ormgraph.MemberRelation):
        return False
    connection.session.execute(stmtgraph.I_A_GRMEMBERIN,(relation.idd,relation.ido,relation.type,relation.creation_date))
    return True

def insert_member_out_relation(relation):
    if not isinstance(relation, ormgraph.MemberRelation):
        return False
    connection.session.execute(stmtgraph.I_A_GRMEMBEROUT,(relation.ido,relation.idd,relation.type,relation.creation_date))
    return True

def insert_bounded_share_in_relation(relation):
    if not isinstance(relation, ormgraph.BoundedShareRelation):
        return False
    connection.session.execute(stmtgraph.I_A_GRBOUNDEDSHAREIN,(relation.idd,relation.ido,relation.type,relation.creation_date,relation.perm,relation.interval_init,relation.interval_end))
    return True

def insert_bounded_share_out_relation(relation):
    if not isinstance(relation, ormgraph.BoundedShareRelation):
        return False
    connection.session.execute(stmtgraph.I_A_GRBOUNDEDSHAREOUT,(relation.ido,relation.idd,relation.type,relation.creation_date,relation.perm,relation.interval_init,relation.interval_end))
    return True

def insert_uri_in_relation(relation):
    if not isinstance(relation, ormgraph.UriRelation):
        return False
    connection.session.execute(stmtgraph.I_A_GRURIIN,(relation.idd,relation.ido,relation.type,relation.creation_date,relation.uri))
    return True

def insert_uri_out_relation(relation):
    if not isinstance(relation, ormgraph.UriRelation):
        return False
    connection.session.execute(stmtgraph.I_A_GRURIOUT,(relation.ido,relation.idd,relation.type,relation.creation_date,relation.uri))
    return True
