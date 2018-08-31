from tests.pages.components.page import Page
from tests.services.locators import locator
from tests.pages.components.google_search_bar import GoogleSearchBar
from selenium.webdriver.common.keys import Keys


class GoogleHomePage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)
        self.search_bar = GoogleSearchBar(driver)

    def google_search_button(self):
        return self.find(locator.google_search_button)

    def navigate_to_GoogleSearchPage(self, weight=5, *args, **kwargs):
        self.search_bar.button().send('search').send_keys(Keys.ENTER)
        self.wait_until_page_loads()

