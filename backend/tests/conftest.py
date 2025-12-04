# File: /nba-trade-fit-simulator/nba-trade-fit-simulator/backend/tests/conftest.py

import pytest

@pytest.fixture(scope="session")
def test_client():
    from src.main import app
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function")
def sample_data():
    # TODO: Create sample data for testing
    return {
        "player_id": 1,
        "team_id": 1,
        "expected_fit": "Titular",
        "minutagem_estimada": 30,
        "explicacao": "O jogador tem um PER superior ao titular da posição."
    }