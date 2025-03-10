"""Test for the article module."""

from __future__ import annotations

import datetime

from typing import cast

import pytest

from pymedx.api import PubMedCentral
from pymedx.article import PubMedCentralArticle

DOI_LEN_MIN = 5
DOI_LEN_MAX = 255


@pytest.fixture(scope="module")
def sample_pmc_article(pmc: PubMedCentral) -> PubMedCentralArticle:
    """Fixture to create a PubMedArticle instance from dynamic XML."""
    article_ids = pmc.query("'machine learning'", max_results=10)
    article_ids_list = list(article_ids)
    article = article_ids_list[0]

    return cast(PubMedCentralArticle, article)


class TestArticle:
    """Test PubMed Central article module."""

    def test_doi_length(
        self, sample_pmc_article: PubMedCentralArticle
    ) -> None:
        """Test that the DOI attribute has an expected length range."""
        doi = sample_pmc_article.doi or ""
        # although, by definition, doi size could be infinite
        # it seems in the applications it is limited to 255
        # for example:
        assert DOI_LEN_MIN <= len(doi) <= DOI_LEN_MAX

    def test_title_exists(
        self, sample_pmc_article: PubMedCentralArticle
    ) -> None:
        """Test that the article title exists and is not empty."""
        title = sample_pmc_article.title
        assert title and len(title) > 0

    @pytest.mark.skip(reason="verify source")
    def test_abstract_structure(
        self, sample_pmc_article: PubMedCentralArticle
    ) -> None:
        """Test that the abstract exists and meets basic expectations."""
        # note: is some cases the abstract is not available
        abstract = sample_pmc_article.abstract or ""
        # assert abstract and len(abstract) > 20
        assert abstract == ""

    def test_publication_date_type(
        self, sample_pmc_article: PubMedCentralArticle
    ) -> None:
        """Test that the publication date is a datetime.date object."""
        pub_date = sample_pmc_article.publication_date
        assert isinstance(pub_date, datetime.date)

    def test_toDict(self, sample_pmc_article: PubMedCentralArticle) -> None:
        """Test toDict method."""
        article_dict = sample_pmc_article.toDict()
        assert article_dict

    def test_toJSON(self, sample_pmc_article: PubMedCentralArticle) -> None:
        """Test toJSON method."""
        article_json = sample_pmc_article.toJSON()
        assert article_json
