import datetime

def get_range(start_date,end_date,interval='days',num=1):
    """
    Returns a generator of all the days between two date objects.
    Results include the start and end dates.
    Arguments must be datetime.datetime objects.
    """
    if start_date > end_date:
        raise ValueError('You provided a start_date that comes after the end_date.')
    kwargs={}
    kwargs[interval]=num
    while True:
        yield start_date
        start_date = start_date + datetime.timedelta(**kwargs)
        if start_date > end_date:
            break

