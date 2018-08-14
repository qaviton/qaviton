import logging

from qaviton.core.utils.decorator_util import DecoratorConfig
from qaviton.core.utils.log_handler import get_log_file_directories
from qaviton.core.utils.web import base_functions as base_functions
from qaviton.core.utils.web import expected_conditions_extension as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from qaviton.core.utils.web.locator import WebLocator

###################################################
#          decorator configuration Start          #
###################################################


decorator = DecoratorConfig(retries=3)
selenium_decorator = decorator.generic_decorator


###################################################
#                 WebPage Start                   #
###################################################


class PageInterface(object):

    _PageStep = 0

    def __init__(self, log, driver, url, timeout=60, log_file_directories=None):
        """
        :type log: logging.Logger
        :type driver: WebDriver
        :type url: str
        :type timeout: int | float
        :type log_file_directories: list[str]
        """
        if log_file_directories is None:
            log_file_directories = get_log_file_directories(log)
        self.log = log
        self.log_file_directories = log_file_directories
        self.driver = driver
        self.url = url
        self.timeout = timeout

    def selenium_logger(self, method, t, *args, **kw):
        msg = '[step:{}]:{}: {} {} arguments {}{}'\
            .format(self._step, '[%2.4f sec]' % t, self.__class__.__name__, method.__name__, args, kw)
        self.log.debug(msg)
        if self.log.level <= logging.DEBUG:
            self._save_screenshot()
        self._add_step()

    @property
    def _step(self):
        return PageInterface._PageStep

    @staticmethod
    def _add_step():
        PageInterface._PageStep += 1
        return PageInterface._PageStep

    def _save_screenshot(self, file_name=None):
        try:
            if file_name is None:
                for log_file_directory in self.log_file_directories:
                    self.driver.save_screenshot(log_file_directory + '{}.{}.png'.format(self.log.name, self._step))
            else:
                self.driver.save_screenshot(file_name)
        except Exception as error:
            self.log.exception(error)

    def _get_driver(self, driver):
        if driver is None:
            driver = self.driver
        return driver

    def _get_timeout(self, timeout):
        if timeout is None:
            timeout = self.timeout
        return timeout

    def get_page(self, url=None):
        if url is None:
            url = self.url
        self.driver.get(url)

    def wait(self, driver=None, timeout=None):
        return WebDriverWait(self._get_driver(driver), self._get_timeout(timeout))

    def update_driver(self, driver):
        self.driver = driver
        for attribute in dir(self):
            if not attribute.startswith("__"):
                at = getattr(self, attribute)
                if hasattr(at, "update_driver"):
                    try:
                        at.update_driver(driver)
                    except: pass

    def _find_element(self, locator, driver, index=0):
        """:rtype: WebElement"""
        return base_functions.find_element(locator, self._get_driver(driver), index)

    def _find_elements(self, locator, driver):
        """:rtype: list[WebElement]"""
        return base_functions.find_elements(locator, self._get_driver(driver))

    def _try_to_find_element(self, locator, driver, index=0):
        """:rtype: WebElement"""
        return base_functions.try_to_find_element(locator, self._get_driver(driver), index)

    def _try_to_find_elements(self, locator, driver):
        """:rtype: list[WebElement]"""
        return base_functions.try_to_find_elements(locator, self._get_driver(driver))

    def _find_element_explicitly(self, locator, timeout=None, driver=None, index=0):
        """:rtype: WebElement"""
        return self.wait(driver, timeout).until(EC.presence_of_element_located(locator, index))

    def _find_elements_explicitly(self, locator, timeout=None, driver=None):
        """:rtype: list[WebElement]"""
        return self.wait(driver, timeout).until(EC.presence_of_all_elements_located(locator))

    def _try_to_find_element_explicitly(self, locator, timeout=None, driver=None, index=0):
        """:rtype: WebElement"""
        try:
            return self.wait(driver, timeout).until(EC.presence_of_element_located(locator, index))
        except:
            return None

    def _try_to_find_elements_explicitly(self, locator, timeout=None, driver=None):
        """:rtype: list[WebElement]"""
        try:
            return self.wait(driver, timeout).until(EC.presence_of_all_elements_located(locator))
        except:
            return None

    def _get_element_last_children(self, element, timeout=3):
        """:rtype: list[WebElement]"""
        locator = WebLocator.xpath('./*')
        elements = []
        while True:
            try:
                elements = self._find_elements_explicitly(locator, timeout, element)
                locator[1] += '/*'
            except:
                return elements

    def _get_elements_last_children(self, elements):
        """:rtype: list[WebElement]"""
        children_elements = []
        for element in elements:
            children_elements += self._get_element_last_children(element)
        return children_elements

    def _get_element_children(self, element, timeout=3):
        """:rtype: list[WebElement] | []"""
        try:
            return self._find_elements_explicitly(WebLocator.xpath('./*'), timeout, element)
        except:
            return []

    def _get_elements_children(self, elements):
        """:rtype: list[WebElement]"""
        children_elements = []
        for element in elements:
            children_elements += self._get_element_children(element)
        return children_elements


###################################################
#                 WebPage End                     #
###################################################


decorator.decorator_log = PageInterface.selenium_logger


###################################################
#          decorator configuration End            #
###################################################
