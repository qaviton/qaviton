from qaviton.locator import Locator


class locator(Locator):
    # you can use a variety of methods to build locators
    type_submit = ('type', 'submit')
    qaviton_logo = ('id', 'site-logo')
    qaviton_menu_home_button = ('xpath', '//a[text()="LOGIN"]')
    SIGN_UP_FOR_A_BETA = ('text', 'SIGN UP FOR A BETA')

    # you can use the Locator directly to build your locator
    qaviton_email_demo_request = Locator.xpath('//input[@placeholder="Your Email"]')
    qaviton_company_demo_request = Locator.xpath('//input[@placeholder="Company"]')
    qaviton_name_demo_request = Locator.xpath('//input[@placeholder="Name"]')

    qaviton_send_demo_request = Locator.tuple(
        Locator.xpath('//button[@type="submit"]//*[text()="SEND"]'),
        Locator.index(type_submit, index=0))

    # you can use 'tuple' or 'list' to build a redundant locator and support self healing
    google_search_bar = (
        ('id', 'lst-ib'),
        ('index', 2, ('xpath', '//input')),
        ('xpath', '//input[@type="text"][@value=""]'))

    google_search_button = ('name', 'btnK')
    google_linkedin_search_result = ('text', 'LinkedIn: Log In or Sign Up')

    # id/test-id is the best choice for locators.
    linkedin_reg_firstname = ('id', 'reg-firstname')
    linkedin_reg_lastname = ('id', 'reg-lastname')
    linkedin_reg_email = ('id', 'reg-email')
    linkedin_reg_password = ('id', 'reg-password')
    linkedin_reg_submit = ('id', 'registration-submit')
