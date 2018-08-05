from appium.webdriver import Remote as MobileDriver
from selenium.webdriver import Remote as WebDriver
from qaviton.utils import organize
from qaviton import settings


class TestingTypes:
    """values need to equal vars(Platforms())"""
    WEB = 'web'
    MOBILE = 'mobile'
    IoT = 'iot'
    CLOUD = 'cloud'
    PC = 'pc'
    CODE = 'code'
    DB = 'db'


class Platforms:
    """all the testing platforms with drivers & desired capabilities"""

    def __init__(self):
        self.list_of_desired_capabilities_and_testing_types = []
        self.web = WebPlatform(self)
        self.mobile = MobilePlatform(self)
        self.iot = IoTPlatform(self)
        self.cloud = CloudPlatform(self)
        self.pc = PCPlatform(self)
        self.code = CodePlatform(self)
        self.db = DBPlatform(self)

    @property
    def get(self):
        """:rtype: [{}]"""
        return self.list_of_desired_capabilities_and_testing_types


class Platform:
    def __init__(self, platforms: Platforms, testing_type):
        self.platforms = platforms
        self.testing_type = testing_type
        self.list_of_desired_capabilities_and_testing_type = []

    def add(self, desired_capabilities: dict):
        descaps_testtype = dict(desired_capabilities=desired_capabilities, testing_type=self.testing_type)
        self.platforms.list_of_desired_capabilities_and_testing_types.append(descaps_testtype)
        self.list_of_desired_capabilities_and_testing_type.append(
            dict(desired_capabilities=desired_capabilities, testing_type=self.testing_type))

    def adds(self, desired_capabilities: list):
        for i in desired_capabilities:
            self.add(i)

    @property
    def get(self):
        """:rtype: [{}]"""
        return self.list_of_desired_capabilities_and_testing_type


class WebPlatform(Platform):
    def __init__(self, platforms):
        super(self.__class__, self).__init__(platforms, TestingTypes.WEB)


class MobilePlatform(Platform):
    def __init__(self, platforms):
        super(self.__class__, self).__init__(platforms, TestingTypes.MOBILE)


class IoTPlatform(Platform):
    def __init__(self, platforms):
        super(self.__class__, self).__init__(platforms, TestingTypes.IoT)


class CloudPlatform(Platform):
    def __init__(self, platforms):
        super(self.__class__, self).__init__(platforms, TestingTypes.CLOUD)


class PCPlatform(Platform):
    def __init__(self, platforms):
        super(self.__class__, self).__init__(platforms, TestingTypes.PC)


class CodePlatform(Platform):
    def __init__(self, platforms):
        super(self.__class__, self).__init__(platforms, TestingTypes.CODE)


class DBPlatform(Platform):
    def __init__(self, platforms):
        super(self.__class__, self).__init__(platforms, TestingTypes.DB)


class Model:
    def __init__(self, desired_capabilities=None, driver_url=settings.driver_url,
                 testing_type=TestingTypes.PC, data=None):

        # set testing type: web, mobile, iot
        self.testing_type = testing_type

        if desired_capabilities is not None:
            # set test desired capabilities for running driver
            self.desired_capabilities = desired_capabilities

            # set driver url
            self.driver_url = driver_url

            # set driver type
            if self.testing_type == TestingTypes.WEB:
                self.driver_api = WebDriver
            elif self.testing_type == TestingTypes.MOBILE:
                self.driver_api = MobileDriver

        # send data for data driven testing
        if data is not None:
            self.data = data

    def driver(self, command_executor=None, desired_capabilities=None, **kw):
        """return the desired driver
        if desired_capabilities is a list of platforms then you can use the drivers function
        :param command_executor: it's the remote driver url: default='http://127.0.0.1:4444/wd/hub'
        :param desired_capabilities: {"browserName": "chrome", "version": "67.0", "platform": "WINDOWS"}
        :param kw: browser_profile=None, proxy=None, keep_alive=False, file_detector=None, options=None
        :rtype: WebDriver || MobileDriver
        """
        if command_executor is None:
            command_executor = self.driver_url
        if desired_capabilities is None:
            desired_capabilities = self.desired_capabilities

        return self.driver_api(command_executor=command_executor,
                               desired_capabilities=desired_capabilities, **kw)

    def drivers(self, command_executor=None, desired_capabilities=None, *args):
        """return the desired drivers
        :param command_executor:  it's the remote driver url: default='http://127.0.0.1:4444/wd/hub'
        :param desired_capabilities: [{"browserName": "chrome", "version": "67.0", "platform": "WINDOWS"}]
        :type desired_capabilities: [{}]
        :param args: ({"browser_profile": None, "proxy": None, "keep_alive": False, "file_detector": None, "options": None}):
        :type args: ({})
        :rtype: [WebDriver || MobileDriver]
        """
        if command_executor is None:
            command_executor = self.driver_url
        if desired_capabilities is None:
            desired_capabilities = self.desired_capabilities
        args = list(args)
        while len(args) < len(desired_capabilities):
            args.append({})
        drivers = []
        for i in range(len(desired_capabilities)):
            drivers.append(
                self.driver(command_executor=command_executor, desired_capabilities=desired_capabilities[i], **args[i]))
        return drivers


class Models:
    def __init__(self, platforms: Platforms, driver_url=settings.driver_url, data=None):
        if isinstance(data, list):
            organized_data = organize.add(platforms.get, dict(data=data))
            self.models = [Model(driver_url=driver_url, **i) for i in organized_data]
        else:
            self.models = [Model(driver_url=driver_url, data=data, **i) for i in platforms.get]

    @property
    def get(self):
        """:rtype: [Model]"""
        return self.models
