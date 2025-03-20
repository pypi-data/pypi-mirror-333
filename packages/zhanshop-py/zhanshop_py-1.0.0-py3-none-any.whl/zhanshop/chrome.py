import time
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from zhanshop.app import App
from zhanshop.env import Env


class Chrome():
    serverUrl = None
    options = None
    driver = None
    elementTimeout = 5
    def __init__(self, elementTimeout = 5, serverUrl = None):
        self.driver = None
        if(serverUrl == None):
            self.serverUrl = App.make(Env).get("service.webdriver_host", "http://127.0.0.1:4444")
        else:
            self.serverUrl = serverUrl

        self.options = {}
        self.elementTimeout = elementTimeout

    def open(self, url):
        driver = webdriver.Remote(command_executor=self.serverUrl, options=self.getServerOption())
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => false
            })
            """
        })
        try:
            driver.get(url)
        except Exception:
            driver.quit()
        self.driver = driver
        return self
    def getDriver(self):
        """
        获取驱动
        :return:
        """
        return self.driver
    """
    
    """
    def setServerOption(self, key, value = None):
        """
        设置谷歌浏览器参数
        :param key:
        :param value:
        :return:
        """
        self.options[key] = value
        return self
    def getServerOption(self):
        """
        获取谷歌浏览器参数
        @return:
        """
        options = Options()
        for k, v in self.options.items():
            if (v == None):
                options.add_argument(k)
            else:
                options.add_experimental_option(k, v)
        return options

    def getElementById(self, name)->WebElement:
        """
        通过 id 查找 HTML 元素
        :param idName:
        :return:
        """
        startTime = time.time()
        while True:
            try:
                element = self.driver.find_element(By.ID, name)
                break
            except Exception:
                element = None
            time.sleep(0.3)
            if (time.time() - startTime > self.elementTimeout): break
        return element

    def getElementsByClassName(self, name):
        """
        通过 类名 查找 HTML 元素
        :param Name:
        :return:
        """
        startTime = time.time()
        while True:
            elements = self.driver.find_elements(By.CLASS_NAME, name)
            if (len(elements) > 0): break
            time.sleep(0.3)
            if(time.time() - startTime > self.elementTimeout): break
        return elements

    def getChildByClassName(self, webElement, name)->List[WebElement]:
        """
        通过 类名 查找子节点 HTML 元素
        :param webElement:
        :param Name:
        :return:
        """
        startTime = time.time()
        while True:
            elements = webElement.find_elements(By.CLASS_NAME, name)
            if (len(elements) > 0): break
            time.sleep(0.3)
            if (time.time() - startTime > self.elementTimeout): break
        return elements

    def getElementsByTagName(self, name):
        """
        通过 标签名 查找 HTML 元素
        :param Name:
        :return:
        """
        startTime = time.time()
        while True:
            elements = self.driver.find_elements(By.TAG_NAME, name)
            if (len(elements) > 0): break
            time.sleep(0.3)
            if (time.time() - startTime > self.elementTimeout): break
        return elements

    def getChildByTagName(self, webElement, name)->List[WebElement]:
        """
        通过 标签名 查找子节点 HTML 元素
        :param webElement:
        :param Name:
        :return:
        """
        startTime = time.time()
        while True:
            elements = webElement.find_elements(By.TAG_NAME, name)
            if (len(elements) > 0): break
            time.sleep(0.3)
            if (time.time() - startTime > self.elementTimeout): break
        return elements

    def getElementsByName(self, name):
        """
        通过 name=名 查找 HTML 元素
        :param name:
        :return:
        """
        startTime = time.time()
        while True:
            elements = self.driver.find_elements(By.NAME, name)
            if (len(elements) > 0): break
            time.sleep(0.3)
            if (time.time() - startTime > self.elementTimeout): break
        return elements
    def executeScript(self, code):
        """
        执行javascript脚本
        :param code:
        :return:
        """
        startTime = time.time()
        while True:
            result = self.driver.execute_script(code)
            if (result != None): break
            time.sleep(0.3)
            if (time.time() - startTime > self.elementTimeout): break
        return result

    def javascript(self):
        """
        封装一定的javascript脚本
        :return:
        """
        pass

    def getHtml(self):
        try:
            return self.driver.page_source
        except Exception as e:
            return ""

    def quit(self):
        return self.driver.quit()

