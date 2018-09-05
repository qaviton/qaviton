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

from time import sleep
from selenium.webdriver import Remote
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import POLL_FREQUENCY
from qaviton.drivers.common.webdriver import WebDriver as WE
from qaviton.drivers.common.webelement import WebElement


class WebDriver(WE, Remote):
    """
    Controls a browser by sending commands to a remote server.
    This server is expected to be running the WebDriver wire protocol
    as defined at
    https://github.com/SeleniumHQ/selenium/wiki/JsonWireProtocol

    :Attributes:
     - session_id - String ID of the browser session started and controlled by this WebDriver.
     - capabilities - Dictionaty of effective capabilities of this browser session as returned
         by the remote server. See https://github.com/SeleniumHQ/selenium/wiki/DesiredCapabilities
     - command_executor - remote_connection.RemoteConnection object used to execute commands.
     - error_handler - errorhandler.ErrorHandler object used to handle errors.
    """

    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None, browser_profile=None, proxy=None,
                 keep_alive=False, file_detector=None, options=None):

        Remote.__init__(self, command_executor, desired_capabilities, browser_profile,
                        proxy, keep_alive, file_detector, options)

    def create_web_element(self, element_id):
        """
        Creates a web element with the specified element_id.
        Overrides method and appium Selenium WebDriver in order to always create the qaviton extended WebElement
        """
        return WebElement(self, element_id)

    def zoom(self, percent=200, *args, **kwargs):
        """ zoom like appium for selenium (will not work for all browsers)
            Zooms in on an element a certain amount

                :Args:
                 - percent - (optional) amount to zoom. Defaults to 200%
                 - args/kwargs - catch any unwanted arguments that may come from appium zoom

                :Usage:
                    driver.zoom(150)
                    driver.zoom(50)
                    driver.zoom(100)
                """
        self.execute_script("document.body.style.zoom = arguments[0]+'%';", str(percent))
        return self

    def drag_and_drop(self, origin_el, destination_el):
        """Drag the origin element to the destination element

        :Args:
         - originEl - the element to drag
         - destinationEl - the element to drag to
        """
        ActionChains(self).drag_and_drop(origin_el, destination_el).perform()
        return self

    def scroll_element_into_view(self, element, retries=4):
        """ selenium only: scrolling function to scroll until element is visible (whole window scroll)
        :type element: WebElement
        :param retries: integer bigger or equal to 0
        :rtype: WebElement
        """
        for retry in range(1+retries):
            try:
                self.execute_script("arguments[0].scrollIntoView(true);", element)
                return element
            except Exception as e:
                if retry == retries:
                    raise e
                sleep(POLL_FREQUENCY)
        return element

    def get_attributes(self, element):
        """ get all the attributes
        :rtype: dict
        """
        return self.execute_script(
            "var items = {}; "
            "for (index = 0; index < arguments[0].attributes.length; ++index) { "
            "items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; "
            "return items;",
            element)
