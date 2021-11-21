# encoding: utf-8
import requests
from fsutil import getj, postj
import json
import conf
from conf import *

for c in conf.__dict__:
    if str(c).startswith("__"):
        continue
    print("conf: %s=%s" % (c, conf.__dict__[c]))

def get_t_token():
    resp = requests.post(url='https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', headers={'content-type': 'application/json; charset=utf-8'}, json={"app_id": app_id, "app_secret": app_secret})
    return json.loads(resp.text)['tenant_access_token']

def get_user_token():
    """
    TODO 如果过期了，就去 refresh_token。获取
    click here: https://open.feishu.cn/open-apis/authen/v1/index?redirect_uri=http://127.0.0.1:5000/redirect&app_id=cli_a1093f4447f9d00c&state=1
    """
    token = requests.get("http://127.0.0.1:5000/token").text
    print("get token %s" % (token,))
    return token

# 如果过期了，就去 refresh_token
user_token = None

def get_operate_member_collection(file_token, file_type):
    """
    获取文档协作者列表
    https://open.feishu.cn/document/ukTMukTMukTM/uATN3UjLwUzN14CM1cTN
    """
    global user_token
    if not user_token:
        user_token = get_user_token()
    return postj("https://open.feishu.cn/open-apis/drive/permission/member/list", user_token, json_data={"token": file_token, "type": file_type})

def get_file_token_by_wiki_token(token, wiki_token):
    """
    通过 wiki_token 获取 file_token
    https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/wiki-v2/space/get_node
    wiki_token: wiki文件链接的最后部分
    """
    resp = getj("https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token=%s" % (wiki_token,), access_token=token)
    data = resp["node"]
    return data['obj_token'], data['obj_type']

def add_app_as_space_member(app_open_id):
    """
    添加应用为知识空间成员 
    """
    global user_token
    if not user_token:
        user_token = get_user_token()
    space_id = "7011396001814544388"
    # url = "https://open.feishu.cn/open-apis/wiki/v2/spaces/%s" % (space_id)
    url = "https://open.feishu.cn/open-apis/wiki/v2/spaces/%s/members" % (space_id)
    body = {"member_type": "openid", "member_id": app_open_id, "member_role": "member"}
    resp = postj(url=url, access_token=user_token, json_data=body)
    return resp

def get_space_list(token, page_size):
    """
    通过 token 获取 知识空间列表
    """
    url = "https://open.feishu.cn/open-apis/wiki/v2/spaces?page_size=%s" % (page_size, )
    resp = getj(url, access_token=token)
    return resp

def get_space_info(token, space_id):
    # , data={"space_id": space_id}
    return getj("https://open.feishu.cn/open-apis/wiki/v2/spaces/%s" % (space_id, ), access_token=token)

def get_nodes_by_space_id(token, space_id):
    return getj("https://open.feishu.cn/open-apis/wiki/v2/spaces/%s/nodes" % (space_id,), access_token=token, data={"page_size": 50})

def get_doc_content_by_file_token(token, file_token):
    return getj("https://open.feishu.cn/open-apis/doc/v2/%s/content" % (file_token, ), access_token=token)

"""
所有的 parse 函数都会返回一段 html 代码.
TODO 这些解析应该放到前端去做
"""
def parse_block(block_data : str) -> str:
    pass

def parse_title(title_data : str) -> str:
    """
    解析文件头
    """
    elements: list = title_data['elements']
    style: dict = title_data['style']
    align_style = style.get('align')
    

def parse_doc(data : str) -> str:
    doc, version = data['content'], data['revision']
    jdata = json.loads(doc)
    print(jdata['title'])
    print("============")
    print(jdata['body'])

if __name__ == "__main__":
    # =========================获取应用的 open_id
    # file_token, file_type = get_file_token_by_wiki_token(user_token,"wikcnKUlL4f1Li9sYKLZQCN6Drf")
    # print(file_token, file_type)
    # get_operate_member_collection(file_token, file_type)
    # =========================

    # =========================添加应用到知识库成员
    # resp = add_app_as_space_member("ou_d6727dbe967ee7f59feb608b5e968ac0")
    # print(resp)
    # =========================

    t_token = get_t_token()
    # =========================使用应用的 token 查看有权限的知识空间
    # resp = get_space_list(t_token, 10)
    # print(resp)
    # =========================

    # =========================获取知识空间信息
    # print(get_space_info(t_token, 7011396001814544388))
    # =========================

    # =========================获取节点by space——id
    # print(get_nodes_by_space_id(t_token, 7011396001814544388))
    # =========================

    # =========================测试文件内容
    file_token, file_type = get_file_token_by_wiki_token(token=t_token, wiki_token="wikcnvFapTea0i1ekiEyj3cnfRh")
    print(file_token)
    doc_data = get_doc_content_by_file_token(t_token, file_token)
    # =========================


    # TODO 解析文档内容并显示到前端
    
    parse_doc(doc_data)

