import unittest
import uuid
from komlog.komfig import logging
from komlog.komlibs.ai.decisiontree.model import decisiontree

class AiDecisiontreeModelDecisiontreeTest(unittest.TestCase):
    ''' komlog.komlibs.ai.decisiontree.model.decisiontree tests '''

    def test_create_DecisionTreeNode_success(self):
        ''' creating a DecisionTreeNode object should succeed '''
        feature = 'SOME_FEATURE'
        value = 234234
        leaf_node = False
        children = []
        result = None
        node = decisiontree.DecisionTreeNode(feature, value, leaf_node=leaf_node, children=children, result=result)
        self.assertEqual(node.feature, feature)
        self.assertEqual(node.value, value)
        self.assertEqual(node.children, children)
        self.assertEqual(node.leaf_node, leaf_node)
        self.assertEqual(node.result, result)

    def test_create_DecisionTree_success(self):
        ''' creating a DecisionTree object should succeed '''
        children = []
        dtree = decisiontree.DecisionTree(children)
        self.assertEqual(dtree.children, children)

    def test_serialization_process_DecisionTree_success(self):
        features = ['a','b','c']
        values = [1,2,3]
        leaf_node = [True, False]
        result = [False, *features]
        children = []
        for f in features:
            for v in values:
                for l in leaf_node:
                    for r in result:
                        children.append(decisiontree.DecisionTreeNode(feature=f,value=v, leaf_node=l, result=r))
        children = sorted(children, key = lambda x: x.feature+str(x.value)+str(x.leaf_node)+str(x.result))
        dtree = decisiontree.DecisionTree(children=children)
        serialization = dtree.serialize()
        dtree2 = decisiontree.DecisionTree.load(serialization)
        children2= sorted(dtree2.children, key = lambda x: x.feature+str(x.value)+str(x.leaf_node)+str(x.result))
        self.assertEqual(len(dtree.children),len(dtree2.children))
        for i in range(len(children)):
            self.assertEqual(children[i].feature, children2[i].feature)
            self.assertEqual(children[i].value, children2[i].value)
            self.assertEqual(children[i].children, children2[i].children)
            self.assertEqual(children[i].leaf_node, children2[i].leaf_node)
            self.assertEqual(children[i].result, children2[i].result)

