from tests.pages.components.page import Page
from tests.config.locators import locator


class YnetHomePage(Page):
    def c3_Hor(self):
        return self.find_all(locator.c3_Hor)

    def evritiframe_1(self):
        return self.find_all(locator.evritiframe_1)

    def multiarticles_15(self):
        return self.find_all(locator.multiarticles_15)

    def multiarticles_5(self):
        return self.find_all(locator.multiarticles_5)

    def close_console(self):
        return self.find_all(locator.close_console)
    
    def su_iframe(self):
        return self.find_all(locator.su_iframe)

    def xButtn(self):
        return self.find_all(locator.xButtn)

    def console_resize(self):
        return self.find_all(locator.console_resize)

    def first_title(self):
        return self.find_all(locator.first_title)

    def arrows(self):
        return self.find_all(locator.arrows)

    def mainSearchSelectText(self):
        return self.find_all(locator.mainSearchSelectText)

    def teaserxnet_1(self):
        return self.find_all(locator.teaserxnet_1)

    def iframe_container(self):
        return self.find_all(locator.iframe_container)

    def null(self):
        return self.find_all(locator.null)

    def ads_300x250_4(self):
        return self.find_all(locator.ads_300x250_4)
