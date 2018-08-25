import pytest
from qaviton.utils import unique_id
from qaviton import crosstest
from qaviton.navigator import Navigator
from tests.data.platforms.navigation_platforms import platforms
from tests.services.app import App
import time


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_navigator(platform: crosstest.Platform, request):
    t = time.time()
    test = platform.setup(request)
    print('time to get test platform {}'.format(time.time() - t))

    t = time.time()
    driver = test.driver()
    print('time to get driver {}'.format(time.time() - t))

    t = time.time()
    app = App(driver)
    print('time to get app model {}'.format(time.time() - t))

    # manual navigation connection configuration
    navigate = Navigator(app.google_home)
    navigate.connect_all(
        (app.google_home.navigate_to_GoogleSearchPage, app.google_search),
        (app.google_search.navigate_to_LinkedinHomePage, app.linkedin_home))

    try:
        # money time for this feature
        t = time.time()
        navigate.to(app.linkedin_home)
        print('time to get navigation calc {}'.format(time.time() - t))

        t = time.time()
        navigate.perform()
        print('time to get navigation {}'.format(time.time() - t))

        # this is what the tester will want to test
        app.linkedin_home.register.register_and_submit(
            firstname='test123',
            lastname='456',
            email='testmail',
            password='123456gg')
    finally:
        try:
            driver.quit()
        except:
            pass


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_navigator_with_auto_connect(platform: crosstest.Platform, request):
    test = platform.setup(request)
    driver = test.driver()
    app = App(driver)
    try:
        app.navigate.to(app.linkedin_home)
        app.navigate.perform()

        # this is what the tester will want to test
        app.linkedin_home.register.register_and_submit(
            firstname='test123',
            lastname='456',
            email='testmail',
            password='123456gg')
    finally:
        try:
            driver.quit()
        except:
            pass