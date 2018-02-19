import urllib.request

def http_get(url):
    with urllib.request.urlopen(url) as f:
        return f.read()
