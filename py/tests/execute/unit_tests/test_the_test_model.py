import pytest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from qaviton import test_model


platforms = test_model.Platforms()
platforms.web.add(DesiredCapabilities.CHROME)
platforms.web.add(DesiredCapabilities.FIREFOX)

@pytest.mark.parametrize('test', platforms.get(), ids=(lambda test: str(test.id)))
def test_platforms(test):
    assert test == DesiredCapabilities.CHROME or test == DesiredCapabilities.FIREFOX



