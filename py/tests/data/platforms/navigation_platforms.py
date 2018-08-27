from qaviton import crosstest
from tests.data.private import hubip
from tests.data.platforms.supported_platforms import sessionTimeout

app = 'https://www.google.com/'
screenResolution = "1000x860x24"


# create cross-platform testing object
platforms = crosstest.Platforms()
platforms.web.command_executor = 'http://'+hubip+':4444/wd/hub'


# add chrome browser support
platforms.web({
    'browserName': "chrome",
    'version': "",
    'platform': "ANY",
    'app': app,
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
    'app': app,
    'screenResolution': screenResolution,
    'sessionTimeout': sessionTimeout,
    'enableVNC': True,
    'enableVideo': True,
    'name': "{}",
    'videoName': "{}.mp4",
    'logName': "{}.log"})
