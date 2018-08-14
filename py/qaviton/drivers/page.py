from logging import Logger
from time import sleep
from time import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import POLL_FREQUENCY
from qaviton.core.utils.web.locator import WebLocator
from qaviton.core.utils.web import expected_conditions_extension as EC
from qaviton.core.utils.web.page_interface import PageInterface
from qaviton.core.utils.web.page_interface import selenium_decorator


class WebPage(PageInterface):

    def __init__(self, log, driver, url, timeout=60, log_file_directories=None):
        """
        :type log: Logger
        :type driver: WebDriver
        :type url: str
        :type timeout: int | float
        :type log_file_directories: list[str]
        """
        PageInterface.__init__(self, log, driver, url, timeout, log_file_directories)

    def wait_until_page_loads(self, timeout=None, driver=None):
        t = time()
        driver, timeout = self._get_driver(driver), self._get_timeout(timeout)
        self.wait(driver, timeout).until(lambda x: driver.execute_script("return document.readyState;") == "complete")
        while True:
            c1 = self.count_all_elements(driver)
            sleep(POLL_FREQUENCY)
            c2 = self.count_all_elements(driver)
            sleep(POLL_FREQUENCY)
            c3 = self.count_all_elements(driver)
            if c1 == c2 == c3:
                break
            elif timeout <= time()-t:
                raise TimeoutException

    def count_all_elements(self, driver=None):
        return len(self.find_all_elements(driver))

    def find_all_elements(self, driver=None):
        if driver is None:
            driver = self.driver
        return driver.find_elements_by_css_selector("*")

    def find_elements(self, locator, driver=None):
        """ find elements
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type driver: WebDriver | WebElement
        :rtype: list[WebElement]
        """
        return self._find_elements(locator, driver)

    def find_element(self, locator, driver=None, index=0):
        """ find element
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type driver: WebDriver | WebElement
        :type index: int
        :rtype: WebElement
        """
        return self._find_element(locator, driver, index)

    def find_elements_explicitly(self, locator, timeout=None, driver=None):
        """ wait until element is found
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :rtype: list[WebElement]
        """
        return self._find_elements_explicitly(locator, timeout, driver)

    def find_element_explicitly(self, locator, timeout=None, driver=None, index=0):
        """ wait until element is found
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :type index: int
        :rtype: WebElement
        """
        return self._find_element_explicitly(locator, timeout, driver, index)

    def try_to_find_elements(self, locator, driver=None):
        """ try to find elements if any exist
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type driver: WebDriver | WebElement
        :rtype: list[WebElement] | []
        """
        return self._try_to_find_elements(locator, driver)

    def try_to_find_element(self, locator, driver=None, index=0):
        """ try to find element if it exist
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type driver: WebDriver | WebElement
        :type index: int
        :rtype: WebElement | None
        """
        return self._try_to_find_element(locator, driver, index)

    def try_to_find_elements_explicitly(self, locator, timeout=None, driver=None):
        """ try to wait & find elements if any exist
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :rtype: list[WebElement] | []
        """
        return self._try_to_find_elements_explicitly(locator, timeout, driver)

    def try_to_find_element_explicitly(self, locator, timeout=None, driver=None, index=0):
        """ try to wait & find element if it exist
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :type index: int
        :rtype: WebElement | None
        """
        return self._try_to_find_element_explicitly(locator, timeout, driver, index)

    def get_elements_text(self, locator, timeout=None, driver=None):
        """ get text from elements
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :rtype: list[str]
        """
        element_list, elements_text = self._find_elements_explicitly(locator, timeout, driver), []
        for i in range(len(element_list)):
            elements_text.append(element_list[i].text)
        return elements_text

    def get_elements_last_children(self, locator, timeout=None, driver=None):
        """ get the last children from located elements
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :rtype: list[WebElement]
        """
        elements = self.find_elements_explicitly(locator, timeout, driver)
        return self._get_elements_last_children(elements)

    def try_to_get_elements_text(self, locator, timeout=None, driver=None):
        """ get text from elements if any elements are located
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :rtype: list[str] | []
        """
        element_list, elements_text = self.try_to_find_elements_explicitly(locator, timeout, driver), []
        for i in range(len(element_list)):
            elements_text.append(element_list[i].text)
        return elements_text

    def click_on_element(self, locator, timeout=None, driver=None, index=0):
        """ click on an element
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :type index: int
        :rtype: WebElement
        """
        return self.wait(driver, timeout).until(EC.element_to_be_clickable(locator, index)).click()

    def click_on_elements(self, locator, timeout=None, driver=None):
        """ click on all located elements
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :rtype: list[WebElement]
        """
        elements = self._try_to_find_elements_explicitly(locator, timeout, driver)
        for element in elements:
            self.wait(driver, timeout).until(EC.element_to_be_clickable(WebLocator.element(element))).click()
        return elements

    def drag_element_to_element(self, locator_from, locator_to, timeout=None, driver=None):
        """ drag and drop source element on a target element or on a (x,y) offset
        :type locator_from: tuple(str, str | list[WebElement] | WebElement)
        :type locator_to: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :rtype: tuple(WebElement)
        """
        source = self._find_element_explicitly(locator_from, timeout, driver)
        target = self._find_element_explicitly(locator_to, timeout, driver)
        ActionChains(self.driver).drag_and_drop(source, target).perform()
        return source, target

    def drag_element_to_offset(self, locator, offset_x, offset_y, timeout=None, driver=None):
        """ drag and drop source element on a target element or on a (x,y) offset
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type offset_x: int
        :type offset_y: int
        :type timeout: int
        :type driver: WebDriver | WebElement
        :rtype: WebElement
        """
        source = self._find_element_explicitly(locator, timeout, driver)
        ActionChains(self.driver).drag_and_drop_by_offset(source, offset_x, offset_y).perform()

    def hover_on_element(self, locator, timeout=None, driver=None):
        """ drag and drop source element on a target element or on a (x,y) offset
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :rtype: WebElement
        """
        element = self._find_element_explicitly(locator, timeout, driver)
        ActionChains(self.driver).move_to_element(element).perform()
        return element

    def scroll_element_into_view(self, locator, timeout=None, driver=None):
        """ This is a scrolling function to scroll until element is visible (whole window scroll)
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :rtype: WebElement
        """
        element = self._find_element_explicitly(locator, timeout, driver)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            return element
        except Exception as error:
            self.log.exception(error)

    def scroll_page(self, x, y):
        """ this is a page scrolling function
        :type x: int
        :type y: int"""
        self.driver.execute_script("scroll(arguments[0], arguments[1]);", x, y)

    def send_characters_to_element(self, locator, characters='', timeout=None, driver=None):
        """ click on element, clear element text, send individual characters to element
        :type locator: (tuple(str, str | list[WebElement] | WebElement)
        :type characters: str
        :type timeout: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: WebElement
        """
        element = self.click_on_element(locator, timeout, driver)
        element.clear()
        s = str(characters)
        for i in range(len(s)):
            element.send_keys(s[i])
        return element

    def send_characters_to_elements(self, locator, characters='', timeout=None, driver=None):
        """ send text to multiple elements
        :type locator: (tuple(str, str | list[WebElement] | WebElement)
        :type text: str
        :type timeout: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: WebElement
        """
        elements = self._find_elements_explicitly(locator, timeout, driver)
        for i in range(len(elements)):
            self.send_characters_to_element(WebLocator.element(elements[i]), characters),
        return elements

    def send_in_chunks_to_element(self, locator, text='', size=1, timeout=None, driver=None):
        """ write in chunks
        :type locator: (tuple(str, str | list[WebElement] | WebElement)
        :type text: str
        :type size: int
        :type timeout: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: WebElement
        """
        i, element = 0, self.wait(driver, timeout).until(EC.element_to_be_clickable(locator)).click()
        element.clear()
        while i < len(text):
            if i + size > len(text):
                end_point = len(text)
                if i == 0:
                    s_chunk = text
                else:
                    s_chunk = text[i:end_point]
            else:
                end_point = i + size
                s_chunk = text[i:end_point]
            element.send_keys(s_chunk)
            i += size
        return element

    def send_to_element(self, locator, text='', timeout=None, driver=None):
        """ send text to element
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type text: str
        :type timeout: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: WebElement
        """
        return self._find_element_explicitly(locator, timeout, driver).send_keys(text)

    def send_to_elements(self, locator, text='', timeout=None, driver=None):
        """ send text to multiple elements
        :type locator: (tuple(str, str | list[WebElement] | WebElement)
        :type text: str
        :type timeout: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: WebElement
        """
        elements = self._find_elements_explicitly(locator, timeout, driver)
        for i in range(len(elements)):
            self.send_to_element(WebLocator.element(elements[i]), text),
        return elements

    def select_element_from_list(self, locator, choice, timeout=None, driver=None):
        """ select an option off a list
        :type locator: (tuple(str, str | list[WebElement] | WebElement)
        :type choice: str
        :type timeout: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: WebElement
        """
        elements = self._get_elements_last_children(self._find_elements_explicitly(locator, timeout, driver))
        element = self._try_to_find_element_explicitly(locator, timeout, driver)
        element.send_keys(str(choice))
        for element in elements:
            if element.text == choice:
                element.click()
                return element

    def select_element_from_multilist(self, locator_open_list, locator_list, choice, timeout=None, driver=None):
        """ select a choice from a multi drop down list
        :type locator_open_list: tuple(str, str | list[WebElement] | WebElement)
        :type locator_list: tuple(str, str | list[WebElement] | WebElement)
        :type choice: str
        :type timeout: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: WebElement
        """
        element_to_open_or_close_list = self.wait(driver, timeout).until(EC.element_to_be_clickable(locator_open_list)).click()
        elements = self._get_elements_last_children(self._find_elements_explicitly(locator_list, timeout, driver))
        for element in elements:
            if element.text == choice:
                self.wait(driver, timeout).until(EC.element_to_be_clickable(WebLocator.element(element))).click()
                self.wait(driver, timeout).until(EC.element_to_be_clickable(WebLocator.element(element_to_open_or_close_list))).click()
                return element

    def replace_url(self, pattern, replace):
        """ replace url pattern
        :type pattern: str
        :type replace: str
        """
        self.driver.get(self.driver.current_url.replace(pattern, replace))

    def try_to_click_until_element_is_created(self, locator_to_click, locator_condition, condition_expected_results=1,
                                              tries=8, timeout=2, delay=0.5, driver=None):
        """ try to click on element, check if condition element created, if not, click again
        :type locator_to_click: tuple(str, str | list[WebElement] | WebElement)
        :type locator_condition: tuple(str, str | list[WebElement] | WebElement)
        :type condition_expected_results: int
        :type tries: int
        :type timeout: float | int
        :type delay: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: list[WebElement]
        """
        for i in range(tries):
            t = time()
            try:
                self.wait(driver, timeout).until(EC.element_to_be_clickable(WebLocator.element(locator_to_click))).click()
                element_condition = self.try_to_find_elements_explicitly(locator_condition, timeout, driver)
                if len(element_condition) >= condition_expected_results:
                    return element_condition
            except: pass
            t = time() - t
            if t < delay:
                sleep(delay - t)
        return []

    @selenium_decorator()
    def click_until_element_is_created(self, locator_to_click, locator_condition, condition_expected_results=1,
                                       tries=8, timeout=2, delay=0.5, driver=None):
        """ click on element, check if condition element created, if not, click again
        :type locator_to_click: tuple(str, str | list[WebElement] | WebElement)
        :type locator_condition: tuple(str, str | list[WebElement] | WebElement)
        :type condition_expected_results: int
        :type tries: int
        :type timeout: float | int
        :type delay: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: list[WebElement]
        """
        for i in range(tries):
            t = time()
            try:
                self.wait(driver, timeout).until(EC.element_to_be_clickable(WebLocator.element(locator_to_click))).click()
                element_condition = self.try_to_find_elements_explicitly(locator_condition, timeout, driver)
                if len(element_condition) >= condition_expected_results:
                    return element_condition
            except: pass
            t = time() - t
            if t < delay:
                sleep(delay - t)
        raise NoSuchElementException

    def try_to_click_until_condition_as_expected(self, locator_to_click, locator_condition,
                                                 condition_expected_results, tries=8, timeout=2, delay=0.5, driver=None):
        """ try to click on element, check if condition element is deleted, if not, click again
        :type locator_to_click: tuple(str, str | list[WebElement] | WebElement)
        :type locator_condition: tuple(str, str | list[WebElement] | WebElement)
        :type condition_expected_results: int
        :type tries: int
        :type timeout: float | int
        :type delay: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: list[WebElement]
        """
        for i in range(tries):
            t = time()
            try:
                self.wait(driver, timeout).until(EC.element_to_be_clickable(WebLocator.element(locator_to_click))).click()
                element_condition = self.try_to_find_elements_explicitly(locator_condition, timeout, driver)
                if len(element_condition) == condition_expected_results:
                    return element_condition
            except: pass
            t = time() - t
            if t < delay:
                sleep(delay - t)
        return []

    def click_until_condition_as_expected(self, locator_to_click, locator_condition, condition_expected_results,
                                          tries=8, timeout=2, delay=0.5, driver=None):
        """ click on element, check if condition element is deleted, if not, click again
        :type locator_to_click: tuple(str, str | list[WebElement] | WebElement)
        :type locator_condition: tuple(str, str | list[WebElement] | WebElement)
        :type condition_expected_results: int
        :type tries: int
        :type timeout: float | int
        :type delay: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: list[WebElement]
        """
        for i in range(tries):
            t = time()
            try:
                self.wait(driver, timeout).until(EC.element_to_be_clickable(WebLocator.element(locator_to_click))).click()
                element_condition = self.try_to_find_elements_explicitly(locator_condition, timeout, driver)
                if len(element_condition) == condition_expected_results:
                    return element_condition
            except: pass
            t = time() - t
            if t < delay:
                sleep(delay - t)
        raise Exception("condition expectation failed")

    def try_to_click_until_element_is_deleted(self, locator_to_click, locator_condition=None,
                                              condition_expected_results=0, tries=8, timeout=2, delay=0.5, driver=None):
        """ try to find element, try to click, check if element exist... if its not deleted retry!
        :type locator_to_click: tuple(str, str | list[WebElement] | WebElement)
        :type locator_condition: tuple(str, str | list[WebElement] | WebElement)
        :type condition_expected_results: int
        :type tries: int
        :type timeout: float | int
        :type delay: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: list[WebElement]
        """
        if locator_condition is None:
            locator_condition = locator_to_click
        for i in range(tries):
            t = time()
            try:
                self.wait(driver, timeout).until(EC.element_to_be_clickable(WebLocator.element(locator_to_click))).click()
                element_condition = self.try_to_find_elements_explicitly(locator_condition, timeout, driver)
                if len(element_condition) <= condition_expected_results:
                    return element_condition
            except: pass
            t = time() - t
            if t < delay:
                sleep(delay - t)
        return []

    def click_until_element_is_deleted(self, locator_to_click, locator_condition=None,
                                       condition_expected_results=0, tries=8, timeout=2, delay=0.5, driver=None):
        """ try to find element, try to click, check if element exist... if its not deleted retry!
        :type locator_to_click: tuple(str, str | list[WebElement] | WebElement)
        :type locator_condition: tuple(str, str | list[WebElement] | WebElement)
        :type condition_expected_results: int
        :type tries: int
        :type timeout: float | int
        :type delay: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: list[WebElement]
        """
        if locator_condition is None:
            locator_condition = locator_to_click
        for i in range(tries):
            t = time()
            try:
                self.wait(driver, timeout).until(
                    EC.element_to_be_clickable(WebLocator.element(locator_to_click))).click()
                element_condition = self.try_to_find_elements_explicitly(locator_condition, timeout, driver)
                if len(element_condition) <= condition_expected_results:
                    return element_condition
            except:
                pass
            t = time() - t
            if t < delay:
                sleep(delay - t)
        raise Exception("element could not be deleted")

    def try_to_confirm_element_is_deleted(self, locator, expected_results=0,
                                          tries=8, timeout=2, delay=0.5, driver=None):
        """ try to find element, confirm element deleted, check if element exist... if its not deleted retry!
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type expected_results: int
        :type tries: int
        :type timeout: float | int
        :type delay: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: list[WebElement]
        """
        for i in range(tries):
            t = time()
            try:
                elements = self.try_to_find_elements_explicitly(locator, timeout, driver)
                if len(elements) <= expected_results:
                    return True
            except:
                pass
            t = time() - t
            if t < delay:
                sleep(delay - t)
        return False

    def confirm_element_is_deleted(self, locator, expected_results=0,
                                   tries=8, timeout=2, delay=0.5, driver=None):
        """ try to find element, confirm element deleted, check if element exist... if its not deleted retry!
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type expected_results: int
        :type tries: int
        :type timeout: float | int
        :type delay: float | int
        :type driver: selenium WebDriver/WebElement
        :rtype: list[WebElement]
        """
        for i in range(tries):
            t = time()
            try:
                elements = self.try_to_find_elements_explicitly(locator, timeout, driver)
                if len(elements) <= expected_results:
                    return elements
            except:
                pass
            t = time() - t
            if t < delay:
                sleep(delay - t)
        raise Exception("element is expected to be deleted but did not")

    def refresh_page_until_element_is_found(self, locator, timeout=30, tries=3, driver=None):
        """ method to find element, if element is not found method will refresh the page and retry
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type tries: int
        :type driver: WebDriver | WebElement
        :rtype: list[WebElement]
        """
        for i in range(tries):
            elements = self._try_to_find_elements_explicitly(locator, timeout, driver)
            if len(elements) == 0:
                self.log.debug(self.driver.current_url)
                self.driver.refresh()
            else:
                return elements
        raise NoSuchElementException("elements are not present after page refresh")

    def click_until_url_changes(self, locator, url_change, tries=5, index=0, timeout=2, delay=2, driver=None):
        """ click on element, check if url changed, if not, click again
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type url_change: str
        :type tries: int
        :type index: int
        :type timeout: int
        :type delay: int
        :type driver: WebDriver | WebElement
        :rtype: list[WebElement]
        """
        for i in range(tries):
            sleep(delay)
            elements = self._try_to_find_elements_explicitly(locator, timeout, driver)
            url = self.driver.current_url
            if url_change == url or url_change in url:
                return elements
            else:
                if len(elements) > index:
                    try:
                        elements[index].click()
                    except Exception as error:
                        self.log.exception(error)
                else:
                    raise NoSuchElementException
        raise Exception("element has been clicked but url change did not occur")

    def element_is_not_clickable(self, locator, timeout=None, driver=None, index=0):
        """
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type driver: WebDriver | WebElement
        :type index: int
        :rtype: WebElement
        """
        element = self.wait(driver, timeout).until(EC.presence_of_element_located(locator, index))
        try:
            self.wait(driver, timeout).until(EC.element_to_be_clickable(WebLocator.element(element))).click()
        except:
            return element
        raise Exception("element should not be clickable")

    def element_is_deleted(self, locator, expected_elements=0, timeout=None, driver=None):
        """
        search for element, expect not to find it
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type expected_elements: int
        :type timeout: int
        :type driver: WebDriver | WebElement
        :rtype: WebElement
        """
        elements = self._try_to_find_elements_explicitly(locator, timeout, driver)
        if len(elements) > expected_elements:
            raise Exception('{} found {} elements that should not exist'.format(locator, len(elements)))
        return elements
