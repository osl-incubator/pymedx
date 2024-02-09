"""Test PubMedCentral class."""


from pymedx.api import PubMedCentral


class TestPMC:
    """Test the helpers module."""

    def test_query_results(self):
        """Test the batches function."""
        email = "email@email.com"
        tool = "testing"
        collector = PubMedCentral(tool=tool, email=email)
        query = (
            'chile AND wastewater ("2000/01/01"[Publication Date]'
            ' : "3000"[Publication Date])'
        )
        results = collector.query(query=query, max_results=10)
        listed = list(results)
        assert len(listed) > 0
        assert len(listed[0].title) > 0
        assert len(listed[0].pmc_id) > 0
