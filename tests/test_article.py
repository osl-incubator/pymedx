"""Test for the article module."""

from __future__ import annotations

import datetime

from typing import cast

import pytest

from pymedx.api import PubMed
from pymedx.article import PubMedArticle

DOI_LEN_MIN = 5
DOI_LEN_MAX = 255


@pytest.fixture(scope="module")
def sample_article(pubmed: PubMed) -> PubMedArticle:
    """Fixture to create a PubMedArticle instance from dynamic XML."""
    pubmed_articles = pubmed.query("COVID-19 vaccines", max_results=10)
    article_ids = [pm.pubmed_id for pm in pubmed_articles]

    articles = pubmed._getArticles(article_ids[:1])
    article = next(articles)

    return cast(PubMedArticle, article)


class TestArticle:
    """Test article module."""

    def test_doi_length(self, sample_article: PubMedArticle) -> None:
        """Test that the DOI attribute has an expected length range."""
        doi = sample_article.doi
        # although, by definition, doi size could be infinite
        # it seems in the applications it is limited to 255
        # for example:
        # https://github.com/BirkbeckCTP/janeway/
        # blob/v1.5.1-RC-4/src/core/models.py#L1322
        assert DOI_LEN_MIN <= len(doi) <= DOI_LEN_MAX

    def test_title_exists(self, sample_article: PubMedArticle) -> None:
        """Test that the article title exists and is not empty."""
        title = sample_article.title
        assert title and len(title) > 0

    def test_abstract_structure(self, sample_article: PubMedArticle) -> None:
        """Test that the abstract exists and meets basic expectations."""
        abstract = sample_article.abstract or ""
        assert "vaccines" in abstract

    def test_publication_date_type(
        self, sample_article: PubMedArticle
    ) -> None:
        """Test that the publication date is a datetime.date object."""
        pub_date = sample_article.publication_date
        assert isinstance(pub_date, datetime.date)

    def test_toDict(self, sample_article: PubMedArticle) -> None:
        """Test toDict method."""
        article_dict = sample_article.toDict()
        assert article_dict

    def test_toJSON(self, sample_article: PubMedArticle) -> None:
        """Test toJSON method."""
        article_json = sample_article.toJSON()
        assert article_json
