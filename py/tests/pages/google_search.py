from qaviton.page import Page
from tests.services.locators import locator


class GoogleSearchPage(Page):
    def google_linkedin_search_result(self):
        return self.find(locator.google_linkedin_search_result)

    def navigate_to_LinkedinHomePage(self):
        self.google_linkedin_search_result().click()
        self.wait_until_page_loads()
