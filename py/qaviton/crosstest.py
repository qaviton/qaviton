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

"""cross-platform testing implementation"""

from selenium.webdriver.remote.file_detector import UselessFileDetector
from selenium.webdriver.remote.command import Command
from threaders import threaders
from qaviton.drivers.webdriver import WebDriver
from qaviton.drivers.mobile_driver import MobileDriver
from qaviton import settings
from qaviton.exceptions import MissingRequiredCapabilitiesException, DriverConnectionException


# TODO: add more platforms

class API:
    """values need to equal vars(Platforms())"""
    WEB = WebDriver
    MOBILE = MobileDriver
    # IoT = 'iot'
    # CLOUD = 'cloud'
    # PC = 'pc'
    # CODE = 'code'
    # DB = 'db'


class Platforms:
    """all the testing platforms with drivers & desired capabilities"""

    def __init__(self, sessionTimeout: int = 600):
        self.platform_list = []
        self.sessionTimeout = sessionTimeout
        self.web = WebPlatform(self)
        self.mobile = MobilePlatform(self)
        # self.iot = IoTPlatform(self)
        # self.cloud = CloudPlatform(self)
        # self.pc = PCPlatform(self)
        # self.code = CodePlatform(self)
        # self.db = DBPlatform(self)

    def get(self):
        """:rtype: [{}]"""
        return self.platform_list


class _Platform:
    def __init__(self, platforms: Platforms, api):
        self.platforms = platforms
        self.api = api

    def __call__(self, platform):
        """ add platforms to test against
        :param platform: send dictionary of desired capabilities or a list of them
        :type platform: dict or list
        """
        return self.add(platform)

    def add(self, platform):
        if isinstance(platform, list):
            for p in platform:
                self.add(p)
        self.platforms.platform_list.append(Platform(platform))
        return self


class WebPlatform(_Platform):
    """ The WebPlatform is using Selenium Remote Webdriver API:
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

    def __init__(self, platforms: Platforms):
        super(self.__class__, self).__init__(platforms, API.WEB)
        self.command_executor = settings.webdriver_url

    def __call__(self, desired_capabilities, command_executor=None,
                 browser_profile=None, proxy=None,
                 keep_alive=False, file_detector=None, options=None):
        """
        Add a new platform of webdriver configuration that will issue commands using the wire protocol.

            :Args:
                 - app - your app url/file
                 - size - window size; can be 'max', 'min', '800x600' or None for headless/nonesizable browsers
                 - command_executor - Either a string representing URL of the remote server or a custom
                     remote_connection.RemoteConnection object. Defaults to 'http://127.0.0.1:4444/wd/hub'.
                 - desired_capabilities - A dictionary of capabilities to request when
                     starting the browser session. Required parameter.
                 - browser_profile - A selenium.webdriver.firefox.firefox_profile.FirefoxProfile object.
                     Only used if Firefox is requested. Optional.
                 - proxy - A selenium.webdriver.common.proxy.Proxy object. The browser session will
                     be started with given proxy settings, if possible. Optional.
                 - keep_alive - Whether to configure remote_connection.RemoteConnection to use
                     HTTP keep-alive. Defaults to False.
                 - file_detector - Pass custom file detector object during instantiation. If None,
                     then default LocalFileDetector() will be used.
                 - options - instance of a driver options.Options class
        """
        if command_executor is None:
            command_executor = self.command_executor

        platform = locals()
        del platform['self']
        platform['api'] = self.api
        super(self.__class__, self).__call__(platform)


class MobilePlatform(_Platform):

    def __init__(self, platforms):
        super(self.__class__, self).__init__(platforms, API.MOBILE)
        self.command_executor = settings.mobiledriver_url

    def __call__(self, desired_capabilities, command_executor=settings.mobiledriver_url,
                 browser_profile=None, proxy=None, keep_alive=False):
        """
        Add a new platform of webdriver configuration that will issue commands using the wire protocol.

            :Args:
                 - app - your app url/file
                 - size - window size; can be 'max', 'min', '800x600' or None for headless/nonesizable browsers
                 - command_executor - Either a string representing URL of the remote server or a custom
                     remote_connection.RemoteConnection object. Defaults to 'http://127.0.0.1:4444/wd/hub'.
                 - desired_capabilities - A dictionary of capabilities to request when
                     starting the browser session. Required parameter.
                 - browser_profile - A selenium.webdriver.firefox.firefox_profile.FirefoxProfile object.
                     Only used if Firefox is requested. Optional.
                 - proxy - A selenium.webdriver.common.proxy.Proxy object. The browser session will
                     be started with given proxy settings, if possible. Optional.
                 - keep_alive - Whether to configure remote_connection.RemoteConnection to use
                     HTTP keep-alive. Defaults to False.
        """
        if command_executor is None:
            command_executor = self.command_executor

        platform = locals()
        del platform['self']
        platform['api'] = self.api
        super(self.__class__, self).__call__(platform)


# class IoTPlatform(Platform):
#
#     driver_url = WebPlatform.driver_url
#
#     def __init__(self, platforms):
#         super(self.__class__, self).__init__(platforms, API.IoT)
#
#
# class CloudPlatform(Platform):
#
#     driver_url = WebPlatform.driver_url
#
#     def __init__(self, platforms):
#         super(self.__class__, self).__init__(platforms, API.CLOUD)
#
#
# class PCPlatform(Platform):
#
#     driver_url = WebPlatform.driver_url
#
#     def __init__(self, platforms):
#         super(self.__class__, self).__init__(platforms, API.PC)
#
#
# class CodePlatform(Platform):
#
#     driver_url = WebPlatform.driver_url
#
#     def __init__(self, platforms):
#         super(self.__class__, self).__init__(platforms, API.CODE)
#
#
# class DBPlatform(Platform):
#
#     driver_url = WebPlatform.driver_url
#
#     def __init__(self, platforms):
#         super(self.__class__, self).__init__(platforms, API.DB)


class Platform:
    def __init__(self, platform: dict):

        self.platform = dict(platform)

    def setup(self, request):
        """ use this from inside the test to get a matching
        :param request: pytest fixture request
        :rtype: TestCase
        """
        name = request.node.name
        self.platform["desired_capabilities"]["name"] = name
        self.platform["desired_capabilities"]["logName"] = name + '.log'
        self.platform["desired_capabilities"]["videoName"] = name + '.mp4'
        self.platform["desired_capabilities"]["enableVNC"] = True
        self.platform["desired_capabilities"]["enableVideo"] = True
        for k in ('app', 'sessionTimeout', 'screenResolution'):
            if k not in self.platform["desired_capabilities"].keys():
                raise MissingRequiredCapabilitiesException("missing capability: "+k)
        return TestCase(self.platform)


class TestCase:
    def __init__(self, platform):
        self.platform = platform
        self.name = platform["desired_capabilities"]["name"]

    def driver(self, platform=None, connection_timeout=None, page_load_timeout=None, retry=None):
        """return desired driver
        if platform is a list of platforms then you can use the drivers function

        platform = {desired_capabilities, app, size, command_executor,
                 browser_profile, proxy, keep_alive, file_detector, options}

        :param platform: dictionary with:
                    command_executor: it's the remote driver url: default='http://127.0.0.1:4444/wd/hub'
                    desired_capabilities: {"browserName": "chrome", "version": "67.0", "platform": "WINDOWS"}
                    browser_profile=None, proxy=None, keep_alive=False, file_detector=None, options=None
        :param connection_timeout:
        :param page_load_timeout:
        :param retry:
        :rtype: WebDriver or MobileDriver
        """

        if platform is None:
            platform = self.platform

        if platform['api'] == API.WEB:
            # set retry
            if retry is None:
                retry = settings.webdriver_retries

            # set page load timeout
            if connection_timeout is None:
                connection_timeout = settings.webdriver_connection_timeout

            # get remote connection
            for r in range(retry+1):
                try:
                    # from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
                    # driver: WebDriver = platform['api'](
                    #     command_executor=platform['command_executor'],
                    #     desired_capabilities=platform['desired_capabilities'],
                    #     browser_profile=platform['browser_profile'],
                    #     proxy=platform['proxy'],
                    #     keep_alive=platform['keep_alive'],
                    #     file_detector=platform['file_detector'],
                    #     options=platform['options'])
                    # get driver from thread with timeout for connection
                    driver: WebDriver = threaders.thread(
                        platform['api'],
                        command_executor=platform['command_executor'],
                        desired_capabilities=platform['desired_capabilities'],
                        browser_profile=platform['browser_profile'],
                        proxy=platform['proxy'],
                        keep_alive=platform['keep_alive'],
                        file_detector=platform['file_detector'],
                        options=platform['options']
                    ).get_and_join(timeout=connection_timeout)
                    break
                except Exception as e:
                    if r == retry:
                        raise DriverConnectionException("webdriver connection could not be established") from e

            # set local file detector
            driver.file_detector = UselessFileDetector()

            # set page load timeout
            if page_load_timeout is None:
                page_load_timeout = settings.webdriver_page_load_timeout

            # get app url
            for r in range(retry + 1):
                try:
                    # page load from thread with timeout
                    threaders.thread(driver.execute, Command.GET, {'url': platform["desired_capabilities"]["app"]}).get_and_join(timeout=page_load_timeout)
                    # driver.get(platform["desired_capabilities"]["app"])
                    break
                except Exception as e:
                    if r == retry:
                        driver.quit()
                        raise Exception("url could not be loaded") from e

            # try:
            #     resolution = platform["desired_capabilities"]['screenResolution'].split("x")
            #     # driver.execute_script("window.moveTo(arguments[0], arguments[1]);", 0, 0)
            #     try:
            #         driver.set_window_position(0, 0)
            #     except Exception as e:
            #         print(e)
            #     try:
            #         driver.set_window_size(int(resolution[0]), int(resolution[1]))
            #     except:
            #         driver.maximize_window()
            # except Exception as e:
            #     # driver.quit()
            #     # raise RequiredCapabilitiesException("setting screen size failed: please make sure your screenResolution capability is correct - example: 800x600x24 ") from e
            #     print("cannot set the screen size")

        if platform['api'] == API.MOBILE:
            # set retry
            if retry is None:
                retry = settings.mobiledriver_retries
            # set page load timeout
            if connection_timeout is None:
                connection_timeout = settings.mobiledriver_connection_timeout
            for r in range(retry + 1):
                try:
                    driver: MobileDriver = threaders.thread(
                        platform['api'],
                        command_executor=platform['command_executor'],
                        desired_capabilities=platform['desired_capabilities'],
                        browser_profile=platform['browser_profile'],
                        proxy=platform['proxy'],
                        keep_alive=platform['keep_alive']
                    ).get_and_join(timeout=connection_timeout)
                    break
                except Exception as e:
                    if r == retry:
                        try:
                            driver.quit()
                        except:
                            pass
                        raise DriverConnectionException("webdriver connection could not be established") from e
        return driver

    def drivers(self, platforms=None):
        """return the desired drivers
        :param command_executor:  it's the remote driver url: default='http://127.0.0.1:4444/wd/hub'
        :param desired_capabilities: [{"browserName": "chrome", "version": "67.0", "platform": "WINDOWS"}]
        :type desired_capabilities: [{}]
        :param args: ({"browser_profile": None, "proxy": None, "keep_alive": False, "file_detector": None, "options": None}):
        :type platforms: [{}]
        :rtype: [WebDriver or MobileDriver]
        """
        if platforms is None:
            platforms = self.platform
        drivers = []
        for i in platforms:
            drivers.append(self.driver(i))
        return drivers


# generate test id
id = lambda i: str(i.id)


# get driver from platform
def get_driver(platform: Platform, request):
    return platform.setup(request).driver()


# get drivers from platform
def get_drivers(platform: Platform, request):
    return platform.setup(request).drivers()
