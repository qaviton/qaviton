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

"""The WebDriver implementation."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.command import Command
from qaviton.drivers.common.web_functions import WebFunctions
from qaviton.drivers.common.webelement import WebElement
from qaviton.drivers.support import expected_conditions_extension as EC
from qaviton.locator import Locator


class WebDriver(WebFunctions):
    """
    Controls a browser by sending commands to a remote server.
    This server is expected to be running the WebDriver wire protocol
    as defined at
    https://github.com/SeleniumHQ/selenium/wiki/JsonWireProtocol

    :Attributes:
     - session_id - String ID of the browser session started and controlled by this WebDriver.
     - capabilities - Dictionary of effective capabilities of this browser session as returned
         by the remote server. See https://github.com/SeleniumHQ/selenium/wiki/DesiredCapabilities
     - command_executor - remote_connection.RemoteConnection object used to execute commands.
     - error_handler - errorhandler.ErrorHandler object used to handle errors.
    """

    _web_element_cls = WebElement

    def click(self, locator, timeout=0, index=0):
        """ click on an element
        :type locator: tuple(str, str | list[WebElement] | WebElement)
        :type timeout: int
        :type index: int
        :rtype: WebElement
        """
        element = WebDriverWait(self, timeout).until(EC.element_to_be_clickable(locator, index))
        element._execute(Command.CLICK_ELEMENT)
        return element

    def get_element_last_children(self, element, timeout=3):
        """ get the last elements in the tree from the root element
        :type element: WebElement
        :rtype: list[WebElement]
        """
        locator = Locator.xpath('./*')
        elements = []
        while True:
            try:
                elements = element.find_all(locator, timeout)
                locator = (locator[0], locator[1] + '/*')
            except:
                return elements

    def get_elements_last_children(self, elements):
        """ get the last elements in the tree from the root element
        :type elements: list[WebElement]
        :rtype: list[WebElement]
        """
        children_elements = []
        for element in elements:
            children_elements += self.get_element_last_children(element)
        return children_elements

    def get_element_children(self, element, timeout=3):
        """ get the last element in the tree from the root element
        :type element: WebElement
        :rtype: list[WebElement] | []
        """
        try:
            return element.find_all(Locator.xpath('./*'), timeout)
        except:
            return []

    def get_elements_children(self, elements):
        """:rtype: list[WebElement]"""
        children_elements = []
        for element in elements:
            children_elements += self.get_element_children(element)
        return children_elements






















