# _*_ coding:utf-8 _*_
__author__ = 'Eddie'

import os
import re
import time
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

import sql
import tbjpy
from rfs_web.app import BaseHandle

class TerminalHandle(BaseHandle.BaseHandle):
    def __init__(self,platformName,platfromVersion,deviceName,udid,appPackage,appActivity,host,port=None,timeout=None,**kwargs):
        super(TerminalHandle,self).__init__()
        self.init_drive_error = None
        if not timeout:
            self.timeout = 15
        if not port:
            self.port = 4723
        else:
            self.port = port
        if not host:
            self.host = '127.0.0.1'
        else:
            self.host = host
        self._desired_caps = {
            'platformName':platformName,
            'platfromVersion':platfromVersion,
            'deviceName':deviceName,
            'udid':udid,
            'appPackage':appPackage,
            'appActivity':appActivity,
            'unicodeKeyboard':True,
		    'resetKeyboard':True,
            #'autoLaunch':False
        }
        if kwargs:
            self._desired_caps.update(kwargs)

        while True:
            if self.conn_webdrive():
                break
            time.sleep(1)

    def conn_webdrive(self):
        try:
            self.driver = webdriver.Remote('http://%s:%d/wd/hub' % (self.host,self.port),self._desired_caps)
            return True
        except Exception,e:
            print 'Error: ',str(e)
            if str(e) == "<urlopen error [Errno 61] Connection refused>":
                return False
            else:
                if str(e)[0] == '<' and str(e)[-1] == '>':
                    msg = str(e)[1:-1]
                else:
                    msg = str(e)
                self.init_drive_error = msg
                return True

    def setUp(self):
        #self.driver.launch_app()
        pass

    # def tearDown(self):
    #     print 333
    #     "Hook method for deconstructing the test fixture after testing it."
    #     pass

    @classmethod
    def setUpClass(cls):
        #cls.driver.launch_app()
        pass

    #@classmethod
    def tearDownClass(self):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        #print 111
        self.driver.close_app()
        #print 121
        pass

    def find(self,loc):
        try:
            WebDriverWait(self.driver,self.timeout).until(lambda drive:drive.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except Exception,e:
            print u"%s 页面中超时%ds未能找到 %s 元素%s" %(self,self.timeout,loc,e)

    def click_keys(self,loc):
        self.find(loc).click()

    def clear_keys(self,loc):
        self.find(loc).clear()

    def send_keys(self,loc,value):
        sleep(3)
        self.find(loc).send_keys(value)

    def click_button(self,loc):
        self.find(loc).click()

    def isElement(self,identifyBy,c):
        #self.drive.implicitly_wait(60)
        flag=None
        try:
            if identifyBy == "id":
                #self.driver.implicitly_wait(60)
                self.driver.find_element_by_id(c)
            elif identifyBy == "xpath":
                #self.driver.implicitly_wait(60)
                self.driver.find_element_by_xpath(c)
            elif identifyBy == "class":
                #self.driver.implicitly_wait(60)
                self.driver.find_element_by_class_name(c)
            flag = True
        except NoSuchElementException,e:
            flag = False
        finally:
            return flag

    def doesExist(self,identifyBy,c):
        i = 1
        while not self.isElement(self,identifyBy):
            sleep(1)
            i = i+1
            if i >= 10:
                return False
        else:
            return True

    def screenshot(self):
        path = "D:\\"
        title = "appium_test_result"
        timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        new_path = os.path.join(path, title)
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
            self.driver.get_screenshot_as_file(new_path+"\\"+"result_" + timestr + ".png")
        else:
            self.driver.get_screenshot_as_file(new_path+"\\"+"result_" + timestr + ".png")

    def screenshot_True(self):
        path = "D:\\"
        title = "appium_test_result"
        timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        new_path = os.path.join(path, title)
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
            self.driver.get_screenshot_as_file(new_path+"\\"+"result_True_" + timestr + ".png")
        else:
            self.driver.get_screenshot_as_file(new_path+"\\"+"result_True_" + timestr + ".png")

    def screenshot_Error(self):
        path = "D:\\"
        title = "appium_test_result"
        timestr = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        new_path = os.path.join(path, title)
        #print 1
        if not os.path.isdir(new_path):
            os.makedirs(new_path)
            self.driver.get_screenshot_as_file(new_path+"\\"+"result_Error_" + timestr + ".png")
        else:
            self.driver.get_screenshot_as_file(new_path+"\\"+"result_Error_" + timestr + ".png")

    def fetch_coord(self,location,size):
        #'''location:{'y':1050,'x':'100'}
        #   size:{'weidth':100,'heigth':100'''
        start_x = location['x']
        start_y = location['y']
        average_x = size['width'] / 3.0
        average_y = size['height'] / 4.0
        coord_list = []
        for i in range(4):
            _y = int(start_y + average_y * i + average_y / 2)
            for j in range(3):
                _x = int(start_x + average_x * j + average_x / 2)
                coord_list.append([(_x,_y)])
        return coord_list

class AppHandle(TerminalHandle):
    def __init__(self,platformName,platfromVersion,deviceName,udid,appPackage,appActivity,host,port=None,timeout=None,**kwargs):
        super(AppHandle,self).__init__(platformName,platfromVersion,deviceName,udid,appPackage,appActivity,host,port,timeout=None,**kwargs)

    #进入更多模块
    def click_more(self):
        self.click_button((By.ID, tbjpy.more))

    #点击我的帐号
    def click_myaccount(self):
        self.click_button((By.ID, tbjpy.loginbtn))

    #登录，输入帐号
    def input_login_phone(self,phone_num):
        self.send_keys((By.ID, tbjpy.input_phone), phone_num)
        next_btn_state=self.driver.find_element_by_id(tbjpy.next).get_attribute("enabled")
        if next_btn_state=='false':
            #self.screenshot_Error()
            self.back()
            raise Exception('手机号不满11位')
            #self.back()

    #登录，输入帐号后点击下一步
    def click_next(self):
        self.click_keys((By.ID, tbjpy.next))
        sleep(2)
        if self.isElement("id", tbjpy.verify_input)==True:
            #self.screenshot_Error()
            self.back()
            self.back()
            #print 22
            raise Exception('进入注册模块')

    #登录，输入密码
    def input_login_passwd(self,passwd):
        self.send_keys((By.ID, tbjpy.input_login_passwd), passwd)
        next_btn_state=self.driver.find_element_by_id(tbjpy.click_login_button).get_attribute("enabled")
        if next_btn_state=='false':
            #self.screenshot_Error()
            self.back()
            self.back()
            raise Exception('密码不满6位或为空')

    #登录，输入密码后确定
    def click_login_button(self):
        self.click_button((By.ID, tbjpy.click_login_button))

    #退出登录
    def logout(self):
        self.click_button((By.ID, tbjpy.logout))

    #注册，输入帐号
    def input_sign_Account(self,sign_Account):
        self.send_keys((By.ID, tbjpy.input_phone), sign_Account)
        self.click_button((By.ID, tbjpy.next))

    def back1(self):
        self.click_button((By.ID, tbjpy.back1))

    #手机相关信息输出,并截图
    def phonemessage(self):
         #版本
        version=os.popen("adb shell grep ro.build.version.release /system/build.prop").read()
        version1=re.search("(?<==).*", version)
        print u'手机版本:'+version1.group(0)
        #型号
        # model =os.popen("adb shell grep ro.product.model /system/build.prop").read()
        # model1 =re.search("(?<==).*", model )
        # print u'手机型号:'+model1.group(0)
        # #系统版本
        # brand =os.popen("adb shell grep ro.product.brand /system/build.prop").read()
        # brand1 =re.search("(?<==).*", brand )
        # print u'手机系统版本:'+brand1.group(0)
        # a="D:\\appium\\appiumresult\\result_"+ model1.group(0) + timestr + ".jpg"
        # a = model1.group(0).split()
        # b = "".join(a)
        # sleep(2)
        # self.driver.get_screenshot_as_file("D:\\appium\\appiumresult\\result_"+b+ timestr + ".jpg")

    #注册设置登陆密码
    def send_signpwd(self,signpwd):
        self.send_keys((By.ID, tbjpy.set_login_password), signpwd)

    #点击密码管理按钮
    def rl_pwd_manager(self):
        self.click_button((By.ID, tbjpy.rl_pwd_manager))

    #点击修改登陆密码按钮
    def change_login_pwd_layout(self):
        self.click_button((By.ID, tbjpy.change_login_pwd_layout))

    #修改登陆密码
    def send_old_pwd(self,old_pwd):
        self.send_keys((By.ID, tbjpy.old_password_input), old_pwd)

    #设置并重复密码
    def set_pwd(self,set_pwd,repeat_pwd):
        self.send_keys((By.ID, tbjpy.new_password_input), set_pwd)
        self.send_keys((By.ID, tbjpy.confilm_new_password), repeat_pwd)
        self.click_button((By.ID, tbjpy.modify_login_pwd))

    #点击修改交易密码按钮
    def rlyt_update_trans_pwd(self):
        self.click_button((By.ID, tbjpy.rlyt_update_trans_pwd))

    #点击完成按钮
    def click_complete_btn(self):
        self.click_button((By.ID, tbjpy.complete_btn))

    #点击找回交易密码按钮
    def rlyt_find_trade_pwd(self):
        self.click_button((By.ID, tbjpy.rlyt_find_trade_pwd))

    #输入交易密码
    def send_trade_pwd(self,trade_pwd):
        # print 66,trade_pwd
        sleep(4)
        p=self.driver.find_element_by_id(tbjpy.key).location
        d=self.driver.find_element_by_id(tbjpy.key).size
        coord_list = self.fetch_coord(p,d)
        # print 44
        #输入六位安全密码
        for i in trade_pwd:
            self.driver.tap(coord_list[int(i) -1])
            sleep(1)
        sleep(2)

    #输入原交易密码
    def send_old_trade_pwd(self,old_trade_pwd):
        sleep(2)
        p=self.driver.find_element_by_id(tbjpy.key).location
        d=self.driver.find_element_by_id(tbjpy.key).size
        coord_list = self.fetch_coord(p,d)
        #输入六位安全密码
        for i in old_trade_pwd:
            self.driver.tap(coord_list[int(i) -1])
            sleep(1)
        sleep(2)
        if self.isElement("xpath", tbjpy.check_old_tradepwd)==True:
            #print 33
            #self.screenshot_Error()
            self.back1()
            self.back()
            self.back()
            raise Exception('原交易密码输入位数不够')
        elif self.isElement("xpath", tbjpy.check_tradepwd_reminder)==True:
            #print 111
            #self.screenshot_Error()
            self.click_sure_nothing()
            self.back1()
            self.back()
            self.back()
            raise Exception('原交易密码错误')

    #输入新交易密码
    def send_new_trade_pwd(self,new_trade_pwd):
        sleep(2)
        p=self.driver.find_element_by_id(tbjpy.key).location
        d=self.driver.find_element_by_id(tbjpy.key).size
        coord_list = self.fetch_coord(p,d)
        #输入六位安全密码
        for i in new_trade_pwd:
            self.driver.tap(coord_list[int(i) -1])
            sleep(1)
        sleep(2)
        if self.isElement("xpath", tbjpy.check_set_tradepwd)==True:
            #print 44
            #self.screenshot_Error()
            self.back1()
            self.back()
            self.back()
            raise Exception('新交易密码输入位数不够')

    #输入重复交易密码
    def send_repeat_trade_pwd(self,repeat_trade_pwd):
        sleep(2)
        p=self.driver.find_element_by_id(tbjpy.key).location
        d=self.driver.find_element_by_id(tbjpy.key).size
        coord_list = self.fetch_coord(p,d)
        for i in repeat_trade_pwd:
            self.driver.tap(coord_list[int(i) -1])
            sleep(1)
        sleep(2)
        complete_btn_state=self.driver.find_element_by_id(tbjpy.complete_btn).get_attribute("enabled")
        if complete_btn_state=='false':
            #print 55
            #self.screenshot_Error()
            self.back1()
            self.back()
            self.back()
            self.back()
            raise Exception('重复交易密码不够位数')

    #输入找回交易密码相关信息并修改
    # def find_trade_pwd(self,username,card):
    #     self.click_button((By.ID,tbjpy.rlyt_find_trade_pwd))
    #     self.send_keys((By.ID,tbjpy.full_name_value),username)
    #     self.send_keys((By.ID,tbjpy.input_value),card)
    #     self.click_button((By.ID,tbjpy.next_btn))
    #     sleep(5)
    #     myms = sql.mysql_connect(sql.db_info)
    #     sleep(5)
    #     # verify_code1=myms.sql_assign_exec("select content from mdp_message WHERE recipients="+ tbjdata.loginid(1) + " ORDER BY create_time DESC LIMIT 1")
    #     #verify_code2=re.search('\d{6}', verify_code1)
    #     verify_code3=verify_code2.group(0)
    #     self.send_keys((By.ID,tbjpy.verify_input),verify_code3)
    #     print 2
    #     self.click_button((By.ID,tbjpy.btn_next))
    #     self.driver.implicitly_wait(10)
    #     sleep(5)

    #点击账户余额按钮
    def click_account_balance(self):
        sleep(1)
        self.click_button((By.ID, tbjpy.rl_account_balance))
        sleep(1)

    #点击我的资产按钮
    def myproperty(self):
        self.click_button((By.ID, tbjpy.myasset))

    #点击进入余额并退出
    def click_payment_details(self):
        sleep(3)
        self.click_button((By.ID, tbjpy.rl_payment_details))
        self.click_button((By.ID, tbjpy.back1))

    #返回
    def back(self):
        self.click_button((By.ID, tbjpy.back1))

    #点击充值按钮
    def click_recharge(self):
        self.driver.implicitly_wait(5)
        self.click_button((By.ID, tbjpy.rl_recharge))

    #充值
    def rl_recharge(self,topup_num):
        sleep(5)
        self.send_keys((By.XPATH, tbjpy.czje), topup_num)
        self.click_button((By.XPATH, tbjpy.recharge_submit))
        if self.isElement("xpath", tbjpy.send_true_monkey)==True:
            #print 112
            #self.screenshot_Error()
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back()
            self.back()
            raise Exception('充值金额错误')
        if self.isElement("xpath", tbjpy.recharge_choose_bankcard)==True:
            #print 223
            #self.screenshot_Error()
            self.click_button((By.ID, tbjpy.click_sure))
            self.back()
            self.back()
            raise Exception('请选择银行卡')

    def rl_recharge43(self,topup_num):
        sleep(5)
        self.send_keys((By.XPATH, tbjpy.czje), topup_num)
        self.click_button((By.XPATH, tbjpy.recharge_submit))
        if self.isElement("xpath", tbjpy.send_true_monkey)==True:
            #print 112
            #self.screenshot_Error()
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back()
            #self.back()
            raise Exception('充值金额错误')
        if self.isElement("xpath", tbjpy.recharge_choose_bankcard)==True:
            #print 223
            #self.screenshot_Error()
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back()
            #self.back()
            raise Exception('请选择银行卡')

    #点击余额转出按钮
    def click_balance_out(self):
        self.click_button((By.ID, tbjpy.rl_balance_out))
        sleep(3)

    #余额转出
    def rl_balance_out(self,out_num):
        sleep(5)
        #print 11
        self.send_keys((By.XPATH, tbjpy.zcje), out_num)
        sleep(3)
        submit_btn_state=self.driver.find_element_by_xpath(tbjpy.submit).get_attribute("enabled")
        self.click_button((By.XPATH, tbjpy.submit))
        sleep(1)
        if self.isElement("id", tbjpy.key)==False:
            #self.screenshot_Error()
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back()
            self.back()
            raise Exception('提现金额错误')

    #余额转出
    def rl_balance_out43(self,out_num):
        sleep(5)
        #print 11
        self.send_keys((By.XPATH, tbjpy.zcje), out_num)
        sleep(3)
        submit_btn_state=self.driver.find_element_by_xpath(tbjpy.submit).get_attribute("enabled")
        self.click_button((By.XPATH, tbjpy.submit))
        sleep(1)
        if self.isElement("id", tbjpy.key)==False:
            #self.screenshot_Error()
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back()
            #self.back()
            raise Exception('提现金额错误')

    #进入余额转出并确定
    def rl_balance_outqd(self):
        self.click_button((By.XPATH, tbjpy.click_sure))
        self.click_button((By.ID, tbjpy.back1))

    #点击进入回款路径
    def click_return_path_label(self):
        self.click_button((By.ID, tbjpy.return_path_label))
        sleep(3)

    #充值或者转出成功后点击确定按钮
    def click_money_success(self):
        self.click_button((By.XPATH, tbjpy.check_money_success))

    #无其他判断的确定
    def click_sure_nothing(self):
        self.click_button((By.ID, tbjpy.click_sure))

    #确定
    def click_sure(self):
        self.click_button((By.ID, tbjpy.true))
        sleep(4)
        # print 443
        if self.isElement("xpath", tbjpy.reminder_sure_button)==True:
            self.screenshot()
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back()
        elif self.isElement("xpath", tbjpy.server_error)==True:
            # print 331
            self.screenshot()
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back()
        elif self.isElement("xpath", tbjpy.buy_title_error)==True:
            self.screenshot()
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back()
        elif self.isElement("xpath", tbjpy.product_money_buy)==True:
            #self.screenshot_Error()
            # print 113
            self.screenshot()
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back()
        elif self.isElement("xpath", tbjpy.product_not_support_buy)==True:
            # print 445
            self.screenshot()
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            raise Exception('该产品暂不支持购买！')
        elif self.isElement("xpath", tbjpy.product_beyond_money)==True:
            # print 556
            # self.screenshot_Error()
            self.screenshot()
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back()
        elif self.isElement("xpath", tbjpy.check_buy_box)==True:
            #self.screenshot_Error()
            print 113
            self.screenshot()
            check_buy_box_text=self.driver.find_element_by_xpath(tbjpy.check_buy_box).get_attribute("name")
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back1()
            self.back()
            #self.back()
            raise Exception('交易密码错误')

    #确定
    def click_sure43(self):
        self.click_button((By.ID, tbjpy.true))
        sleep(2)
        if self.isElement("xpath", tbjpy.withhold_submit)==True:
            self.screenshot()
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back()
        elif self.isElement("xpath", tbjpy.remind_exceed_monkey)==True:
            #self.screenshot_Error()
            self.screenshot()
            print 111
            remind_exceed_monkey_text=self.driver.find_element_by_xpath(tbjpy.remind_exceed_monkey).get_attribute("name")
            #print 334,remind_exceed_monkey_text
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            raise Exception(remind_exceed_monkey_text)
        # elif self.isElement("id",tbjpy.key)==True:
        #     #print 441
        #     #self.screenshot_Error()
        #     raise Exception('交易密码不足位数')
        elif self.isElement("xpath", tbjpy.product_not_support_buy)==True:
            print 445
            self.screenshot()
            #self.screenshot_Error()
            #print '该产品暂不支持购买！'
            #print 112
            raise Exception('该产品暂不支持购买！')
        elif self.isElement("xpath", tbjpy.check_buy_box)==True:
            print 222
            self.screenshot()
            #self.screenshot_Error()
            #print 113
            check_buy_box_text=self.driver.find_element_by_xpath(tbjpy.check_buy_box).get_attribute("name")
            # print check_buy_box_text
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            self.back1()
            #self.back()
            #self.back()
            raise Exception('交易密码错误')

    #新用户时，设置交易密码
    def set_new_people_trade_pwd(self,new_people_trade_pwd,repeat_trade_pwd):
        self.click_button((By.ID, tbjpy.true))
        self.driver.implicitly_wait(5)
        p=self.driver.find_element_by_id(tbjpy.key).location
        d=self.driver.find_element_by_id(tbjpy.key).size
        coord_list = self.fetch_coord(p,d)
        for i in new_people_trade_pwd:
            self.driver.tap(coord_list[int(i) -1])
            sleep(1)
        for i in repeat_trade_pwd:
            self.driver.tap(coord_list[int(i) -1])
            sleep(1)
        sleep(2)
        # self.click_button((By.ID,tbjpy.complete_btn))

    #选择银行账户点击
    def click_bank(self):
        sleep(3)
        self.click_button((By.XPATH, tbjpy.bank))

    #选择第一个银行账户确定
    def click_banksure(self):
        sleep(4)
        #self.clickButton((By.XPATH,tbjpy.yhzh))
        self.click_button((By.XPATH, tbjpy.tcqd))

    #点击忘记密码按钮
    def click_forgetpwd(self):
        self.click_button((By.ID, tbjpy.forget_password))
        #title=self.driver.find_element_by_id(tbjpy.title).text
        #self.assertEqual("找回密码",title,'error')
        self.click_button((By.ID, tbjpy.next))

    #输入身份证
    def send_person_id(self,person_ID):
        self.send_keys((By.ID, tbjpy.input_value), person_ID)

    #下一步
    def nextbtn(self):
        self.click_button((By.ID, tbjpy.next_btn))

    #找回密码
    def click_back_pwd(self,back_pwd):
        self.send_keys((By.ID, tbjpy.set_login_password), back_pwd)

    #找回密码，下一步按钮点击操作
    def click_back_pwd_nextbtn(self):
        self.click_button((By.ID, tbjpy.click_back_pwd_nextbtn))

    #点击精品推荐入口按钮
    def click_hot_product(self):
        self.click_button((By.ID, tbjpy.hot_product))

    #精品推荐页购买按钮
    def ll_top_content(self):
        self.click_button((By.ID, tbjpy.hot_product_buy42))
        #if self.isElement("xpath",tbjpy.check_recommendation_reminder)==True:
        #     print 222
        #     check_recommendation_reminder_text=self.driver.find_element_by_xpath(tbjpy.check_recommendation_reminder).get_attribute("name")
        #     print check_recommendation_reminder_text
        #     raise Exception(check_recommendation_reminder_text)

    #输出精品推荐页的项目名称及期限
    def get_hot_product_message(self):
        get_hot_product_name=self.driver.find_element_by_id(tbjpy.hot_product_name).get_attribute("text")
        print get_hot_product_name
        get_hot_product_period=self.driver.find_element_by_id(tbjpy.hot_product_period).get_attribute("text")
        print get_hot_product_period

    #计算器的打开
    def calcopen(self):
        self.click_button((By.ID, tbjpy.calc_btn))
        # self.send_keys((By.ID,tbjpy.purchase_amount_edit),tbjdata.purchase_amount_edit)
        self.click_button((By.ID, tbjpy.calc_earnings_btn))

    #计算器的关闭
    def calcclose(self):
        self.click_button((By.ID, tbjpy.calc_close))

    #购买按钮
    def click_buy(self):
        self.click_button((By.ID, tbjpy.hot_product_buy_btn))

    #输入购买金额
    def send_buy_money(self,amount):
        sleep(6)
        self.send_keys((By.XPATH, tbjpy.hot_product_buy_money), amount)
        #print 33
        # hot_product_buy_money_sure_state=self.driver.find_element_by_id(tbjpy.hot_product_buy_money_sure).get_attribute("enabled")
        # if hot_product_buy_money_sure_state=='false':
        #     raise Exception('输入金额为空')

    #输入购买金额后的确定按钮
    def send_buy_monkey_sure(self):
        #print 111
        self.click_button((By.XPATH, tbjpy.hot_product_buy_money_sure))
        #print 445
        sleep(4)
        if self.isElement("xpath", tbjpy.buy_title_error)==True:
            # print 3345
            self.screenshot()
            self.click_button((By.XPATH, tbjpy.reminder_sure_button))
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            #print 2
            self.back()
        elif self.isElement("id", tbjpy.key)==False:
            # print 3335
            self.screenshot()
            # print 4445
            self.click_button((By.XPATH, tbjpy.balance_cancel))
            # print 5556
            self.back()
                # self.back()
                # e='失败'
                # actual=False
        # elif self.isElement("id",tbjpy.key)==False:
        #     print 222
        #     #print '金额不正确'
        #     raise Exception('金额不正确')
        # if self.isElement("xpath",tbjpy.check_buy_box)==True:
        #     print 222
        #     self.screenshot_Error()
        #     check_buy_box_text=self.driver.find_element_by_xpath(tbjpy.check_buy_box).get_attribute("name")
        #     print check_buy_box_text
        #     raise Exception(check_buy_box_text)

    #输入验证码之后确认的操作
    def qd(self):
        self.click_button((By.ID, tbjpy.true))
        self.click_button((By.XPATH, tbjpy.truetwo))
        self.click_button((By.ID, tbjpy.back1))

    #点击理财产品按钮
    def tab_financing_products(self):
        self.click_button((By.ID, tbjpy.tab_financing_products))

    #4.2版本我的资产-铜宝入口
    def myassert_tongbao42(self):
        self.click_button((By.ID, tbjpy.tongbao_assets_layout42))

    #4.3版本我的资产-铜宝入口
    def myassert_tongbao43(self):
        self.click_button((By.ID, tbjpy.tongbao_assets_layout43))

    #5.0版本理财产品铜宝入口
    def click_financing_products_tb(self):
        self.click_button((By.XPATH, tbjpy.financing_products_tb))
    #
    # #5.0版本定期理财定期理财入口
    # def click_financing_products_reqular(self):
    #     self.click_button((By.XPATH,tbjpy.financing_products_reqular))
    #
    # #5.0版本银行票据银行票据入口
    # def click_financing_products_tb(self):
    #     self.click_button((By.XPATH,tbjpy.financing_products_bill))

    #5.0点击理财产品的第二个选项
    def click_second_financing_name(self):
        self.click_button((By.XPATH, tbjpy.second_financing_name))

    #5.0点击理财产品第二个选项的第一个产品
    def click_second_financing_name_first(self):
        self.click_button((By.XPATH, tbjpy.second_financing_name_first))

    #选择第一个理财产品进行点击
    def click_frist_financing_product(self):
        self.click_button((By.XPATH, tbjpy.frist_financing_product))
        #sleep(5)

    #理财产品购买按钮
    def click_product_purchase_view(self):
        self.click_button((By.ID, tbjpy.product_purchase_view))
        sleep(5)

    #新手理财产品购买的提交按钮
    def newpeople_buy_commit(self):
        self.click_button((By.XPATH, tbjpy.newpeople_buy_commit))
        if self.isElement("xpath", tbjpy.newpeople_buy_commit_title)==True:
            self.click_button((By.ID, tbjpy.click_sure))
            self.back()
            self.screenshot_True()
            actual=False
            e='只能新用户购买'

    #转让市场购买按钮
    def transfer_market_buy(self):
        self.click_button((By.ID, tbjpy.transfer_buy))

    #转让市场支付按钮
    def transfer_market_pay(self):
        self.click_button((By.XPATH, tbjpy.transfer_pay))

    #点击我的资产按钮
    def click_myasset(self):
        self.click_button((By.ID, tbjpy.myasset))

    #4.3-5.0版本账户余额入口
    def click_balance5(self):
        self.click_button((By.ID, tbjpy.balance_entry5))

    #进入信息中心并返回
    def click_message(self):
        self.click_button((By.ID, tbjpy.message))
        self.click_button((By.ID, tbjpy.back1))

    #进入当前收益
    def click_income_component(self):
        self.click_button((By.ID, tbjpy.income_component))

    #进入累计收益
    def tv_right_option(self):
        self.click_button((By.ID, tbjpy.tv_right_option))
        self.click_button((By.ID, tbjpy.back1))
        self.click_button((By.ID, tbjpy.back1))

    #铜宝页面，未登陆状态，点击登录
    def click_tongbao_login(self):
        self.click_button((By.ID, tbjpy.buy_tongbao_check))

    #进入铜宝
    def click_tongbao(self):
        self.click_button((By.ID, tbjpy.tongbao_assets_layout))

    #铜宝转入
    def tongbao_in(self):
        self.click_button((By.ID, tbjpy.tongbao_in))

    #铜宝转出
    def tongbao_out(self):
        self.click_button((By.ID, tbjpy.tongbao_out))

    #进入铜宝后返回
    def tbback(self):
        self.click_button((By.ID, tbjpy.back1))

    #查看用户个人信息
    def click_user_infojr(self):
        u"""查看用户个人信息"""
        self.click_button((By.ID, tbjpy.rl_user_info))

    #点击银行卡管理按钮
    def click_bankcard_manager(self):
        self.click_button((By.ID, tbjpy.rl_bankcard_manager))

    #添加银行卡
    def add_bankcard(self):
        self.click_button((By.ID, tbjpy.rlyt_add_bankCard))

    #持卡人信息
    def add_personalInformation(self):
        self.click_button((By.ID, tbjpy.true))
        sleep(10)
        # self.send_keys((By.XPATH,tbjpy.card_personid),tbjdata.input_value)
        # self.send_keys((By.XPATH,tbjpy.card_name),tbjdata.full_name_value)

    #添加中国银行银行卡
    def add_bank_card(self):
        self.click_button((By.XPATH, tbjpy.choose_bank))
        self.click_button((By.XPATH, tbjpy.choose_one_bank))

    #输入银行卡号
    def send_bank_card(self):
        # self.send_keys((By.XPATH,tbjpy.bank_id),tbjdata.card)
        pass

    #输入手机号并绑定
    def send_phone_num(self):
        # self.send_keys((By.XPATH,tbjpy.iphone_num),tbjdata.phone)
        pass

    def bind(self):
        #绑定
        self.click_button((By.XPATH, tbjpy.binding))

    #输入验证码
    # def send_verify_code(self):
    #     myms = sql.mysql_connect(sql.db_info)
    #     sleep(7)
    #     # verifycode1=myms.sql_assign_exec("select content from mdp_message WHERE recipients="+ tbjdata.loginid(1) + " ORDER BY create_time DESC LIMIT 1")
    #     verifycode2=re.search('\d{6}', verifycode1)
    #     verifycode3=verifycode2.group(0)

    #输入验证码并点击完成按钮
    def send_verifycode_sure(self):
        sleep(5)
        myms = sql.mysql_connect(sql.db_info)
        sleep(5)
        # verify_code1=myms.sql_assign_exec("select content from mdp_message WHERE recipients="+ tbjdata.loginid(1) + " ORDER BY create_time DESC LIMIT 1")
        # verify_code2=re.search('\d{6}', verify_code1)
        # verify_code3=verify_code2.group(0)
        # self.send_keys((By.ID,tbjpy.verify_input),verify_code3)
        print 2
        self.click_button((By.ID, tbjpy.btn_next))
        self.driver.implicitly_wait(10)

    #校验用户个人信息
    def verify_person_info(self):
        #校验用户个人信息，账户，实名认证，身份认证，投资风格
        # user_name=self.driver.find_element_by_id(tbjpy.user_name).text
        # a=self.assertEqual(tbjdata.user_namestr,user_name,'error')
        # print a
        # full_name=self.driver.find_element_by_id(tbjpy.full_name).text
        # b=self.assertEqual(tbjdata.full_namestr,full_name,'error')
        # print b
        # id_card=self.driver.find_element_by_id(tbjpy.id_card).text
        # c=self.assertEqual(tbjdata.id_cardstr,id_card,'error')
        # print c
        # level_value=self.driver.find_element_by_id(tbjpy.tv_risk_level_value).text
        # d=self.assertEqual(tbjdata.level_valuestr,level_value,'error')
        # print d
        # self.click_button((By.ID,tbjpy.back2))
        pass

    #普通产品购买流程(除新手，铜宝之外的产品)
    def normal_product(self,amount,trade_num,expect=True,ending=None):
        actual=None
        code=111
        try:
            sleep(6)
            self.send_buy_money(amount)
            self.screenshot()
            self.send_buy_monkey_sure()
            sleep(4)
            # if self.isElement("id",tbjpy.key)==False:
            #     print 3335
            #     self.screenshot()
            #     print 4445
            #     self.click_button((By.XPATH,tbjpy.balance_cancel))
            #     print 5556
            #     self.back()
            #     # self.back()
            #     e='失败'
            #     actual=False
            # else:
                # print 223
            self.send_trade_pwd(trade_num)
            self.click_sure()
            sleep(5)
            if self.isElement("xpath", tbjpy.check_buy_success_btn)==True:
                # print 1111
                self.screenshot()
                actual=True
                e='购买成功'
                self.click_button((By.XPATH, tbjpy.check_buy_success_btn))
                if self.isElement("id", tbjpy.hot_product_name42)==True:
                    pass
                else:
                    self.back()
                    # print 2212
                        # self.back()
            elif self.isElement("id", tbjpy.cancel_item)==True:
                #print 445
                #self.screenshot_Error()
                #print '该产品暂不支持购买！'
                self.screenshot()
                actual=True
                e='购买成功'
                self.click_button((By.ID, tbjpy.cancel_item))
                self.click_button((By.XPATH, tbjpy.check_buy_success_btn))
                if self.isElement("id", tbjpy.hot_product_name42)==True:
                    pass
                else:
                    self.back()
                        # self.back()
            else:
                self.screenshot()
                actual=False
                e='购买失败'
        except Exception,e:
            actual=False
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #新手产品购买流程
    def new_people_product(self,trade_num,expect=True,ending=None):
        actual=None
        code=111
        try:
            sleep(4)
            self.newpeople_buy_commit()
            self.screenshot()
            # print 222
            sleep(4)
            self.send_trade_pwd(trade_num)
            self.click_sure()
            sleep(6)
            if self.isElement("xpath", tbjpy.check_buy_success_btn)==True:
                # print 221111
                self.screenshot()
                actual=True
                e='购买成功'
                self.click_button((By.XPATH, tbjpy.check_buy_success_btn))
                if self.isElement("id", tbjpy.hot_product_name42)==True:
                    pass
                else:
                    self.back()
            elif self.isElement("id", tbjpy.cancel_item)==True:
                self.screenshot()
                actual=True
                e='购买成功'
                self.click_button((By.ID, tbjpy.cancel_item))
                self.click_button((By.XPATH, tbjpy.check_buy_success_btn))
                if self.isElement("id", tbjpy.hot_product_name42)==True:
                    pass
                else:
                    self.back()
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #铜宝转入流程
    def tongbaoin(self,amount,trade_num,expect=True,ending=None):
        actual=None
        code=111
        try:
            self.tongbao_in()
            self.driver.implicitly_wait(10)
            self.send_buy_money(amount)
            self.send_buy_monkey_sure()
            sleep(4)
            self.send_trade_pwd(trade_num)
            self.click_sure()
            sleep(10)
            if self.isElement("id", tbjpy.cancel_item)==True:
                # print 2211
                self.screenshot()
                actual=True
                e='铜宝转入成功'
                self.click_button((By.ID, tbjpy.cancel_item))
                self.click_button((By.XPATH, tbjpy.check_buy_success_btn))
                if self.isElement("id", tbjpy.hot_product_name42)==True:
                    pass
                else:
                    self.back()
            elif self.isElement("xpath", tbjpy.check_buy_success_btn)==True:
                #print 1
                #self.screenshot_True()
                self.screenshot()
                actual=True
                e='铜宝转入成功'
                self.click_button((By.XPATH, tbjpy.check_buy_success_btn))
                self.back()
            else:
                # print 2
                self.screenshot()
                #self.screenshot_Error()
                actual=False
                e='铜宝转入失败'
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #覆盖安装功能
    def test_install(self):
        self.driver.implicitly_wait(10)
        #self.driver.shake()
        #覆盖安装，所要覆盖安装的apk的路径
        os.system("adb install -r  D:\\apk\\TBJ_android_APP_GDT_FEED2.apk")
        #os.system("adb install -r  D:\\apk\\TBJ_4.2.0_109_0720_2305.apk")
        sleep(3)
        check_install_successs=os.popen("adb install -r  D:\\apk\\TBJ_android_APP_GDT_FEED2.apk").read().strip()
        sleep(2)
        success="Success"
        if re.search(success, check_install_successs) !=None:
        #if re.match(success, check) !=None:
            print u'强制覆盖安装成功！'
        else:
            print u'因为apk包签名不同或者版本低于当前版本等其他原因，所以放弃强制安装！'

    #理财产品页面
    def finance_layout(self):
        x=self.driver.get_window_size()['width']
        finance_up=self.driver.find_element_by_id(tbjpy.financing_up).location
        finance_up_location_y=finance_up['y']
        finance_up_y=finance_up_location_y
        finance_down=self.driver.find_element_by_xpath(tbjpy.financing_down).location
        finance_down_location_y=finance_down['y']
        finance_down_size=self.driver.find_element_by_xpath(tbjpy.financing_down).size
        finance_down_size_y=finance_down_size['height']
        finance_down_y=finance_down_location_y+finance_down_size_y
        location=self.driver.find_element_by_xpath('//android.widget.FrameLayout/android.widget.LinearLayout[@index=0]').size
        location_y=location['height']-1
        menu_default_y=self.driver.find_element_by_id(tbjpy.menu_default).location['y']
        menu_default_height=self.driver.find_element_by_id(tbjpy.menu_default).size['height']
        menu_default_y2=menu_default_y+menu_default_height+1
        print menu_default_y2,location_y

    def click_login51(self):
        self.click_button((By.ID, tbjpy.click_login51))

    def setting51(self):
        self.click_button((By.ID, tbjpy.set51))

    #4.2版本信息中心滑动
    def message_slide(self,expect):
        code=11
        self.click_button((By.ID, tbjpy.message))
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        sleep(4)
        server_table=self.driver.find_element_by_xpath(tbjpy.server_table).location
        server_table_y=server_table['y']
        server_table_size=self.driver.find_element_by_xpath(tbjpy.server_table).size
        server_table_size_y=server_table_size['height']
        server_table_size_y=server_table_y+server_table_size_y
        sleep(2)
        message_bottom_tab=self.driver.find_element_by_id(tbjpy.message_bottom).location
        message_bottom_tab_y=message_bottom_tab['y']
        message_time=self.driver.find_elements_by_id(tbjpy.message_time)[0].get_attribute("text")
        #print message_time
        try:
            self.screenshot()
            self.driver.swipe(x/2,server_table_size_y+1,x/2,message_bottom_tab_y-1,5000)
            message_time2=self.driver.find_elements_by_id(tbjpy.message_time)[0].get_attribute("text")
            self.screenshot()
            while message_time!=message_time2:
                self.driver.swipe(x/2,server_table_size_y+1,x/2,message_bottom_tab_y-1,5000)
                message_time=message_time2
                message_time2=self.driver.find_elements_by_id(tbjpy.message_time)[0].get_attribute("text")
                #self.screenshot()
                actual=True
                e='success'
            self.screenshot()
            self.back()
        except Exception,e:
            self.screenshot()
            actual=False
            e='fail'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending


    #4.2查看交易记录滑动
    def check_all_trade_record(self,expect):
        code=11
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        #print x,y
        try:
            self.click_button((By.XPATH, tbjpy.trade_record))
            self.screenshot()
            while self.isElement("id", tbjpy.trade_record_footer)==False:
                self.driver.swipe(x/2,y-1,x/2,0,3000)
                #self.screenshot()
                actual=True
                e='success'
            self.screenshot()
            self.back()
        except Exception,e:
            actual=True
            e='fail'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.3查看交易记录滑动
    def check_all_trade_record43(self,expect):
        code=11
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        #print x,y
        try:
            self.click_button((By.ID, tbjpy.trade_record43))
            self.screenshot()
            while self.isElement("id", tbjpy.trade_record_footer)==False:
                self.driver.swipe(x/2,y-1,x/2,0,3000)
                self.screenshot()
                actual=True
                e='success'
            self.back()
        except Exception,e:
            self.back()
            actual=True
            e='success'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.2查看当前收益
    def now_income(self,expect):
        code=11
        self.click_button((By.ID, tbjpy.now_income))
        #print product_name
        try:
            x=self.driver.get_window_size()['width']
            y=self.driver.get_window_size()['height']
            #print x,y
            sleep(2)
            if self.isElement("xpath", tbjpy.not_hold_nowincome)==True:
                # print 3333
                self.screenshot()
                self.back()
                actual=True
                e='success'
            else:
                server_table=self.driver.find_element_by_xpath(tbjpy.server_table).location
                server_table_y=server_table['y']
                server_table_size=self.driver.find_element_by_xpath(tbjpy.server_table).size
                server_table_size_y=server_table_size['height']
                server_table_size_y=server_table_y+server_table_size_y
                sleep(2)
                product_name=self.driver.find_elements_by_id(tbjpy.product_name)[0].get_attribute("text")
                self.screenshot()
                self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
                product_name2=self.driver.find_elements_by_id(tbjpy.product_name)[0].get_attribute("text")
                self.screenshot()
                while product_name!=product_name2:
                    self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
                    product_name=product_name2
                    product_name2=self.driver.find_elements_by_id(tbjpy.product_name)[0].get_attribute("text")
                    self.screenshot()
                    actual=True
                    e='success'
                self.screenshot()
                self.back()
        except Exception,e:
            self.screenshot()
            self.back()
            actual=True
            e='success'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.3查看当前收益
    def now_income43(self,expect):
        code=11
        self.click_button((By.ID, tbjpy.now_income43))
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        # print x,y
        sleep(2)
        #print product_name
        try:
            if self.isElement("xpath", tbjpy.not_hold_nowincome)==True:
                # print 3333
                self.screenshot()
                self.back()
                actual=True
                e='success'
            else:
                server_table=self.driver.find_element_by_xpath(tbjpy.server_table).location
                server_table_y=server_table['y']
                server_table_size=self.driver.find_element_by_xpath(tbjpy.server_table).size
                server_table_size_y=server_table_size['height']
                server_table_size_y=server_table_y+server_table_size_y
                sleep(2)
                product_name=self.driver.find_elements_by_id(tbjpy.product_time43)[0].get_attribute("text")
                self.screenshot()
                self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
                product_name2=self.driver.find_elements_by_id(tbjpy.product_time43)[0].get_attribute("text")
                self.screenshot()
                while product_name!=product_name2:
                    self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
                    sleep(4)
                    product_name=product_name2
                    product_name2=self.driver.find_elements_by_id(tbjpy.product_name)[0].get_attribute("text")
                    # self.screenshot()
                    actual=True
                    e='success'
                    # self.back()
                self.screenshot()
                self.back()
        except Exception,e:
            #print 2
            self.screenshot()
            self.back()
            actual=True
            e='success'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.2查看铜宝累计收益
    def check_tongbao_income(self,expect):
        code=11
        self.click_button((By.ID, tbjpy.tongbao_assets_layout42))
        self.click_button((By.XPATH, tbjpy.tongbao_income))
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        print x,y
        sleep(2)
        server_table=self.driver.find_element_by_xpath(tbjpy.server_table).location
        server_table_y=server_table['y']
        server_table_size=self.driver.find_element_by_xpath(tbjpy.server_table).size
        server_table_size_y=server_table_size['height']
        server_table_size_y=server_table_y+server_table_size_y
        sleep(2)
        tongbao_time=self.driver.find_elements_by_id(tbjpy.tongbao_time)[0].get_attribute("text")
        # print product_name
        try:
            self.screenshot()
            self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,1000)
            sleep(2)
            self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,1000)
            tongbao_time2=self.driver.find_elements_by_id(tbjpy.tongbao_time)[0].get_attribute("text")
            self.screenshot()
            while tongbao_time!=tongbao_time2:
                self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
                sleep(2)
                self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
                tongbao_time=tongbao_time2
                tongbao_time2=self.driver.find_elements_by_id(tbjpy.tongbao_time)[0].get_attribute("text")
                actual=True
                e='success'
            self.screenshot()
            self.back()
            self.back()
                #self.back()
        except Exception,e:
            self.screenshot()
            actual=False
            e='fail'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.3查看铜宝累计收益
    def check_tongbao_income43(self,expect):
        code=11
        self.click_button((By.ID, tbjpy.tongbao_assets_layout43))
        self.click_button((By.XPATH, tbjpy.tongbao_income))
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        print x,y
        sleep(4)
        server_table=self.driver.find_element_by_xpath(tbjpy.server_table).location
        server_table_y=server_table['y']
        server_table_size=self.driver.find_element_by_xpath(tbjpy.server_table).size
        server_table_size_y=server_table_size['height']
        server_table_size_y=server_table_y+server_table_size_y
        sleep(2)
        tongbao_time=self.driver.find_elements_by_id(tbjpy.tongbao_time)[0].get_attribute("text")
        #print product_name
        try:
            self.screenshot()
            self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,6000)
            sleep(2)
            self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
            tongbao_time2=self.driver.find_elements_by_id(tbjpy.tongbao_time)[0].get_attribute("text")
            self.screenshot()
            while tongbao_time!=tongbao_time2:
                self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
                sleep(2)
                self.driver.swipe(x/2,y-1,x/2,server_table_size_y+1,5000)
                tongbao_time=tongbao_time2
                tongbao_time2=self.driver.find_elements_by_id(tbjpy.tongbao_time)[0].get_attribute("text")

                actual=True
                e='success'
            self.screenshot()
            self.back()
            self.back()
                #self.back()
        except Exception,e:
            self.screenshot()
            actual=False
            e='fail'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.2我的资产页面产品信息
    def check_myproperty_product(self,expect):
        code=11
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        sleep(2)
        server_table=self.driver.find_element_by_xpath(tbjpy.server_table).location
        server_table_y=server_table['y']
        server_table_size=self.driver.find_element_by_xpath(tbjpy.server_table).size
        server_table_size_y=server_table_size['height']
        server_table_size_y=server_table_y+server_table_size_y
        myproperty_bottom_tab=self.driver.find_element_by_id(tbjpy.myproperty_bottom_tab).location
        myproperty_bottom_tab_y=myproperty_bottom_tab['y']
        sleep(2)
        myproperty_product_name=self.driver.find_elements_by_id(tbjpy.myproperty_product_name)[0].get_attribute("text")
        #print myproperty_product_name
        #print product_name
        try:
            self.screenshot()
            #print 22
            products=self.driver.find_elements_by_id(tbjpy.myproperty_bottom_amount)
            for product in products:
                product.click()
                # self.screenshot()
                self.back()
            #self.screenshot()
            #self.driver.swipe(x/2,myproperty_bottom_tab_y-1,x/2,server_table_size_y+1,3000)
            self.driver.swipe(x/2,myproperty_bottom_tab_y-2,x/2,server_table_size_y+1,1000)
            #print 33
            myproperty_product_name2=self.driver.find_elements_by_id(tbjpy.tongbao_time)[0].get_attribute("text")
            #self.screenshot()
            #print 33,myproperty_bottom_tab_y,server_table_size_y,myproperty_product_name2,myproperty_product_name
            #print myproperty_product_name!=myproperty_product_name2
            while myproperty_product_name!=myproperty_product_name2:
                #print 44
                products=self.driver.find_elements_by_id(tbjpy.myproperty_bottom_amount)
                for product in products:
                    product.click()
                    # self.screenshot()
                    self.back()
                self.driver.swipe(x/2,myproperty_bottom_tab_y-2,x/2,server_table_size_y+1,1000)
                sleep(5)
                myproperty_product_name=myproperty_product_name2
                myproperty_product_name2=self.driver.find_elements_by_id(tbjpy.myproperty_product_name)[0].get_attribute("text")
                self.screenshot()
                #print myproperty_product_name,myproperty_product_name2
                actual=True
                e='success'
        except Exception,e:
            self.screenshot()
            actual=False
            e='fail'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #4.3我的投资查看
    def my_investment_slide43(self,expect):
        code=11
        self.click_button((By.ID, tbjpy.my_investment43))
        try:
            if self.isElement("id", tbjpy.investment_view_header)==False:
                # print 333
                self.screenshot()
                self.back()
                actual=True
                e='success'
            else:
                x=self.driver.get_window_size()['width']
                y=self.driver.get_window_size()['height']
                sleep(3)
                investment_view_header=self.driver.find_element_by_id(tbjpy.investment_view_header).location
                investment_view_header_y=investment_view_header['y']
                investment_view_header_size=self.driver.find_element_by_id(tbjpy.investment_view_header).size
                investment_view_header_size_y=investment_view_header_size['height']
                investment_view_y=investment_view_header_y+investment_view_header_size_y
                sleep(2)
                #print 55
                myproperty_product_name=self.driver.find_elements_by_id(tbjpy.myproperty_product_name)[0].get_attribute("text")
                print investment_view_header_y,investment_view_header_size_y,investment_view_y
            # try:
                #print 22
                products=self.driver.find_elements_by_id(tbjpy.myproperty_bottom_amount)
                #print 44
                for product in products:
                    product.click()
                    # self.screenshot()
                    self.back()
                self.driver.swipe(x/2,y-1,x/2,investment_view_header_size_y+1,1000)
                myproperty_product_name2=self.driver.find_elements_by_id(tbjpy.tongbao_time)[0].get_attribute("text")
                while myproperty_product_name!=myproperty_product_name2:
                    #print 444
                    products=self.driver.find_elements_by_id(tbjpy.myproperty_bottom_amount)
                    print products
                    sleep(2)
                    # for product in products:
                    #     product.click()
                    #     self.screenshot()
                    #     self.back()

                    sleep(5)
                    #print 444
                    myproperty_product_name=myproperty_product_name2
                    myproperty_product_name2=self.driver.find_elements_by_id(tbjpy.myproperty_product_name)[0].get_attribute("text")
                    self.driver.swipe(x/2,y-1,x/2,investment_view_header_size_y+1,1000)
                    actual=True
                    e='success'
                self.screenshot()
                self.back()
        except Exception,e:
                self.screenshot()
                self.back()
                actual=True
                e='fail'
        finally:
                result=str(actual)==str(expect)
                ending={'code':code,'message':e,'result':result}
                return ending

    #5.0转让市场购买
    def buy_transfer(self,trade_num,expect=True,ending=None):
        actual=None
        code=111
        try:
            sleep(5)
            #print 3333
            self.click_button((By.ID, tbjpy.transfer_buy))
            if self.isElement("xpath", tbjpy.Bond_dialog_message)==True:
                self.screenshot()
                self.click_button((By.ID, tbjpy.click_sure))
                self.back()
                # self.back()
                actual=False
                e='失败'
            else:
                sleep(3)
                self.transfer_market_pay()
                print 555
                self.send_trade_pwd(trade_num)
                self.click_sure()
                sleep(6)
                if self.isElement("xpath", tbjpy.check_newbuy_success_btn)==True:
                    self.screenshot_True()
                    actual=True
                    e='购买成功'
                    self.click_button((By.XPATH, tbjpy.check_buy_success_btn))
                    if self.isElement("id", tbjpy.hot_product_name42)==True:
                        pass
                    else:
                        self.back()
                        print 2212
                        # self.back()
                elif self.isElement("id", tbjpy.cancel_item)==True:
                #print 445
                #self.screenshot_Error()
                #print '该产品暂不支持购买！'
                    self.screenshot()
                    actual=True
                    e='购买成功'
                    self.click_button((By.ID, tbjpy.cancel_item))
                    self.click_button((By.XPATH, tbjpy.check_buy_success_btn))
                    if self.isElement("id", tbjpy.hot_product_name42)==True:
                        pass
                    else:
                        self.back()
                        # self.back()
                else:
                    self.screenshot()
                    actual=False
                    e='购买失败'
        except Exception,e:
            actual=False
        finally:
            result=str(e)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    #5.2预约专区购买
    def buy_order(self,amount3,recharge_num,trade_num,expect=True,ending=None):
        actual=None
        code=111
        # try:
        sleep(5)
        self.click_button((By.ID, tbjpy.product_purchase_view))
        if self.isElement("xpath", tbjpy.sale_on_time)==True:
                # print 33211
            self.screenshot()
            self.click_button((By.ID, tbjpy.click_sure))
            print 1
            self.back()
                # actual=True
            print 2
        elif self.isElement("xpath", tbjpy.Bond_dialog_message)==True:
            self.screenshot()
            self.click_button((By.ID, tbjpy.click_sure))
            self.back()
            print 6
            actual=True
                # self.back()
                # actual=False
                # e='失败'
            # elif self.isElement("xpath",tbjpy.sale_on_time)==True:
            #     # print 33211
            #     self.screenshot()
            #     self.click_button((By.ID,tbjpy.click_sure))
            #     print 1
            #     self.back()
            #     # actual=True
            #     print 2
        else:
            sleep(3)
            self.send_buy_money(amount3)
            self.screenshot()
            self.send_buy_monkey_sure()
            print 5556
            self.send_trade_pwd(trade_num)
            self.click_sure()
            sleep(6)
            if self.isElement("xpath", tbjpy.supple_tongbao)==True:
                print 2
                self.screenshot()
                self.click_button((By.XPATH, tbjpy.supple_tongbao))
                self.tongbaoin(recharge_num,trade_num)
                self.back()
            elif self.isElement("xpath", tbjpy.check_newbuy_success_btn)==True:
                print 3
                self.screenshot_True()
                actual=True
                e='购买成功'
                self.click_button((By.XPATH, tbjpy.check_buy_success_btn))
                if self.isElement("id", tbjpy.hot_product_name42)==True:
                    pass
                else:
                    self.back()
                    print 2212
                        # self.back()
            elif self.isElement("id", tbjpy.cancel_item)==True:
                self.screenshot()
                actual=True
                e='购买成功'
                self.click_button((By.ID, tbjpy.cancel_item))
                self.click_button((By.XPATH, tbjpy.check_buy_success_btn))
                if self.isElement("id", tbjpy.hot_product_name42)==True:
                    pass
                else:
                    self.back()
                        # self.back()
            else:
                self.screenshot()
                actual=False
                e='购买失败'
            actual=True
        # except Exception,e:
        #     actual=False
        # finally:
        #     result=str(actual)==str(expect)
        #     ending={'code':code,'message':e,'result':result}
        #     return ending


    #4.2理财购买
    def buy_financing_products42(self,amount2,amount3,trade_num,expect):
        code=11
        # print 11
        x=self.driver.get_window_size()['width']
        server_table=self.driver.find_element_by_xpath(tbjpy.server_table).location
        server_table_y=server_table['y']
        server_table_size=self.driver.find_element_by_xpath(tbjpy.server_table).size
        server_table_size_y=server_table_size['height']
        server_table_size_y=server_table_y+server_table_size_y
        myproperty_bottom_tab=self.driver.find_element_by_id(tbjpy.myproperty_bottom_tab).location
        myproperty_bottom_tab_y=myproperty_bottom_tab['y']
        # print server_table_size_y,myproperty_bottom_tab_y
        financing_name42=self.driver.find_elements_by_id(tbjpy.financing_name42)[0].get_attribute("text")
        products=self.driver.find_elements_by_id(tbjpy.financing_name42)
        try:
            for product in products:
                product.click()
                financing_title=self.driver.find_element_by_id(tbjpy.financing_title).get_attribute("text")
                self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                sleep(3)
                if self.isElement("id", tbjpy.product_purchase_view)==True:
                    #self.click_button((By.ID,tbjpy.click_sure))
                    # print 334
                    self.screenshot()
                    self.back()
                elif self.isElement("xpath", tbjpy.dialog_message)==True:
                    self.click_button((By.ID, tbjpy.click_sure))
                    self.back()
                elif self.isElement("xpath", tbjpy.identity_card)==True:
                    # print 11
                    self.back()
                elif re.findall(u"新手",financing_title)!=[]:
                    # print 1
                    self.new_people_product(trade_num,expect)
                #铜宝转入
                elif re.findall(u"铜宝",financing_title)!=[]:
                    # print 2
                    self.tongbaoin(amount2,trade_num,expect)
                else:
                    # print 3
                    self.normal_product(amount3,trade_num,expect)
            # self.driver.swipe(x/2,myproperty_bottom_tab_y-2,x/2,server_table_size_y+1,5000)
        # try:
        #     financing_name422=self.driver.find_elements_by_id(tbjpy.financing_name42)[0].get_attribute("text")
        #     print 33
        #     self.screenshot()
        #     while financing_name42!=financing_name422:
        #     # while self.isElement("xpath",tbjpy.long_time_seal)==False:
        #         print 44
        #         sleep(5)
        #         for product in products:
        #             product.click()
        #             financing_title=self.driver.find_element_by_id(tbjpy.financing_title).get_attribute("text")
        #             self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
        #             if self.isElement("id",tbjpy.product_purchase_view)==True:
        #                 #self.click_button((By.ID,tbjpy.click_sure))
        #                 print 334
        #                 self.screenshot()
        #                 self.back()
        #             elif self.isElement("xpath",tbjpy.dialog_message)==True:
        #                 self.click_button((By.ID,tbjpy.click_sure))
        #                 self.back()
        #             elif self.isElement("xpath",tbjpy.identity_card)==True:
        #                 print 11
        #                 self.back()
        #             elif re.findall(u"新手",financing_title)!=[]:
        #                 print 1
        #                 self.new_people_product(trade_num,expect)
        #             #铜宝转入
        #             elif re.findall(u"铜宝",financing_title)!=[]:
        #                 print 2
        #                 self.tongbaoin(amount2,trade_num,expect)
        #             else:
        #                 print 3
        #                 self.normal_product(amount3,trade_num,expect)
        #         financing_name42=financing_name422
        #         financing_name422=self.driver.find_elements_by_id(tbjpy.financing_name42)[0].get_attribute("text")
        #         self.driver.swipe(x/2,myproperty_bottom_tab_y-2,x/2,server_table_size_y+1,1000)
            self.screenshot()
            actual=True
            e='success'
                #self.back()
        except Exception,e:
            self.screenshot()
            actual=False
            e='fail'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending
            pass

    def buy_hot_product51(self,amount2,amount3,trade_num,expect):
        # print 33
        code=11
        x=self.driver.get_window_size()['width']
        banner=self.driver.find_element_by_id(tbjpy.hot_product_name).location
        banner_y=banner['y']
        self.driver.swipe(x/2,0,x/2,banner_y,1000)
        sleep(4)
        try:
            # print 31
            hot_product51_names=self.driver.find_elements_by_id(tbjpy.hot_product_name)
            # print 32
            sleep(3)
            for product in hot_product51_names:
                # print 333
                product.click()
                # print 44
                sleep(3)
                financing_title=self.driver.find_element_by_id(tbjpy.financing_title).get_attribute("text")
                # self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                # print 3333
                if self.isElement("xpath", tbjpy.dialog_message)==True:
                    self.screenshot()
                    self.click_button((By.ID, tbjpy.click_sure))
                    self.back()
                elif self.isElement("xpath", tbjpy.seal_message)==True:
                    self.screenshot()
                    self.click_button((By.ID, tbjpy.click_sure))
                    self.back()
                elif self.isElement("xpath", tbjpy.identity_card)==True:
                    # print 11
                    self.back()
                elif re.findall(u"新手",financing_title)!=[]:
                    # print 1
                    self.new_people_product(trade_num,expect)
                #铜宝转入
                elif re.findall(u"铜宝",financing_title)!=[]:
                    # print 22
                    self.tongbaoin(amount2,trade_num,expect)
                else:
                    # print 3
                    sleep(3)
                    self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                    self.normal_product(amount3,trade_num,expect)
                actual=True
                e='success'
                #self.back()
        except Exception,e:
            self.screenshot()
            actual=False
            e='fail'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending

    def buy_financing_products51(self,amount2,amount3,trade_num,expect):
        code=11
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        self.screenshot()
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        product_form51s=self.driver.find_elements_by_id(tbjpy.product_form51)
        finance_lable_default=self.driver.find_element_by_xpath(tbjpy.finance_lable).location
        finance_lable_default_y=finance_lable_default['y']
        finance_lable_default_size=self.driver.find_element_by_xpath(tbjpy.finance_lable).size
        finance_lable_default_size_y=finance_lable_default_size['height']
        finance_lable_size_y=finance_lable_default_y+finance_lable_default_size_y
        tongbao_52_default=self.driver.find_element_by_id(tbjpy.tongbao_52).location
        tongbao_52_default_y=tongbao_52_default['y']
        tongbao_52_default_size=self.driver.find_element_by_id(tbjpy.tongbao_52).size
        tongbao_52_default_size_y=tongbao_52_default_size['height']
        tongbao_52_size_y=tongbao_52_default_y+tongbao_52_default_size_y
        product_form51s=self.driver.find_elements_by_id(tbjpy.product_form51)
        try:
            financing_name=self.driver.find_element_by_id("com.tongbanjie.android:id/tv_name").get_attribute("text")
            print financing_name
            for product_form51 in product_form51s[3:4]:
                self.driver.swipe(x/2,tongbao_52_size_y+1,x/2,finance_lable_size_y+1,1000)
                # print 11
                if re.findall(u"产品",financing_name)!=[]:
                    # print 22
                    pass
                else:
                    # print 33
                    self.screenshot()
                    product_form51.click()
                    financing_text=self.driver.find_element_by_id(tbjpy.financing_text).get_attribute("text")
                    sleep(3)
                    product_name51s=self.driver.find_elements_by_id(tbjpy.product_name51)
                    sleep(2)
                    # print 22
                    if self.isElement("xpath", tbjpy.shelf_empty)==True:
                        self.screenshot()
                        self.back()
                    elif re.findall(u"产品",financing_name)!=[]:
                        sleep(3)
                        self.driver.tap([(200, 100)])
                        # print 22
                        # pass
                    elif self.isElement("xpath", tbjpy.product_advance_notice)==True:
                        # print 3344
                        self.screenshot()
                        self.click_button((By.XPATH, tbjpy.product_advance_notice_back))
                        # pass
                    elif re.findall(u"转让专区",financing_text)!=[]:
                        # print 113
                        self.screenshot()
                        for product_name in product_name51s:
                            self.screenshot()
                            product_name.click()
                            self.buy_transfer(trade_num,expect)
                        self.back()
                    elif self.isElement("xpath", tbjpy.terminal_title)==True:
                        # print 333
                        sleep(3)
                        sort_menu_default=self.driver.find_element_by_id(tbjpy.sort_menu_default).location
                        sort_menu_default_y=sort_menu_default['y']
                        # print 33
                        sort_menu_default_size=self.driver.find_element_by_id(tbjpy.sort_menu_default).size
                        sort_menu_default_size_y=sort_menu_default_size['height']
                        # print 44
                        sort_menu_default_size_y=sort_menu_default_y+sort_menu_default_size_y
                        # print sort_menu_default_y,sort_menu_default_size_y,sort_menu_default_size_y
                        for product_name in product_name51s:
                            # print 112
                            product_name.click()
                            financing_title=self.driver.find_element_by_id(tbjpy.financing_title).get_attribute("text")
                            self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                            sleep(3)
                            #print 3333
                            if self.isElement("id", tbjpy.product_purchase_view)==True:
                                #print 22
                                self.screenshot()
                                self.back()
                            elif re.findall(u"产品",financing_name)!=[]:
                                self.screenshot()
                                self.driver.tap([(200, 100)])
                                # print 22
                                # pass
                            elif self.isElement("xpath", tbjpy.sale_on_time)==True:
                                self.screenshot()
                                self.click_button((By.ID, tbjpy.click_sure))
                                self.back()
                            elif self.isElement("xpath", tbjpy.dialog_message)==True:
                                self.screenshot()
                                self.click_button((By.ID, tbjpy.click_sure))
                                self.back()
                            elif self.isElement("xpath", tbjpy.seal_message)==True:
                                self.screenshot()
                                self.click_button((By.ID, tbjpy.click_sure))
                                self.back()
                            elif self.isElement("xpath", tbjpy.identity_card)==True:
                                #print 11self.screenshot()
                                self.screenshot()
                                self.back()
                            elif re.findall(u"新手",financing_title)!=[]:
                                #print 1
                                self.screenshot()
                                # self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                                self.new_people_product(trade_num,expect)
                            # #铜宝转入
                            # elif re.findall(u"铜宝",financing_title)!=[]:
                            #     print 2
                            #     self.tongbaoin(amount2,trade_num,expect)
                            #转让市场
                            # elif re.findall(u"转让",financing_title)!=[]:
                            #     print 22
                            #     self.buy_transfer(trade_num,expect)
                            elif re.findall(u"转让专区",financing_text)!=[]:
                                for product_name in product_name51s:
                                    self.screenshot()
                                    product_name.click()
                                    self.buy_transfer(trade_num,expect)
                                self.back()
                            else:
                                # print 3
                                # self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                                sleep(3)
                                self.normal_product(amount3,trade_num,expect)
                        actual=True
                        e='success'
                        self.back()
                    else:
                        for product_name in product_name51s:
                            # print 111
                            product_name.click()
                            financing_title=self.driver.find_element_by_id(tbjpy.financing_title).get_attribute("text")
                            self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                            sleep(4)
                            #print 3333
                            if self.isElement("id", tbjpy.product_purchase_view)==True:
                                # print 221
                                self.screenshot()
                                self.back()
                            elif self.isElement("xpath", tbjpy.dialog_message)==True:
                                self.screenshot()
                                self.click_button((By.ID, tbjpy.click_sure))
                                self.back()
                            elif self.isElement("xpath", tbjpy.sale_on_time)==True:
                                self.screenshot()
                                self.click_button((By.ID, tbjpy.click_sure))
                                self.back()
                            elif self.isElement("xpath", tbjpy.identity_card)==True:
                                # print 112
                                self.back()
                            elif re.findall(u"新手",financing_title)!=[]:
                                # print 13
                                # self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                                self.new_people_product(trade_num,expect)
                            else:
                                # print 3
                                # self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                                self.normal_product(amount3,trade_num,expect)
                        # print 222
                        sleep(3)
                        self.back()
                        actual=True
                        e='success'
                        # print 333
                        pass
            # print 33333
            actual=True
            e='success'
        except Exception,e:
            self.screenshot()
            actual=False
            e='fail'
        finally:
            result=str(actual)==str(expect)
            ending={'code':code,'message':e,'result':result}
            return ending
        pass

    def buy_financing_products52(self,amount2,amount3,recharge_num,trade_num,expect):
        code=11
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        self.screenshot()
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        product_form51s=self.driver.find_elements_by_id(tbjpy.product_form51)
        finance_lable_default=self.driver.find_element_by_xpath(tbjpy.finance_lable).location
        finance_lable_default_y=finance_lable_default['y']
        finance_lable_default_size=self.driver.find_element_by_xpath(tbjpy.finance_lable).size
        finance_lable_default_size_y=finance_lable_default_size['height']
        finance_lable_size_y=finance_lable_default_y+finance_lable_default_size_y
        tongbao_52_default=self.driver.find_element_by_id(tbjpy.tongbao_52).location
        tongbao_52_default_y=tongbao_52_default['y']
        tongbao_52_default_size=self.driver.find_element_by_id(tbjpy.tongbao_52).size
        tongbao_52_default_size_y=tongbao_52_default_size['height']
        tongbao_52_size_y=tongbao_52_default_y+tongbao_52_default_size_y
        product_form51s=self.driver.find_elements_by_id(tbjpy.product_form51)
        try:
            financing_name=self.driver.find_element_by_id("com.tongbanjie.android:id/tv_name").get_attribute("text")
            print financing_name
            for product_form51 in product_form51s[:4]:
                self.driver.swipe(x/2,tongbao_52_size_y+1,x/2,finance_lable_size_y+1,1000)
                # print 11
                #self.click_button((By.XPATH,"//android.widget.TextView[@text='产品预告']"))
                if re.findall(u"产品",financing_name)!=[]:
                    # print 22
                    pass
                else:
                    # print 33
                    self.screenshot()
                    product_form51.click()
                    financing_text=self.driver.find_element_by_id(tbjpy.financing_text).get_attribute("text")
                    sleep(3)
                    product_name51s=self.driver.find_elements_by_id(tbjpy.product_name51)
                    sleep(2)
                    # print 22
                    if self.isElement("xpath", tbjpy.shelf_empty)==True:
                        self.screenshot()
                        self.back()
                    elif self.isElement("xpath", tbjpy.product_advance_notice)==True:
                        # print 3344
                        self.screenshot()
                        self.click_button((By.XPATH, tbjpy.product_advance_notice_back))
                        # pass
                    elif re.findall(u"转让专区",financing_text)!=[]:
                        for product_name in product_name51s[0:1]:
                            product_name.click()
                            self.buy_transfer(trade_num,expect)
                        self.back()
                    elif re.findall(u"预约专区",financing_text)!=[]:
                        for product_name in product_name51s:
                            # print 3345,product_name51s
                            product_name.click()
                            self.buy_order(amount3,recharge_num,trade_num,expect)
                        # print 223
                        self.back()
                        # print 3332
                    elif self.isElement("xpath", tbjpy.terminal_title)==True:
                        # print 333
                        sleep(3)
                        sort_menu_default=self.driver.find_element_by_id(tbjpy.sort_menu_default).location
                        sort_menu_default_y=sort_menu_default['y']
                        # print 33
                        sort_menu_default_size=self.driver.find_element_by_id(tbjpy.sort_menu_default).size
                        sort_menu_default_size_y=sort_menu_default_size['height']
                        # print 44
                        sort_menu_default_size_y=sort_menu_default_y+sort_menu_default_size_y
                        # print sort_menu_default_y,sort_menu_default_size_y,sort_menu_default_size_y
                        for product_name in product_name51s:
                            #print 111
                            product_name.click()
                            financing_title=self.driver.find_element_by_id(tbjpy.financing_title).get_attribute("text")
                            self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                            sleep(3)
                            #print 3333
                            if self.isElement("id", tbjpy.product_purchase_view)==True:
                                #print 22
                                self.screenshot()
                                self.back()
                            elif self.isElement("xpath", tbjpy.sale_on_time)==True:
                                self.screenshot()
                                self.click_button((By.ID, tbjpy.click_sure))
                                self.back()
                            elif self.isElement("xpath", tbjpy.dialog_message)==True:
                                self.screenshot()
                                self.click_button((By.ID, tbjpy.click_sure))
                                self.back()
                            elif self.isElement("xpath", tbjpy.seal_message)==True:
                                self.screenshot()
                                self.click_button((By.ID, tbjpy.click_sure))
                                self.back()
                            elif self.isElement("xpath", tbjpy.identity_card)==True:
                                #print 11self.screenshot()
                                self.screenshot()
                                self.back()
                            elif re.findall(u"新手",financing_title)!=[]:
                                #print 1
                                self.screenshot()
                                # self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                                self.new_people_product(trade_num,expect)
                            # #铜宝转入
                            # elif re.findall(u"铜宝",financing_title)!=[]:
                            #     print 2
                            #     self.tongbaoin(amount2,trade_num,expect)
                            #转让市场
                            # elif re.findall(u"转让",financing_title)!=[]:
                            #     print 22
                            #     self.buy_transfer(trade_num,expect)
                            else:
                                # print 3
                                # self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                                sleep(3)
                                self.normal_product(amount3,trade_num,expect)
                        self.back()
                    else:
                        for product_name in product_name51s:
                            # print 111
                            product_name.click()
                            financing_title=self.driver.find_element_by_id(tbjpy.financing_title).get_attribute("text")
                            self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                            sleep(4)
                            #print 3333
                            if self.isElement("id", tbjpy.product_purchase_view)==True:
                                # print 221
                                self.screenshot()
                                self.back()
                            elif self.isElement("xpath", tbjpy.dialog_message)==True:
                                self.screenshot()
                                self.click_button((By.ID, tbjpy.click_sure))
                                self.back()
                            elif self.isElement("xpath", tbjpy.sale_on_time)==True:
                                self.screenshot()
                                self.click_button((By.ID, tbjpy.click_sure))
                                self.back()
                            elif self.isElement("xpath", tbjpy.identity_card)==True:
                                # print 112
                                self.back()
                            elif re.findall(u"预约专区",financing_text)!=[]:
                                for product_name in product_name51s:
                                    # print 3345
                                    product_name.click()
                                    self.buy_order(amount3,recharge_num,trade_num,expect)
                            elif re.findall(u"新手",financing_title)!=[]:
                                # print 13
                                # self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                                self.new_people_product(trade_num,expect)
                            else:
                                # print 3
                                # self.driver.find_element_by_id(tbjpy.product_purchase_view).click()
                                self.normal_product(amount3,trade_num,expect)
                        # print 222
                        actual=True
                        self.back()
                actual=True
                e='success'
                #self.back()
        except Exception,e:
            print 443
            self.screenshot()
            actual=False
            e='fail'
        finally:
            result=str(actual)==str(expect)
            print result,actual,expect
            ending={'code':code,'message':e,'result':result}
            return ending
        pass

class Data(object):
    def __init__(self):
        #测试帐号
        self.phone_num='13735865796'
        #帐号长度不满11位
        self.phone_num_e1='1373586579'
        #未注册帐号
        self.phone_num_e2='13735865792'
        #拟注册帐号
        self.sign_num='13735865787'
        #测试帐号密码
        self.passwd='654321'
        #密码和帐号不匹配
        self.passwd_e1='123456'
        #密码不满六位
        self.passwd_e2='65432'
        #注册设置的密码
        self.sign_pwd='123456'
        #原登录密码
        self.old_pwd='654321'
        #错误的原登录密码
        self.old_pwd_e1='123456'
        #新置登录密码
        self.set_pwd='654321'
        #重复新登录密码
        self.repeat_pwd='654321'
        #重复新登录密码与新置登录密码不匹配
        self.repeat_pwd_e1='123456'
        #原交易密码
        self.old_trade_pwd='654321'
        #错误的原交易密码
        self.old_trade_pwd_e1='123456'
        #原交易密码位数不够
        self.old_trade_pwd_e2='12345'
        #新交易密码
        self.new_trade_pwd='654321'
        #新交易密码位数不够
        self.new_trade_pwd_e1='65432'
        #重复新置密码
        self.repeat_trade_pwd='654321'
        #重复新置密码位数不够
        self.repeat_trade_pwd_e1='65432'
        #重复新置密码与新置密码不匹配
        self.repeat_trade_pwd_e2='123456'
        #充值金额
        self.topup_num='100'
        #充值金额为空
        self.topup_num_e1=''
        #交易密码
        self.trade_pwd='654321'
        #错误的交易密码
        self.trade_pwd_e='654322'
        #提现金额
        self.out_num='100'
        #充值金额为空
        self.out_num_e1=''
        #铜宝转入金额
        self.tongbaoin_num='100'
        #铜宝转出金额
        self.tongbaoout_num='100'
        #普通产品购买金额
        self.normal_product_num='300'
        self.person_ID=''
        #铜宝充值金额
        self.recharge_num='100'
        pass

if __name__ == '__main__':
    kw = {'deviceName': '', 'autoLaunch': False, 'unicodeKeyboard': True, 'udid': u'f48e92875b1b', 'appPackage': 'com.tongbanjie.android', 'resetKeyboard': True, 'platformName': 'Android', 'appActivity': 'TBJMainFragmentActivity', 'platfromVersion': '4.3'}

    driver = webdriver.Remote('http://%s:%d/wd/hub' % (u'192.168.2.35',4720),kw)
