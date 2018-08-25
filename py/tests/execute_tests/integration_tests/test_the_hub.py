import pytest
from qaviton import crosstest
from qaviton.utils import unique_id
from tests.data.platforms.supported_platforms import platforms


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)
def test_models_with_drivers(platform: crosstest.Platform, request):
    test = platform.setup(request)
    driver = test.driver()

    if test.platform["api"] == crosstest.API.WEB:
        driver.get("https://github.com/SeleniumHQ/selenium/wiki/Grid2")

    elif test.platform["api"] == crosstest.API.MOBILE:
        driver.find_element_by_accessibility_id("Add Contact").click()
