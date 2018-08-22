from qaviton.page import Page
from tests.pages.locators import locator


class GoogleHomePage(Page):
    def google_search_bar(self):
        return self.find(locator.google_search_bar)

    def google_search_button(self):
        return self.find(locator.google_search_button)

    def navigate_to_GoogleSearchPage(self, search):
        self.google_search_bar().send_keys(search)
        self.google_search_button().click()