import urllib.request
import os
import shutil
import urllib.parse
import requests
import csv
import io

def write(data, fn):
    with open(fn,'wb') as fout:
        fout.write(data)

def makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def reset_dir(out_dir):
    shutil.rmtree(out_dir,ignore_errors=True)
    os.makedirs(out_dir)

def read_csv(fn):
    col_name_list = None
    ret = []
    with io.open(fn,'r',encoding='utf-8-sig') as fin:
        for line in csv.reader(fin):
            if col_name_list is None:
                col_name_list = list(line)
            else:
                if len(line) == 0:
                    continue
                assert(len(line)==len(col_name_list))
                ret.append({col_name_list[i]:line[i] for i in range(len(col_name_list))})
    return ret
