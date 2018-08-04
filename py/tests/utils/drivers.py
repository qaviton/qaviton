from appium import webdriver


def get(driver_url, desired_caps):
    return webdriver.Remote(driver_url, desired_caps)

