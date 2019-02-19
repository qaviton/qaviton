from tests.pages.components.page import Page
from tests.config.locators import locator
from tests.pages.components.google_search_bar import GoogleSearchBar
from selenium.webdriver.common.keys import Keys


class GoogleHomePage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)
        self.search_bar = GoogleSearchBar(driver)

    def google_search_button(self):
        return self.find(locator.google_search_button)

    def navigate_to_GoogleSearchPage(self, weight=5, *args, **kwargs):
        try:
            self.search_bar.button().send('search').send_keys(Keys.ENTER)
        except:
            self.get_page("https://www.google.com/search?source=hp&ei=M_"
                          "-PW4X2J8epsgGix4rIAQ&q=sd&oq=sd&gs_l=psy-ab.3."
                          ".35i39k1j0j0i131k1l2j0j0i10i1k1j0l4.1997.2074."
                          "0.3892.3.2.0.0.0.0.174.174.0j1.1.0....0...1c.1"
                          ".64.psy-ab..2.1.174.0...0.gG-PzboHJ8c")
        self.wait_until_page_loads()

