import cv2
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import win32api
import win32con
# from pyquery import PyQuery as pq
# import requests
import re
import time
class AjkHuaKuai:
    def __init__(self):
        self.url = 'https://www.anjuke.com/captcha-verify/?callback=shield&from=antispam&history=aHR0cHM6Ly93d3cuYW5qdWtlLmNvbS9zeS1jaXR5Lmh0bWw%3D'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)

    def get_huakuai(self):
        """
        获取滑块
        :return: 滑块对象
        """
        self.browser.get(self.url)
        slider = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ISDCaptcha > div.dvc-slider > div.dvc-slider__handler > svg')))
        return slider
    def get_picture(self):
        a = self.browser.find_element(By.CSS_SELECTOR,'#ISDCaptcha > div.dvc-captcha > div > img.dvc-captcha__bgImg')#.get_attribute('src')
        # print(a)
        actions = ActionChains(self.browser)
        actions.context_click(a).perform()
        win32api.keybd_event(86, 0, 0, 0)  # 按V
        win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放V
        time.sleep(1)
        win32api.keybd_event(96, 0, 0, 0)  # 按0
        win32api.keybd_event(96, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放0
        # win32api.keybd_event(110, 0, 0, 0)  # 按.
        # win32api.keybd_event(110, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放.
        # win32api.keybd_event(80, 0, 0, 0)  # 按p
        # win32api.keybd_event(80, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放p
        # win32api.keybd_event(78, 0, 0, 0)  # 按n
        # win32api.keybd_event(78, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放n
        # win32api.keybd_event(71, 0, 0, 0)  # 按g
        # win32api.keybd_event(71, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放g
        win32api.keybd_event(13, 0, 0, 0)  # 按回车
        win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放回车
        win32api.keybd_event(89, 0, 0, 0)  # 按y
        win32api.keybd_event(89, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放y
        # headers = {
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        #     'referer': 'https://www.anjuke.com/captcha-verify/?callback=shield&from=antispam&history=aHR0cHM6Ly93d3cuYW5qdWtlLmNvbS9zeS1jaXR5Lmh0bWw%3D',
        #
        # }
        # cookies = {
        #     'cookie': 'id58 = c5 / nn1sDpUhQja / bKz1NAg ==',
        # }
        # r = requests.get(url=a,headers=headers,cookies=cookies)
        # with open('4.png', 'wb') as f:
        #     f.write(r.content)

    def is_white_line(self,imgpath):
        img = cv2.imread(imgpath)
        white = 0
        maxpx = 200
        maxline = 22
        for y in range(20, 480):
            for x in range(0, 270):
                if int(img[x, y, 0]) >= maxpx and int(img[x, y, 1]) >= maxpx and int(img[x, y, 2]) >= maxpx:
                    white += 1
                    if white == maxline:
                        return y
                else:
                    white = 0
    def move_to_ok(self,slider,track):
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track
    def get_cookies(self):
        return self.browser.get_cookies()
    def main(self):
        slider = self.get_huakuai()
        self.get_picture()
        time.sleep(3)
        y = self.is_white_line("C:/Users/HP/Downloads/0.jfif")
        print('阴影坐标',y)
        width = 280
        move = (y/480)*width-7-42
        print('偏移量',int(move))
        track = self.get_track(move)
        self.move_to_ok(slider,track)
        time.sleep(1)
        html = self.browser.page_source
        success = re.search('安居客互联网房产信息服务商，为广大用户提供满意的找房体验,也为开发商、中介公司、经纪人和业主提供高效的网络推广平台，已覆盖 全国381个城市、60万经纪人。挑好房就上安居客',html)
        if success:
            print(self.get_cookies())
        else:
            # self.browser.refresh()
            self.main()
if __name__ == '__main__':
    a = AjkHuaKuai()
    a.main()


