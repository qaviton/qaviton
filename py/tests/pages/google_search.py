from qaviton.page import Page
from tests.services.locators import locator
from tests.pages.components.google_search_bar import GoogleSearchBar


class GoogleSearchPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)
        self.search_bar = GoogleSearchBar(driver)

    def google_search_result(self, text):
        return self.find(locator.text(text))

    def go_to(self, search):
        self.google_search_result(search).click()
        self.wait_until_page_loads()

    def navigate_to_LinkedinHomePage(self, weight=5, *args, **kwargs):
        try:
            self.go_to('LinkedIn: Log In or Sign Up')
        except Exception as e:
            text = []
            for span in self.find_all(locator.xpath('//span[@dir="ltr"]')):
                if 'LinkedIn: Log In or Sign Up' in span.text or 'LinkedIn: Log In or Sign Up' == span.text:
                    span.click_at()
                    span.try_to_click()
                    self.wait_until_page_loads()
                    assert self.no_such_element(locator.xpath('//span[@dir="ltr"]'))
                    return
                text.append(span.text)
            raise Exception('LinkedIn: Log In or Sign Up - text not found: {}'.format(text)) from e

    def navigate_to_YnetHomePage(self, weight=5, *args, **kwargs):
        self.go_to('ynet - חדשות, כלכלה, ספורט, בריאות')

    def navigate_to_GoogleSearchPage(self, weight=5, *args, **kwargs):
        self.go_to('')