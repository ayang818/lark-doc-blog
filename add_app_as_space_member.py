# encoding=utf-8

import requests
space_id = "7011396001814544388"
# url = "https://open.feishu.cn/open-apis/wiki/v2/spaces/%s" % (space_id)
url = "https://open.feishu.cn/open-apis/wiki/v2/spaces/%s/members" % (space_id)
headers = {"Authorization": "Bearer u-51QDOGZV7T9qPs0tIGb6id", "Content-Type": "application/json; charset=utf-8"}
body = {"member_type": "openid", "member_id": "ou_7d4f7392ad7d7ee8d3078f86dc6099f8", "member_role": "member"}
resp = requests.post(url=url, headers=headers, json=body)
print(resp.__dict__)

# print(requests.get(url, headers=headers).text)
# curl -X POST -d 'member_type=openid' -d 'member_id=cli_a1093f4447f9d00c' -d 'member_role=admin' 
