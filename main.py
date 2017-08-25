# -*- coding:utf-8 -*-
#  Author: Bluef1ash
import sys
import threading
from queue import Queue

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from lxml import etree
from selenium.webdriver import Chrome, ActionChains
from time import sleep
from window import Ui_MainWindow
import os


class Ui_Main(QtWidgets.QWidget, Ui_MainWindow):
    """
    主窗口自定义设置
    """

    def __init__(self):
        super(Ui_Main, self).__init__()
        self.setupUi(self)
        self.formThread = None
        self.queue = None
        self.mainWindow = None

    def setupUi(self, MainWindow):
        super(Ui_Main, self).setupUi(MainWindow)
        self.mainWindow = MainWindow
        self.mainWindow.setMaximumSize(self.mainWindow.width(), self.mainWindow.height())
        self.mainWindow.setMinimumSize(self.mainWindow.width(), self.mainWindow.height())
        self.mainWindow.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.startButton.clicked.connect(self.on_start_button_clicked)

    def on_start_button_clicked(self):
        """
        开始执行按钮单击槽
        :return:
        """
        username = self.username.text()
        password = self.password.text()
        chromeDriver = os.path.dirname(os.path.realpath(__file__)) + "\chromedriver.exe"
        if os.path.exists(chromeDriver):
            if self.editCheckedRadio.isChecked():
                editType = 1
            elif self.editResearchRadio.isChecked():
                editType = 2
            else:
                editType = 0
            if username != "" and password != "" and editType != 0:
                self.queue = Queue()
                self.formThread = FormThread()
                self.formThread.setChromeDriver(chromeDriver)
                self.formThread.setUsername(username)
                self.formThread.setPassword(password)
                self.formThread.setQueue(self.queue)
                self.formThread.setEditType(editType)
                self.formThread.start()
                self.formThread.trigger.connect(self.trigger)
                self.startButton.setText("正在运行")
                self.startButton.setDisabled(True)
                self.mainWindow.showMinimized()
            elif editType == 0:
                QtWidgets.QMessageBox.critical(self, "错误", "必须选择执行动作！")
            else:
                QtWidgets.QMessageBox.critical(self, "错误", "用户名或密码不能为空！")

        else:
            QMessageBox.critical(self, "错误", "Chrome驱动不存在！")

    def trigger(self, types):
        """
        接收业务逻辑线程信号并修改UI
        :param types:
        :return:
        """
        if types == "noSave":
            self.formThread.pause()
            # 处理无法保存项
            question = QMessageBox.question(self, "询问", "修改成功，是否继续？", QMessageBox.Yes | QMessageBox.No)
            self.queue.put(question)
            if question == QMessageBox.No:
                self.formThread.stop()
            else:
                self.formThread.resume()
        elif types == "finish":
            index = self.queue.get()
            QMessageBox.information(self, "恭喜", "恭喜！本次运行共执行" + str(index) + "次")
            self.startButton.setText("开始运行")
            self.startButton.setDisabled(False)
            self.mainWindow.showNormal()
            self.mainWindow.activateWindow()
        elif types == "noList":
            QMessageBox.information(self, "恭喜", "并没有需要修改的条目")


class FormThread(QThread):
    """
    业务逻辑线程
    """
    trigger = pyqtSignal(str)

    def __init__(self):
        super(FormThread, self).__init__()
        self.__chromeDriver = None
        self.__chrome = None
        self.__username = None
        self.__password = None
        self.__queue = None
        self.__editType = None
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False

    def setChromeDriver(self, chromeDriver):
        self.__chromeDriver = chromeDriver

    def setUsername(self, username):
        self.__username = username

    def setPassword(self, password):
        self.__password = password

    def setQueue(self, queue):
        self.__queue = queue

    def setEditType(self, editType):
        self.__editType = editType

    def run(self):
        """
        启动函数
        为“山东省残疾人基本服务状况和需求信息数据动态更新系统”自动填表专门制作，使用前安装Chrome浏览器并下载驱动
        :return:
        """
        os.environ["webdriver.chrome.driver"] = self.__chromeDriver  # "./chromedriver.exe"
        self.__chrome = Chrome(self.__chromeDriver)
        # 窗口最大化，可有可无，看情况
        self.__chrome.maximize_window()
        # 打开网址
        self.__chrome.get("http://dtgx.sddpf.org.cn/dtgx2017/a/login")
        # 输入账户密码
        self.__chrome.find_element_by_id('username').clear()
        self.__chrome.find_element_by_id("username").send_keys(self.__username)
        self.__chrome.find_element_by_id('password').clear()
        self.__chrome.find_element_by_id('password').send_keys(self.__password)
        # 输入完用户密码当然就是提交了，通过'name'为login来找到提交按钮
        self.__chrome.find_element_by_xpath('//form[@id="loginForm"]/table//tr/td/input[@type="submit"]').click()
        # 计数器
        i = 1
        if self.__editType == 1:
            while True:
                if self.__editNotChecked():
                    continue
                else:
                    break
        else:
            while True:
                if self.__editResearchType():
                    continue
                else:
                    break

        i += 1
        # 浏览器退出
        self.__chrome.quit()
        self.__queue.put(i)
        self.trigger.emit("finish")

    def __editNotChecked(self):
        """
        更改未验证项
        :return:
        """
        # 打开列表页并查询
        self.__chrome.get("http://dtgx.sddpf.org.cn/dtgx2017/a/dynamicupdate/register/eformityRegister/list")
        self.__chrome.find_element_by_xpath(
            '//form[@id="searchForm"]/ul/li/div[@id="s2id_ext1"]/a[@class="select2-choice"]').click()
        self.__chrome.find_element_by_xpath(
            '//div[@id="select2-drop"]/ul[@class="select2-results"]/li[4]/div[@class="select2-result-label"]').click()
        self.__chrome.find_element_by_xpath('//form[@id="searchForm"]/ul/li/input[@id="btnSubmit"]').click()
        pageSource = etree.HTML(self.__chrome.page_source)
        editLinkXpath = '//table[@id="contentTable"]/tbody/tr[1]/td[last()]/a[1]'
        # 判断是否有需要修改的条目
        if len(pageSource.xpath(editLinkXpath)) == 0:
            self.trigger.emit("noList")
            return False

        # 点击“修改”链接
        self.__chrome.find_element_by_xpath(editLinkXpath).click()
        # 点击保存按钮
        self.__chrome.find_element_by_xpath(
            '//form[@id="inputForm"]/div[@class="tab-content"]/div[@class="form-actions"]/input[@id="subBut"]').click()
        # 处理确认消息框
        confirm = self.__chrome.switch_to_alert()
        if r"确定要修改吗" in confirm.text:
            confirm.accept()
            if self.__chrome.page_source.find("sfzNum") == -1:
                self.trigger.emit("noSave")
                self.__flag.wait()
                question = self.__queue.get()
                if question == QMessageBox.No:
                    return False

            return True
        else:
            self.trigger.emit("sfz")
            self.__flag.wait()
            question = self.__queue.get()
            if question == QMessageBox.No:
                return False
            return True

    def __editResearchType(self):
        """
        更改调查类型
        :return:
        """
        self.__chrome.get("http://dtgx.sddpf.org.cn/dtgx2017/a/dynamicupdate/register/eformityRegister/integratedQuery")
        self.__chrome.find_element_by_xpath('//form[@id="searchForm"]//div[@id="tab1"]//a[@id="g200Button"]').click()
        sleep(3)
        self.__chrome.switch_to.frame("jbox-iframe")
        self.__chrome.find_element_by_xpath('//span[@id="tree_1_switch"]').click()
        sleep(1)
        ActionChains(self.__chrome).double_click(
            self.__chrome.find_element_by_xpath('//span[@id="tree_4_span"]')).perform()
        self.__chrome.switch_to.default_content()
        self.__chrome.find_element_by_xpath('//*[@id="researchMethod2"]').click()
        self.__chrome.find_element_by_xpath('//*[@id="btnSubmit"]').click()
        pageSource = etree.HTML(self.__chrome.page_source)
        if len(pageSource.xpath('//*[@id="contentTable"]/tbody/tr[1]/td[2]')) == 0:
            self.trigger.emit("noList")
            return False
        idCardNumber = pageSource.xpath('//*[@id="contentTable"]/tbody/tr[1]/td[2]/text()')[0].strip()
        self.__chrome.get("http://dtgx.sddpf.org.cn/dtgx2017/a/dynamicupdate/register/eformityRegister/list")
        self.__chrome.find_element_by_xpath('//input[@id="g2"]').send_keys(idCardNumber)
        self.__chrome.find_element_by_xpath('//input[@id="btnSubmit"]').click()
        pageSource = etree.HTML(self.__chrome.page_source)
        if len(pageSource.xpath('//*[@id="contentTable"]/tbody/tr[1]/td[10]/a[1]')) == 0:
            self.trigger.emit("noList")
            return False
        self.__chrome.find_element_by_xpath('//*[@id="contentTable"]/tbody/tr[1]/td[10]/a[1]').click()
        self.__chrome.find_element_by_xpath('//*[@id="researchMethod1"]').click()
        self.__chrome.find_element_by_xpath('//*[@id="subBut"]').click()
        confirm = self.__chrome.switch_to_alert()
        if r"确定要修改吗" in confirm.text:
            confirm.accept()
            if self.__chrome.page_source.find("sfzNum") == -1:
                self.trigger.emit("noSave")
                self.__flag.wait()
                question = self.__queue.get()
                if question == QMessageBox.No:
                    return False

            return True
        else:
            self.trigger.emit("sfz")
            self.__flag.wait()
            question = self.__queue.get()
            if question == QMessageBox.No:
                return False

            return True


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Main()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
