'''

This file implements some methods for numeric aggregate operations

'''

import numpy as np

def aggregate_timeseries_data(data, bins=1, interval=None):
    ''' 
    aggregate_timeseries_data
    
    Aggregate data array passed in the data parameter. The data
    passed contains tuples with the timestamp and value. (ts,value)
    
    the interval argument is a tuple with the max and min timestamp
    of the interval selected. If interval is null, the max and min
    will be calculated from the data passed.
    
    The interval will be splitted in as many intervals as indicated
    with the bins parameter. If not bins parameter is passed, 1 will
    be selected as default, meaning the interval will not be partitioned
    '''
    if len(data)==0:
        return []
    data=np.array(data)
    data_bins=[]
    if interval==None:
        interval_min=data[:,0].min()
        interval_max=data[:,0].max()
    else:
        interval_min,interval_max=interval if interval[0]<interval[1] else (interval[1],interval[0])
    interval_width=(interval_max-interval_min)/float(bins)
    for i in range(0,bins):
        if i==0:
            its=interval_min
            ets=interval_min+interval_width
            interval_data=data[(data[:,0]>=its) & (data[:,0]<ets)][:,1]
        elif i==bins-1:
            its=interval_min+i*interval_width
            ets=interval_max
            interval_data=data[(data[:,0]>=its) & (data[:,0]<=ets)][:,1]
        else:
            its=interval_min+i*interval_width
            ets=its+interval_width
            interval_data=data[(data[:,0]>=its) & (data[:,0]<ets)][:,1]
        interval_mean=interval_data.mean() if interval_data.size>0 else None
        if interval_mean is not None:
            data_bins.append([its,interval_mean])
    return data_bins

