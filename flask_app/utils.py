import arrow
import scipy
import math


def current_time() -> str:
    now = arrow.now('US/Eastern')

    date_time = now.format('hh:mm:ss A DD-MM-YYYY ')
    return date_time

def getRating(lst):
    print("This is the mean now:{} ",scipy.mean(lst))
    return math.floor(scipy.mean(lst))
