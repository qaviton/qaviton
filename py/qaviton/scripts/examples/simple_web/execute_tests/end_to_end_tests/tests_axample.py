import threading


def test_app1(app):
    app.navigate(app.linkedin_home).register.register_and_submit()


def test_app2(app, app2):
    app.navigate(app.linkedin_home).register.register_and_submit()
    app2.navigate(app2.linkedin_home).register.register_and_submit()


def test_app3(app):
    app.navigate(app.qaviton_home).SIGN_UP_FOR_A_BETA()
    app.qaviton_home.qaviton_menu_home_button()
    app.qaviton_home.qaviton_logo()
    app.qaviton_home.qaviton_send_demo_request()
    app.qaviton_home.qaviton_name_demo_request()
    app.qaviton_home.qaviton_company_demo_request()
    app.qaviton_home.qaviton_email_demo_request()


def test_app4(app, app2):
    t1 = threading.Thread(target=lambda: app.navigate(app.google_search).search_bar.search('qaviton'))
    t2 = threading.Thread(target=lambda: app2.navigate(app2.google_search).search_bar.search('cats'))
    t1.start(), t2.start()
    t1.join(), t2.join()


def test_app5(app):
    app.navigate(app.linkedin_home)


def test_app6(app):
    app.navigate(app.google_home).google_search_button()


def test_app7(app, app2):
    app.navigate(app.google_search).search_bar.button()
    app2.navigate(app2.google_search).search_bar.button()
