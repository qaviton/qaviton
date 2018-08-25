from qaviton.page import Page
from qaviton.navigator import Navigator
from tests.pages.google_search import GoogleSearchPage
from tests.pages.google_home import GoogleHomePage
from tests.pages.linkedin_home import LinkedinHomePage


class App(Page):
    """use the app page to include all your pages/components in a single page application"""
    def __init__(self, driver):
        Page.__init__(self, driver)
        self.google_home = GoogleHomePage(driver)
        self.google_search = GoogleSearchPage(driver)
        self.linkedin_home = LinkedinHomePage(driver)

        self.navigate = Navigator(self.google_home, auto_connect=self)
