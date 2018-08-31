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
from qaviton.drivers.common.functions import WebFunctions
from qaviton.drivers.common.webelement import WebElement
from qaviton.drivers.support import expected_conditions as EC


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
        if timeout == 0:
            element = self.find(locator)
            element.click()
        else:
            element = WebDriverWait(self, timeout).until(EC.element_to_be_clickable(locator, index))
            element._execute(Command.CLICK_ELEMENT)
        return element

    def quit(self):
        """
        Quits the driver and closes every associated window.

        :Usage:
            driver.quit()
        """
        try:
            self.execute(Command.QUIT)
        except:
            pass
        finally:
            self.stop_client()

    @staticmethod
    def find_element_last_children(element, timeout=0):
        """ get the last elements in the tree from the root element
        :type element: WebElement
        :type timeout: int
        :rtype: list[WebElement] | []
        """
        return element.find_last_children(timeout)

    @staticmethod
    def find_elements_last_children(elements, timeout=0):
        """ get the last elements in the tree from the root element
        :type elements: list[WebElement]
        :type timeout: int
        :rtype: list[WebElement] | []
        """
        children_elements = []
        for element in elements:
            children_elements += element.find_last_children(timeout)
        return children_elements

    @staticmethod
    def find_element_children(element, timeout=0):
        """ get the last element in the tree from the root element
        :type element: WebElement
        :type timeout: int
        :rtype: list[WebElement] | []
        """
        return element.find_children(timeout)

    @staticmethod
    def get_elements_children(elements, timeout=0):
        """ get elements children
        :type timeout: int
        :rtype: list[WebElement] | []
        """
        children_elements = []
        for element in elements:
            children_elements += element.find_children(timeout)
        return children_elements

    @staticmethod
    def drag_to_offset(origin_el, xoffset, yoffset):
        """
        Holds down the left mouse button on the source element,
           then moves to the target offset and releases the mouse button.

        :Args:
         - source: The element to mouse down.
         - xoffset: X offset to move to.
         - yoffset: Y offset to move to.
         :type origin_el: WebElement
         :rtype: WebDriver
        """
        return origin_el.drag_to_offset(xoffset, yoffset)

    @staticmethod
    def hover(element):
        """ hover/move cursor to element
        :type element: WebElement
        :rtype: WebDriver
        """
        return element.hover()

    @staticmethod
    def hover_and_click(element):
        """ hover/move cursor to element and click
        :type element: WebElement
        :rtype: WebDriver
        """
        return element.hover_and_click()
















