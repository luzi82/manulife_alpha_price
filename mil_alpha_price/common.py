import urllib.request
import os
import shutil

def http_get(url):
    with urllib.request.urlopen(url) as f:
        return f.read()

def download(url, output):
    data = http_get(url)
    with open(output,'wb') as fout:
        fout.write(data)

def makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def reset_dir(out_dir):
    shutil.rmtree(out_dir,ignore_errors=True)
    os.makedirs(out_dir)
