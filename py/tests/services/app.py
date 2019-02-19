from qaviton.navigator import Navigator
from tests.config.locators import locator
from tests.pages.components.page import Page
from tests.pages.google_search import GoogleSearchPage
from tests.pages.google_home import GoogleHomePage
from tests.pages.linkedin_home import LinkedinHomePage
from tests.pages.ynet_home import YnetHomePage
from tests.pages.qaviton_home import QavitonHomePage


class App(Page):
    """use the app page to include all your
    pages/components/api/services/flows
    in a single page application
    """

    locator = locator

    def __init__(self, driver, platform):
        Page.__init__(self, driver, platform=platform)
        self.google_home = GoogleHomePage(driver)
        self.google_search = GoogleSearchPage(driver)
        self.linkedin_home = LinkedinHomePage(driver)
        self.ynet_home = YnetHomePage(driver)
        self.qaviton_home = QavitonHomePage(driver)

        self.navigate = Navigator(self.google_home, auto_connect=self)
