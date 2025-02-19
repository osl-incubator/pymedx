"""Test PubMedCentral class."""

from __future__ import annotations

import datetime

from typing import cast

from lxml import etree as xml
from pymedx.api import PubMedCentral
from pymedx.article import PubMedCentralArticle


class TestPMC:
    """Test the helpers module."""

    def test_query_results(self) -> None:
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
        pmc_article = cast(PubMedCentralArticle, listed[0])
        assert len(listed) > 0
        assert len(pmc_article.title or "") > 0
        assert len(pmc_article.pmc_id or "") > 0

    def test_extracting_date(self) -> None:
        """Test date extraction."""
        root = xml.Element("root")
        date = xml.SubElement(root, "pub-date")
        xml.SubElement(date, "year").text = "\n2024"
        xml.SubElement(date, "month").text = "2\n"
        xml.SubElement(date, "day").text = "9"

        test_collector = PubMedCentralArticle()

        result = test_collector._extractPublicationDate(root)
        expected = datetime.datetime.strptime("2024/2/9", "%Y/%m/%d")

        assert result == expected

    def test_extracting_date_None(self) -> None:
        """Test date extraction."""
        root = xml.Element("root")
        date = xml.SubElement(root, "pub-date")
        xml.SubElement(date, "year").text = ""
        xml.SubElement(date, "month").text = "2\n"
        xml.SubElement(date, "day").text = "9"

        test_collector = PubMedCentralArticle()

        result = test_collector._extractPublicationDate(root)
        expected = None

        assert result == expected
