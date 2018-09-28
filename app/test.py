#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import logging
import os
import sys
from importlib import reload
from logging import Logger
from time import sleep

# from selenium.webdriver.chrome.options import Options
import yaml
from damai_ticket_info import damai_url
from splinter import browser

reload(sys)
sys.setdefaultencoding('utf-8')  # 防止由于Unicode编码与ASCII编码的不兼容造成错误

class BuyTicket(object):
    def __init__(self, username, passwd, order, passengers, seatType, ticketType, daytime, starts, ends):
        # 用户名 密码
        self.username = username
        self.passwd = passwd
        # 车次,选择第几趟,0则从上之下依次点击
        self.order = order
        # 乘客名
        self.passengers = passengers
        # 席位
        self.seatType = seatType
        self.ticketType = ticketType
        # 时间格式2018-02-05
        self.daytime = daytime
        # 起始地和终点
        self.starts = starts
        self.ends = ends

        #self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        #self.initMy_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
        #self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.damai_login_url = damai_url['login_url']
        # 浏览器名称
        self.driver_name = 'firefox'  # chrome firefox
        # 火狐浏览器第三方驱动
        self.executable_path = os.getcwd()+'/geckodriver.exe'  # 获取工程目录下的火狐驱动 chromedriver

    def login(self):
        # 访问登录网址
        self.driver.visit(self.damai_login_url)
        # 填充用户名
        #大麦网登录名id是fm-login-id
        #密码id是fm-login-password
        #self.driver.fill("loginUserDTO.user_name", self.username)
        self.driver.fill("fm-login-id", self.username)
        # sleep(1)
        # 填充密码
        #self.driver.fill("userDTO.password", self.passwd)
        self.driver.fill("fm-login-password", self.passwd)
        clear_button = browser.find_element_by_xpath("//form[@id='loginForm']/div[3]/button[0]")
        clear_button.click()
        # print('请手动输入验证码...')  # 目前没有自动验证码
        # 循环等待登录，登录成功，跳出循环
        while True:
            if self.driver.url != self.initMy_url:
                sleep(1)
            else:
                break

"""
    def start_buy(self):
        # 这些设置都是必要的
        # chrome_options = Options()
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-setuid-sandbox")
        # chrome_options.add_argument("disable-infobars")  # 禁用网页上部的提示栏
        # self.driver = Browser(driver_name=self.driver_name, options=chrome_options, executable_path=self.executable_path)
        self.driver = Browser(driver_name=self.driver_name,
                              executable_path=self.executable_path)
        # 设置窗口大小尺寸
        self.driver.driver.set_window_size(1400, 1000)
        # 用户登录
        self.login()
        # 进入选票网站
        self.driver.visit(self.ticket_url)
        try:
            logbticket.info("购票页面开始....")
            # print("购票页面开始....")
            # sleep(1)
            # 加载查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.daytime})

            self.driver.reload()

            count = 0
            if self.order != 0:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text("查询").click()
                    count = count+1
                    logbticket.info("第 %d 次点击查询..." % count)
                    # print("第 %d 次点击查询..." % count)
                    # sleep(1)
                    try:
                        self.driver.find_by_text("预订")[self.order - 1].click()  # 点击第几个“预订”
                        sleep(1.5)
                    except Exception as e:  # e是Exception 的一个instance
                        # print(e)
                        # print("预订失败...")
                        logbticket.error(e)
                        logbticket.error("预订失败...")
                        continue
            else:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text("查询").click()
                    count += 1
                    logbticket.info("第 %d 次点击查询..." % count)
                    # print("第 %d 次点击查询..." % count)
                    try:
                        for i in self.driver.find_by_text("预订"):
                            i.click()
                            sleep(1)
                    except Exception as e:
                        # print(e)
                        # print("预订失败...")
                        logbticket.error(e)
                        logbticket.error("预订失败...")
                        continue

            # print("开始预订....")
            logbticket.info("开始预订....")
            # sleep(1)
            # self.driver.reload()
            sleep(1)
            # print("开始选择用户....")
            logbticket.info("开始选择用户....")
            for p in self.passengers:
                pg = self.driver.find_by_text(p)  # .last.click()
                pg.last.click()
            # print("提交订单....")
            logbticket.info("提交订单....")
            sleep(1)
            i = 0
            while len(self.passengers) > 0:
                i = i + 1
                seat_id_string = "seatType_" + str(i)
                ticket_id_string = "ticketType_" + str(i)
                self.driver.find_by_xpath('//select[@id="%s"]/option[@value="%s"]'
                                          % (seat_id_string, self.seatType)).first._element.click()
                self.driver.find_by_xpath('//select[@id="%s"]//option[@value="%s"]'
                                          % (ticket_id_string, self.ticketType)).first._element.click()
                self.passengers.pop()
                sleep(1)
            self.driver.find_by_id("submitOrder_id").click()
            # print("开始选座...")
            logbticket.info("开始选座...")
            sleep(1.5)
            # print("确认选座....")
            logbticket.info("确认选座....")
            self.driver.find_by_text("qr_submit_id").click()

        except Exception as e:
            # print(e)
            logbticket.error(e)
"""



city = {"深圳": "%u6DF1%u5733%2CSZQ",
        "武汉": "%u6B66%u6C49%2CWHN",
        "随州": "%u968F%u5DDE%2CSZN"}

seatT = {"硬卧": "3",
         "软卧": "4",
         "硬座": "1",
         "二等座": "O",
         "一等座": "M",
         "商务座": "9"}

ticketT = {"成人票": "1"}

if __name__ == '__main__':
    # # 用户名
    # username = "hugoodboy"
    # # 密码
    # password = "198324"
    # # 车次选择，0代表所有车次
    # order = 3
    # # 乘客名，比如passengers = ['丁小红', '丁小明']
    # # 学生票需注明，注明方式为：passengers = ['丁小红(学生)', '丁小明']
    # passengers = ["胡迎春", "柳淑琼"]
    # # 日期，格式为：'2018-01-20'
    # daytime = "2018-04-18"
    # # 出发地(需填写cookie值)
    # starts = city["武汉"]  # 武汉
    # # 目的地(需填写cookie值)
    # ends = city["深圳"]  # 深圳
    # # 席别
    # seatType = "一等座"  # 软卧
    # # 票种
    # ticketType = "1"  # 成人票

    logbticket = Logger("bticket.log", logging.DEBUG, logging.ERROR)
    try:
        with open("profile.yml", "r") as f:
            btconfig = yaml.safe_load(f)
    except OSError:
        logbticket.error("Can't open config file: profile.yml")
        raise

    # 用户名
    username = btconfig['username']
    # 密码
    password = btconfig['password']
    # 车次选择，0代表所有车次
    order = btconfig['order']
    # 乘客名，比如passengers = ['丁小红', '丁小明']
    passengers = btconfig['passengers']
    # 日期，格式为：'2018-01-20'
    daytime = btconfig['daytime']
    # 出发地(需填写cookie值)
    # cfgstart = btconfig['starts']
    starts = city[btconfig['starts'].encode('utf-8')]  # 武汉,将unicode格式编码为utf-8格式
    # 目的地(需填写cookie值)
    # cfgend = btconfig['ends']
    ends = city[btconfig['ends'].encode('utf-8')]  # 北京,将unicode格式编码为utf-8格式
    # 席别
    seatType = seatT[btconfig['seatType'].encode('utf-8')]  # 二等座,将unicode格式编码为utf-8格式
    # 票种
    ticketType = ticketT[btconfig['ticketType'].encode('utf-8')]  # 成人票,将unicode格式编码为utf-8格式

    BuyTicket(username, password, order, passengers, seatType, ticketType, daytime, starts, ends).start_buy()
