from qaviton.page import Page
from tests.pages.locators import locator


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

    def register_and_submit(self, firstname, lastname, email, password):
        self.reg_firstname().send_keys(firstname)
        self.reg_lastname().send_keys(lastname)
        self.reg_email().send_keys(email)
        self.reg_password().send_keys(password)
        self.reg_submit().click()
