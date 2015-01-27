#!/usr/bin/env python
#coding utf-8

import math
import uuid
import json
import copy
from komfig import logger

class DecisionTreeNode:
    def __init__(self, attribute,value,parentid=None,nodeid=None,endnode=False,result=False):
        self.attribute=attribute
        self.value=value
        self.parentid=parentid
        if not nodeid:
            self.nodeid=str(uuid.uuid4())
        else:
            self.nodeid=nodeid
        self.endnode=endnode
        self.result=result

class DecisionTree:
    def __init__(self, jsontree=None,rawdata=None):
        self.jsontree=jsontree
        self.raw_data=rawdata
        if self.jsontree:
            self.load_jsontree()
        elif self.raw_data:
            self.generate_tree()

    def generate_tree(self):
        keys=[]
        for row in self.raw_data:
            for key in list(row.keys()):
                keys.append(key)
        keys=list(set(keys))
        #remove result key
        keys.remove('result')
        #logger.logger.debug('VAmos a generar el arbol con '+str(self.raw_data)+' Y '+str(keys))
        self.tree=self.learn_tree(rows=self.raw_data,attributes=keys)

    def learn_tree(self,rows,attributes,parentid=None):
        #logger.logger.debug('llamada a learn_tree, con rows: '+str(rows)+' y attr:'+str(attributes))
        #print('LLamada nueva', end=' ')
        #print rows
        #print attributes
        node_list=[]
        local_attributes=copy.deepcopy(attributes)
        if len(rows)==0:
            node_list.append(DecisionTreeNode(attribute='',value=1,parentid=parentid,endnode=True,result=False))
        else:
            t=0
            p=0
            n=0
            for row in rows:
                t+=1
                if row['result']==True:
                    p+=1
                else:
                    n+=1
            #print(t,p,n)
            if t==p:
                #print('Todos POSITIVOS')
                node_list.append(DecisionTreeNode(attribute='',value=1,parentid=parentid,endnode=True,result=True))
            elif t==n:
                #print('Todos NEGATIVOS')
                node_list.append(DecisionTreeNode(attribute='',value=1,parentid=parentid,endnode=True))
            elif len(local_attributes)==0: #aqui deberia devolver que es necesario aumentar la precision del hash de las muestras de entrenamiento
                #print('ME QUEDE SIN ATRIBUTOS')
                #print('ESTAS SON LAS ROWS QUE NO SE HAN PODIDO DETERMINAR')
                #print(rows)
                node_list.append(DecisionTreeNode(attribute='',value=1,parentid=parentid,endnode=True))
            else:
                #print('POSITIVOS Y NEGATIVOS ENTRE LAS VARIABLES')
                next_att=self.__get_attribute(rows,local_attributes)
                #logger.logger.debug('Atributo seleccionado: '+next_att)
                #print(next_att)
                local_attributes.remove(next_att)
                different_values=[]
                for row in rows:
                    if row['result']:
                        different_values.append(row[next_att])
                different_values=list(set(different_values))
                #logger.logger.debug('Evaluaremos rows con '+next_att+'='+str(different_values))
                for value in different_values:
                    #logger.logger.debug('Empezamos con '+next_att+'='+str(value))
                    selected_rows=[]
                    for row in rows:
                        if row[next_att]==value:
                            selected_rows.append(row)
                    if len(selected_rows)==1:
                        #print('ULTIMA ROW DEL GRUPO')
                        new_node=DecisionTreeNode(attribute=next_att,value=value,parentid=parentid,endnode=True,result=selected_rows[0]['result'])
                        #logger.logger.debug('ultima row del grupo. anadimos el siguiente nodo: '+str(new_node.__dict__))
                        node_list.append(new_node)
                    else:
                        #print('VARIOS ROWS CON ATTRIBUTO ENTRE LOS VALORES POSITIVOS, CONTINUAMOS CON LA SIGUIENTE ITERACION')
                        new_node=DecisionTreeNode(attribute=next_att,value=value,parentid=parentid,endnode=False)
                        node_list.append(new_node)
                        #logger.logger.debug('Iterando nuevamente con las siguientes rows: '+str(selected_rows)+'attributes: '+str(local_attributes))
                        more_nodes=self.learn_tree(rows=selected_rows,attributes=local_attributes,parentid=new_node.nodeid)
                        for node in more_nodes:
                            node_list.append(node)
        return node_list

    def __get_attribute(self,rows,attributes):
        gain={}
        att=''
        for attribute in attributes:
            gain[attribute]=self.__G(rows,attribute)
        maxgain=0.0
        #print('Atributos: ', end=' ')
        #print(attributes)
        #print('Ganancias: ', end=' ')
        #print(gain)
        for key,value in gain.items():
            if maxgain<=value:
                maxgain=value
                att=key
        return att

    def __G(self,rows,attribute):
        return self.__B(rows,attribute)-self.__R(rows,attribute)

    def __B(self,rows,attribute):
        p=0.0
        n=0.0
        for row in rows:
            if row['result']:
                p+=1
            else:
                n+=1
        q=p/(p+n)
        try:
            result=-(q*math.log(q,2)+(1-q)*math.log(1-q,2))
        except ValueError:
            result=0
        return result

    def __R(self,rows,attribute):
        p=0.0
        n=0.0
        pk=0.0
        nk=0.0
        values=[]
        total=0.0
        for row in rows:
            try:
                values.append(row[attribute])
            except KeyError:
                row[attribute]=0
                values.append(row[attribute])
        d=list(set(values))
        for k in d:
            selected_rows=[]
            for row in rows:
                if row['result']:
                    p+=1
                else:
                    n+=1
                if row[attribute]==k:
                    selected_rows.append(row)
                    if row['result']:
                        pk+=1
                    else:
                        nk+=1
            total+=(pk+nk)/(p+n)*self.__B(selected_rows,attribute)
        return total

    def get_jsontree(self):
        elements=[]
        for element in self.tree:
            elements.append(json.dumps(element.__dict__))
        self.jsontree=json.dumps(elements)
        return self.jsontree

    def load_jsontree(self):
        self.tree=[]
        elements=json.loads(self.jsontree)
        for element in elements:
            nodedict=json.loads(element)
            self.tree.append(DecisionTreeNode(**nodedict))
            
    def evaluate_row(self,row):
        def eval_node(parentid=None):
            for node in self.tree:
                if node.parentid==parentid:
                    try:
                        if row[node.attribute]==node.value:
                            if node.endnode==True:
                                return node.result
                            else:
                                return eval_node(parentid=node.nodeid)
                    except KeyError:
                        if node.attribute=='' and node.endnode:
                            return node.result
                        else:
                            pass
            return False
        return eval_node()

