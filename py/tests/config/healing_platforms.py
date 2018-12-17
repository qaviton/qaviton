from qaviton import crosstest
from tests.config.private import hub
from tests.config.navigation_platforms import sessionTimeout, app, screenResolution


# create cross-platform testing object
platforms = crosstest.Platforms()
platforms.web.command_executor = hub


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

