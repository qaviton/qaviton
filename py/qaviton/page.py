# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
the page implementation for GUI model based testing
"""

from time import sleep
from time import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import POLL_FREQUENCY

from qaviton.locator import Locator
from qaviton.drivers.support import expected_conditions as EC
from qaviton.pager.interface import PageInterface
from qaviton.drivers.common.webelement import WebElement
from qaviton.crosstest import WebDriver, MobileDriver
from qaviton import settings
from qaviton.utils.helpers import dynamic_delay

class Page(PageInterface):

    def __init__(self, driver, timeout=settings.page_timeout, url=None):
        """
        :type driver: WebDriver or MobileDriver
        :type url: str
        :type timeout: int | float
        """
        PageInterface.__init__(self, driver, timeout)
        self.driver = driver
        self.url = url

    def find(self, locator: tuple, timeout: int = 0, index=0):
        """find element with locator value
        :param locator: locate by method like id and value
        :param timeout: how long to search
        :param index: parameter for special cases
                  where a list of elements is in the locator,
                  the default element to return is elements[0]
        :rtype: WebElement
        """
        return self.driver.find(locator, timeout, index)

    def find_all(self, locator: tuple, timeout: int = 0):
        """find all elements with locator value
        :param timeout: how long to search
        :param locator: locate by method like id and value
        :rtype: list[WebElement]"""
        return self.driver.find_all(locator, timeout)

    def try_to_find(self, locator: tuple, timeout=0, index=0):
        """try to find element
        :param index: parameter for special cases
                      where a list of elements is in the locator,
                      the default element to return is elements[0]
        :param timeout: how long to search
        :param locator: locate by method like id and value
        :rtype: WebElement | None"""
        return self.driver.try_to_find(locator, timeout, index)

    def try_to_find_all(self, locator: tuple, timeout=0):
        """try to find elements
        :param timeout: how long to search
        :param locator: locate by method like id and value
        :rtype: list[WebElement] | None"""
        return self.driver.try_to_find_all(locator, timeout)

    def get_elements_text(self, locator, timeout=0):
        """ get text from elements
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: list[str]
        """
        return self.driver.get_elements_text(locator, timeout)

    def find_last_children(self, locator, timeout=0):
        """ get the last elements in the tree from the root element
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: list[WebElement]
        """
        return self.find(locator, timeout).find_last_children(timeout)

    def find_all_last_children(self, locator, timeout=0):
        """ get the last elements in the tree from the root elements
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: list[WebElement]
        """
        children_elements = []
        for element in self.find_all(locator, timeout):
            children_elements += element.find_last_children(timeout)
        return children_elements

    def find_children(self, locator, timeout=0):
        """ get the child elements of the parent
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: list[WebElement] | []
        """
        return self.find(locator, timeout).find_children(timeout)

    def find_all_children(self, locator, timeout=0):
        """ get elements children
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: list[WebElement]
        """
        children_elements = []
        for element in self.find_all(locator, timeout):
            children_elements += element.find_children(timeout)
        return children_elements

    def zoom(self, percent=200, element=None, steps=50):
        """zoom in/out (might not work for any webbrowser)"""
        return self.driver.zoom(percent=percent, element=element, steps=steps)

    def get_page(self, url=None):
        """works for web, not mobile
        if url is set to None nothing will happen
        """
        if self.url is None:
            if url is None:
                return self
            self.driver.get(url)
            return self
        elif url is None:
            self.driver.get(self.url)
            return self
        return self

    def wait_until_page_loads(self, timeout=None):
        """check that the page has finished loading and all elements are present"""
        timeout = self._get_timeout(timeout)
        t = time()
        self.wait(self.driver, timeout).until(
            lambda x: self.driver.execute_script("return document.readyState;") == "complete")
        while True:
            c1 = self.count_all_elements_in_the_page()
            sleep(POLL_FREQUENCY)
            c2 = self.count_all_elements_in_the_page()
            sleep(POLL_FREQUENCY)
            c3 = self.count_all_elements_in_the_page()
            if c1 == c2 == c3:
                break
            elif timeout <= time()-t:
                raise TimeoutException
        return self

    def count_all_elements_in_the_page(self):
        """:rtype: int"""
        return len(self.find_all_elements_in_the_page())

    def find_all_elements_in_the_page(self):
        """:rtype: list[WebElement]"""
        return self.driver.find_elements_by_css_selector("*")

    def click(self, locator, timeout=0, index=0):
        """ click on an element
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type index: int
        :rtype: WebElement
        """
        return self.driver.click(locator, timeout, index)

    def click_all(self, locator, timeout=0):
        """ click on all located elements
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: list[WebElement]
        """
        elements = self.find_all(locator, timeout)
        for element in elements:
            element.click(timeout=timeout)
        return elements

    def drag_and_drop(self, source_locator, target_locator, timeout=0):
        """ drag and drop source element on a target element or on a (x,y) offset
        :type source_locator: tuple(str, str | list[WebElement] | WebElement)
        :type target_locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: WebElement
        """
        source = self.find(source_locator, timeout)
        self.driver.drag_and_drop(source, self.find(target_locator, timeout))
        return source

    def drag_to_offset(self, locator, offset_x, offset_y, timeout=0):
        """ drag and drop source element on a target element or on a (x,y) offset
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type offset_x: int
        :type offset_y: int
        :type timeout: int
        :rtype: WebElement
        """
        return self.driver.drag_to_offset(self.find(locator, timeout), offset_x, offset_y)

    def hover(self, locator, timeout=0):
        """ drag and drop source element on a target element or on a (x,y) offset
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: Page
        """
        return self.driver.hover(self.find(locator, timeout))

    def hover_and_click(self, locator, timeout=0):
        """ hover/move cursor to element and click
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: Page
        """
        return self.driver.hover_and_click(self.find(locator, timeout))

    def scroll_element_into_view(self, locator, timeout=0, retries=5):
        """ selenium only: scrolling function to scroll until element is visible (whole window scroll)
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :param retries: integer bigger or equal to 0
        :rtype: WebElement
        """
        return self.driver.scroll_element_into_view(self.driver.find(locator, timeout), retries)

    def clear(self, locator, timeout=0):
        return self.find(locator, timeout).clear()

    def send(self, locator, keys, timeout=0):
        """ click on element, clear element text, send keys to element.
        :type locator: (tuple(str, str | list[WebElement] | WebElement)
        :type keys: str
        :type timeout: float | int
        :rtype: WebElement
        """
        return self.click(locator, timeout).clear().send_keys(keys)

    def send_chars(self, locator, chars='', timeout=0):
        """ click on element, clear element text, send individual characters to element.
        this function is useful in flacky applications, where the send keys function can cause issues.
        :type locator: (tuple(str, str | list[WebElement] | WebElement)
        :type chars: str
        :type timeout: float | int
        :rtype: WebElement
        """
        return self.click(locator, timeout).clear().send_chars(chars)

    def send_all(self, locator, keys, timeout=0):
        """ send text to multiple elements
        :type locator: (tuple(str, str | list[WebElement] | WebElement)
        :type keys: str
        :type timeout: float | int
        :rtype: WebElement
        """
        elements = self.find_all(locator, timeout)
        for element in elements:
            element.click(timeout=timeout).clear().send_keys(keys)
        return elements

    def select_from_dropdown(self, locator, choice, timeout=0):
        """ select a choice from a drop down list
        :type locator: (tuple(str, str | list[WebElement] | WebElement)
        :type choice: str
        :type timeout: float | int
        :rtype: WebElement
        """
        elements = self.find_all_last_children(self.find_all(locator, timeout))
        element = self.try_to_find(locator, timeout)
        element.send_keys(choice)
        for element in elements:
            if element.text == choice:
                element.click()
                return element

    def multi_select_from_dropdown(self, locator_open_list, locator_list, choice, timeout=0):
        """ select a choice from a multi drop down list
        :type locator_open_list: tuple(str, str | list[WebElement] | WebElement)
        :type locator_list: tuple(str, str | list[WebElement] | WebElement)
        :type choice: str
        :type timeout: float | int
        :rtype: WebElement
        """
        element_to_open_or_close_list = self.click(locator_open_list, timeout)
        elements = self.find_all_last_children(self.find_all(locator_list, timeout))
        for element in elements:
            if element.text == choice:
                element.click(timeout=timeout)
                element_to_open_or_close_list.click(timeout=timeout)
                return element

    def replace_url(self, pattern, replace):
        """ replace url pattern
        :type pattern: str
        :type replace: str
        """
        self.driver.get(self.driver.current_url.replace(pattern, replace))

    def try_to_click_until_element_is_created(self, locator_to_click, locator_of_created_element,
                                              retries=7, timeout=2, delay=POLL_FREQUENCY):
        """ try to click on element, check if condition element is created, if not, click again.
        return True for success and NoSuchElementException for failure,
        if an exception occurred in the last try, it will be returned.

        :type locator_to_click: tuple(str, str | list[WebElement] | WebElement)
        :type locator_of_created_element: tuple(str, str | list[WebElement] | WebElement)
        :type retries: int
        :type timeout: float | int
        :type delay: float | int
        :rtype: bool | Exception
        """
        for i in range(1+retries):
            t = time()
            try:
                initial_results = self.try_to_find_all(locator_of_created_element)
                self.click(locator_to_click, timeout)
                if len(self.try_to_find_all(locator_of_created_element, timeout)) > len(initial_results):
                    return True
                elif i == retries:
                    return NoSuchElementException("element might have been clicked but nothing happened")
            except Exception as e:
                if i == retries:
                    return e
            dynamic_delay(t, delay)

    def click_until_element_is_created(self, locator_to_click, locator_of_created_element,
                                       retries=7, timeout=2, delay=POLL_FREQUENCY):
        """ click on element, check if condition element is created, if not, click again.
        return True for success raise NoSuchElementException for failure.

        :type locator_to_click: tuple(str, str | list[WebElement] | WebElement)
        :type locator_of_created_element: tuple(str, str | list[WebElement] | WebElement)
        :type retries: int
        :type timeout: float | int
        :type delay: float | int
        :rtype: list[WebElement]
        """
        for i in range(1+retries):
            t = time()
            try:
                initial_results = self.try_to_find_all(locator_of_created_element)
                self.click(locator_to_click, timeout)
                if len(self.try_to_find_all(locator_of_created_element, timeout)) > len(initial_results):
                    return True
                elif i == retries:
                    raise NoSuchElementException("element might have been clicked but nothing happened")
            except Exception as e:
                if i == retries:
                    raise NoSuchElementException("element might have been clicked but nothing happened") from e
            dynamic_delay(t, delay)

    def try_to_click_until_condition_as_expected(self, locator_to_click, locator_condition,
                                                 condition_expected_results,
                                                 retries=7, timeout=2, delay=POLL_FREQUENCY):
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
        for i in range(1+retries):
            t = time()
            try:
                self.click(locator_to_click, timeout)
                if len(self.try_to_find_all(locator_condition, timeout)) == condition_expected_results:
                    return element_condition
            except:
                pass
            dynamic_delay(t, delay)
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
                self.wait(driver, timeout).until(EC.element_to_be_clickable(Locator.element(locator_to_click))).click()
                element_condition = self.try_to_find_elements_explicitly(locator_condition, timeout, driver)
                if len(element_condition) == condition_expected_results:
                    return element_condition
            except:
                pass
            dynamic_delay(t, delay)
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
                self.wait(driver, timeout).until(EC.element_to_be_clickable(Locator.element(locator_to_click))).click()
                element_condition = self.try_to_find_elements_explicitly(locator_condition, timeout, driver)
                if len(element_condition) <= condition_expected_results:
                    return element_condition
            except:
                pass
            dynamic_delay(t, delay)
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
                    EC.element_to_be_clickable(Locator.element(locator_to_click))).click()
                element_condition = self.try_to_find_elements_explicitly(locator_condition, timeout, driver)
                if len(element_condition) <= condition_expected_results:
                    return element_condition
            except:
                pass
            dynamic_delay(t, delay)
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
            dynamic_delay(t, delay)
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
            dynamic_delay(t, delay)
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
            self.wait(driver, timeout).until(EC.element_to_be_clickable(Locator.element(element))).click()
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
