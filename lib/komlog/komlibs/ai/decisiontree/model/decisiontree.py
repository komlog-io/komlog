import json
from komlog.komfig import logging

class DecisionTreeNode:
    def __init__(self, attribute=None, value=None, node_id=None, parent_id=None, end_node=False, result=False, serialization=None):
        if serialization:
            self.node_id=None
            self._deserialize(serialized_content=serialization)
        else:
            self.attribute=attribute
            self.value=value
            self.node_id=node_id
            self.parent_id=parent_id
            self.end_node=end_node
            self.result=result

    def serialize(self):
        serialization={}
        serialization['a']=self.attribute
        serialization['v']=self.value
        serialization['pi']=self.parent_id
        serialization['ni']=self.node_id
        serialization['en']=1 if self.end_node else 0
        serialization['r']=1 if self.result else 0
        return json.dumps(serialization)

    def _deserialize(self, serialized_content):
        if not self.node_id is None:
            return
        serialized_dict=json.loads(serialized_content)
        for key in ['a','v','pi','ni','en','r']:
            if key not in serialized_dict:
                return
        self.attribute=serialized_dict['a']
        self.value=serialized_dict['v']
        self.parent_id=serialized_dict['pi']
        self.node_id=serialized_dict['ni']
        self.end_node=True if serialized_dict['en']==1 else False
        self.result=True if serialized_dict['r']==1 else False

class DecisionTree:
    def __init__(self, nodes=None, serialization=None):
        if serialization:
            self.nodes=None
            self._deserialize(serialized_content=serialization)
        else:
            self.nodes=nodes if nodes else []

    def serialize(self):
        elements=[]
        for element in self.nodes:
            elements.append(element.serialize())
        return json.dumps(elements)

    def _deserialize(self, serialized_content):
        if not self.nodes is None:
            return
        self.nodes=[]
        for node in json.loads(serialized_content):
            self.nodes.append(DecisionTreeNode(serialization=node))

    def evaluate_row(self,row):
        def eval_node(parent_id=1):
            for node in self.nodes:
                if node.parent_id==parent_id:
                    if node.attribute in row and row[node.attribute]==node.value:
                        if node.end_node==True:
                            return node.result
                        else:
                            return eval_node(parent_id=node.node_id)
                    elif node.attribute=='' and node.end_node:
                        return node.result
            return False
        return eval_node()

