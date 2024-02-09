"""Tests for the api module."""


from pymedx.api import PubMedCentral


class TestPubMed:
    """Tests for PubMed."""

    def test_initialization(self, pmc: PubMedCentral):
        """Test the initialization of the PubMed class."""
        assert pmc.tool == "TestTool"
        assert pmc.email == "test@example.com"

    def test_rate_limit_not_exceeded(self, pmc: PubMedCentral):
        """Test that the rate limit is not exceeded initially."""
        assert not pmc._exceededRateLimit()

    def test_query(self, pmc: PubMedCentral):
        """Test a simple query. This will hit the live PubMed API."""
        # Use a very specific query to limit results
        articles = pmc.query(
            query="COVID-19 vaccines",
            max_results=10,
        )
        articles = list(articles)  # Convert from generator to list
        assert len(articles) > 0  # Assert that we got some results

    def test_get_total_results_count(self, pmc: PubMedCentral):
        """Test getting the total results count for a query."""
        count = pmc.getTotalResultsCount(query="COVID-19 vaccines")
        assert isinstance(count, int)
        assert count > 0  # Assert that the query matches some results
