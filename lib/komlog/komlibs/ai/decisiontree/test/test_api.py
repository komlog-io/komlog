import unittest
import uuid
import pandas as pd
import pickle
from komlog.komfig import logging
from komlog.komlibs.ai.decisiontree import api
from komlog.komlibs.ai import exceptions, errors
from komlog.komlibs.textman.model import variables
from komlog.komlibs.ai.decisiontree.model import decisiontree

class AiDecisiontreeApiTest(unittest.TestCase):
    ''' komlog.komlibs.ai.decisiontree.api tests '''

    def test_B_success(self):
        ''' __B should succeed for typical values and always be in [0,1] interval '''
        data = pd.DataFrame([
            {'a':1,'b':2,'label':'label1'},
            {'a':1,'b':2,'label':'label1'},
            {'a':1,'b':2,'label':'label1'},
            {'a':1,'b':2,'label':'label2'},
            {'a':1,'b':2,'label':'label2'},
            {'a':1,'b':2,'label':'label3'},
        ])
        label = 'label1'
        self.assertEqual(getattr(api,'__B')(data,label), 1)
        label = 'label2'
        self.assertTrue(getattr(api,'__B')(data,label) > 0.9)
        label = 'label3'
        self.assertTrue(getattr(api,'__B')(data,label) > 0.6)
        label = 'label4'
        self.assertEqual(getattr(api,'__B')(data,label) , 0)
        data = pd.DataFrame()
        self.assertEqual(getattr(api,'__B')(data,label) , 0)
        data = pd.DataFrame([
            {'a':1,'b':2,'label':'label1'},
            {'a':1,'b':2,'label':'label1'},
        ])
        label = 'label1'
        self.assertEqual(getattr(api,'__B')(data,label) , 0)

    def test_R_success(self):
        ''' __R should succeed for typical values and always be in [0,1] interval '''
        data = pd.DataFrame([
            {'a':1,'b':1,'label':'label1'},
            {'a':1,'b':1,'label':'label1'},
            {'a':1,'b':1,'label':'label1'},
            {'a':1,'b':2,'label':'label2'},
            {'a':1,'b':2,'label':'label2'},
            {'a':1,'b':2,'label':'label3'},
        ])
        label = 'label1'
        feat = 'a'
        self.assertEqual(getattr(api,'__R')(data,feat,label), 1)
        feat = 'c'
        self.assertEqual(getattr(api,'__R')(data,feat,label), 1)
        feat = 'b'
        self.assertEqual(getattr(api,'__R')(data,feat,label), 0)
        label = 'label4'
        feat = 'a'
        self.assertEqual(getattr(api,'__R')(data,feat,label), 0)
        feat = 'c'
        self.assertEqual(getattr(api,'__R')(data,feat,label), 0)
        data = pd.DataFrame()
        label = 'label1'
        feat = 'a'
        self.assertEqual(getattr(api,'__R')(data,feat,label), 0)

    def test_G_success(self):
        ''' __G should succeed for typical values and always be in [0,1] interval '''
        data = pd.DataFrame([
            {'a':1,'b':1,'label':'label1'},
            {'a':1,'b':1,'label':'label1'},
            {'a':1,'b':1,'label':'label1'},
            {'a':1,'b':2,'label':'label2'},
            {'a':1,'b':2,'label':'label2'},
            {'a':1,'b':2,'label':'label3'},
        ])
        label = 'label1'
        feat = 'a'
        self.assertEqual(getattr(api,'__G')(data,feat,label), 0)
        feat = 'c'
        self.assertEqual(getattr(api,'__G')(data,feat,label), 0)
        feat = 'b'
        self.assertEqual(getattr(api,'__G')(data,feat,label), 1)
        label = 'label4'
        feat = 'a'
        self.assertEqual(getattr(api,'__G')(data,feat,label), 0)
        feat = 'c'
        self.assertEqual(getattr(api,'__G')(data,feat,label), 0)
        data = pd.DataFrame()
        label = 'label1'
        feat = 'a'
        self.assertEqual(getattr(api,'__G')(data,feat,label), 0)

    def test_get_iteration_values_failure_label_not_found(self):
        ''' get_iteration_values should fail if we try to identify a label whose features info is missing '''
        data = pd.DataFrame([
            {'a':1,'b':1,'c':34,'d':234,'e':243,'f':232,'g':114, 'label':'label1'},
            {'a':1,'b':1,'c':34,'d':234,'f':232,'g':114, 'label':'label2'},
            {'a':1,'b':1,'c':34,'d':234,'f':232,'g':114, 'label':'label3'},
            {'a':1,'b':1,'c':34,'e':243,'f':232,'g':114, 'label':'label2'},
            {'a':1,'b':1,'d':234,'e':243,'f':232,'g':114, 'label':'label1'},
            {'a':1,'c':34,'d':234,'e':243,'f':232,'g':114, 'label':'label1'},
        ])
        label_groups = data.groupby('label').groups
        features = {key:data.columns[data.loc[index].notnull().any()].drop('label').tolist() for key,index in label_groups.items()}
        labels = ['label5']
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            for values in api._get_iteration_values(data, features, labels):
                pass
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_GIV_LNF)
        self.assertEqual(cm.exception.extra, {'no_features':labels})

    def test_get_iteration_values_failure_label_has_no_more_features(self):
        ''' get_iteration_values should fail if we try to identify a label whose features info is None '''
        data = pd.DataFrame([
            {'a':1,'b':1,'c':34,'d':234,'e':243,'f':232,'g':114, 'label':'label1'},
            {'a':1,'b':1,'c':34,'d':234,'f':232,'g':114, 'label':'label2'},
            {'a':1,'b':1,'c':34,'d':234,'f':232,'g':114, 'label':'label3'},
            {'a':1,'b':1,'c':34,'e':243,'f':232,'g':114, 'label':'label2'},
            {'a':1,'b':1,'d':234,'e':243,'f':232,'g':114, 'label':'label1'},
            {'a':1,'c':34,'d':234,'e':243,'f':232,'g':114, 'label':'label1'},
            {'label':'label5'},
        ])
        label_groups = data.groupby('label').groups
        features = {key:data.columns[data.loc[index].notnull().any()].drop('label').tolist() for key,index in label_groups.items()}
        labels = ['label5']
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            for values in api._get_iteration_values(data, features, labels):
                pass
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_GIV_FEX)

    def test_get_iteration_values_failure_error_sorting_features(self):
        ''' get_iteration_values should fail if we dont know how to sort features '''
        data = pd.DataFrame([
            {'a':1,'b':1,'c':34,'d':234,'e':243,'f':232,'g':114, 'label':'label1'},
            {'a':1,'b':1,'c':34,'d':234,'f':232,'g':114, 'label':'label2'},
            {'a':1,'b':1,'c':34,'d':234,'f':232,'g':114, 'label':'label3'},
            {'a':1,'b':1,'c':34,'e':243,'f':232,'g':114, 'label':'label2'},
            {'a':1,'b':1,'d':234,'e':243,'f':232,'g':114, 'label':'label1'},
            {'a':1,'c':34,'d':234,'e':243,'f':232,'g':114, 'label':'label1'},
        ])
        label_groups = data.groupby('label').groups
        features = {key:data.columns[data.loc[index].notnull().any()].drop('label').tolist() for key,index in label_groups.items()}
        labels = ['label1']
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            for values in api._get_iteration_values(data, features, labels):
                pass
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_GIV_ESF)

    def test_get_iteration_values_success_all_labels_share_feature(self):
        ''' get_iteration_values should return the same feature if it is the best for all labels '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':1,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':2,'l_2':1,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':3,'l_2':1,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label3'},
            {'l_1':4,'l_2':1,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label4'},
            {'l_1':5,'l_2':1,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label5'},
            {'l_1':6,'l_2':1,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label6'},
            {'l_1':7,'l_2':1,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label7'},
        ])
        label_groups = data.groupby('label').groups
        features = {key:data.columns[data.loc[index].notnull().any()].drop('label').tolist() for key,index in label_groups.items()}
        labels = ['label1','label2','label3','label4','label5','label6','label7']
        i = 1
        for feat, value, f_data in api._get_iteration_values(data, features, labels):
            self.assertEqual(feat,'l_1')
            self.assertEqual(value,i)
            i += 1
        self.assertEqual(i,8)

    def test_get_iteration_values_success_different_features_per_label(self):
        ''' get_iteration_values should return the best feature for each label '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_2':1,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_2':2,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_2':3,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
        ])
        label_groups = data.groupby('label').groups
        features = {key:data.columns[data.loc[index].notnull().any()].drop('label').tolist() for key,index in label_groups.items()}
        labels = ['label1','label2']
        i = 1
        for feat, value, f_data in api._get_iteration_values(data, features, labels):
            if i<5:
                self.assertEqual(feat,'l_1')
                self.assertEqual(value,i)
            else:
                self.assertEqual(feat,'l_2')
                self.assertEqual(value,i-4)
            i += 1
        self.assertEqual(i,8)

    def test_train_multi_classifier_failure_no_data(self):
        ''' test_multi_classifier should fail if dataset is empty '''
        data = pd.DataFrame()
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            api._train_multi_classifier(data)
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_TMCL_EDF)

    def test_train_multi_classifier_success_detect_features_and_labels(self):
        ''' train_multi_classifier should return the best feature for each label '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':1,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':2,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':3,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
        ])
        nodes = api._train_multi_classifier(data)
        self.assertEqual(len(nodes),4)

    def test_train_multi_classifier_success_detect_features_and_labels_with_children(self):
        ''' train_multi_classifier should return the best feature for each label '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':2,'l_2':5,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':5,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label3'},
        ])
        nodes = api._train_multi_classifier(data)
        total_nodes = 0
        for node in nodes:
            if node.feature == 'l_2':
                total_nodes +=1
                self.assertEqual(node.value,4)
                self.assertEqual(node.children,[])
                self.assertEqual(node.leaf_node,True)
                self.assertEqual(node.result,{'label1':1})
            elif node.feature == 'l_1' and node.value == 2:
                total_nodes +=1
                self.assertEqual(node.value,2)
                self.assertEqual(node.children,[])
                self.assertEqual(node.leaf_node,True)
                self.assertEqual(node.result,{'label2':1})
            elif node.feature == 'l_1' and node.value == 1:
                total_nodes +=1
                self.assertEqual(node.value,1)
                self.assertEqual(len(node.children),2)
                self.assertEqual(node.leaf_node,False)
                self.assertEqual(node.result,{'label1':0.5,'label3':0.5})
                for child in node.children:
                    if child.feature == 'l_2' and child.value == 4:
                        total_nodes +=1
                        self.assertEqual(child.value,4)
                        self.assertEqual(child.children,[])
                        self.assertEqual(child.leaf_node,True)
                        self.assertEqual(child.result,{'label1':1})
                    elif child.feature == 'l_2' and child.value == 5:
                        total_nodes +=1
                        self.assertEqual(child.value,5)
                        self.assertEqual(child.children,[])
                        self.assertEqual(child.leaf_node,True)
                        self.assertEqual(child.result,{'label3':1})
        self.assertEqual(total_nodes,5)

    def test_train_multi_classifier_success_only_train_passed_labels(self):
        ''' train_multi_classifier should return the nodes to identify only the selected labels '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':1,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':2,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':3,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
        ])
        nodes = api._train_multi_classifier(data, labels=['label1'])
        self.assertEqual(len(nodes),1)

    def test_train_multi_classifier_failure_conflicts_same_label(self):
        ''' train_multi_classifier should fail if there are conflicts '''
        data = pd.DataFrame([
            {'l_1':1, 'l_2':2, 'l_3':3, 'label':'label1'},
            {'l_1':1, 'l_2':2, 'l_3':3, 'label':'!label1'},
            {'l_4':1, 'l_5':2, 'l_6':3, 'label':'label1'},
            {'l_4':1, 'l_5':2, 'l_6':3, 'label':'!label1'},
        ])
        conflicts = pd.DataFrame(columns = ['label1','!label1'], index=['label1','!label1'])
        conflicts.loc['label1','label1'] = 0
        conflicts.loc['label1','!label1'] = 1
        conflicts.loc['!label1','label1'] = 1
        conflicts.loc['!label1','!label1'] = 0
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            nodes = api._train_multi_classifier(data, conflicts=conflicts)
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_TMCL_UCFL)
        data = cm.exception.extra['conflicts']
        data_labels = data.label.unique()
        conflict_labels = set()
        for label in conflicts.index:
            if conflicts.loc[conflicts.index == label, data_labels].sum(axis=1).item() > 0:
                conflict_labels.add(label)
        self.assertEqual(conflict_labels, {'label1','!label1'})


    def test_train_multi_classifier_failure_passed_labels_not_in_data(self):
        ''' train_multi_classifier should fail if we try to train for a missing label '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':1,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':2,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':3,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
        ])
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            nodes = api._train_multi_classifier(data, labels=['label3'])
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_GIV_LNF)

    def test_train_multi_classifier_failure_passed_features_missing_label(self):
        ''' train_multi_classifier should return the nodes to identify only the selected labels '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':1,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':2,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':3,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
        ])
        features = {'label1':['l_1','l_2','l_3','l_4','l_5','l_6','l_7']}
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            nodes = api._train_multi_classifier(data, features=features)
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_GIV_LNF)

    def test_train_multi_classifier_success_multiple_labels_identified_no_conflicts_passed(self):
        ''' train_multi_classifier should return the nodes with probabilities for multiple labels  '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
        ])
        nodes = api._train_multi_classifier(data)
        for node in nodes:
            self.assertEqual(node.result, {'label1':0.5,'label2':0.5})

    def test_train_multi_classifier_failure_multiple_labels_identified_conflicts_passed_between_them(self):
        ''' train_multi_classifier should fail if we find unresolved conflicts between labels  '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
        ])
        conflicts = pd.DataFrame(columns = ['label1','label2'], data=[[0,1],[1,0]],index=['label1','label2'])
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            nodes = api._train_multi_classifier(data, conflicts=conflicts)
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_TMCL_UCFL)
        data = cm.exception.extra['conflicts']
        data_labels = data.label.unique()
        conflict_labels = set()
        for label in conflicts.index:
            if conflicts.loc[conflicts.index == label, data_labels].sum(axis=1).item() > 0:
                conflict_labels.add(label)
        self.assertEqual(conflict_labels, {'label1','label2'})

    def test_train_multi_classifier_failure_multiple_labels_identified_conflicts_passed_between_them_but_not_in_labels(self):
        ''' train_multi_classifier should fail if we find unresolved conflicts between labels, even if those labels are not in the labels list to train '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
        ])
        conflicts = pd.DataFrame(columns = ['label1','label2'], data=[[0,1],[1,0]],index=['label1','label2'])
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            nodes = api._train_multi_classifier(data, conflicts=conflicts)
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_TMCL_UCFL)
        data = cm.exception.extra['conflicts']
        data_labels = data.label.unique()
        conflict_labels = set()
        for label in conflicts.index:
            if conflicts.loc[conflicts.index == label, data_labels].sum(axis=1).item() > 0:
                conflict_labels.add(label)
        self.assertEqual(conflict_labels, {'label1','label2'})

    def test_train_multi_classifier_failure_multiple_labels_identified_conflicts_passed_dont_affect(self):
        ''' train_multi_classifier should return the nodes with probabilities for multiple labels  '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label1'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label2'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'label3'},
        ])
        conflicts = pd.DataFrame(
            columns = ['label1','label2','label3'], 
            data=[[0,1,0],[1,0,0],[0,0,0]],
            index=['label1','label2','label3'])
        nodes = api._train_multi_classifier(data, conflicts=conflicts)
        for node in nodes:
            if node.feature == 'l_1' and node.value == 2:
                self.assertEqual(node.result, {'label2':1})
            else:
                self.assertEqual(node.result, {'label1':0.75,'label3':0.25})

    def test_train_multi_classifier_failure_multiple_labels_conflicts_with_some_labels_others_not(self):
        ''' train_multi_classifier a more realistic test for datapoint identification '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri2'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri3'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri4'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri5'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri6'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri7'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
        ])
        conflicts = pd.DataFrame(
            columns = ['uri1','uri2','uri3','uri4','uri5','uri6','uri7','!uri1','!uri2','!uri3','!uri4','!uri5','!uri6','!uri7'],
            data=[
                [0,1,1,1,1,1,1,1,0,0,0,0,0,0],
                [1,0,1,1,1,1,1,0,1,0,0,0,0,0],
                [1,1,0,1,1,1,1,0,0,1,0,0,0,0],
                [1,1,1,0,1,1,1,0,0,0,1,0,0,0],
                [1,1,1,1,0,1,1,0,0,0,0,1,0,0],
                [1,1,1,1,1,0,1,0,0,0,0,0,1,0],
                [1,1,1,1,1,1,0,0,0,0,0,0,0,1],
            ],
            index=['uri1','uri2','uri3','uri4','uri5','uri6','uri7'])
        labels = ['uri1','uri2','uri3','uri4','uri5','uri6','uri7']
        nodes = api._train_multi_classifier(data, labels=labels, conflicts=conflicts)
        for node in nodes:
            if node.feature == 'l_1' and node.value == 1:
                self.assertEqual(node.result, {'uri1':1})
            elif node.feature == 'l_1' and node.value == 2:
                self.assertEqual(node.result, {'uri2':1})
            elif node.feature == 'l_1' and node.value == 3:
                self.assertEqual(node.result, {'uri3':1})
            elif node.feature == 'l_1' and node.value == 4:
                self.assertEqual(node.result, {'uri4':1})
            elif node.feature == 'l_1' and node.value == 5:
                self.assertEqual(node.result, {'uri5':1})
            elif node.feature == 'l_1' and node.value == 6:
                self.assertEqual(node.result, {'uri6':1})
            elif node.feature == 'l_1' and node.value == 7:
                self.assertEqual(node.result, {'uri7':1})

    def test_train_multi_classifier_failure_multiple_labels_unresolvable_conflicts_found(self):
        ''' train_multi_classifier a more realistic test for datapoint identification '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri2'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri3'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri4'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri5'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri6'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri7'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
        ])
        conflicts = pd.DataFrame(
            columns = ['uri1','uri2','uri3','uri4','uri5','uri6','uri7','!uri1','!uri2','!uri3','!uri4','!uri5','!uri6','!uri7'],
            data=[
                [0,1,1,1,1,1,1,1,0,0,0,0,0,0],
                [1,0,1,1,1,1,1,0,1,0,0,0,0,0],
                [1,1,0,1,1,1,1,0,0,1,0,0,0,0],
                [1,1,1,0,1,1,1,0,0,0,1,0,0,0],
                [1,1,1,1,0,1,1,0,0,0,0,1,0,0],
                [1,1,1,1,1,0,1,0,0,0,0,0,1,0],
                [1,1,1,1,1,1,0,0,0,0,0,0,0,1],
            ],
            index=['uri1','uri2','uri3','uri4','uri5','uri6','uri7'])
        labels = ['uri1','uri2','uri3','uri4','uri5','uri6','uri7']
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            nodes = api._train_multi_classifier(data, labels=labels, conflicts=conflicts)
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_TMCL_UCFL)
        data = cm.exception.extra['conflicts']
        data_labels = data.label.unique()
        req_labels = [label for label in labels if label in data_labels]
        conflict_labels = set()
        for label in req_labels:
            if conflicts.loc[conflicts.index == label, data_labels].sum(axis=1).item() > 0:
                conflict_labels.add(label)
        self.assertEqual(conflict_labels, {'uri1','uri2'})

    def test_train_multi_classifier_failure_multiple_labels_self_conflict(self):
        ''' train_multi_classifier a more realistic test for datapoint identification '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri2'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri3'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri4'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri5'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri6'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri7'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
        ])
        conflicts = pd.DataFrame(
            columns = ['uri1','uri2','uri3','uri4','uri5','uri6','uri7','!uri1','!uri2','!uri3','!uri4','!uri5','!uri6','!uri7'],
            data=[
                [1,1,1,1,1,1,1,1,0,0,0,0,0,0], # uri1 conflict with itself is the conflict cause
                [1,0,1,1,1,1,1,0,1,0,0,0,0,0],
                [1,1,0,1,1,1,1,0,0,1,0,0,0,0],
                [1,1,1,0,1,1,1,0,0,0,1,0,0,0],
                [1,1,1,1,0,1,1,0,0,0,0,1,0,0],
                [1,1,1,1,1,0,1,0,0,0,0,0,1,0],
                [1,1,1,1,1,1,0,0,0,0,0,0,0,1],
            ],
            index=['uri1','uri2','uri3','uri4','uri5','uri6','uri7'])
        labels = ['uri1','uri2','uri3','uri4','uri5','uri6','uri7']
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            nodes = api._train_multi_classifier(data, labels=labels, conflicts=conflicts)
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_TMCL_UCFL)
        data = cm.exception.extra['conflicts']
        data_labels = data.label.unique()
        req_labels = [label for label in labels if label in data_labels]
        conflict_labels = set()
        for label in req_labels:
            if conflicts.loc[conflicts.index == label, data_labels].sum(axis=1).item() > 0:
                conflict_labels.add(label)
        self.assertEqual(conflict_labels, {'uri1'})

    def test_train_multi_classifier_failure_multiple_labels_missing_conflict_with_negated_uri(self):
        ''' train_multi_classifier a more realistic test for datapoint identification '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri2'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri3'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri4'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri5'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri6'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri7'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'uri7'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri1'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri2'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri3'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri4'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri5'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114, 'label':'!uri6'},
        ])
        conflicts = pd.DataFrame(
            columns = ['uri1','uri2','uri3','uri4','uri5','uri6','uri7','!uri1','!uri2','!uri3','!uri4','!uri5','!uri6','!uri7'],
            data=[
                [0,1,1,1,1,1,1,1,0,0,0,0,0,0],
                [1,0,1,1,1,1,1,0,1,0,0,0,0,0],
                [1,1,0,1,1,1,1,0,0,1,0,0,0,0],
                [1,1,1,0,1,1,1,0,0,0,1,0,0,0],
                [1,1,1,1,0,1,1,0,0,0,0,1,0,0],
                [1,1,1,1,1,0,1,0,0,0,0,0,1,0],
                [1,1,1,1,1,1,0,0,0,0,0,0,0,1],
            ],
            index=['uri1','uri2','uri3','uri4','uri5','uri6','uri7'])
        labels = ['uri1','uri2','uri3','uri4','uri5','uri6','uri7']
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            nodes = api._train_multi_classifier(data, labels=labels, conflicts=conflicts)
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_TMCL_UCFL)
        data = cm.exception.extra['conflicts']
        data_labels = data.label.unique()
        req_labels = [label for label in labels if label in data_labels]
        conflict_labels = set()
        for label in req_labels:
            if conflicts.loc[conflicts.index == label, data_labels].sum(axis=1).item() > 0:
                conflict_labels.add(label)
        self.assertEqual(conflict_labels, {'uri1'})

    def test_train_multi_classifier_failure_multiple_labels_missing_conflict_with_negated_uri_ignore_feature(self):
        ''' train_multi_classifier a more realistic test for datapoint identification '''
        data = pd.DataFrame([
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'uri1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri1'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri2'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri3'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri4'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri5'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri6'},
            {'l_1':1,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri7'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'uri2'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri1'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri3'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri4'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri5'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri6'},
            {'l_1':2,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri7'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'uri3'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri1'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri2'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri4'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri5'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri6'},
            {'l_1':3,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri7'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'uri4'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri1'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri2'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri3'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri5'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri6'},
            {'l_1':4,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri7'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'uri5'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri1'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri2'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri3'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri4'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri6'},
            {'l_1':5,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri7'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'uri6'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri1'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri2'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri3'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri4'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri5'},
            {'l_1':6,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri7'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'uri7'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri1'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri2'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri3'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri4'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri5'},
            {'l_1':7,'l_2':4,'l_3':34,'l_4':234,'l_5':243,'l_6':232,'l_7':114,'date':uuid.uuid1(),'label':'!uri6'},
        ])
        conflicts = pd.DataFrame(
            columns = ['uri1','uri2','uri3','uri4','uri5','uri6','uri7','!uri1','!uri2','!uri3','!uri4','!uri5','!uri6','!uri7'],
            data=[
                [0,1,1,1,1,1,1,1,0,0,0,0,0,0],
                [1,0,1,1,1,1,1,0,1,0,0,0,0,0],
                [1,1,0,1,1,1,1,0,0,1,0,0,0,0],
                [1,1,1,0,1,1,1,0,0,0,1,0,0,0],
                [1,1,1,1,0,1,1,0,0,0,0,1,0,0],
                [1,1,1,1,1,0,1,0,0,0,0,0,1,0],
                [1,1,1,1,1,1,0,0,0,0,0,0,0,1],
            ],
            index=['uri1','uri2','uri3','uri4','uri5','uri6','uri7'])
        labels = ['uri1','uri2','uri3','uri4','uri5','uri6','uri7']
        with self.assertRaises(exceptions.DTreeGenerationException) as cm:
            nodes = api._train_multi_classifier(data, labels=labels, conflicts=conflicts, ignore_features=['date'])
        self.assertEqual(cm.exception.error, errors.Errors.E_ADA_TMCL_UCFL)
        data = cm.exception.extra['conflicts']
        data_labels = data.label.unique()
        dates = data.date.unique()
        req_labels = [label for label in labels if label in data_labels]
        conflict_labels = set()
        for label in req_labels:
            if conflicts.loc[conflicts.index == label, data_labels].sum(axis=1).item() > 0:
                conflict_labels.add(label)
        self.assertEqual(conflict_labels, {'uri1'})

