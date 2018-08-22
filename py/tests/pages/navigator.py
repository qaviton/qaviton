from qaviton.navigator import Navigator, Graph
from tests.pages.google_home import GoogleHomePage
from tests.pages.google_search import GoogleSearchPage
from tests.pages.linkedin_home import LinkedinHomePage


class Navigate(Navigator):
    graph = Graph()

    def __init__(self, driver, timeout=None):
        Navigator.__init__(self, driver, GoogleHomePage, timeout)


Navigate.add(GoogleHomePage)
Navigate.add(GoogleSearchPage)
Navigate.add(LinkedinHomePage)

Navigate.connect(GoogleHomePage, GoogleSearchPage, GoogleHomePage.navigate_to_GoogleSearchPage)
Navigate.connect(GoogleSearchPage, LinkedinHomePage, GoogleSearchPage.navigate_to_LinkedinHomePage)
