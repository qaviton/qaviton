from qaviton.navigator import Navigator
from tests.pages.components.page import Page
from tests.pages.qaviton_home import QavitonHomePage
from tests.pages.linkedin_home import LinkedinHomePage
from tests.pages.google_search import GoogleSearchPage
from tests.pages.google_home import GoogleHomePage


class App(Page):
    """use the app page to include all your
    pages/components/api/services/flows
    in a single page application
    """
    def __init__(self, driver, platform):
        Page.__init__(self, driver, platform=platform)
        self.qaviton_home = QavitonHomePage(driver)
        self.linkedin_home = LinkedinHomePage(driver)
        self.google_search = GoogleSearchPage(driver)
        self.google_home = GoogleHomePage(driver)

        self.navigate = Navigator(self.qaviton_home, auto_connect=self)
