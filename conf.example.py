# 应用 id
app_id = "cli_a1093f4447f9d00c"
# 应用 secret
app_secret = ""
# 知识库 id
space_id = "7011396001814544388"
# 重定向地址
redirect_url = "http://127.0.0.1:5000/redirect"
# https://open.feishu.cn/open-apis/authen/v1/index?redirect_uri=http://127.0.0.1:5000/redirect&app_id=cli_a1093f4447f9d00c&state=1
get_code_url = "https://open.feishu.cn/open-apis/authen/v1/index?redirect_uri=%s&app_id=%s&state=1" % (redirect_url , app_id)