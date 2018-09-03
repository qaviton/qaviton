def test_app1(app):
    app.navigate(app.linkedin_home).register.register_and_submit()


def test_app2(app):
    app.navigate(app.linkedin_home).register.register_and_submit()


def test_app3(app):
    navigated_page = app.navigate(app.google_search)
    assert app.navigate.current_page == app.navigate.from_page == app.google_search == navigated_page
    navigated_page = app.navigate(app.linkedin_home)
    assert app.navigate.current_page == app.navigate.from_page == app.linkedin_home == navigated_page
    app.linkedin_home.register.register_and_submit()


def test_app4(app):
    app.navigate(app.linkedin_home)
    app.navigate(app.linkedin_home).register.register_and_submit()


def test_app5(app):
    app.navigate(app.linkedin_home)


def test_app6(app):
    app.navigate(app.google_home).google_search_button()


def test_app7(app):
    app.navigate(app.google_search)
    app.navigate(app.google_search)
    app.google_search.search_bar.button()
