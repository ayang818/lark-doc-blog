# encoding=utf-8
import io
from flask import Flask, request, send_file
import logging
import requests
import json
from conf import *
from flask_cors import CORS
from api import get_t_token, get_doc_content_by_file_token, get_file_token_by_wiki_token, get_children_nodes, get_node_meta_msg, get_doc_media_by_file_token, get_docs_metadata_msg
import traceback
import functools
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO,
                    filename='lark-doc-blog-py.log',
                    filemode='a'
                    )

Flask.logger_name = 'logger'
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
user_token = ""
# t_token = get_t_token()
t_token = get_t_token()

# ================ 测试接口 ================


@app.route("/")
def index():
    return '点击链接生成user_token <a href="%s">飞书开放平台登录</a><br/> t_token: %s' % (get_code_url, t_token)


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

# 不管 3 7 21 refresh 了再说


def refresh_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            logging.error(e)
            logging.error("token expired! refresh token")
            global t_token
            t_token = get_t_token()
            # 自动做重试
            return func(*args, **kwargs)
    return wrapper


@app.route("/doc/<wiki_token>")
@refresh_token
def doc_content(wiki_token):
    """
    获取文档 json 格式内容；参照
    """
    file_token, _ = get_file_token_by_wiki_token(t_token, wiki_token)
    doc_content = get_doc_content_by_file_token(t_token, file_token)
    return doc_content


@app.route("/doc/metadata", methods=['POST'])
@refresh_token
def docs_meta_data():
    # 批量获取时间接口
    body = json.loads(request.get_data())
    reqList = body.get('req')
    token_list = []
    for item in reqList:
        token_list.append(
            {'docs_token': item.get('docsToken'),
             'docs_type': item.get('docsType')})
    request_docs = {
        'request_docs': token_list
    }
    resp = get_docs_metadata_msg(t_token, request_docs)
    return resp


@app.route("/node/<wiki_token>/children")
# refresh token 必须放在里面
@refresh_token
def get_node_children(wiki_token):
    if wiki_token == 'default':
        wiki_token = root_wiki_node_token
    resp = get_children_nodes(t_token, space_id, wiki_token)
    return {'children': [
        {
            'wiki_token': it.get('node_token'),
            'doc_token': it.get('obj_token'),
            'title': it.get('title'),
            'parent_node_token': it.get('parent_node_token'),
            'doc_type': it.get('obj_type'),
            'node_type': it.get('node_type'),
            'has_child': it.get('has_child')} for it in resp.get('items', [])]}


@app.route('/download/<file_token>')
@refresh_token
def download_media(file_token):
    if not file_token:
        return ''
    bcontent = get_doc_media_by_file_token(t_token, file_token)
    return send_file(io.BytesIO(bcontent), mimetype='image/jpg')


if __name__ == "__main__":
    app.run("127.0.0.1", 5000)
