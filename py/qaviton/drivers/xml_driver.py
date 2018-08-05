from qaviton.locator import Locator
from lxml import etree
from lxml import cssselect
from lxml import html
from io import StringIO


class XMLDriver:
    def __init__(self, xml: str):
        self.xml = xml
        self.parser = None
        self.set_parser(xml)
        try:
            self.tree = etree.parse(StringIO(xml))
        except etree.XMLSyntaxError:
            self.tree = html.fromstring(xml)
            # self.tree = etree.XMLParser(recover=True)

    def set_parser(self, xml: str):
        if "html>" in xml or "<html":
            self.parser = 'HTML'
            etree.HTMLParser()
        else:
            self.parser = 'XML'
            etree.XMLParser()

    def find(self, locator):
        """find elements using xpath
        :param locator: ('XPATH', '//a')
        :type locator: (str, str)
        :rtype: []
        """
        if locator[0] in (Locator.BY.CSS, Locator.BY.CSS_SELECTOR):
            return self.find_by_css(locator[1])
        elif locator[0] != Locator.BY.XPATH:
            locator = Locator.xpath_translator(*locator)
        return self.tree.xpath(locator[1])

    def find_by_xpath(self, xpath: str):
        """find elements using xpath
        :param xpath:
        :rtype: []
        """
        return self.tree.xpath(xpath)

    def find_by_css(self, css: str, namespaces=None, translator='xml'):
        """find elements using css

        To use CSS namespaces, you need to pass a prefix-to-namespace
        mapping as ``namespaces`` keyword argument::

            rdfns = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
            select_ns = cssselect.CSSSelector('root > rdf|Description',
                                               namespaces={'rdf': rdfns})

            rdf = etree.XML((
                 '<root xmlns:rdf="%s">'
                   '<rdf:Description>blah</rdf:Description>'
                 '</root>') % rdfns)
            [(el.tag, el.text) for el in select_ns(rdf)]
            [('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description', 'blah')]
        :param css:
        :param namespaces:
        :param translator:
        :rtype: []
        """
        return cssselect.CSSSelector(css, namespaces=namespaces, translator=translator)

    def get_text(self, locator):
        """get elements text using xpath
        :param locator: ('XPATH', '//a')
        :rtype: [str]
        """
        return [element.text for element in self.find(locator)]