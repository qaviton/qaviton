from selenium.webdriver.common.keys import Keys
from qaviton.page import Page
from tests.services.locators import locator


class GoogleSearchBar(Page):
    def button(self):
        return self.find(locator.google_search_bar)

    def search(self, search):
        self.button().send_keys(search).send_keys(Keys.ENTER)
        self.wait_until_page_loads()
