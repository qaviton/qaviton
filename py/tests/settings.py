from qaviton import crosstest
from qaviton.utils import path


app = [
    # web
    'file://' + path.of(__file__)('../../apps/ContactManager/ContactManager.html'),
    # mobile
    path.of(__file__)('../../apps/ContactManager/ContactManager.apk')
]

screenResolution = "800x600x24"
sessionTimeout = 60


# create cross-platform testing object
platforms = crosstest.Platforms()


# add chrome browser support
platforms.web({
    'browserName': "chrome",
    'version': "",
    'platform': "ANY",
    'app': app[0],
    'screenResolution': screenResolution,
    'sessionTimeout': sessionTimeout,
    'enableVNC': True,
    'enableVideo': True,
    'name': "{}",
    'videoName': "{}.mp4",
    'logName': "{}.log"})


# add firefox browser support
platforms.web({
    "browserName": "firefox",
    "marionette": True,
    "acceptInsecureCerts": True,
    'app': app[0],
    'screenResolution': screenResolution,
    'sessionTimeout': sessionTimeout,
    'enableVNC': True,
    'enableVideo': True,
    'name': "{}",
    'videoName': "{}.mp4",
    'logName': "{}.log"})


# add internet explorer browser support
platforms.web({
    "browserName": "internet explorer",
    "version": "",
    "platform": "WINDOWS",
    'app': app[0],
    'screenResolution': screenResolution,
    'sessionTimeout': sessionTimeout,
    'enableVNC': True,
    'enableVideo': True,
    'name': "{}",
    'videoName': "{}.mp4",
    'logName': "{}.log"})


# add android mobile support
platforms.mobile({
    'platformName': "Android",
    'platformVersion': "6.0",
    'deviceName': "emulator-5554",
    'app': app[1],
    'appPackage': 'com.example.android.contactmanager',
    'appActivity': '.ContactManager',
    'screenResolution': screenResolution,
    'sessionTimeout': sessionTimeout,
    'enableVNC': True,
    'enableVideo': True,
    'name': "{}",
    'videoName': "{}.mp4",
    'logName': "{}.log"})
