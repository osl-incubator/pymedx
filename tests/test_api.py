"""Tests for the api module."""

from __future__ import annotations

from pymedx.api import PubMed


class TestPubMed:
    """Tests for PubMed."""

    def test_initialization(self, pubmed: PubMed, api_email: str) -> None:
        """Test the initialization of the PubMed class."""
        assert pubmed.tool == "TestTool"
        assert pubmed.email == api_email

    def test_rate_limit_not_exceeded(self, pubmed: PubMed) -> None:
        """Test that the rate limit is not exceeded initially."""
        assert not pubmed._exceededRateLimit()

    def test_query(self, pubmed: PubMed) -> None:
        """Test a simple query. This will hit the live PubMed API."""
        # Use a very specific query to limit results
        result = pubmed.query(
            query="COVID-19 vaccines",
            max_results=10,
        )
        articles = list(result)  # Convert from generator to list
        assert len(articles) > 0  # Assert that we got some results

    def test_get_total_results_count(self, pubmed: PubMed) -> None:
        """Test getting the total results count for a query."""
        count = pubmed.getTotalResultsCount(query="COVID-19 vaccines")
        assert isinstance(count, int)
        assert count > 0  # Assert that the query matches some results
