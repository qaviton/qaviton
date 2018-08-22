import pytest
from qaviton.utils import unique_id
from qaviton import crosstest
from tests.data.navigation_platforms import platforms
from tests.pages.app import AppPage
import time


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_models_with_drivers(platform: crosstest.Platform, request):
    test = platform.setup(request)
    driver = test.driver()
    app = AppPage(driver)

    # money time for this feature
    t = time.time()
    app.navigate.to(app.linkedin_home).perform()
    print(time.time()-t)

    # this is what we want to test
    app.linkedin_home.register.register_and_submit(
        firstname='test123',
        lastname='456',
        email='testmail',
        password='123456gg')
