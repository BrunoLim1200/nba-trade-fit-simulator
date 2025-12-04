import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from src.main import app
from src.schemas.analysis import PlayerAdvancedStats, TeamStats


class TestSimulationAPI:
    """Testes de integração para os endpoints da API de simulação"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = TestClient(app)

    @patch("src.api.routes.simulation.nba_client")
    def test_search_players_returns_results(self, mock_nba_client):
        """Busca de jogadores retorna resultados formatados"""
        mock_nba_client.search_player_by_name.return_value = [
            {"id": 1, "full_name": "LeBron James", "is_active": True},
            {"id": 2, "full_name": "LeBron James Jr.", "is_active": False},
        ]
        
        response = self.client.get("/api/v1/players/search?name=lebron")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["full_name"] == "LeBron James"

    @patch("src.api.routes.simulation.nba_client")
    def test_search_players_limits_results(self, mock_nba_client):
        """Busca de jogadores limita a 10 resultados"""
        mock_nba_client.search_player_by_name.return_value = [
            {"id": i, "full_name": f"Player {i}", "is_active": True}
            for i in range(20)
        ]
        
        response = self.client.get("/api/v1/players/search?name=player")
        
        assert response.status_code == 200
        assert len(response.json()) == 10

    def test_search_players_requires_min_length(self):
        """Busca requer mínimo de 2 caracteres"""
        response = self.client.get("/api/v1/players/search?name=a")
        
        assert response.status_code == 422

    @patch("src.api.routes.simulation.nba_client")
    def test_get_all_teams_returns_list(self, mock_nba_client):
        """Endpoint de times retorna lista de times"""
        mock_nba_client.get_all_teams.return_value = [
            {"id": 1, "full_name": "Lakers", "abbreviation": "LAL", "city": "LA"},
            {"id": 2, "full_name": "Celtics", "abbreviation": "BOS", "city": "Boston"},
        ]
        
        response = self.client.get("/api/v1/teams")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    @patch("src.api.routes.simulation.fit_simulator")
    def test_simulate_fit_returns_result(self, mock_simulator):
        """Endpoint de simulação retorna resultado estruturado"""
        from src.schemas.simulation import SimulationResponse
        from src.schemas.analysis import FitLabel
        import asyncio
        
        mock_result = SimulationResponse(
            player_id=1,
            player_name="Test Player",
            team_id=100,
            team_name="Test Team",
            fit_score=85,
            fit_label=FitLabel.STARTER,
            reasons=["Bom encaixe"]
        )
        
        async def async_return(*args, **kwargs):
            return mock_result
        
        mock_simulator.simulate_fit = async_return
        
        response = self.client.get("/api/v1/simulate-fit?player_id=1&team_id=100")
        
        assert response.status_code == 200
        data = response.json()
        assert data["fit_score"] == 85
        assert data["player_name"] == "Test Player"

    def test_simulate_fit_requires_player_id(self):
        """Simulação requer player_id"""
        response = self.client.get("/api/v1/simulate-fit?team_id=100")
        
        assert response.status_code == 422

    def test_simulate_fit_requires_team_id(self):
        """Simulação requer team_id"""
        response = self.client.get("/api/v1/simulate-fit?player_id=1")
        
        assert response.status_code == 422
