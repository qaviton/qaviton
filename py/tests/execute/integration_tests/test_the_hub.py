import pytest
from qaviton import crosstest
from tests.settings import platforms


@pytest.mark.parametrize('platform', platforms.get(), ids=crosstest.id)
def test_models_with_drivers(platform: crosstest.Platform, request):
    test = platform.setup(request)
    print(test.platform)
    driver = test.driver()
    try:
        if test.platform["api"] == crosstest.API.WEB:
            driver.get("https://github.com/SeleniumHQ/selenium/wiki/Grid2")
            # driver.get(app[0])
            pass
        elif test.platform["api"] == crosstest.API.MOBILE:
            driver.find_element_by_accessibility_id("Add Contact").click()
    finally:
        driver.quit()
