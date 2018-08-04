from tests import conftest


def organize(data_lists):
    """
        data_lists = [(1,),(1,2,3),(1,2),(1,2,3,4)]
        will return:

        [[1, 1, 1, 1],[1, 1, 1, 2],[1, 1, 1, 3],[1, 1, 1, 4],[1, 1, 2, 1],[1, 1, 2, 2],
         [1, 1, 2, 3],[1, 1, 2, 4],[1, 1, 3, 1],[1, 1, 3, 2],[1, 1, 3, 3],[1, 1, 3, 4],
         [1, 2, 1, 1],[1, 2, 1, 2],[1, 2, 1, 3],[1, 2, 1, 4],[1, 2, 2, 1],[1, 2, 2, 2],
         [1, 2, 2, 3],[1, 2, 2, 4],[1, 2, 3, 1],[1, 2, 3, 2],[1, 2, 3, 3],[1, 2, 3, 4]]

    :type data_lists: []
    :rtype: []
    """
    try:
        data_lists.sort(key=len)

        all_possibilities = 1
        for i in range(len(data_lists)):
            all_possibilities *= len(data_lists[i])

        data = [[] for _ in range(all_possibilities)]

        looper = all_possibilities
        for data_list in data_lists:
            looper /= len(data_list)
            d = 0
            while d < all_possibilities:
                for i in data_list:
                    for _ in range(int(looper)):
                        data[d].append(i)
                        d += 1
        return data
    except ZeroDivisionError as e:
        raise ZeroDivisionError("empty lists are not allowed") from e


# data_lists = []
# organize(data_lists)
#
# data_lists = [(123, '5555'),(1,2,3,0,0),(1,2),(1,2,3,4)]
# organize(data_lists)
#
#
# data_lists = [(),(1,2,3),(1,2),(1,2,3,4)]
# organize(data_lists)
#

from appium.webdriver import Remote as MobileDriver
from selenium.webdriver import Remote as WebdDiver


class TestingTypes:
    WEB = 'WEB'
    MOBILE = 'MOBILE'
    IoT = 'IoT'
    CLOUD = 'CLOUD'
    PC = 'PC'


class Platforms:
    def __init__(self):
        self.web = []
        self.mobile = []
        self.iot = []
        self.cloud = []
        self.pc = []


class TestModel:
    def __init__(self, desired_capabilities=None, driver_url='http://127.0.0.1:4444/wd/hub',
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
                self.remote_driver = WebdDiver
            elif self.testing_type == TestingTypes.MOBILE:
                self.remote_driver = MobileDriver

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

        return self.remote_driver(command_executor=command_executor,
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


def create():
    pass
