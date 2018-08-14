from selenium import webdriver


class WebDriverManager:

    @staticmethod
    def open(driver=None, url=None):
        """
        :type driver: webdriver.Firefox
        :type url: str
        """
        if driver is None:
            driver = webdriver.Firefox()
        if url is not None:
            driver.get(url)
        driver.maximize_window()
        return driver

    @staticmethod
    def open_Firefox(url=None):
        """
        :type url: str
        """
        driver = webdriver.Firefox()
        return WebDriverManager.open(driver, url)

    @staticmethod
    def open_Chrome(url=None):
        """
        :type url: str
        """
        driver = webdriver.Chrome()
        return WebDriverManager.open(driver, url)

    @staticmethod
    def open_PhantomJS(url=None):
        """
        :type url: str
        """
        driver = webdriver.PhantomJS()
        return WebDriverManager.open(driver, url)

    @staticmethod
    def open_Android(url=None):
        """
        :type url: str
        """
        driver = webdriver.Android()
        return WebDriverManager.open(driver, url)
