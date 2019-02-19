from qaviton import crosstest
from qaviton.utils import path
from tests.config.private import hub


app = [
    # web
    'https://contacts.google.com/',
    # 'file://' + path.of(__file__)('../../apps/ContactManager/ContactManager.html'),
    # 'file:///home/ubuntu/ContactManager.html',
    # mobile
    path.of(__file__)('../../../apps/ContactManager/ContactManager.apk')
]

screenResolution = "800x600x24"
sessionTimeout = 600


# create cross-platform testing object
platforms = crosstest.Platforms()
platforms.web.command_executor = hub


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
    'version': "61.0",
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


# # add internet explorer/opera browser support (not working with selenoid!)
# platforms.web({
#     "browserName": "opera",
#     "version": "",
#     "platform": "ANY",
#     'app': app[0],
#     'screenResolution': screenResolution,
#     'sessionTimeout': sessionTimeout,
#     'enableVNC': True,
#     'enableVideo': True,
#     'name': "{}",
#     'videoName': "{}.mp4",
#     'logName': "{}.log"})


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
