import datetime

def get_range(start_date,end_date,interval='days',num=1,reverse_order=False):
    """
    Returns a generator of all the days between two date objects.
    Results include the start and end dates.
    Arguments must be datetime.datetime objects.
    """
    if start_date > end_date:
        raise ValueError('You provided a start_date that comes after the end_date.')
    kwargs={}
    kwargs[interval]=num
    if reverse_order:
        while True:
            yield end_date
            end_date = end_date - datetime.timedelta(**kwargs)
            if end_date < start_date:
                if end_date.day == start_date.day:
                    end_date=start_date
                else:
                    break
    else:
        while True:
            yield start_date
            start_date = start_date + datetime.timedelta(**kwargs)
            if start_date > end_date:
                if end_date.day == start_date.day:
                    start_date=end_date
                else:
                    break

