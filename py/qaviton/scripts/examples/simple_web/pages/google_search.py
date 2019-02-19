from tests.pages.components.page import Page
from tests.config.locators import locator
from tests.pages.components.google_search_bar import GoogleSearchBar
from selenium.webdriver.common.keys import Keys


class GoogleSearchPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)
        self.search_bar = GoogleSearchBar(driver)

    def google_search_result(self, text):
        return self.find(locator.text(text))

    def go_to(self, search):
        self.search_bar.button().send(search).send_keys(Keys.ENTER)
        self.wait_until_page_loads()
        try:
            self.google_search_result(search).click()
            self.wait_until_page_loads()
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            text = []
            for span in self.find_all(locator.xpath('//span[@dir="ltr"]')):
                if search in span.text or search == span.text:
                    span.click_at()
                    span.try_to_click()
                    self.wait_until_page_loads()
                    assert self.no_such_element(locator.xpath('//span[@dir="ltr"]'))
                    return
                text.append(span.text)
            raise Exception('{} - text not found: {}'.format(search, text)) from e
        
    def navigate_to_LinkedinHomePage(self, weight=5, *args, **kwargs):
        try:
            self.go_to('LinkedIn: Log In or Sign Up')
        except:
            self.get_page("https://www.linkedin.com/")
            self.wait_until_page_loads()

    def navigate_to_QavitonHomePage(self, weight=5, *args, **kwargs):
        try:
            self.go_to('QAVITON - NEXT GENERATION QA AUTOMATION ...')
        except:
            self.get_page("https://www.google.com/")
            self.wait_until_page_loads()


