from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class ByExtension(By):
    """
    This is an extension to the By class
    use this class to choose a locating strategy for web elements!
    """
    list = 'list'
    tuple = 'tuple'
    element = 'element'
    elements = 'elements'


class ByExtensionMap:
    """
    This extension is intended for mappings in the By class
    """
    cls = 'class'
    css = 'css'
    text = 'text'
    attribute_name = 'attribute_name'


class WebLocator(object):
    """ this is the WebPage element webLocator class
        it is intended to be inherited by other locators of real pages.
        place all common search methods under this super class:

        format method:
            is used only when a paired search (list/tuple that consists of 2 values)
            is required to change the format of its index[1] value.
            example usage:

                import WebLocator

                class WebLocator(WebLocator):
                    button1 = ('id', 'button{}-id')
                    name = ('text', '{name}')

                webLocator = WebLocator

                print(webLocator.format(webLocator.button1, 1))
                print(webLocator.format(webLocator.common.name, name="louis bow"))

                >> ['id', 'button1-id']
                >> ['text', 'louis bow']

        element method:
            give it an element and get in return a tuple like so:
            (webLocator.element(element))

        text method:
            give it a text and get in return a tuple like so:
            ('text', element)

        __call__ method:
            give it any attribute name & value and get in return a tuple like so:
            (<attribute name string>, <attribute value string>)
    """

    @staticmethod
    def format(locator, *args, **kw):
        """
        :type locator: tuple
        :rtype: tuple
        """
        if len(locator) > 1:
            if isinstance(locator[1], str):
                return locator[0], locator[1].format(*args, **kw)

    @staticmethod
    def add(locator, value):
        """
        :type locator: tuple
        :type value: str
        :rtype: tuple
        """
        if len(locator) > 1:
            return locator[0], locator[1] + value

    @staticmethod
    def any(locator):
        """
        this method maps the element locating strategy to its value
        :type locator: tuple
                example: webLocator=('class', 'top.right')
        """
        by, value = locator

        # match to existing strategies
        if by in vars(ByExtension).values() or by in vars(By).values():
            return locator

        # map to extension strategies
        elif by == ByExtensionMap.cls:
            return WebLocator.cls(value)
        elif by == ByExtensionMap.css:
            return WebLocator.css(value)
        elif by == ByExtensionMap.text:
            return WebLocator.text(value)
        elif by == ByExtensionMap.attribute_name:
            return WebLocator.attribute_name(value)

        # find element using any attribute
        else:
            by, value = By.XPATH, "//*[@{}='{}']".format(by, value)
        return by, value

    @staticmethod
    def list(list_of_locators):
        """ return a mapped list of locators
        :type list_of_locators: list[tuple]
        :param list_of_locators: a list of locator tuples """
        return ByExtension.list, list_of_locators

    @staticmethod
    def tuple(tuple_of_locators):
        """ return a mapped tuple of locators
        :type tuple_of_locators: tuple[tuple]
        :param tuple_of_locators: a tuple of locator tuples """
        return ByExtension.tuple, tuple_of_locators

    @staticmethod
    def element(web_element):
        """ return a mapped web element
        :type web_element: WebElement """
        return ByExtension.element, web_element

    @staticmethod
    def elements(list_of_web_elements):
        """ return a mapped list of web elements
        :type list_of_web_elements: list[WebElement] """
        return ByExtension.elements, list_of_web_elements

    @staticmethod
    def attribute_name(attribute_name_locator):
        """ return a mapped web element by its attribute name
        :type attribute_name_locator: string """
        return By.XPATH, "//*[starts-with(@{},'')]".format(attribute_name_locator)

    @staticmethod
    def text(text_locator):
        """ return a mapped web element by its text
        :type text_locator: string """
        return By.XPATH, "//*[{}()='{}']".format(ByExtensionMap.text, text_locator)

    @staticmethod
    def xpath(xpath_locator):
        """ return a mapped web element by xpath
        :type xpath_locator: string """
        return By.XPATH, xpath_locator

    @staticmethod
    def css(css_locator):
        """ return a mapped web element by css
        :type css_locator: string """
        return By.CSS_SELECTOR, css_locator

    @staticmethod
    def cls(class_locator):
        """ return a mapped web element by its class
        :type class_locator: string """
        return By.CLASS_NAME, class_locator

    @staticmethod
    def id(id_locator):
        """ return a mapped web element by its id
        :type id_locator: string """
        return By.ID, id_locator

    @staticmethod
    def link_text(link_text_locator):
        """ return a mapped web element by its link text
        :type link_text_locator: string """
        return By.LINK_TEXT, link_text_locator

    @staticmethod
    def partial_link_text(partial_link_text_locator):
        """ return a mapped web element by its partial link text
        :type partial_link_text_locator: string """
        return By.PARTIAL_LINK_TEXT, partial_link_text_locator

    @staticmethod
    def tag_name(tag_name_locator):
        """ return a mapped web element by its html tag name
        :type tag_name_locator: string """
        return By.TAG_NAME, tag_name_locator

    @staticmethod
    def name(name_locator):
        """ return a mapped web element by its name property
        :type name_locator: string """
        return By.NAME, name_locator
