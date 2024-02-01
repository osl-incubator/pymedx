"""Module for handling articles."""
import datetime
import json

from typing import Any, Dict, List, Optional, Union
from xml.etree.ElementTree import Element

from .helpers import getContent


class PubMedArticle(object):
    """Data class that contains a PubMed article."""

    __slots__ = (
        "pubmed_id",
        "title",
        "abstract",
        "keywords",
        "journal",
        "publication_date",
        "authors",
        "methods",
        "conclusions",
        "results",
        "copyrights",
        "doi",
        "xml",
    )

    def __init__(
        self,
        xml_element: Optional[Element] = None,
        *args: List[Any],
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

    def _extractPubMedId(self, xml_element: Element) -> Union[str, None, int]:
        path = ".//ArticleId[@IdType='pubmed']"
        return getContent(element=xml_element, path=path)

    def _extractTitle(self, xml_element: Element) -> Union[str, None, int]:
        path = ".//ArticleTitle"
        return getContent(element=xml_element, path=path)

    def _extractKeywords(self, xml_element: Element) -> List[Any]:
        path = ".//Keyword"
        return [
            keyword.text
            for keyword in xml_element.findall(path)
            if keyword is not None
        ]

    def _extractJournal(self, xml_element: Element) -> Union[str, None, int]:
        path = ".//Journal/Title"
        return getContent(element=xml_element, path=path)

    def _extractAbstract(self, xml_element: Element) -> Union[str, None, int]:
        path = ".//AbstractText"
        return getContent(element=xml_element, path=path)

    def _extractConclusions(
        self: object, xml_element: Element
    ) -> Union[str, None, int]:
        path = ".//AbstractText[@Label='CONCLUSION']"
        return getContent(element=xml_element, path=path)

    def _extractMethods(self, xml_element: Element) -> Union[str, None, int]:
        path = ".//AbstractText[@Label='METHOD']"
        return getContent(element=xml_element, path=path)

    def _extractResults(self, xml_element: Element) -> Union[str, None, int]:
        path = ".//AbstractText[@Label='RESULTS']"
        return getContent(element=xml_element, path=path)

    def _extractCopyrights(
        self, xml_element: Element
    ) -> Union[str, None, int]:
        path = ".//CopyrightInformation"
        return getContent(element=xml_element, path=path)

    def _extractDoi(self, xml_element: Element) -> Union[str, None, int]:
        path = ".//ArticleId[@IdType='doi']"
        return getContent(element=xml_element, path=path)

    def _extractPublicationDate(
        self, xml_element: Element
    ) -> Optional[datetime.date]:
        # Get the publication date

        # Get the publication elements
        publication_date = xml_element.find(
            ".//PubMedPubDate[@PubStatus='pubmed']"
        )
        if publication_date is not None:
            publication_year = getContent(publication_date, ".//Year", None)

            publication_month = getContent(publication_date, ".//Month", "1")

            publication_day = getContent(publication_date, ".//Day", "1")

            # Construct a datetime object from the info
            date_str: str = (
                f"{publication_year}/{publication_month}/{publication_day}"
            )

            return datetime.datetime.strptime(date_str, "%Y/%m/%d")

        # Unable to parse the datetime
        return None

    def _extractAuthors(
        self, xml_element: Element
    ) -> List[dict[str, Union[str, None, int]]]:
        return [
            {
                "lastname": getContent(author, ".//LastName", None),
                "firstname": getContent(author, ".//ForeName", None),
                "initials": getContent(author, ".//Initials", None),
                "affiliation": getContent(
                    author, ".//AffiliationInfo/Affiliation", None
                ),
            }
            for author in xml_element.findall(".//Author")
        ]

    def _initializeFromXML(self, xml_element: Element) -> None:
        """Parse an XML element into an article object."""
        # Parse the different fields of the article
        self.pubmed_id = self._extractPubMedId(xml_element)
        self.title = self._extractTitle(xml_element)
        self.keywords = self._extractKeywords(xml_element)
        self.journal = self._extractJournal(xml_element)
        self.abstract = self._extractAbstract(xml_element)
        self.conclusions = self._extractConclusions(xml_element)
        self.methods = self._extractMethods(xml_element)
        self.results = self._extractResults(xml_element)
        self.copyrights = self._extractCopyrights(xml_element)
        self.doi = self._extractDoi(xml_element)
        self.publication_date = self._extractPublicationDate(xml_element)
        self.authors = self._extractAuthors(xml_element)
        self.xml = xml_element

    def toDict(self) -> Dict[Any, Any]:
        """Convert the parsed information to a Python dict."""
        return {key: self.__getattribute__(key) for key in self.__slots__}

    def toJSON(self) -> str:
        """Dump the object as JSON string."""
        return json.dumps(
            {
                key: (
                    value
                    if not isinstance(value, (datetime.date, Element))
                    else str(value)
                )
                for key, value in self.toDict().items()
            },
            sort_keys=True,
            indent=4,
        )
