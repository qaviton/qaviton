from qaviton import crosstest
from tests.config.secret import hub


web_app = 'https://www.qaviton.com/'
# mobile_app = path.of(__file__)('../../../apps/ContactManager/ContactManager.apk')


screenResolution = "800x600x24"
sessionTimeout = 60


# create cross-platform testing object
platforms = crosstest.Platforms()
platforms.web.command_executor = hub


# add chrome browser support
platforms.web({
    'browserName': "chrome",
    'version': "",
    'platform': "ANY",
    'app': web_app,
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
    'app': web_app,
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
#     'app': web_app,
#     'screenResolution': screenResolution,
#     'sessionTimeout': sessionTimeout,
#     'enableVNC': True,
#     'enableVideo': True,
#     'name': "{}",
#     'videoName': "{}.mp4",
#     'logName': "{}.log"})


# # add android mobile support
# platforms.mobile({
#     'platformName': "Android",
#     'platformVersion': "6.0",
#     'deviceName': "emulator-5554",
#     'app': mobile_app,
#     'appPackage': 'com.example.android.contactmanager',
#     'appActivity': '.ContactManager',
#     'screenResolution': screenResolution,
#     'sessionTimeout': sessionTimeout,
#     'enableVNC': True,
#     'enableVideo': True,
#     'name': "{}",
#     'videoName': "{}.mp4",
#     'logName': "{}.log"})
