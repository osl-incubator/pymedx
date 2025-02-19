"""Tests for the book module."""

from __future__ import annotations

import datetime

from typing import cast

import pytest

from pymedx.api import PubMed
from pymedx.article import PubMedArticle

DOI_LEN_MIN = 5
DOI_LEN_MAX = 255
TITLE_LEN_MIN = 10


@pytest.fixture
def book_article(pubmed: PubMed) -> PubMedArticle:
    """Fixture to create a PubMedBookArticle instance from dynamic XML."""
    return cast(PubMedArticle, next(pubmed._getArticles(["7"])))


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
