# **********************************************************
#  Author        : Fan Yang
#  Email         : yangfan43@baidu.com
#  Last modified : 2018-06-25 15:50
#  Filename      : util_io.py
#  Description   : 
#  *********************************************************

#from utils import *
from util_func import *
import cPickle as pickle
import json
import io

@file_check
def read_json(json_file):
    return json.loads(open(json_file).read())

@file_check
def read_pkl(pkl_file):
    return pickle.load(open(pkl_file, "rb"))

@file_check 
def read_txt(*args):
    return [[args[1][i](item) for i, item in enumerate(line.strip().split())] for line in open(args[0]).readlines()]

@file_check
def read_csv(file):
    pass

def save_pkl(data, path):
    with open(path, "wb") as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

def save_json(data, path):
    data = json.dumps(data)
    with open(path, "w") as file:
        file.write(data)

if __name__ == "__main__":
    file_name = "tp.txt"
    result = read_txt(file_name, [str, float])
    print result
    
