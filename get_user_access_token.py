# encoding=utf-8
import time
from flask import Flask, request
import logging
import requests
import json

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)

app_id = "cli_a1093f4447f9d00c"
app_secret = "wXzGQiFw48Pwbiaw33a3acBneOYyC4F1"
space_id = "7011396001814544388"
redirect_url = "http://127.0.0.1:5000/redirect"
get_code_url = "https://open.feishu.cn/open-apis/authen/v1/index?redirect_uri=%s&app_id=%s&state=1" % (redirect_url , app_id)

def get_t_token():
    resp = requests.post(url='https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', headers={'content-type': 'application/json; charset=utf-8'}, json={"app_id": app_id, "app_secret": app_secret})
    return json.loads(resp.text)['tenant_access_token']


@app.route("/redirect")
def redirect():
    code = request.args['code']
    logging.info("code=%s", code)
    resp = requests.post('https://open.feishu.cn/open-apis/authen/v1/access_token', headers={'Authorization': 'Bearer %s' % (get_t_token()), 'Content-Type': "application/json; charset=utf-8"}, json={"code": code, "grant_type": "authorization_code"})
    logging.info("resp=%s", resp.text)
    token = json.loads(resp.text)['data']['access_token']
    logging.info("user access_token is = %s" % token)
    return token

if __name__ == "__main__":
    app.run("127.0.0.1", 5000)

