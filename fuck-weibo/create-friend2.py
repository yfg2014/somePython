import random
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 关注用户
def follow(uidList):
    # uid中第一行，用于手动扫码登录
    firstId = '6199298208'
    for uid in uidList:
        if uid == '':
            print('已执行完数据')
            return
        # 检查用户状态是否正常
        response = requests.get("https://weibo.com/ajax/profile/info?uid=" + uid)
        if response.status_code != 200:
            print(f'用户{uid}状态异常')
            continue

        # 打开网页
        driver.get('https://weibo.com/u/' + uid)
        # 第一个用户稍作停留，用手机扫码登录，生成cookie
        if uid==firstId:
            time.sleep(60)
        # 等待元素加载完成
        wait = WebDriverWait(driver, 10)
        elements = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "FollowBtn_m_1UJhp"))
        )
        # 获取元素的文本
        text = elements.text
        # print(text)
        # print("开始处理第{i}个用户".format(i=uidList.index(uid)+1))
        # 关注总是需要验证码，怎么解决呢？
        if text == '关注':
            elements.click()
            print('关注成功')
            # 关注后页面停留数秒，模拟真人操作
            random_number = random.randint(0, 10)
            time.sleep(random_number)
        else:
            # print(f'用户{uid}已经关注')
            # 暂停1秒很重要，否则会报错
            time.sleep(1)
            continue
        print("------------------------")


if __name__ == '__main__':
    # 创建浏览器实例
    driver = webdriver.Firefox()
    # 读取本地文件测试
    with open('uid.txt', 'r') as f:
        # 去掉每行的换行符
        uidList = f.read().splitlines()
    # 获取某个区间的数据,每次只执行区间数据，避免一次性执行所有数据引起微博封控
    # print(uidList[0:5])
    # uidList = uidList[0:200]
    offset = 0
    step = 100
    for i in range(0, 14):
        newList = uidList[offset:offset + step]
        follow(newList)
        offset += step
        # 睡眠三分钟后再执行第二个100条数据
        print("------------------------")
        print(f'当前执行到第{offset}个用户,睡眠五分钟后再执行')
        print("------------------------")
        # time.sleep(300)
