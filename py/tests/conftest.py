import pytest
import datetime
import os
from tests.utils.helpers import ensure_dir


def pytest_configure(config):
    if not hasattr(config, "slaveinput"):
        current_day = (datetime.datetime.now().strftime("%Y_%m_%d_%H_%S"))
        ensure_dir("results")
        ensure_dir(os.path.join("results", current_day))
        result_dir = os.path.join(os.path.dirname(__file__), "results", current_day)
        ensure_dir(result_dir)
        result_dir_test_run = result_dir
        ensure_dir(os.path.join(result_dir_test_run, "screenshots"))
        ensure_dir(os.path.join(result_dir_test_run, "logcat"))
        config.screen_shot_dir = os.path.join(result_dir_test_run, "screenshots")
        config.logcat_dir = os.path.join(result_dir_test_run, "logcat")


class DeviceLogger:
    def __init__(self, logcat_dir, screenshot_dir):
        self.screenshot_dir = screenshot_dir
        self.logcat_dir = logcat_dir


@pytest.fixture(scope="session")
def device_logger(request):
    logcat_dir = request.config.logcat_dir
    screenshot_dir = request.config.screen_shot_dir
    return DeviceLogger(logcat_dir, screenshot_dir)


# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


DRIVER_URL = 'http://localhost:4723/wd/hub'
PLATFORM_NAME = 'Android'
PLATFORM_VERSION = '6.0'
DEVICE_NAME = 'emulator-5554'


desired_caps = dict(
    platformName=PLATFORM_NAME,
    platformVersion=PLATFORM_VERSION,
    deviceName=DEVICE_NAME)


desired_caps_app1 = dict(
    app=PATH('../../../../sample-code/apps/ContactManager/ContactManager.apk'),
    appPackage='com.example.android.contactmanager',
    appActivity='.ContactManager',
    **desired_caps)


desired_caps_app2 = dict(
    app=PATH('../../../../sample-code/apps/ApiDemos/bin/ApiDemos-debug.apk'),
    appPackage='com.example.android.contactmanager',
    appActivity='.ContactManager',
    **desired_caps)


apps = [
    PATH('../../../sample-code/apps/ApiDemos/bin/ApiDemos-debug.apk'),
    PATH('../../../sample-code/apps/ContactManager/ContactManager.apk'),
    "http://appium.github.io/appium/assets/ApiDemos-debug.apk"
]



platforms = {
    "web": [
        {
            "browserName": "android",
            "version": "",
            "platform": "ANDROID"
        },
        {
            "browserName": "chrome",
            "version": "67.0",
            "platform": "WINDOWS"
        },
        {
            "browserName": "firefox",
            "version": "58.0",
            "platform": "WINDOWS"
        },
        {
            "browserName": "internet explorer",
            "version": "10.0",
            "platform": "WINDOWS"
        },
        {
            "browserName": "android",
            "version": "",
            "platform": "ANDROID"
        }
    ],

    "mobile": [
        {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "emulator-5554"
        },
        {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "emulator-5554",
            "appPackage": "com.example.android.contactmanager",
            "appActivity": ".ContactManager"
        },
        {
            "platformName": "Android",
            "platformVersion": "6.0",
            "deviceName": "emulator-5554",
            "appActivity": ".graphics.TouchPaint",
            "app": apps[0],
            "appiumVersion": "1.3.4",
        }
    ]
}
