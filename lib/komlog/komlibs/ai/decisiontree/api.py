import math
import copy
import uuid
import traceback
from komlog.komlibs.ai import exceptions, errors
from komlog.komlibs.ai.decisiontree.model.decisiontree import DecisionTree, DecisionTreeNode
from komlog.komlibs.textman.model import variables
from komlog.komfig import logging

FEAT_WEIGHT = {
    variables.LINE:1,
    variables.COLUMN:0.75,
    variables.NUMERIC:0.5,
    variables.RELATIVE:0.3
}

def get_dtree_classifier(data, labels=None, conflicts=None, ignore_features=None):
    return DecisionTree.train(trainf=_train_multi_classifier, data=data, labels=labels, conflicts=conflicts, ignore_features=ignore_features)

def load_dtree(serialization):
    return DecisionTree.load(serialization)

def _train_multi_classifier(data, labels=None, features=None, conflicts=None, ignore_features=None):
    '''
    params:
    - data: dataframe with training set. labels will be set using the 'label' column.
    - labels: list of labels to generate dtree nodes from this level (this param is modified in each iteration).
       You can set it at the beggining to indicate the labels you want to classify. by default, all data labels will be classified.
    - conflicts: Because classification is multi-labeled, you can indicate incompatibilities between labels.
    - features: for internal use only (this function calls itself recursively). If features is None, will generate a feature list per label.
    '''
    if features == None or labels == None:
        if data.shape[0] == 0:
            raise exceptions.DTreeGenerationException(error=errors.Errors.E_ADA_TMCL_EDF)
        label_groups = data.groupby('label').groups
        labels = list(label_groups.keys()) if labels == None else labels
        features = {key:data.columns[data.loc[index].notnull().any()].drop('label').tolist() for key,index in label_groups.items()} if features == None else features
        feats_to_delete = ignore_features if ignore_features else []
        for value in features.values():
            for feat in feats_to_delete:
                try:
                    value.remove(feat)
                except ValueError:
                    pass
    nodes = []
    for feat, value, fv_data in _get_iteration_values(data, features, labels):
        fv_labels = fv_data.label.unique()
        req_lbls = set([label for label in fv_labels if label in labels])
        req_lbls_rownum = fv_data.loc[fv_data['label'].isin(req_lbls)].shape[0]
        stats = {label:fv_data.loc[fv_data['label'] == label].shape[0]/req_lbls_rownum for label in req_lbls}
        conflict_l = set()
        last_feat_l = set()
        identified_l = set()
        n_features = copy.deepcopy(features)
        n_features = {label:fv_data[[f for f in n_features[label] if fv_data[f].notnull().any()]].columns.tolist() for label in fv_labels}
        for label in req_lbls:
            n_features[label].remove(feat)
            last_feature = True if not n_features[label] else False
            identified = True if stats[label] == 1 else False
            if last_feature:
                if conflicts is not None and conflicts.loc[conflicts.index == label,fv_labels].sum(axis=1).item() > 0:
                    raise exceptions.DTreeGenerationException(error = errors.Errors.E_ADA_TMCL_UCFL, extra={'conflicts':fv_data})
                    #l = conflicts[fv_labels].columns[conflicts.loc[conflicts.index == label, fv_labels].any()].tolist()
                    #conflict_l.update([label,*l])
                else:
                    last_feat_l.add(label)
            elif identified:
                if not(conflicts is not None and conflicts.loc[conflicts.index == label,fv_labels].sum(axis=1).item() > 0):
                    identified_l.add(label)
        #if conflict_l:
            #raise exceptions.DTreeGenerationException(error = errors.Errors.E_ADA_TMCL_UCFL, extra={'conflicts':conflict_l})
        nid = uuid.uuid4().hex
        req_lbls = list(req_lbls - last_feat_l - identified_l)
        if not req_lbls:
            nodes.append(DecisionTreeNode(feature=feat, value=value, leaf_node=True, result=stats))
        else:
            try:
                children = _train_multi_classifier(data=fv_data, labels=req_lbls, features=n_features, conflicts=conflicts)
            except exceptions.DTreeGenerationException as e:
                if e.error == errors.Errors.E_ADA_GIV_ESF:
                    nodes.append(DecisionTreeNode(feature=feat, value=value, leaf_node=True, result=stats))
                else:
                    raise
            else:
                nodes.append(DecisionTreeNode(feature=feat, value=value, leaf_node=False, children=children, result=stats))
    return nodes

def _get_iteration_values(data, features, labels):
    label_best_feats = {}
    for label in labels:
        if not label in features:
            raise exceptions.DTreeGenerationException(error = errors.Errors.E_ADA_GIV_LNF, extra={'no_features':[label]})
        elif not features[label]:
            raise exceptions.DTreeGenerationException(error = errors.Errors.E_ADA_GIV_FEX)
        gain = {feat:__G(data, feat, label) for feat in features[label]}
        try:
            scores = sorted(list(gain.items()), key=lambda x: (x[1]*FEAT_WEIGHT[x[0].split('_')[0]]), reverse=True)
            label_best_feats.setdefault(scores[0][0],[]).append(label)
        except Exception as e:
            ex_info=traceback.format_exc().splitlines()
            for line in ex_info:
                logging.logger.error(line)
            raise exceptions.DTreeGenerationException(error = errors.Errors.E_ADA_GIV_ESF) # error sorting feats
    for feat, labels in label_best_feats.items():
        f_data = data.loc[data['label'].isin(labels), feat]
        f_values = f_data[f_data.notnull()].unique()
        for value in f_values:
            v_data = data[data[feat] == value]
            yield (feat,value,v_data)

def __G(data, feat, label):
    return __B(data, label) - __R(data, feat, label)

def __B(data, label):
    try:
        q = data[data['label'] == label].shape[0]/data.shape[0]
        return -(q*math.log2(q)+(1-q)*math.log2(1-q))
    except (KeyError, ValueError):
        return 0

def __R(data, feat, label):
    result = 0
    try:
        f_data = data[feat]
    except KeyError:
        return __B(data, label)
    else:
        tr = data.shape[0]
        f_values = f_data.unique()
        for v in f_values:
            v_rows = data[f_data == v]
            tk = v_rows.shape[0]
            try:
                result += tk / tr * __B(v_rows, label)
            except ZeroDivisionError:
                v_rows = data[f_data.isnull()]
                tk = v_rows.shape[0]
                result += tk / tr * __B(v_rows, label)
        return result

