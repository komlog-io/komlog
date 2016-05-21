import math
import copy
from komlog.komlibs.ai.decisiontree.model import decisiontree
from komlog.komlibs.textman.model import variables
from komlog.komfig import logging

ATT_PRIORITY = {
    variables.LINE:1,
    variables.COLUMN:2,
    variables.NUMERIC:3,
    variables.RELATIVE:4
}

def generate_decision_tree(training_set):
    keys=set()
    for row in training_set:
        if 'result' in row and row['result']==True:
            for key in list(row.keys()):
                keys.add(key)
    if 'result' in keys:
        keys.remove('result')
    tree_nodes=_learn_tree(rows=training_set, attributes=keys)
    return decisiontree.DecisionTree(nodes=tree_nodes)

def get_decision_tree_from_serialized_data(serialization):
    dtree=decisiontree.DecisionTree(serialization=serialization)
    return dtree

def _learn_tree(rows, attributes, parent_id=1):
    result_found=None
    next_node_id=parent_id+1
    node_list=[]
    total_rows=len(rows)
    positives=0
    negatives=0
    if len(rows)==0:
        return [decisiontree.DecisionTreeNode(attribute='', value=1, node_id=next_node_id, parent_id=parent_id, end_node=True, result=False)]
    for row in rows:
        if row['result'] is True:
            positives=positives+1
        elif row['result'] is False:
            negatives=negatives+1
    if positives>0 and negatives==0:
        result_found=True
        #return [decisiontree.DecisionTreeNode(attribute='', value=1, node_id=next_node_id, parent_id=parent_id, end_node=True, result=True)]
    elif negatives>0 and positives==0:
        result_found=False
        #return [decisiontree.DecisionTreeNode(attribute='', value=1, node_id=next_node_id, parent_id=parent_id, end_node=True, result=False)]
    #else:
    if len(attributes)==0:
        ''' No more atts to compare, should generate more relations for comparing '''
        if result_found is not None:
            return [decisiontree.DecisionTreeNode(attribute='', value=1, node_id=next_node_id, parent_id=parent_id, end_node=True, result=result_found)]
        else:
            return [decisiontree.DecisionTreeNode(attribute='', value=1, node_id=next_node_id, parent_id=parent_id, end_node=True, result=False)]
    next_att=_get_attribute(rows,attributes)
    if result_found is not None and not next_att.split('_')[0] in (variables.LINE,variables.COLUMN):
        return [decisiontree.DecisionTreeNode(attribute='', value=1, node_id=next_node_id, parent_id=parent_id, end_node=True, result=result_found)]
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
    for attribute in attributes:
        gain[attribute]=__G(rows,attribute)
    gains = sorted(gain.items(), key= lambda x: -x[1])
    filter_gain=gains[0][1]*0.5
    candidates=[]
    for i, g in enumerate(gains):
        if g[1]>filter_gain:
            candidates.append(g[0])
        else:
            break;
    try:
        scores= sorted(candidates, key=lambda x: (ATT_PRIORITY[x.split('_')[0]],abs(int(x.split('_')[1]))))
        att = scores[0]
    except Exception:
        att = ''
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
            rows[i][attribute]=None
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

