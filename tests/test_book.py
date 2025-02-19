"""Tests for the book module."""

from __future__ import annotations

import datetime

from pathlib import Path
from typing import cast

import pytest

from lxml import etree
from lxml.etree import _Element
from pymedx.api import PubMed
from pymedx.article import PubMedArticle
from pymedx.book import PubMedBookArticle

DOI_LEN_MIN = 5
DOI_LEN_MAX = 255
TITLE_LEN_MIN = 10


@pytest.fixture
def book_article(pubmed: PubMed) -> PubMedArticle:
    """Fixture to create a PubMedBookArticle instance from dynamic XML."""
    return cast(PubMedArticle, next(pubmed._getArticles(["7"])))


@pytest.fixture
def pubmed_book_article(pubmed: PubMed) -> PubMedBookArticle:
    """Fixture to create a PubMedBookArticle instance from dynamic XML."""
    path_data = Path(__file__).parent / "data" / "pmid_ 31815395.xml"
    with open(path_data, "r", encoding="utf-8") as file:
        xml_content = file.read()
    xml_element: _Element = etree.fromstring(xml_content)
    return PubMedBookArticle(xml_element=xml_element)


class TestPubMedBookArticle:
    """Tests for PubMedBookArticle."""

    def test_initialization_from_xml(
        self, book_article: PubMedArticle
    ) -> None:
        """Test initialization of PubMedBookArticle."""
        title = book_article.title
        doi = book_article.doi

        assert isinstance(title, str) and len(title) > TITLE_LEN_MIN
        assert isinstance(doi, str) and DOI_LEN_MIN <= len(doi) <= DOI_LEN_MAX

    def test_publication_date_format(
        self, book_article: PubMedArticle
    ) -> None:
        """Test the publication date format."""
        assert isinstance(book_article.publication_date, datetime.datetime)

    def test_authors_structure(self, book_article: PubMedArticle) -> None:
        """Test the structure of authors."""
        assert isinstance(book_article.authors, list), "Authors is not a list"
        if book_article.authors:  # Only test if there are authors
            assert all("lastname" in author for author in book_article.authors)

    def test_multi_values(
        self, pubmed_book_article: PubMedBookArticle
    ) -> None:
        """Test if the attributes don't have multi values."""
        expected_abstract = (
            "Understanding of biological processes and aberrations in disease "
            "conditions has over the years moved away from the study of "
            "single molecules to a more holistic and all-encompassing view "
            "to investigate the entire spectrum of proteins. This method, "
            "termed proteomics, has been enabled principally by mass "
            "spectrometry techniques. The power of mass spectrometry-based "
            "proteomics lays in its ability to investigate an entire proteome "
            "and associated expression or modification states of a huge "
            "amount of proteins in one single experiment. This massive "
            "amount of data requires a high level of automation in data "
            "processing to render it into a reduced set of information that "
            "can be used to answer the initial hypotheses, explore the "
            "biology or contextualize molecular changes associated with a "
            "physiological attribute. This chapter gives an overview of the "
            "most common proteomic approaches, biological sample "
            "considerations and data acquisition methods, data processing, "
            "software solutions for the various steps and further functional "
            "analyses of biological data. This enables the comparison of "
            "various datasets as a summation of individual experiments, to "
            "cross-compare sample types and other metadata. There are many "
            "approach pipelines in existence that cover specialist "
            "disciplines and data analytics steps, and it is a certainty "
            "that many more data analysis methodologies will be generated "
            "over the coming years, but it also emphasizes the inherent place "
            "of proteomic technologies in research in elucidating the nature "
            "of biological processes and understanding of disease etiology."
        )

        assert (
            pubmed_book_article.doi == "10.15586/computationalbiology.2019.ch8"
        )
        assert pubmed_book_article.title == "Computational Biology"
        assert pubmed_book_article.abstract == expected_abstract
        assert pubmed_book_article.pubmed_id == "31815395"
