import math
import copy
from komlibs.ai.decisiontree.model import decisiontree
from komfig import logger


def generate_decision_tree(training_set):
    keys=set()
    for row in training_set:
        if 'result' in row and row['result']==True:
            for key in list(row.keys()):
                keys.add(key)
    keys.remove('result')
    tree_nodes=_learn_tree(rows=training_set, attributes=keys)
    return decisiontree.DecisionTree(nodes=tree_nodes)

def get_decision_tree_from_serialized_data(serialization):
    dtree=decisiontree.DecisionTree(serialization=serialization)
    return dtree

def _learn_tree(rows, attributes, parent_id=1):
    next_node_id=parent_id+1
    node_list=[]
    total_rows=len(rows)
    positive_sum=0
    if len(rows)==0:
        return [decisiontree.DecisionTreeNode(attribute='', value=1, node_id=next_node_id, parent_id=parent_id, end_node=True, result=False)]
    for row in rows:
        positive_sum=positive_sum+1 if row['result'] else positive_sum-1
    if total_rows==positive_sum:
        return [decisiontree.DecisionTreeNode(attribute='', value=1, node_id=next_node_id, parent_id=parent_id, end_node=True, result=True)]
    elif total_rows==-positive_sum:
        return [decisiontree.DecisionTreeNode(attribute='', value=1, node_id=next_node_id, parent_id=parent_id, end_node=True, result=False)]
    else:
        if len(attributes)==0:
            return [decisiontree.DecisionTreeNode(attribute='', value=1, node_id=next_node_id, parent_id=parent_id, end_node=True, result=False)]
        next_att=_get_attribute(rows,attributes)
        attributes.remove(next_att)
        next_att_values=[]
        for row in rows:
            if row['result']:
                next_att_values.append(row[next_att])
        next_att_values=list(set(next_att_values))
        for value in next_att_values:
            selected_rows=[]
            for row in rows:
                if row[next_att]==value:
                    selected_rows.append(row)
            if len(selected_rows)==1:
                node_list.append(decisiontree.DecisionTreeNode(attribute=next_att,value=value, node_id=next_node_id, parent_id=parent_id,end_node=True,result=selected_rows[0]['result']))
                next_node_id+=1
            else:
                new_node=decisiontree.DecisionTreeNode(attribute=next_att,value=value,node_id=next_node_id, parent_id=parent_id, end_node=False)
                next_node_id+=1
                node_list.append(new_node)
                next_round_attributes=copy.deepcopy(attributes)
                for node in _learn_tree(rows=selected_rows, attributes=next_round_attributes, parent_id=new_node.node_id):
                    node_list.append(node)
                    next_node_id+=1
    return node_list

def _get_attribute(rows, attributes):
    gain={}
    att=''
    for attribute in attributes:
        gain[attribute]=__G(rows,attribute)
    maxgain=0.0
    for key,value in gain.items():
        if maxgain<=value:
            maxgain=value
            att=key
    return att

def __G(rows, attribute):
    return __B(rows,attribute)-__R(rows,attribute)

def __B(rows, attribute):
    p=0.0
    t=len(rows)
    for i in range(t):
        if rows[i]['result']:
            p+=1
    q=p/t
    try:
        result=-(q*math.log(q,2)+(1-q)*math.log(1-q,2))
    except ValueError:
        result=0
    return result

def __R(rows, attribute):
    values=set()
    tk=0.0
    result=0.0
    tr=len(rows)
    for i in range(tr):
        try:
            values.add(rows[i][attribute])
        except KeyError:
            rows[i][attribute]=0
            #values.add(0)
    d=list(values)
    for k in d:
        tk=0
        selected_rows=[]
        for row in rows:
            if row[attribute]==k:
                tk+=1
                selected_rows.append(row)
        result+=tk/tr*__B(selected_rows,attribute)
    return result

