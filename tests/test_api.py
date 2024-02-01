"""Tests for the api module."""

import pytest

from pymedx.api import (
    PubMed,
)


class TestPubMed:
    """Tests for PubMed."""

    @pytest.fixture
    def pubmed(self) -> PubMed:
        """Fixture to create a PubMed instance."""
        return PubMed(tool="TestTool", email="test@example.com")

    def test_initialization(self, pubmed: PubMed):
        """Test the initialization of the PubMed class."""
        assert pubmed.tool == "TestTool"
        assert pubmed.email == "test@example.com"

    def test_rate_limit_not_exceeded(self, pubmed: PubMed):
        """Test that the rate limit is not exceeded initially."""
        assert not pubmed._exceededRateLimit()

    def test_query(self, pubmed: PubMed):
        """Test a simple query. This will hit the live PubMed API."""
        # Use a very specific query to limit results
        articles = pubmed.query(
            query="COVID-19 vaccines",
            min_date="2021-01-01",
            max_date="2021-01-31",
            max_results=10,
        )
        articles = list(articles)  # Convert from generator to list
        assert len(articles) > 0  # Assert that we got some results

    def test_get_total_results_count(self, pubmed: PubMed):
        """Test getting the total results count for a query."""
        count = pubmed.getTotalResultsCount(query="COVID-19 vaccines")
        assert isinstance(count, int)
        assert count > 0  # Assert that the query matches some results
