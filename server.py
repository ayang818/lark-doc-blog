# encoding=utf-8
from flask import Flask, request
import logging
import requests
import json
from conf import *
from flask_cors import CORS
from api import get_t_token, get_doc_content_by_file_token, get_file_token_by_wiki_token, get_children_nodes, get_node_msg

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
user_token = ""
t_token = get_t_token()

# ================ 测试接口 ================


@app.route("/")
def index():
    return '点击链接生成user_token <a href="%s">飞书开放平台登录</a>' % (get_code_url,)


@app.route("/redirect")
def redirect():
    """
    首先需要登录 http://localhost:5000/ 获取 user_token
    """
    code = request.args['code']
    logging.info("code=%s", code)
    resp = requests.post('https://open.feishu.cn/open-apis/authen/v1/access_token', headers={'Authorization': 'Bearer %s' % (
        get_t_token()), 'Content-Type': "application/json; charset=utf-8"}, json={"code": code, "grant_type": "authorization_code"})
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
# ================ 测试接口 ================


@app.route("/doc/<wiki_token>")
def doc_content(wiki_token):
    """
    获取文档 json 格式内容；参照
    """
    file_token, _ = get_file_token_by_wiki_token(t_token, wiki_token)
    doc_content = get_doc_content_by_file_token(t_token, file_token)
    return doc_content


@app.route("/node/<wiki_token>/children")
def get_node_children(wiki_token):
    if wiki_token == 'default':
        wiki_token = root_wiki_node_token
    resp = get_children_nodes(t_token, space_id, wiki_token)
    return {'children': [
        {
            'node_token': it.get('node_token'),
            'wiki_token': it.get('obj_token'),
            'title': it.get('title'),
            'parent_node_token': it.get('parent_node_token'),
            'node_type': it.get('node_type')} for it in resp.get('items', [])]}


if __name__ == "__main__":
    app.run("127.0.0.1", 5000)
