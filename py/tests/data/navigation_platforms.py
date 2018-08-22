from qaviton import crosstest
from tests.private import hubip


app = 'https://www.google.com/'
screenResolution = "800x600x24"
sessionTimeout = 60


# create cross-platform testing object
platforms = crosstest.Platforms()
platforms.web.command_executor = 'http://'+hubip+':4444/wd/hub'


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
