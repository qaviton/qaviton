from qaviton.locator import Locator


class locator(Locator):
    google_search_bar = ('id', 'lst-ib')
    google_search_button = ('name', 'btnK')
    google_linkedin_search_result = ('text', 'LinkedIn: Log In or Sign Up')
    linkedin_reg_firstname = ('id', 'reg-firstname')
    linkedin_reg_lastname = ('id', 'reg-lastname')
    linkedin_reg_email = ('id', 'reg-email')
    linkedin_reg_password = ('id', 'reg-password')
    linkedin_reg_submit = ('id', 'registration-submit')