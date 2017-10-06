import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

from komlog.komlibs.textman.model import variables

def get_document_vector(samples):
    total_weight = 0
    features = {}
    num_samples = len(samples)
    for sample in samples:
        num_elements = len(sample)
        element_count = {}
        for element in sample:
            if element > variables.DEFAULT_NEWLINE_HASH:
                element_count[element] = element_count.setdefault(element,0) + 1
        sample_features = {feat:num_elements/element_count[feat] for feat in element_count.keys()}
        for feat,weight in sample_features.items():
            features[feat] = features.setdefault(feat,0) + weight
            total_weight += weight
    normalized_features = {feat:features[feat]/total_weight for feat in features.keys()}
    return normalized_features

def get_matching_documents(query, docs, threshold=None, count=1):
    def euclidean_distance_nan_aware(u,v):
        d = 0
        for ui,vi in zip(u,v):
            if not np.isnan(vi):
                d += (ui-vi)**2
        d = np.sqrt(d)
        c_factor = u.size/(u.size-np.isnan(v).sum())
        return d * c_factor
    dids = []
    rows = []
    for did, features in docs.items():
        dids.append(did)
        rows.append(features)
    dids.append('query')
    rows.append(query)
    df = pd.DataFrame(index=dids, data=rows)
    #df = df.fillna(0)
    distances = cdist(df.loc['query':'query'],df.iloc[0:-1], lambda u,v: euclidean_distance_nan_aware(u,v))
    distances = np.append(distances,0)
    df['dist'] = distances
    #df = df.fillna(0) <- aquí afectaría menos a la distancia?
    df = df.drop('query')
    df = df.sort_values('dist')
    documents = []
    i = 0
    while i<count:
        try:
            if threshold != None:
                if df.iloc[i].dist < threshold:
                    documents.append(df.iloc[i].name)
                else:
                    break
            else:
                documents.append(df.iloc[i].name)
        except IndexError:
            break
        else:
            i += 1
    return documents

