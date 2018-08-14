from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from threaders import threaders
from qaviton.core.utils.web.locator import ByExtension
from qaviton.core.utils.web.locator import WebLocator


def find_element(locator, driver, index=0):
    """Looks up an element. Logs and re-raises ``WebDriverException``
    if thrown.
    :type locator: tuple
    :type driver: WebDriver
    :type index: int
    :rtype: WebElement
    """
    by, value = WebLocator.any(locator)
    if by == ByExtension.elements:
        return value[index]
    elif by == ByExtension.element:
        return value
    elif by in (ByExtension.tuple, ByExtension.list):
        pool = threaders.ThreadPool(len(value), collect_results=True)
        for location in value:
            pool.put(try_to_find_element, location, driver, index)
        element = pool.get_and_stop()
        if element is None:
            raise NoSuchElementException
        return element
    return driver.find_element(by, value)


def find_elements(locator, driver):
    """
        :type locator: tuple
    :type driver: WebDriver
    :type index: int
    :rtype: list[WebElement]"""
    by, value = WebLocator.any(locator)
    if by == ByExtension.elements:
        return value
    elif by == ByExtension.element:
        return [value]
    elif by in (ByExtension.tuple, ByExtension.list):
        pool = threaders.ThreadPool(len(value), collect_results=True)
        for location in value:
            pool.put(try_to_find_elements, location, driver)
        elements = pool.get_and_stop()
        if elements is None:
            raise NoSuchElementException
        return elements
    return driver.find_elements(by, value)


def try_to_find_element(locator, driver, index=0):
    """:rtype: WebElement | None"""
    try:
        return find_element(locator, driver, index)
    except:
        return None


def try_to_find_elements(locator, driver):
    """:rtype: list[WebElement] | None"""
    try:
        return find_elements(locator, driver)
    except:
        return None
