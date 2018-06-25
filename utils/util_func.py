# **********************************************************
#  Author        : Fan Yang
#  Email         : yangfan43@baidu.com
#  Last modified : 2018-06-25 15:50
#  Filename      : util_func.py
#  Description   : 
#  *********************************************************

#from utils import *
import os
# decorator 
def time_usage(func):
    def warpper(*args):
        start = time.time()
        result = func(*args)
        end = time.time()
        print "Time usage for running {} : {}".format(func.__name__, end-start)
        return result
    return warpper

def file_check(func):
    def wrapper(*args):
        if not os.path.exists(args[0]):
            print "{} file not exists.".format(args[0])
            return None
        return func(*args)
    return wrapper

# func
def calc_iou(seg1, seg2):
    s1, e1 = seg1
    s2, e2 = seg2
    s_min = s1 if s1 < s2 else s2
    s_max = s1 if s1 > s2 else s2
    e_min = e1 if e1 < e2 else e2
    e_max = e1 if e1 > e2 else e2
    tmp_iou = 1.0*(e_min - s_max)/(e_max - s_min)
    return 0.0 if tmp_iou < 0 else tmp_iou

def calc_max_iou(prob_seg, gt_segs):
    max_iou = 0.0
    for item in gt_segs:
        iou = calc_iou(prob_seg, item)
        max_iou = iou if iou > max_iou else max_iou
    return max_iou

def get_expand(start, end, feat_len, ratio, mode=1):
    """
    mode=0: allow negative 
    mode=1: cut to border 
    mode=2: sysmetric cut to border
    """
    new_start = int(start - ratio*(end-start)/2)
    new_end = int(end + ratio*(end-start)/2)
    if mode == 1:
        new_start = 0 if new_start < 0 else new_start
        new_end = feat_len if new_end > feat_len else new_end
    elif mode == 2:
        min_margin = min(start-new_start, new_end-end)
        new_start = start - min_margin
        new_end = end + min_margin
    return new_start, new_end

def run_job_parallel(*args):
    import multiprocessing
    import math
    func = args[0]
    processor_num = args[1]
    input_list = args[2] 
    params = args[3:]
    part_num = int(math.ceil(1.0 * len(input_list) / processor_num))
    records = []
    for i in xrange(processor_num):
        part_list = input_list[i * part_num : (i + 1) * part_num]
        process = multiprocessing.Process(target = func, args=(part_list, params))
        process.start()
        records.append(process)
    for process in records:
        process.join()

def run_job_parallel_with_pool(*args):
    from multiprocessing import Pool
    func = args[0]
    processor_num = args[1]
    input_list = args[2]
    pool = Pool(processes = processor_num)
    result = pool.map(func, input_list)
    pool.close()
    pool.join()
    return result

if __name__ == "__main__":
    from util_io import read_txt
    all_list = read_txt("tmp.txt", [float])
    import numpy as np
    all_list = np.array(all_list).reshape(-1).tolist() 
    def func(*args):
        for item in args[0]:
            print item
    run_job_parallel(func, 4, all_list)
