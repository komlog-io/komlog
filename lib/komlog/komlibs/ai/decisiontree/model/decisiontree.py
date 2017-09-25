import pickle
from komlog.komfig import logging

class DecisionTreeNode:
    def __init__(self, feature, value, leaf_node=False, children=None, result=None):
        self._feature = feature
        self._value = value
        self._children = [] if not children else children
        self._leaf_node = True if leaf_node else False
        self._result = result

    @property
    def feature(self):
        return self._feature

    @property
    def value(self):
        return self._value

    @property
    def children(self):
        return self._children

    @property
    def leaf_node(self):
        return self._leaf_node

    @property
    def result(self):
        return self._result

class DecisionTree:

    def __init__(self, children=None):
        self._children = [] if not children else children

    @property
    def children(self):
        return self._children

    def serialize(self):
        serial = pickle.dumps(self)
        return serial

    @classmethod
    def load(cls, serialization):
        obj = pickle.loads(serialization)
        if isinstance(obj, cls):
            return obj
        else:
            raise TypeError

    @classmethod
    def train(cls, trainf, **train_kwargs):
        children = trainf(**train_kwargs)
        return cls(children)

    def classify(self, features):
        def evaluate(children):
            result = None
            for node in children:
                if node.feature in features and features[node.feature] == node.value:
                    if node.leaf_node:
                        result = node.result
                    else:
                        result = evaluate(node.children)
                        if not result:
                            result = node.result
                    break
            return result
        return evaluate(self.children)

