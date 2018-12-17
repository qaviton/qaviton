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

    def register_and_submit(self, firstname=None, lastname=None, email=None, password=None):
        # first = threaders.thread(self.reg_firstname)
        # last = threaders.thread(self.reg_lastname)
        # mail = threaders.thread(self.reg_email)
        # pss = threaders.thread(self.reg_password)
        #
        # first = first.get_and_join(timeout=10)
        # last = last.get_and_join(timeout=10)
        # mail = mail.get_and_join(timeout=10)
        # pss = pss.get_and_join(timeout=10)
        #
        # first = threading.Thread(target=first.send_keys, args=(firstname,))
        # last = threading.Thread(target=last.send_keys, args=(lastname,))
        # mail = threading.Thread(target=mail.send_keys, args=(email,))
        # pss = threading.Thread(target=pss.send_keys, args=(password,))
        #
        # first.join()
        # last.join()
        # mail.join()
        # pss.join()

        # self.reg_submit().click()
        self.reg_submit()
        # assert threading.active_count() < 3
