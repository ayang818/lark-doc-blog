import requests

url = "https://open.feishu.cn/open-apis/wiki/v2/spaces"
headers = {"Authorization": "Bearer t-64fdfb630d5a7f2a9846b03ef51b7e4459cd38b5", "Content-Type": "application/json; charset=utf-8"}
requests.get(url, )

 curl -i 'https://open.feishu.cn/open-apis/wiki/v2/spaces?page_size=10'  -H 'Authorization: Bearer t-64fdfb630d5a7f2a9846b03ef51b7e4459cd38b5'