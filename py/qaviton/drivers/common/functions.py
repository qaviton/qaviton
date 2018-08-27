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
the WebFunctions class includes functions
that are common to both driver & element classes of any kind.
this common functionality will provide the best flexibility
possible for automating simple and complex scenarios
"""

from selenium.webdriver.support.ui import WebDriverWait
from qaviton.locator import ByExtension
from qaviton.locator import Locator


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
        return WebFunctions.find(self.locator, driver, self.index)


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
        return WebFunctions.find_all(self.locator, driver)


class WebFunctions:
    """this class is added to ~( webdriver & webelement )~
    to add same functionality to both driver & element
    """

    def heal(self, element, locators_to_heal, locators):
        """ find element attributes and try to send healing info to qaviton.com/proj/heal
        :type element: WebElement
        :type locators_to_heal: list
        :type locators: tuple
        :return:
        """
        pass

    def find(self, locator: tuple, timeout: int = 0, index=0):
        """find element with locator value
        :param locator: locate by method like id and value
        :param timeout: how long to search
        :param index: parameter for special cases
                  where a list of elements is in the locator,
                  the default element to return is elements[0]
        :rtype: WebElement
        """

        # use this locate method if timeout is 0
        def fast(locate):
            return self.find_element(*locate)

        # use this locate method if timeout > 0
        def slow(locate):
            return WebDriverWait(self, timeout).until(presence_of_element_located(locate))

        # classify locator method
        if locator[0] == ByExtension.INDEX:
            return self.find_all(locator[2])[locator[1]]
        by, value = Locator.any(locator)
        if by == ByExtension.ELEMENTS:
            return value[index]
        elif by == ByExtension.ELEMENT:
            return value

        # healing functionality
        elif by in (ByExtension.TUPLE, ByExtension.LIST):
            # choose finding method
            if timeout > 0:
                get = slow
            else:
                get = fast

            # set healing parameters
            locators_to_heal = []
            element = None
            for i in range(len(value)):
                try:
                    # find element
                    element = self.find(value[i])
                    break
                except Exception as e:
                    locators_to_heal.append(value[i])
                    if len(value) == i+1:
                        raise e

            # heal and return
            if len(locators_to_heal) > 0:
                self.heal(element, locators_to_heal, locator)
            return element

        # choose finding method
        if timeout > 0:
            get = slow
        else:
            get = fast

        # find element
        return get((by, value))

    def find_all(self, locator: tuple, timeout: int = 0):
        """find all elements with locator value
        :param timeout: how long to search
        :param locator: locate by method like id and value
        :rtype: list[WebElement]"""

        # use this locate method if timeout is 0
        def fast(locate):
            return self.find_elements(*locate)

        # use this locate method if timeout > 0
        def slow(locate):
            return WebDriverWait(self, timeout).until(presence_of_all_elements_located(locate))

        # classify locator method
        if locator[0] == ByExtension.INDEX:
            return self.find_all(locator[2])[locator[1]]
        by, value = Locator.any(locator)
        if by == ByExtension.ELEMENTS:
            return value
        elif by == ByExtension.ELEMENT:
            return [value]

        # healing functionality
        elif by in (ByExtension.TUPLE, ByExtension.LIST):
            # choose finding method
            if timeout > 0:
                get = slow
            else:
                get = fast

            # set healing parameters
            locators_to_heal = []
            elements = None
            for i in range(len(value)):
                try:
                    # find elements
                    elements = self.find_all(value[i])
                    break
                except Exception as e:
                    locators_to_heal.append(value[i])
                    if len(value) == i+1:
                        raise e

            # heal and return
            if len(locators_to_heal) > 0:
                self.heal(elements[0], locators_to_heal, locator)
            return elements

        # choose finding method
        if timeout > 0:
            get = slow
        else:
            get = fast

        # find elements
        return get((by, value))

    def get_elements_text(self, locator, timeout=0):
        """ get text from elements
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: list[str]
        """
        return [element.text for element in self.find_all(locator, timeout)]

    def try_to_find(self, locator: tuple, timeout=0, index=0):
        """try to find element
        :param index: parameter for special cases
                      where a list of elements is in the locator,
                      the default element to return is elements[0]
        :param timeout: how long to search
        :param locator: locate by method like id and value
        :rtype: WebElement | None"""
        try:
            return self.find(locator, timeout, index)
        except:
            return None

    def try_to_find_all(self, locator: tuple, timeout=0):
        """try to find elements
        :param timeout: how long to search
        :param locator: locate by method like id and value
        :rtype: list[WebElement]"""
        try:
            return self.find_all(locator, timeout)
        except:
            return []

    def try_to_get_elements_text(self, locator, timeout=0):
        """ get text from elements if any elements are located
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :rtype: list[str] | []
        """
        element_list, elements_text = self.try_to_find_all(locator, timeout), []
        for i in range(len(element_list)):
            try:
                elements_text.append(element_list[i].text)
            except:
                pass
        return elements_text
