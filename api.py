# encoding: utf-8
from fsutil import getj, postj
from get_user_access_token import get_t_token

user_token = "u-byZo4Q2HYLGz39J3vJp2Ph"

def get_user_token():
    """
    click here: https://open.feishu.cn/open-apis/authen/v1/index?redirect_uri=http://127.0.0.1:5000/redirect&app_id=cli_a1093f4447f9d00c&state=1
    """
    pass 

def get_operate_member_collection(file_token, file_type):
    """
    获取文档协作者列表
    https://open.feishu.cn/document/ukTMukTMukTM/uATN3UjLwUzN14CM1cTN
    """
    print(postj("https://open.feishu.cn/open-apis/drive/permission/member/list", user_token, json_data={"token": file_token, "type": file_type}))

def get_file_token_by_wiki_token(wiki_token):
    """
    通过 wiki_token 获取 file_token
    https://open.feishu.cn/document/ukTMukTMukTM/uUDN04SN0QjL1QDN/wiki-v2/space/get_node
    wiki_token: wiki文件链接的最后部分
    """
    resp = getj("https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token=%s" % (wiki_token,), user_token)
    data = resp["node"]
    return data['obj_token'], data['obj_type']

def add_app_as_space_member(app_open_id):
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

if __name__ == "__main__":
    # =========================获取应用的 open_id
    # file_token, file_type = get_file_token_by_wiki_token("wikcnKUlL4f1Li9sYKLZQCN6Drf")
    # print(file_token, file_type)
    # get_operate_member_collection(file_token, file_type)
    # =========================

    # =========================添加应用到知识库成员
    # resp = add_app_as_space_member("ou_d6727dbe967ee7f59feb608b5e968ac0")
    # print(resp)
    # =========================

    # =========================使用应用的 token 查看知识空间
    t_token = get_t_token()
    resp = get_space_list(t_token, 10)
    print(resp)
