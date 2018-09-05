def test_linkedin_registration(app):
    app.navigate(app.linkedin_home).register.register_and_submit()


def test_linkedin_registration_again(app):
    app.navigate(app.linkedin_home).register.register_and_submit()


def test_google_search_linkedin(app):
    navigated_page = app.navigate(app.google_search)
    assert app.navigate.current_page == app.navigate.from_page == app.google_search == navigated_page
    navigated_page = app.navigate(app.linkedin_home)
    assert app.navigate.current_page == app.navigate.from_page == app.linkedin_home == navigated_page
    app.linkedin_home.register.register_and_submit()


def test_navigation_works(app):
    app.navigate(app.linkedin_home)
    app.navigate(app.linkedin_home).register.register_and_submit()


def test_qaviton_home(app):
    app.navigate(app.qaviton_home)


def test_google_home(app):
    app.navigate(app.google_home).google_search_button()


def test_qaviton_demo(app):
    app.navigate(app.google_search).search_bar.button()
    app.navigate(app.qaviton_home)
    app.qaviton_home.qaviton_send_demo_request()
