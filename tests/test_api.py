"""Tests for the api module."""


from pymedx.api import (
    PubMed,
)


class TestPubMed:
    """Tests for PubMed."""

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
            max_results=10,
        )
        articles = list(articles)  # Convert from generator to list
        assert len(articles) > 0  # Assert that we got some results

    def test_get_total_results_count(self, pubmed: PubMed):
        """Test getting the total results count for a query."""
        count = pubmed.getTotalResultsCount(query="COVID-19 vaccines")
        assert isinstance(count, int)
        assert count > 0  # Assert that the query matches some results
