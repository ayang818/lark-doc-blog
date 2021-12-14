import json
import requests

def getj(url, access_token, data=None):
    return req('get', url, access_token=access_token, json_data=None, data=data)

def postj(url, access_token, json_data=None):
    return req('post', url, access_token=access_token, json_data=json_data, data=None)
    
def req(method, url, access_token, json_data, data):
    headers = {"Authorization": "Bearer %s" % (access_token, ), "Content-Type": "application/json; charset=utf-8"}
    if method == "get":
        resp = requests.get(url, json=json_data, params=data, headers=headers)
    elif method == "post":
        resp = requests.post(url, json=json_data, data=data, headers=headers)
    jdata = json.loads(resp.text)
    if str(resp.status_code) == "200" and jdata['code'] == 0:
        return jdata["data"]
    else:
        raise Exception(jdata)