from selenium.webdriver import Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
from appium.webdriver.webelement import WebElement as WE
from qaviton.drivers.common.functions import WebFunctions
from qaviton.drivers.support import expected_conditions as EC
from qaviton.locator import Locator


def web_clear(self):
    """override appium and selenium clear method
    in case driver is webbased(selenium).
    Clears the text if it's a text entry element.
    :rtype: WebElement"""
    self._execute(Command.CLEAR_ELEMENT)
    return self


class WebElement(WebFunctions, WE):
    def __init__(self, parent, id_, w3c=False):
        super(self.__class__, self).__init__(parent, id_, w3c)
        if isinstance(parent, Remote):
            self.clear = web_clear

    def try_to_click(self, timeout=0):
        """ try to click on an element
        :type timeout: int
        :rtype: WebElement | None
        """
        try:
            return self.click(timeout)
        except:
            return None

    def click_at(self):
        ActionChains(self.parent).move_to_element_with_offset(self, self.size["width"]/2, self.size["height"]/2).click().perform()
        return self

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
                WebDriverWait(self.parent, timeout)\
                    .until(EC.element_to_be_clickable(Locator.element(self), index))._execute(Command.CLICK_ELEMENT)
            return self
        else:
            element = WebDriverWait(self.parent, timeout).until(EC.element_to_be_clickable(locator, index))
            element._execute(Command.CLICK_ELEMENT)
            return element

    def find_last_children(self, timeout=0):
        """ get the last elements in the tree from the root element
        :type timeout: int
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

    def find_children(self, timeout=0):
        """ get the last element in the tree from the root element

        :type timeout: int
        :rtype: list[WebElement] | []
        """
        try:
            return self.find_all(Locator.xpath('./*'), timeout)
        except:
            return []

    def drag_to_offset(self, xoffset, yoffset):
        """
        Holds down the left mouse button on the source element,
           then moves to the target offset and releases the mouse button.

        :Args:
         - source: The element to mouse down.
         - xoffset: X offset to move to.
         - yoffset: Y offset to move to.
         :rtype: WebElement
        """
        ActionChains(self.parent).drag_and_drop_by_offset(self, xoffset, yoffset).perform()
        return self

    def hover(self):
        """ hover/move cursor to element
        :rtype: WebElement
        """
        ActionChains(self.parent).move_to_element(self).perform()
        return self

    def hover_and_click(self):
        """ hover/move cursor to element and click
        :rtype: WebElement
        """
        ActionChains(self.parent).move_to_element(self).click(self).perform()
        return self

    def send_keys(self, *value):
        """Simulates typing into the element.

        :Args:
            - value - A string for typing, or setting form fields.  For setting
              file inputs, this could be a local file path.

        Use this to send simple key events or to fill out form fields::

            form_textfield = driver.find_element_by_name('username')
            form_textfield.send_keys("admin")

        This can also be used to set file inputs.

        ::

            file_input = driver.find_element_by_name('profilePic')
            file_input.send_keys("path/to/profilepic.gif")
            # Generally it's better to wrap the file path in one of the methods
            # in os.path to return the actual path to support cross OS testing.
            # file_input.send_keys(os.path.abspath("path/to/profilepic.gif"))

        """
        WE.send_keys(self, *value)
        return self

    def send_chars(self, chars=''):
        """send individual characters to element.
        this function is useful in flacky applications, where the send keys function can cause issues.
        :type chars: str
        :rtype: WebElement
        """
        for c in chars:
            self.send_keys(c)
        return self
