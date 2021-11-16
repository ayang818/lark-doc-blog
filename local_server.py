# encoding=utf-8
from flask import Flask, request
import logging
import requests
import json
from conf import *

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
user_token = ""

def get_t_token():
    resp = requests.post(url='https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', headers={'content-type': 'application/json; charset=utf-8'}, json={"app_id": app_id, "app_secret": app_secret})
    return json.loads(resp.text)['tenant_access_token']

@app.route("/")
def index():
    return '点击链接生成user_token <a href="%s">飞书开放平台登录</a>' % (get_code_url,)

@app.route("/redirect")
def redirect():
    code = request.args['code']
    logging.info("code=%s", code)
    resp = requests.post('https://open.feishu.cn/open-apis/authen/v1/access_token', headers={'Authorization': 'Bearer %s' % (get_t_token()), 'Content-Type': "application/json; charset=utf-8"}, json={"code": code, "grant_type": "authorization_code"})
    logging.info("resp=%s", resp.text)
    token = json.loads(resp.text)['data']['access_token']
    logging.info("user access_token is = %s" % token)
    global user_token
    user_token = token
    return "生成 token 为 %s" % (token,)

@app.route("/token")
def get_user_token():
    global user_token
    return user_token

if __name__ == "__main__":
    app.run("127.0.0.1", 5000)

