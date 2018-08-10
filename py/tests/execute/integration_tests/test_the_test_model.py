import pytest
from qaviton import crosstest
from tests.settings import platforms
from tests.settings import app


@pytest.mark.parametrize('platform', platforms.get(), ids=crosstest.id)
def test_models_with_drivers(platform: crosstest.Platform, request):
    test = platform.setup(request)
    driver = test.driver()
    try:
        if test.platform["api"] == crosstest.API.WEB:
            # driver.get("https://github.com/SeleniumHQ/selenium/wiki/Grid2")
            driver.get(app[1])
        elif test.platform["api"] == crosstest.API.MOBILE:
            driver.find_element_by_accessibility_id("Add Contact").click()
    finally:
        driver.quit()
