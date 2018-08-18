from selenium.webdriver import Remote
from selenium.webdriver.remote.webelement import WebElement as we
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.command import Command
from appium.webdriver.webelement import WebElement as WE
from qaviton.drivers.common.web_functions import WebFunctions
from qaviton.drivers.support import expected_conditions_extension as EC
from qaviton.locator import Locator


class WebElement(WebFunctions, WE):
    def __init__(self, parent, id_, w3c=False):
        super(self.__class__, self).__init__(parent, id_, w3c)
        if isinstance(parent, Remote):
            self.clear = we.clear

    def click(self, locator=None, timeout=0, index=0):
        """ click on an element
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type index: int
        :rtype: WebElement
        """
        if locator is None:
            if timeout == 0:
                self._execute(Command.CLICK_ELEMENT)
            else:
                WebDriverWait(self, timeout).until(EC.element_to_be_clickable(Locator.element(self), index))._execute(
                    Command.CLICK_ELEMENT)
            return self
        else:
            element = WebDriverWait(self, timeout).until(EC.element_to_be_clickable(locator, index))
            element._execute(Command.CLICK_ELEMENT)
            return element

    def get_element_last_children(self, timeout=3):
        """ get the last elements in the tree from the root element
        :type element: WebElement
        :rtype: list[WebElement]
        """
        locator = Locator.xpath('./*')
        elements = []
        while True:
            try:
                elements = self.find_all(locator, timeout)
                locator = (locator[0], locator[1] + '/*')
            except:
                return elements

    def get_element_children(self, timeout=3):
        """ get the last element in the tree from the root element
        :type element: WebElement
        :rtype: list[WebElement] | []
        """
        try:
            return self.find_all(Locator.xpath('./*'), timeout)
        except:
            return []

