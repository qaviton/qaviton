from tests.pages.components.page import Page
from tests.config.locators import locator


class QavitonHomePage(Page):
    def SIGN_UP_FOR_A_BETA(self):
        return self.find(locator.SIGN_UP_FOR_A_BETA)

    def qaviton_menu_home_button(self):
        return self.find(locator.qaviton_menu_home_button)

    def qaviton_logo(self):
        return self.find(locator.qaviton_logo)

    def qaviton_send_demo_request(self):
        return self.find(locator.qaviton_send_demo_request)

    def qaviton_name_demo_request(self):
        return self.find(locator.qaviton_name_demo_request)

    def qaviton_company_demo_request(self):
        return self.find(locator.qaviton_company_demo_request)

    def qaviton_email_demo_request(self):
        return self.find(locator.qaviton_email_demo_request)
