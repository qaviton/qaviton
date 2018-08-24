import pytest
from qaviton.utils import unique_id
from qaviton import crosstest
from tests.data.platforms.navigation_platforms import platforms
from tests.services.app import App
import time


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_models_with_drivers(platform: crosstest.Platform, request):
    t = time.time()
    test = platform.setup(request)
    print('time to get test platform {}'.format(time.time() - t))

    t = time.time()
    driver = test.driver()
    print('time to get driver {}'.format(time.time() - t))

    t = time.time()
    app = App(driver)
    print('time to get app model {}'.format(time.time() - t))

    try:
        # money time for this feature
        t = time.time()
        app.navigate.to(app.linkedin_home)
        print('time to get navigation calc {}'.format(time.time() - t))

        t = time.time()
        app.navigate.perform()
        print('time to get navigation {}'.format(time.time() - t))

        # this is what we want to test
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
