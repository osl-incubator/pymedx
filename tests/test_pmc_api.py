"""Tests for the api module."""

from __future__ import annotations

from pymedx.api import PubMedCentral


class TestPubMedCentral:
    """Tests for PubMedCentral."""

    def test_initialization(self, pmc: PubMedCentral, api_email: str) -> None:
        """Test the initialization of the PubMed class."""
        assert pmc.tool == "TestTool"
        assert pmc.email == api_email

    def test_rate_limit_not_exceeded(self, pmc: PubMedCentral) -> None:
        """Test that the rate limit is not exceeded initially."""
        assert not pmc._exceededRateLimit()

    def test_query(self, pmc: PubMedCentral) -> None:
        """Test a simple query. This will hit the live PubMed API."""
        # Use a very specific query to limit results
        articles = pmc.query(
            query="COVID-19 vaccines",
            max_results=10,
        )
        articles_list = list(articles)  # Convert from generator to list
        assert len(articles_list) > 0  # Assert that we got some results

    def test_get_total_results_count(self, pmc: PubMedCentral) -> None:
        """Test getting the total results count for a query."""
        count = pmc.getTotalResultsCount(query="COVID-19 vaccines")
        assert isinstance(count, int)
        assert count > 0  # Assert that the query matches some results
