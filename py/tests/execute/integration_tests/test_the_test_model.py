import pytest
from qaviton import crosstest
from tests.settings import TESTS
from tests.settings import web_apps


@pytest.mark.parametrize('test', TESTS, ids=crosstest.id)
def test_models_with_drivers(test: crosstest.Model):
    driver = test.driver()
    try:
        if test.test_api == crosstest.TestAPI.WEB:
            # driver.get("https://github.com/SeleniumHQ/selenium/wiki/Grid2")
            driver.get(web_apps[0])
        elif test.test_api == crosstest.TestAPI.MOBILE:
            driver.find_element_by_accessibility_id("Add Contact").click()
    finally:
        driver.quit()
