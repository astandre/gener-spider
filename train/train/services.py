import requests


def init_spider(key):
    url = "http://127.0.0.1:8000/spider/init"
    data = {
        "key": key
    }
    r = requests.get(url, json=data)
    result = r.json()
    return result

