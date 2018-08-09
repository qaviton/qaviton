from appium.webdriver import Remote as MobileDriver
from selenium.webdriver import Remote as WebDriver
from selenium.webdriver.remote.command import Command
from qaviton.utils import organize
from qaviton import settings
from threaders import threaders


# TODO: add more platforms

class TestAPI:
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

    def __init__(self):
        self.platform_list = []
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


class Platform:
    def __init__(self, platforms: Platforms, test_api):
        self.platforms = platforms
        self.test_api = test_api

    def __call__(self, platform):
        """ add platforms to test against
        :param platform: send dictionary of desired capabilities or a list of them
        :type platform: dict or list
        """
        self.add(platform)
        return self

    def add(self, platform):
        if isinstance(platform, list):
            for p in platform:
                self.add(p)
        self.platforms.platform_list.append(platform)
        return self


class WebPlatform(Platform):
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
        super(self.__class__, self).__init__(platforms, TestAPI.WEB)

    def __call__(self, desired_capabilities, app, size, command_executor,
                 browser_profile, proxy, keep_alive, file_detector, options):
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
        platform = locals()
        del platform['self']
        platform['api'] = self.test_api
        super(self.__class__, self).__call__(platform)

class MobilePlatform(Platform):

    def __init__(self, platforms):
        super(self.__class__, self).__init__(platforms, TestAPI.MOBILE)


# class IoTPlatform(Platform):
#
#     driver_url = WebPlatform.driver_url
#
#     def __init__(self, platforms):
#         super(self.__class__, self).__init__(platforms, TestAPI.IoT)
#
#
# class CloudPlatform(Platform):
#
#     driver_url = WebPlatform.driver_url
#
#     def __init__(self, platforms):
#         super(self.__class__, self).__init__(platforms, TestAPI.CLOUD)
#
#
# class PCPlatform(Platform):
#
#     driver_url = WebPlatform.driver_url
#
#     def __init__(self, platforms):
#         super(self.__class__, self).__init__(platforms, TestAPI.PC)
#
#
# class CodePlatform(Platform):
#
#     driver_url = WebPlatform.driver_url
#
#     def __init__(self, platforms):
#         super(self.__class__, self).__init__(platforms, TestAPI.CODE)
#
#
# class DBPlatform(Platform):
#
#     driver_url = WebPlatform.driver_url
#
#     def __init__(self, platforms):
#         super(self.__class__, self).__init__(platforms, TestAPI.DB)


class Model:
    def __init__(self, platform: dict, data=None):

        self.platform = platform

        # send data for data driven testing
        if data is not None:
            self.data = data

    def driver(self, platform=None, connection_timeout=None, page_load_timeout=None, retry=None):
        """return the desired driver
        if platform is a list of platforms then you can use the drivers function

        platform = {desired_capabilities, app, size, command_executor,
                 browser_profile, proxy, keep_alive, file_detector, options}

        :param command_executor: it's the remote driver url: default='http://127.0.0.1:4444/wd/hub'
        :param desired_capabilities: {"browserName": "chrome", "version": "67.0", "platform": "WINDOWS"}
        :param kw: browser_profile=None, proxy=None, keep_alive=False, file_detector=None, options=None
        :rtype: WebDriver or MobileDriver
        """
        if platform is None:
            platform = self.platform

        if platform['test_api'] == TestAPI.WEB:
            # set retry
            if retry is None:
                retry = settings.webdriver_retries

            # create thread for timeout actions
            pool = threaders.ThreadPool()

            # get remote connection
            for r in range(retry+1):
                try:
                    # get driver from thread with timeout for connection
                    driver: WebDriver = threaders.thread(
                        platform['test_api'],
                        command_executor=platform['command_executor'],
                        desired_capabilities=platform['desired_capabilities'],
                        browser_profile=platform['browser_profile'],
                        proxy=platform['proxy'],
                        keep_alive=platform['keep_alive'],
                        file_detector=platform['file_detector'],
                        options=platform['options']
                    ).get_and_join(timeout=settings.webdriver_connection_timeout)

                    break
                except Exception as e:
                    print(e)
                raise Exception("webdriver connection could not be established")

            # set page load timeout
            if page_load_timeout is None:
                page_load_timeout = settings.webdriver_page_load_timeout

            # get app url
            for r in range(retry + 1):
                try:
                    threaders.thread(driver.execute, Command.GET, {'url': platform["app"]}).get_and_join(timeout=page_load_timeout)
                    break
                except Exception as e:
                    print(e)
                finally:
                    pool.join()
                    driver.get(platform["app"])
                raise Exception("url could not be loaded")

            if platform["size"] is not None:
                try:
                    if platform["size"] == "max":
                        driver.maximize_window()
                    elif platform["size"] == "min":
                        driver.minimize_window()
                    elif ":" in platform["size"]:
                        size = platform["size"].split("x")
                        driver.set_window_size(int(size[0]), int(size[1]))
                except Exception as e:
                    raise ValueError("size capability valid values are: 'max', 'min', '800x600' or any set of numbers matching this format 'NxN'") from e
            driver.set_page_load_timeout(settings)

        if platform['test_api'] == TestAPI.MOBILE:
            driver = platform['test_api'](
                command_executor=platform['command_executor'],
                desired_capabilities=platform['desired_capabilities'],
                browser_profile=platform['browser_profile'],
                proxy=platform['proxy'],
                keep_alive=platform['keep_alive'])
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


class Models:
    def __init__(self, platforms: Platforms, command_executor='http://127.0.0.1:4444/wd/hub', data=None):
        if isinstance(data, list):
            organized_data = organize.add(platforms.get(), dict(data=data))
            self.models = [Model(driver_url=driver_url, **i) for i in organized_data]
        else:
            self.models = [Model(driver_url=driver_url, data=data, **i) for i in platforms.get()]

    def get(self):
        """:rtype: [Model]"""
        return self.models


# generate test id
id = lambda i: str(i.id)
