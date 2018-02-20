import urllib.request
import os
import shutil
import urllib.parse
import requests

def write(data, fn):
    with open(fn,'wb') as fout:
        fout.write(data)

def makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def reset_dir(out_dir):
    shutil.rmtree(out_dir,ignore_errors=True)
    os.makedirs(out_dir)
