# **********************************************************
#  Author        : Fan Yang
#  Email         : yangfan43@baidu.com
#  Last modified : 2018-06-25 15:50
#  Filename      : util_sample.py
#  Description   : 
#  *********************************************************

from utils import *
from util_func import *

def sample_fix_interval(seq_len, sample_num, rand=False):
    """
        input: seq_len, sample_num 
        output: seq_idx
    """
    if sample_num > seq_len:
        n_times = sample_num/seq_len + 1
        idx = range(seq_len)*n_times
        return np.array(idx[:sample_num])
    
    interval = 1.0*seq_len/sample_num
    start = np.array([int(i*interval) for i in range(sample_num)])
    if rand:
        import random
        offset = np.array([random.randint(0, int(interval-1)) for i in range(sample_num)])
    else:
        offset = np.array([int(interval/2) for i in range(sample_num)])
    idx = start + offset
    return idx


