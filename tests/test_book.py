"""Tests for the book module."""
import datetime

import pytest

DOI_LEN_MIN = 5
DOI_LEN_MAX = 255
TITLE_LEN_MIN = 10


@pytest.fixture
def book_article(pubmed):
    """Fixture to create a PubMedBookArticle instance from dynamic XML."""
    return next(pubmed._getArticles(["7"]))


class TestPubMedBookArticle:
    """Tests for PubMedBookArticle."""

    def test_initialization_from_xml(self, book_article):
        """Test initialization of PubMedBookArticle."""
        title = book_article.title
        doi = book_article.doi

        assert isinstance(title, str) and len(title) > TITLE_LEN_MIN
        assert isinstance(doi, str) and DOI_LEN_MIN <= len(doi) <= DOI_LEN_MAX

    def test_publication_date_format(self, book_article):
        """Test the publication date format."""
        assert isinstance(book_article.publication_date, datetime.datetime)

    def test_authors_structure(self, book_article):
        """Test the structure of authors."""
        assert isinstance(book_article.authors, list), "Authors is not a list"
        if book_article.authors:  # Only test if there are authors
            assert all("lastname" in author for author in book_article.authors)
