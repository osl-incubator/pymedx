"""Configuration for the tests."""

import os

from pathlib import Path
from typing import Dict, Generator, cast

import pytest
import requests_cache

from dotenv import dotenv_values, load_dotenv
from pymedx.api import PubMed, PubMedCentral


@pytest.fixture(scope="session", autouse=True)
def setup_request_cache() -> Generator[None, None, None]:
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


@pytest.fixture(scope="session")
def env() -> dict[str, str]:
    """Return a fixture for the environment variables from .env."""
    dotenv_file = Path(__file__).parent / ".env"
    if dotenv_file.exists():
        load_dotenv(dotenv_file)
        return cast(Dict[str, str], dotenv_values(dotenv_file) or {})
    return {}


@pytest.fixture(scope="session", autouse=True)
def api_email(env: dict[str, str]) -> str:
    """Fixture to create a PubMed instance."""
    return os.getenv("SERVICE_EMAIL", "")


@pytest.fixture(scope="session", autouse=True)
def api_key(env: dict[str, str]) -> str:
    """Fixture to create a PubMed instance."""
    return os.getenv("NCBI_API_KEY", "")


@pytest.fixture(scope="session", autouse=True)
def pubmed(env: dict[str, str], api_key: str, api_email: str) -> PubMed:
    """Fixture to create a PubMed instance."""
    params = dict(tool="TestTool", email=api_email)

    if api_key:
        params["api_key"] = api_key

    return PubMed(**params)


@pytest.fixture(scope="session", autouse=True)
def pmc(env: dict[str, str]) -> PubMedCentral:
    """Fixture to create a PubMed instance."""
    api_email = os.getenv("SERVICE_EMAIL", "")
    params = dict(tool="TestTool", email=api_email)

    api_key = os.getenv("NCBI_API_KEY", "")
    if api_key:
        params["api_key"] = api_key

    return PubMedCentral(**params)
