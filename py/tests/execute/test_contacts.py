import pytest
from tests import conftest
from tests.utils import drivers
from tests.data.count_functions import from_zero_to_hero


def test_add_contacts():
    driver = drivers.get(conftest.DRIVER_URL, conftest.desired_caps_app1)
    el = driver.find_element_by_accessibility_id("Add Contact")
    el.click()

    textfields = driver.find_elements_by_class_name("android.widget.EditText")
    textfields[0].send_keys("Appium User")
    textfields[2].send_keys("someone@appium.io")
    print(driver.page_source)
    assert 'Appium User' == textfields[0].text
    assert 'someone@appium.io' == textfields[2].text

    driver.find_element_by_accessibility_id("Save").click()

    # for some reason "save" breaks things
    alert = driver.switch_to_alert()

    # no way to handle alerts in Android
    driver.find_element_by_android_uiautomator('new UiSelector().clickable(true)').click()

    driver.press_keycode(3)
    driver.quit()


@pytest.mark.parametrize('test_data', from_zero_to_hero, ids=(lambda test: str(test.id)))
def test_data_driven(test_data):
    assert isinstance(test_data, int)



