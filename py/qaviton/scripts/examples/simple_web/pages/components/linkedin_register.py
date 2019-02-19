from tests.pages.components.page import Page
from tests.config.locators import locator


class LinkedinRegister(Page):
    def reg_firstname(self):
        return self.find(locator.linkedin_reg_firstname)

    def reg_lastname(self):
        return self.find(locator.linkedin_reg_lastname)

    def reg_email(self):
        return self.find(locator.linkedin_reg_email)

    def reg_password(self):
        return self.find(locator.linkedin_reg_password)

    def reg_submit(self):
        return self.find(locator.linkedin_reg_submit)

    def register_and_submit(self, firstname='test', lastname='tester', email='tester@qaviton.com', password='123test'):
        self.reg_firstname()
        self.reg_lastname()
        self.reg_email()
        self.reg_password()
        self.reg_submit().click()


