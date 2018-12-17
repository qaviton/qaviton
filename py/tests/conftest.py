import pytest
from tests.services.app import App
from tests.config.navigation_platforms import platforms
# from qaviton.fixtures.dependency import Dependencies, depend, dependencies, dependency
# from qaviton.schedualer import QavitonSchedualing
# from qaviton.heal import Heal
# from tests.parameters.locators import locator
# from qaviton.utils import path
#
#
# # the root directory of your project
# workspace = path.of(__file__)('../../')
#
#
# def pytest_configure(config):
#     # adding dependency feature - parallel dependency is exclusive to qaviton cloud
#     # adding self-healing feature - exclusive to qaviton cloud
#     Dependencies.set_path(path.of(__file__)('dependencies'))
#     if not hasattr(config, "slaveinput"):
#         Dependencies.remove_all()
#         Heal.config(workspace, locator)
#         Heal.signal_session_to_start()
#
#
# def pytest_unconfigure(config):
#     if not hasattr(config, "slaveinput"):
#         try:
#             # dependency teardown
#             Dependencies.remove_all()
#             # self healing teardown
#             Heal.signal_session_to_stop()
#         except:
#             pass
#
#
# def pytest_collection_finish(session):
#     # adding dependency & ordering
#     for item in session.items:
#             try:
#                 Dependencies.add(item.name)
#             except:
#                 pass
#
#
# def pytest_xdist_make_scheduler(config, log):
#     # adding parallel ordering feature - exclusive to qaviton cloud
#     return QavitonSchedualing(config, log)
#
#
# @pytest.fixture(scope='session')
# def heal(autouse=True):
#     """this fixture/feature is exclusive to qaviton cloud.
#
#     requirements:
#         your project's file path (workspace)
#         locator class with all your buttons.
#
#     make sure your workspace conveys your project root directory(where .idea - git).
#     the config method takes only one locator class,
#     so make sure to centralize all your locators
#     to 1 locator file with 1 locator class.
#     """
#     Heal.config(workspace, locator)


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
