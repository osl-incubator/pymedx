"""Configuration for the tests."""
import pytest
import requests_cache


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
