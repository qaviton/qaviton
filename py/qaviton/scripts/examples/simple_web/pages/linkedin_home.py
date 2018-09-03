from tests.pages.components.page import Page
from tests.pages.components.linkedin_register import LinkedinRegister


class LinkedinHomePage(Page):
    def __init__(self, driver, timeout=None):
        Page.__init__(self, driver)
        self.register = LinkedinRegister(driver)
