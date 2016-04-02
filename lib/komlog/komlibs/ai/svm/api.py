'''

This file implements some useful methods related with support vector machine algorithms

'''

import numpy as np
from sklearn import svm
from komlog.komfig import logger
from komlog.komlibs.ai.svm.model import novelty_detection as ndmodel

def generate_novelty_detector_for_datasource(samples):
    inliners=[]
    features={}
    for sample in samples:
        for key,value in sample.items():
            try:
                features[key]+=value
            except Exception:
                features[key]=value
    min_ocurrencies=len(samples)*0.2
    features=[key for key,value in features.items() if value>=min_ocurrencies]
    features=sorted(list(set(features)))
    for sample in samples:
        row=[]
        for feature in features:
            row.append(sample[feature]) if feature in sample else row.append(0)
        inliners.append(row)
    inliners=np.array(inliners)
    shaker=np.random.uniform(-0.5,0.5,inliners.shape)*inliners # we extend the match area by 50% on each side
    train_X=inliners+shaker
    novelty_detector=generate_novelty_detector(X=train_X)
    if novelty_detector:
        return ndmodel.NoveltyDetector(novelty_detector=novelty_detector, features=features)
    else:
        return None

def generate_novelty_detector(X, nu=0.01):
    clf = svm.OneClassSVM(kernel="rbf", nu=nu)
    try:
        clf.fit(X)
    except Exception:
        return None
    else:
        return clf

def is_row_novel(novelty_detector, row):
    try:
        result=novelty_detector.predict(row)
    except Exception:
        return None
    else:
        return result

