from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.expected_conditions import *
from qaviton.drivers.common.functions import WebFunctions


def _element_if_visible(element, visibility=True):
    """:rtype: WebElement"""
    return element if element.is_displayed() == visibility else False


class presence_of_element_located(object):
    """ An expectation for checking that an element is present on the DOM
    of a page. This does not necessarily mean that the element is visible.
    webLocator - used to find the element
    returns the WebElement once it is located
    :rtype: WebElement
    """
    def __init__(self, locator, index=0):
        self.locator = locator
        self.index = index

    def __call__(self, driver):
        return WebFunctions.find(driver, self.locator, self.index)


class visibility_of_element_located(object):
    """ An expectation for checking that an element is present on the DOM of a
    page and visible. Visibility means that the element is not only displayed
    but also has a height and width that is greater than 0.
    webLocator - used to find the element
    returns the WebElement once it is located and visible
    """
    def __init__(self, locator, index=0):
        self.locator = locator
        self.index = index

    def __call__(self, driver):
        try:
            return _element_if_visible(WebFunctions.find(driver, self.locator, self.index))
        except StaleElementReferenceException:
            return False


class presence_of_all_elements_located(object):
    """ An expectation for checking that there is at least one element present
    on a web page.
    webLocator is used to find the element
    returns the list of WebElements once they are located
    :rtype: list[WebElement]
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        return WebFunctions.find_all(driver, self.locator)


class visibility_of_any_elements_located(object):
    """ An expectation for checking that there is at least one element visible
    on a web page.
    webLocator is used to find the element
    returns the list of WebElements once they are located
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        """:rtype: list[WebElement]"""
        return [element for element in WebFunctions.find_all(driver, self.locator) if _element_if_visible(element)]


class visibility_of_all_elements_located(object):
    """ An expectation for checking that all elements are present on the DOM of a
    page and visible. Visibility means that the elements are not only displayed
    but also has a height and width that is greater than 0.
    webLocator - used to find the elements
    returns the list of WebElements once they are located and visible
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        """:rtype: list[WebElement]"""
        try:
            elements = WebFunctions.find_all(driver, self.locator)
            for element in elements:
                if _element_if_visible(element, visibility=False):
                    return False
            return elements
        except StaleElementReferenceException:
            return False


class text_to_be_present_in_element(object):
    """ An expectation for checking if the given text is present in the
    specified element.
    webLocator, text
    """
    def __init__(self, locator, text_, index=0):
        self.locator = locator
        self.text = text_
        self.index = index

    def __call__(self, driver):
        try:
            element_text = WebFunctions.find(driver, self.locator, self.index).text
            return self.text in element_text
        except StaleElementReferenceException:
            return False


class text_to_be_present_in_element_value(object):
    """
    An expectation for checking if the given text is present in the element's
    webLocator, text
    """
    def __init__(self, locator, text_, index=0):
        self.locator = locator
        self.text = text_
        self.index = index

    def __call__(self, driver):
        try:
            element_text = WebFunctions.find(driver, self.locator, self.index).get_attribute("value")
            if element_text:
                return self.text in element_text
            else:
                return False
        except StaleElementReferenceException:
                return False


class invisibility_of_element_located(object):
    """ An Expectation for checking that an element is either invisible or not
    present on the DOM.

    webLocator used to find the element
    """
    def __init__(self, locator, index=0):
        self.locator = locator
        self.index = index

    def __call__(self, driver):
        try:
            return _element_if_visible(WebFunctions.find(driver, self.locator, self.index), False)
        except (NoSuchElementException, StaleElementReferenceException):
            # In the case of NoSuchElement, returns true because the element is
            # not present in DOM. The try block checks if the element is present
            # but is invisible.
            # In the case of StaleElementReference, returns true because stale
            # element reference implies that element is no longer visible.
            return True


class element_to_be_clickable(object):
    """ An Expectation for checking an element is visible and enabled such that
    you can click it.
    """
    def __init__(self, locator, index=0):
        self.locator = locator
        self.index = index

    def __call__(self, driver):
        """:rtype: WebElement"""
        element = visibility_of_element_located(self.locator, self.index)(driver)
        if element and element.is_enabled():
            return element
        else:
            return False


class element_located_to_be_selected(object):
    """An expectation for the element to be located is selected.
    webLocator is a tuple of (by, path)"""
    def __init__(self, locator, index=0):
        self.locator = locator
        self.index = index

    def __call__(self, driver):
        """:rtype: WebElement"""
        return WebFunctions.find(driver, self.locator, self.index).is_selected()


class element_located_selection_state_to_be(object):
    """ An expectation to locate an element and check if the selection state
    specified is in that state.
    webLocator is a tuple of (by, path)
    is_selected is a boolean
    """
    def __init__(self, locator, is_selected, index=0):
        self.locator = locator
        self.is_selected = is_selected
        self.index = index

    def __call__(self, driver):
        try:
            element = WebFunctions.find(driver, self.locator, self.index)
            return element.is_selected() == self.is_selected
        except StaleElementReferenceException:
            return False
