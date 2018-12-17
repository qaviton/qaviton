import pytest
from qaviton import crosstest
from qaviton.utils import unique_id
from tests.config.supported_platforms import platforms, sessionTimeout
from qaviton.utils.condition import relatedclass


@pytest.mark.timeout(sessionTimeout*1.5)
@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_models_with_drivers(platform: crosstest.Platform, request):
    test = platform.setup(request)
    driver = test.driver()

    if test.platform["api"] == crosstest.API.WEB:
        driver.get("https://github.com/SeleniumHQ/selenium/wiki/Grid2")

    elif test.platform["api"] == crosstest.API.MOBILE:
        driver.find_element_by_accessibility_id("Add Contact").click()

    driver.quit()


@pytest.mark.timeout(sessionTimeout*1.5)
@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_new_models_with_drivers(platform, request):
    driver = crosstest.get_driver(platform, request)

    if relatedclass(driver, crosstest.API.WEB):
        driver.get("https://github.com/SeleniumHQ/selenium/wiki/Grid2")

    elif relatedclass(driver, crosstest.API.MOBILE):
        driver.find_element_by_accessibility_id("Add Contact").click()

    driver.quit()
