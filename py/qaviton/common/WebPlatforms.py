# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Selenium Desired Capabilities with Qaviton implementation.
"""

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from qaviton import settings


def add(app, desired_capabilities, size, command_executor=settings.webdriver_url, browser_profile=None,
            proxy=None,keep_alive=False, file_detector=None, options=None):
    """
    a custome function to create your platform requirements
        args:
            - app - your app url/file
                ....
            - size - window size; can be 'max', 'min', '800x600' or None
                for headless/nonesizable browsers
            - command_executor - Either a string representing URL of the remote server or a custom
                remote_connection.RemoteConnection object. Defaults to 'http://127.0.0.1:4444/wd/hub'.
            - desired_capabilities - example: {"browserName": "firefox","marionette": True,"acceptInsecureCerts": True}
                A dictionary of capabilities to request when starting the browser session. Required parameter.
            - browser_profile - A selenium.webdriver.firefox.firefox_profile.FirefoxProfile object.
                Only used if Firefox is requested. Optional.
            - proxy - A selenium.webdriver.common.proxy.Proxy object. The browser session will
                be started with given proxy settings, if possible. Optional.
            - keep_alive - Whether to configure remote_connection.RemoteConnection to use
                HTTP keep-alive. Defaults to False.
            - file_detector - Pass custom file detector object during instantiation. If None,
                then default LocalFileDetector() will be used.
            - options - instance of a driver options.Options class
    :rtype: {}
    """
    return dict(
        desired_capabilities=desired_capabilities,
        app=app,
        size=size,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def firefox(app, size="max", command_executor=settings.webdriver_url, browser_profile=None,
            proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.FIREFOX,
        app=app,
        size=size,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def internetExplorer(app, size="max", command_executor=settings.webdriver_url, browser_profile=None,
                     proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.INTERNETEXPLORER,
        app=app,
        size=size,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def edge(app, size="max", command_executor=settings.webdriver_url, browser_profile=None,
         proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.EDGE,
        app=app,
        size=size,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def chrome(app, size="max", command_executor=settings.webdriver_url, browser_profile=None,
           proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.CHROME,
        app=app,
        size=size,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def opera(app, size="max", command_executor=settings.webdriver_url, browser_profile=None,
          proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.OPERA,
        app=app,
        size=size,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def safari(app, size="max", command_executor=settings.webdriver_url, browser_profile=None,
           proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.SAFARI,
        app=app,
        size=size,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def htmlUnit(app, command_executor=settings.webdriver_url, browser_profile=None,
             proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.HTMLUNIT,
        app=app,
        size=None,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def htmlunitwithJS(app, command_executor=settings.webdriver_url, browser_profile=None,
                   proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS,
        app=app,
        size=None,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def iphone(app, command_executor=settings.webdriver_url, browser_profile=None,
           proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.IPHONE,
        app=app,
        size=None,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def ipad(app, command_executor=settings.webdriver_url, browser_profile=None,
         proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.IPAD,
        app=app,
        size=None,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def android(app, command_executor=settings.webdriver_url, browser_profile=None,
            proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.ANDROID,
        app=app,
        size=None,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def phantomJS(app, command_executor=settings.webdriver_url, browser_profile=None,
              proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.PHANTOMJS,
        app=app,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)


def webKitGTK(app, size=None, command_executor=settings.webdriver_url, browser_profile=None,
              proxy=None,keep_alive=False, file_detector=None, options=None):
    return dict(
        desired_capabilities=DesiredCapabilities.WEBKITGTK,
        app=app,
        size=size,
        command_executor=command_executor,
        browser_profile=browser_profile,
        proxy=proxy,
        keep_alive=keep_alive,
        file_detector=file_detector,
        options=options)

