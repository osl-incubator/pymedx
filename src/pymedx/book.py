"""Module for functions about book article."""
import datetime
import json

from typing import Any, Dict, List, Optional, Union
from xml.etree.ElementTree import Element

from .helpers import getContent


class PubMedBookArticle(object):
    """Data class that contains a PubMed article."""

    __slots__ = (
        "pubmed_id",
        "title",
        "abstract",
        "publication_date",
        "authors",
        "copyrights",
        "doi",
        "isbn",
        "language",
        "publication_type",
        "sections",
        "publisher",
        "publisher_location",
    )

    def __init__(
        self,
        xml_element: Optional[Element] = None,
        *args: List[str],
        **kwargs: Dict[Any, Any],
    ) -> None:
        """Initialize of the object from XML or from parameters."""
        if args:
            # keep it for resolving problems with linter
            pass
        # If an XML element is provided, use it for initialization
        if xml_element is not None:
            self._initializeFromXML(xml_element=xml_element)

        # If no XML element was provided, try to parse the input parameters
        else:
            for field in self.__slots__:
                self.__setattr__(field, kwargs.get(field, None))

    def _extractPubMedId(
        self: object, xml_element: Element
    ) -> Union[str, None, int]:
        path = ".//ArticleId[@IdType='pubmed']"
        return getContent(element=xml_element, path=path)

    def _extractTitle(
        self: object, xml_element: Element
    ) -> Union[str, None, int]:
        path = ".//BookTitle"
        return getContent(element=xml_element, path=path)

    def _extractAbstract(
        self: object, xml_element: Element
    ) -> Union[str, None, int]:
        path = ".//AbstractText"
        return getContent(element=xml_element, path=path)

    def _extractCopyrights(
        self: object, xml_element: Element
    ) -> Union[str, None, int]:
        path = ".//CopyrightInformation"
        return getContent(element=xml_element, path=path)

    def _extractDoi(
        self: object, xml_element: Element
    ) -> Union[str, None, int]:
        path = ".//ArticleId[@IdType='doi']"
        return getContent(element=xml_element, path=path)

    def _extractIsbn(
        self: object, xml_element: Element
    ) -> Union[str, None, int]:
        path = ".//Isbn"
        return getContent(element=xml_element, path=path)

    def _extractLanguage(
        self: object, xml_element: Element
    ) -> Union[str, None, int]:
        path = ".//Language"
        return getContent(element=xml_element, path=path)

    def _extractPublicationType(
        self, xml_element: Element
    ) -> Union[str, None, int]:
        path = ".//PublicationType"
        return getContent(element=xml_element, path=path)

    def _extractPublicationDate(
        self, xml_element: Element
    ) -> Union[str, None, int]:
        path = ".//PubDate/Year"
        return getContent(element=xml_element, path=path)

    def _extractPublisher(self, xml_element: Element) -> Union[str, None, int]:
        path = ".//Publisher/PublisherName"
        return getContent(element=xml_element, path=path)

    def _extractPublisherLocation(
        self, xml_element: Element
    ) -> Union[str, None, int]:
        path = ".//Publisher/PublisherLocation"
        return getContent(element=xml_element, path=path)

    def _extractAuthors(
        self: object, xml_element: Element
    ) -> List[dict[str, Union[str, None, int]]]:
        return [
            {
                "collective": getContent(author, path=".//CollectiveName"),
                "lastname": getContent(element=author, path=".//LastName"),
                "firstname": getContent(element=author, path=".//ForeName"),
                "initials": getContent(element=author, path=".//Initials"),
            }
            for author in xml_element.findall(".//Author")
        ]

    def _extractSections(
        self, xml_element: Element
    ) -> List[dict[str, Union[str, None, int]]]:
        return [
            {
                "title": getContent(section, path=".//SectionTitle"),
                "chapter": getContent(
                    element=section, path=".//LocationLabel"
                ),
            }
            for section in xml_element.findall(".//Section")
        ]

    def _initializeFromXML(self, xml_element: Element) -> None:
        """Parse an XML element into an article object."""
        # Parse the different fields of the article
        self.pubmed_id = self._extractPubMedId(xml_element)
        self.title = self._extractTitle(xml_element)
        self.abstract = self._extractAbstract(xml_element)
        self.copyrights = self._extractCopyrights(xml_element)
        self.doi = self._extractDoi(xml_element)
        self.isbn = self._extractIsbn(xml_element)
        self.language = self._extractLanguage(xml_element)
        self.publication_date = self._extractPublicationDate(xml_element)
        self.authors = self._extractAuthors(xml_element)
        self.publication_type = self._extractPublicationType(xml_element)
        self.publisher = self._extractPublisher(xml_element)
        self.publisher_location = self._extractPublisherLocation(xml_element)
        self.sections = self._extractSections(xml_element)

    def toDict(self) -> Dict[Any, Any]:
        """Convert the parsed information to a Python dict."""
        return {
            key: (self.__getattribute__(key) if hasattr(self, key) else None)
            for key in self.__slots__
        }

    def toJSON(self) -> str:
        """Dump the object as JSON string."""
        return json.dumps(
            {
                key: (
                    value
                    if not isinstance(value, datetime.date)
                    else str(value)
                )
                for key, value in self.toDict().items()
            },
            sort_keys=True,
            indent=4,
        )
