import pytest
import time
from qaviton.utils import unique_id
from qaviton import crosstest
from qaviton.navigator import Navigator
from tests.config.navigation_platforms import platforms
from tests.services.app import App


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

    app.driver.quit()


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_navigator_with_auto_connect(platform, request):
    app = App.from_platform(platform, request)
    app.navigate.to(app.linkedin_home).perform()
    # this is what the tester will want to test
    app.linkedin_home.register.register_and_submit(
        firstname='test123',
        lastname='456',
        email='testmail',
        password='123456gg')
    app.driver.quit()


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_navigator_2_navigations(platform, request):
    app = App.from_platform(platform, request)
    app.navigate(app.google_search)
    assert app.navigate.current_page == app.navigate.from_page == app.google_search
    app.navigate(app.linkedin_home)
    assert app.navigate.current_page == app.navigate.from_page == app.linkedin_home
    # this is what the tester will want to test
    app.linkedin_home.register.register_and_submit(
        firstname='test123',
        lastname='456',
        email='testmail',
        password='123456gg')
    app.driver.quit()


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_navigate_to_self_with_no_possible_navigation(platform, request):
    app = App.from_platform(platform, request)
    app.navigate(app.linkedin_home)
    app.navigate(app.linkedin_home)
    app.linkedin_home.register.reg_submit()
    app.driver.quit()


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_navigate_with_no_possible_navigation(platform, request):
    app = App.from_platform(platform, request)
    app.navigate(app.linkedin_home)
    # with pytest.raises(PathUnreachableException):
    #     app.navigate(app.google_home)
    app.driver.quit()


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_navigate_to_self_with_remote_looped_navigation(platform, request):
    app = App.from_platform(platform, request)
    app.navigate(app.google_home)
    app.google_home.google_search_button()
    app.driver.quit()


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_navigate_to_self_with_looped_navigation(platform, request):
    # setup
    app = App.from_platform(platform, request)

    # test flow
    app.navigate(app.google_search)

    # test scenario
    app.navigate(app.google_search)

    # validation
    app.google_search.search_bar.button()

    # teardown
    app.driver.quit()

