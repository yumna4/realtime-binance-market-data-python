from typing import Any
from typing import Generator
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import sys
import os

from router import market_data

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def start_application():
    app = FastAPI()
    app.include_router(market_data.router, prefix=f"/api/v1/market_data", tags=["Market Data"])
    return app


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """

    _app = start_application()
    yield _app


@pytest.fixture(scope="function")
def client(
    app: FastAPI,
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    with TestClient(app) as client:
        yield client


def test_get_historical_data(client):
    response = client.get("api/v1/market_data/history?timestamp=2024-03-30T11%3A49%3A50&symbol=BTCUSDT")
    assert response.status_code == 200
    assert response.json()["price"] == 69943


def test_get_statistical_oprations(client):
    response = client.get("api/v1/market_data/statistical_operation?start_timestamp=2024-03-30%2011%3A49%3A50&end_timestamp=2024-03-30%2011%3A51%3A50&symbol=BTCUSDT")
    assert response.status_code == 200
    assert response.json()["value"] == 69942