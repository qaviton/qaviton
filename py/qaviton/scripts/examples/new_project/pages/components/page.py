from qaviton.page import Page as page


class Page(page):
    """component with common behavior to all pages & components alike.
    all of your pages & components should inherit from this common page.

    you should always include here a navigation to your initial login page(starting point)
    so that dependent tests could always start fresh if needed.
    """
