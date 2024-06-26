"""Configuration for the tests."""
import os

import pytest
import requests_cache

from pymedx.api import PubMed, PubMedCentral


@pytest.fixture(scope="session", autouse=True)
def setup_request_cache():
    """
    Initialize the cache before any tests.

    Run 'api_cache' is the cache name, and `expire_after`
    defines the expiration of the cache in seconds.

    Set `expire_after` to None for an infinite cache
    Adjust `backend` and `expire_after` as needed.
    """
    requests_cache.install_cache(
        "api_cache", backend="sqlite", expire_after=86400
    )

    # This setup will automatically apply to all tests in the session
    yield
    # Teardown logic if necessary;
    # requests_cache doesn't require special teardown


@pytest.fixture(scope="session", autouse=True)
def pubmed() -> PubMed:
    """Fixture to create a PubMed instance."""
    params = dict(tool="TestTool", email="test@example.com")

    api_key = os.getenv("NCBI_API_KEY", "")
    if api_key:
        params["api_key"] = api_key

    return PubMed(**params)


@pytest.fixture(scope="session", autouse=True)
def pmc() -> PubMedCentral:
    """Fixture to create a PubMed instance."""
    params = dict(tool="TestTool", email="test@example.com")

    api_key = os.getenv("NCBI_API_KEY", "")
    if api_key:
        params["api_key"] = api_key

    return PubMedCentral(**params)
