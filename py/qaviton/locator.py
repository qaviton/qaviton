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


from appium.webdriver.webelement import WebElement
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from qaviton.utils.condition import value_in_many_any


class ByExtension(By):
    """
    This is an extension to the By class
    use this class to choose a locating strategy for web elements!
    """
    ELEMENT = 'element'
    ELEMENTS = 'elements'
    INDEX = 'index'


class ByExtensionMap:
    """
    This extension is intended for mappings in the By class
    """
    CLS = 'class'
    CSS = 'css'
    TEXT = 'text'
    ATTRIBUTE_NAME = 'attribute name'


class Locator:
    """ this is the WebPage element webLocator class
        it is intended to be inherited by other locators of real pages.
        place all common search methods under this super class:

        format method:
            is used only when a paired search (list/tuple that consists of 2 values)
            is required to change the format of its index[1] value.
            example usage:

                import Locator

                class Locator(Locator):
                    button1 = ('id', 'button{}-id')
                    name = ('text', '{name}')

                webLocator = Locator

                print(webLocator.format(webLocator.button1, 1))
                print(webLocator.format(webLocator.common.name, name="louis bow"))

                >> ['id', 'button1-id']
                >> ['text', 'louis bow']

        element method:
            give it an element and get in return a tuple like so:
            (webLocator.element(element))

        text method:
            give it a text and get in return a tuple like so:
            ('text', element)

        __call__ method:
            give it any attribute name & value and get in return a tuple like so:
            (<attribute name string>, <attribute value string>)
    """

    class BY(ByExtension, ByExtensionMap, MobileBy):
        pass

    @staticmethod
    def format(locator, *args, **kw):
        """
        :type locator: tuple
        :rtype: tuple
        """
        if len(locator) > 1:
            if isinstance(locator[1], str):
                return locator[0], locator[1].format(*args, **kw)

    @staticmethod
    def add(locator, value):
        """
        :type locator: tuple
        :type value: str
        :rtype: tuple
        """
        if len(locator) > 1:
            return locator[0], locator[1] + value

    @staticmethod
    def xpath_translator(by, value):
        return By.XPATH, "//*[@{}='{}']".format(by, value)

    @staticmethod
    def any(locator):
        """
        this method maps the element locating strategy to its value
        :type locator: tuple
                example: webLocator=('class', 'top.right')
        """
        by, value = locator

        # match to existing strategies
        if value_in_many_any(by, (vars(ByExtension).values(), vars(By).values(), vars(MobileBy).values())):
            return locator

        # map to extension strategies
        elif by == ByExtensionMap.CLS:
            return Locator.cls(value)
        elif by == ByExtensionMap.CSS:
            return Locator.css(value)
        elif by == ByExtensionMap.TEXT:
            return Locator.text(value)
        elif by == ByExtensionMap.ATTRIBUTE_NAME:
            return Locator.attribute_name(value)

        # find element using any attribute
        else:
            by, value = Locator.xpath_translator(by, value)
        return by, value

    @staticmethod
    def index(locator, index=0):
        """ return an element from a list
        :type locator: tuple
        :param index: what element to return """
        return ByExtension.INDEX, index, locator

    @staticmethod
    def list(*list_of_locators):
        """ return a mapped list of locators
        :type list_of_locators: list or tuple
        :param list_of_locators: a list of locator tuples """
        return [locator for locator in list_of_locators]

    @staticmethod
    def tuple(*tuple_of_locators):
        """ return a mapped tuple of locators
        :type tuple_of_locators: tuple or list
        :param tuple_of_locators: a tuple of locator tuples """
        return tuple_of_locators

    @staticmethod
    def element(web_element):
        """ return a mapped web element
        :type web_element: WebElement """
        return ByExtension.ELEMENT, web_element

    @staticmethod
    def elements(list_of_web_elements):
        """ return a mapped list of web elements
        :type list_of_web_elements: list[WebElement] """
        return ByExtension.ELEMENTS, list_of_web_elements

    @staticmethod
    def attribute_name(attribute_name_locator: str):
        """ return a mapped web element by its attribute name"""
        return By.XPATH, "//*[starts-with(@{},'')]".format(attribute_name_locator)

    @staticmethod
    def text(text_locator: str):
        """ return a mapped web element by its text"""
        return By.XPATH, "//*[{}()='{}']".format(ByExtensionMap.TEXT, text_locator)

    @staticmethod
    def xpath(xpath_locator: str):
        """ return a mapped web element by xpath"""
        return By.XPATH, xpath_locator

    @staticmethod
    def css(css_locator: str):
        """ return a mapped web element by css"""
        return By.CSS_SELECTOR, css_locator

    @staticmethod
    def cls(class_locator: str):
        """ return a mapped web element by its class"""
        return By.CLASS_NAME, class_locator

    @staticmethod
    def id(id_locator: str):
        """ return a mapped web element by its id"""
        return By.ID, id_locator

    @staticmethod
    def link_text(link_text_locator: str):
        """ return a mapped web element by its link text"""
        return By.LINK_TEXT, link_text_locator

    @staticmethod
    def partial_link_text(partial_link_text_locator: str):
        """ return a mapped web element by its partial link text"""
        return By.PARTIAL_LINK_TEXT, partial_link_text_locator

    @staticmethod
    def tag_name(tag_name_locator: str):
        """ return a mapped web element by its html tag name"""
        return By.TAG_NAME, tag_name_locator

    @staticmethod
    def name(name_locator: str):
        """ return a mapped web element by its name property"""
        return By.NAME, name_locator

    @staticmethod
    def ios_predicate(ios_predicate_locator: str):
        """ return a mapped web element by its ios predicate string"""
        return MobileBy.IOS_PREDICATE, ios_predicate_locator

    @staticmethod
    def ios_ui_automation(ios_ui_automation_locator: str):
        """ return a mapped web element by its ios ui automation"""
        return MobileBy.IOS_UIAUTOMATION, ios_ui_automation_locator

    @staticmethod
    def ios_class_chain(ios_class_chain_locator: str):
        """ return a mapped web element by its ios class chain"""
        return MobileBy.IOS_CLASS_CHAIN, ios_class_chain_locator

    @staticmethod
    def android_ui_automation(android_ui_automation_locator: str):
        """ return a mapped web element by its android ui automation"""
        return MobileBy.ANDROID_UIAUTOMATOR, android_ui_automation_locator

    @staticmethod
    def accessibility_id(accessibility_id_locator: str):
        """ return a mapped web element by its accessibility id"""
        return MobileBy.ACCESSIBILITY_ID, accessibility_id_locator

    @staticmethod
    def image(image_locator: str):
        """ return a mapped web element by image"""
        return MobileBy.IMAGE, image_locator



















