import pytest
from qaviton.exceptions import ElementPresenceException
from tests.parameters.healing_platforms import platforms
from tests.services.app import App


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


def test_healing(app):
    app.navigate(app.qaviton_home)
    try:
        app.find(app.locator.google_search_bar)
        raise ElementPresenceException(
            "element {} should not be present on {}"
            .format(app.locator.google_search_bar, app.navigate.current_page))
    except:
        pass

    app.navigate(app.google_home)
    try:
        app.find(app.locator.qaviton_send_demo_request)
        raise ElementPresenceException(
            "element {} should not be present on {}"
            .format(app.locator.google_search_bar, app.navigate.current_page))
    except:
        pass
