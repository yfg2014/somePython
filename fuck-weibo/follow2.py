# -*-coding:utf8-*-
import json
import time
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 全局变量
# 关注的人总页数
total_page = 35
# 登录后cookie
# 请将cookie替换成自己的cookie
cookie="xxxxxxxxx"

def get_uidlist(page=1, next_cursor=0):
    url = f"https://weibo.com/ajax/profile/followContent?page={page}&next_cursor={next_cursor}"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": cookie
    }
    response = requests.get(url=url, headers=headers, verify=False)
    # print(response.status_code)
    # print(response.text)
    if response.status_code == 200 and is_json(response.text):
        userList = []
        for i in response.json()['data']['follows']['users']:
            userList.append(str(i['id']))
        # 写入本地文件
        with open('uid.txt', 'a') as f:
            f.write('\n'.join(userList)+'\n')

        print(url)
        print(f'第{page}页数据获取成功')
    else:
        print(f'第{page}页数据获取失败')
        print("请检查网页是否登录状态,cookie是否最新")
        print(response.text)
        print(response.headers)


# 判断是否是json格式
def is_json(response):
    try:
        json_object = json.loads(response)
    except ValueError as e:
        return False
    return True

if __name__ == '__main__':
    next_cursor = 0
    for i in range(1, total_page+1):
        get_uidlist(page=i, next_cursor=next_cursor)
        next_cursor += 50
        time.sleep(2)
