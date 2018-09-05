import pytest
# import datetime
# import os
# from tests.utils.helpers import ensure_dir
#
#
# def pytest_configure(config):
#     if not hasattr(config, "slaveinput"):
#         current_day = (datetime.datetime.now().strftime("%Y_%m_%d_%H_%S"))
#         ensure_dir("results")
#         ensure_dir(os.path.join("results", current_day))
#         result_dir = os.path.join(os.path.dirname(__file__), "results", current_day)
#         ensure_dir(result_dir)
#         result_dir_test_run = result_dir
#         ensure_dir(os.path.join(result_dir_test_run, "screenshots"))
#         ensure_dir(os.path.join(result_dir_test_run, "logcat"))
#         config.screen_shot_dir = os.path.join(result_dir_test_run, "screenshots")
#         config.logcat_dir = os.path.join(result_dir_test_run, "logcat")
#
#
# class DeviceLogger:
#     def __init__(self, logcat_dir, screenshot_dir):
#         self.screenshot_dir = screenshot_dir
#         self.logcat_dir = logcat_dir
#
#
# @pytest.fixture(scope="session")
# def device_logger(request):
#     logcat_dir = request.config.logcat_dir
#     screenshot_dir = request.config.screen_shot_dir
#     return DeviceLogger(logcat_dir, screenshot_dir)

from qaviton.fixtures.dependency import Dependencies
from qaviton.utils import path
from tests.services.app import App
from tests.parameters.navigation_platforms import platforms
from qaviton.schedualer import QavitonSchedualing
from qaviton.heal import Heal


def pytest_configure(config):
    # adding dependency feature
    Dependencies.set_path(path.of(__file__)('dependencies'))
    if not hasattr(config, "slaveinput"):
        Dependencies.remove_all()


def pytest_unconfigure(config):
    # adding dependency feature
    if not hasattr(config, "slaveinput"):
        Dependencies.remove_all()


def pytest_collection_finish(session):
    # adding dependency & ordering
    # names = Dependencies.get_all()
    # if len(session.items) < len(names):
    #     item_names = [item.name for item in session.items]
    #     for name in list_diff(names, item_names):
    for item in session.items:
            try:
                Dependencies.add(item.name)
            except:
                pass


def pytest_xdist_make_scheduler(config, log):
    return QavitonSchedualing(config, log)


@pytest.fixture(scope='session', autouse=True)
def heal_config(request):
    # locators file
    from tests.parameters.locators import __file__ as locators
    # the root directory of your project
    workspace = path.of(__file__)('../../')

    Heal.config(workspace, locators)
    request.addfinalizer(APP.driver.quit)

@pytest.fixture(scope='session', params=platforms.get())
def app(request):
    """fixture for cross-platform model-based application
    always use session scope for this type of fixture & parameterize your platforms
    :rtype: App
    """
    if isinstance(request.param, list) or isinstance(request.param, tuple):
        APPS = []
        for platform in request.param:
            APPS.append(App.from_platform(platform, request))
            request.addfinalizer(APPS[-1].driver.quit)
        return APPS
    APP = App.from_platform(request.param, request)
    request.addfinalizer(APP.driver.quit)
    return APP
