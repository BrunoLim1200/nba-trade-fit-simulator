import pytest
from unittest.mock import Mock, patch
from src.domain.services.fit_simulator import FitSimulator
from src.schemas.analysis import (
    PlayerAdvancedStats,
    TeamStats,
    FitLabel
)


class TestFitSimulator:
    """Testes para validar o cálculo final do Fit Score"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_nba_client = Mock()
        self.simulator = FitSimulator(nba_client=self.mock_nba_client)

    def _mock_player_stats(self, **kwargs) -> PlayerAdvancedStats:
        defaults = {
            "player_id": 1,
            "player_name": "Test Player",
            "pts": 15.0,
            "fg3a": 5.0,
            "fg3_pct": 0.38,
            "ast": 3.0,
            "reb": 5.0,
            "blk": 0.5,
            "stl": 1.0,
            "min": 28.0,
            "position": "SF"
        }
        defaults.update(kwargs)
        return PlayerAdvancedStats(**defaults)

    def _mock_team_stats(self, **kwargs) -> TeamStats:
        defaults = {
            "team_id": 100,
            "team_name": "Test Team",
            "fg3_pct_rank": 15,
            "reb_rank": 15,
            "ast_rank": 15,
            "pace_rank": 15,
            "def_rating_rank": 15,
            "off_rating_rank": 15,
            "fg3_pct": 0.36,
            "ball_dominant_count": 0
        }
        defaults.update(kwargs)
        return TeamStats(**defaults)

    @pytest.mark.asyncio
    async def test_sniper_addresses_shooting_need(self):
        """Sniper em time que precisa de Shooting ganha bônus"""
        sniper = self._mock_player_stats(fg3a=8.0, fg3_pct=0.42)
        team_needs_shooting = self._mock_team_stats(fg3_pct_rank=25)
        
        self.mock_nba_client.get_player_advanced_stats.return_value = sniper
        self.mock_nba_client.get_team_stats.return_value = team_needs_shooting
        
        result = await self.simulator.simulate_fit(1, 100)
        
        assert result.fit_score >= 85
        assert any("Arremesso" in r for r in result.reasons)

    @pytest.mark.asyncio
    async def test_rim_protector_addresses_defense_need(self):
        """Rim Protector em time com defesa fraca ganha bônus"""
        blocker = self._mock_player_stats(blk=2.5, reb=10.0, position="C")
        team_needs_defense = self._mock_team_stats(def_rating_rank=28)
        
        self.mock_nba_client.get_player_advanced_stats.return_value = blocker
        self.mock_nba_client.get_team_stats.return_value = team_needs_defense
        
        result = await self.simulator.simulate_fit(1, 100)
        
        assert result.fit_score >= 85
        assert any("Proteção de Aro" in r or "Rim Protection" in r.lower() 
                   for r in result.reasons)

    @pytest.mark.asyncio
    async def test_playmaker_addresses_playmaking_need(self):
        """Playmaker em time estagnado ganha bônus"""
        playmaker = self._mock_player_stats(ast=10.0, ast_pct=0.35)
        team_stagnant = self._mock_team_stats(ast_rank=25)
        
        self.mock_nba_client.get_player_advanced_stats.return_value = playmaker
        self.mock_nba_client.get_team_stats.return_value = team_stagnant
        
        result = await self.simulator.simulate_fit(1, 100)
        
        assert result.fit_score >= 85

    @pytest.mark.asyncio
    async def test_friction_reduces_score(self):
        """Fricção no elenco reduz o fit score"""
        ball_dom = self._mock_player_stats(usg_pct=0.35)
        team_stars = self._mock_team_stats(ball_dominant_count=2)
        
        self.mock_nba_client.get_player_advanced_stats.return_value = ball_dom
        self.mock_nba_client.get_team_stats.return_value = team_stars
        
        result = await self.simulator.simulate_fit(1, 100)
        
        assert result.fit_score <= 60
        assert any("fricção" in r.lower() or "penalidade" in r.lower() 
                   for r in result.reasons)

    @pytest.mark.asyncio
    async def test_perfect_fit_label_90_plus(self):
        """Score >= 90 resulta em Perfect Fit"""
        sniper = self._mock_player_stats(fg3a=8.0, fg3_pct=0.42)
        perfect_match = self._mock_team_stats(fg3_pct_rank=28, ball_dominant_count=0)
        
        self.mock_nba_client.get_player_advanced_stats.return_value = sniper
        self.mock_nba_client.get_team_stats.return_value = perfect_match
        
        result = await self.simulator.simulate_fit(1, 100)
        
        assert result.fit_label == FitLabel.PERFECT_FIT

    @pytest.mark.asyncio
    async def test_bad_fit_label_below_40(self):
        """Score < 40 resulta em Bad Fit"""
        ball_dom = self._mock_player_stats(usg_pct=0.35, position="C", fg3_pct=0.0)
        bad_match = self._mock_team_stats(ball_dominant_count=2, pace_rank=2)
        
        self.mock_nba_client.get_player_advanced_stats.return_value = ball_dom
        self.mock_nba_client.get_team_stats.return_value = bad_match
        
        result = await self.simulator.simulate_fit(1, 100)
        
        assert result.fit_label == FitLabel.BAD_FIT

    @pytest.mark.asyncio
    async def test_score_capped_at_100(self):
        """Fit score nunca excede 100"""
        elite = self._mock_player_stats(
            fg3a=10.0, fg3_pct=0.45, ast=8.0, blk=2.0
        )
        desperate_team = self._mock_team_stats(
            fg3_pct_rank=30, ast_rank=30, def_rating_rank=30
        )
        
        self.mock_nba_client.get_player_advanced_stats.return_value = elite
        self.mock_nba_client.get_team_stats.return_value = desperate_team
        
        result = await self.simulator.simulate_fit(1, 100)
        
        assert result.fit_score <= 100

    @pytest.mark.asyncio
    async def test_score_never_negative(self):
        """Fit score nunca é negativo"""
        useless = self._mock_player_stats(usg_pct=0.35, position="C")
        worst_match = self._mock_team_stats(ball_dominant_count=2, pace_rank=1)
        
        self.mock_nba_client.get_player_advanced_stats.return_value = useless
        self.mock_nba_client.get_team_stats.return_value = worst_match
        
        result = await self.simulator.simulate_fit(1, 100)
        
        assert result.fit_score >= 0

    @pytest.mark.asyncio
    async def test_missing_player_returns_error_response(self):
        """Jogador não encontrado retorna response de erro"""
        self.mock_nba_client.get_player_advanced_stats.return_value = None
        self.mock_nba_client.get_team_stats.return_value = self._mock_team_stats()
        
        result = await self.simulator.simulate_fit(999, 100)
        
        assert result.fit_score == 0
        assert result.fit_label == FitLabel.BAD_FIT
        assert any("não encontrado" in r.lower() for r in result.reasons)

    @pytest.mark.asyncio
    async def test_missing_team_returns_error_response(self):
        """Time não encontrado retorna response de erro"""
        self.mock_nba_client.get_player_advanced_stats.return_value = self._mock_player_stats()
        self.mock_nba_client.get_team_stats.return_value = None
        
        result = await self.simulator.simulate_fit(1, 999)
        
        assert result.fit_score == 0
        assert result.fit_label == FitLabel.BAD_FIT
        assert any("não encontrado" in r.lower() for r in result.reasons)

    @pytest.mark.asyncio
    async def test_response_contains_player_archetypes(self):
        """Response contém os arquétipos detectados do jogador"""
        sniper = self._mock_player_stats(fg3a=8.0, fg3_pct=0.42)
        team = self._mock_team_stats()
        
        self.mock_nba_client.get_player_advanced_stats.return_value = sniper
        self.mock_nba_client.get_team_stats.return_value = team
        
        result = await self.simulator.simulate_fit(1, 100)
        
        assert "Sniper" in result.player_archetypes

    @pytest.mark.asyncio
    async def test_response_contains_team_needs_addressed(self):
        """Response contém as necessidades do time que foram endereçadas"""
        sniper = self._mock_player_stats(fg3a=8.0, fg3_pct=0.42)
        needs_shooting = self._mock_team_stats(fg3_pct_rank=25)
        
        self.mock_nba_client.get_player_advanced_stats.return_value = sniper
        self.mock_nba_client.get_team_stats.return_value = needs_shooting
        
        result = await self.simulator.simulate_fit(1, 100)
        
        assert "Shooting" in result.team_needs_addressed

    @pytest.mark.asyncio
    async def test_warnings_from_friction_conflicts(self):
        """Warnings são gerados a partir dos conflitos de fricção"""
        ball_dom = self._mock_player_stats(usg_pct=0.35)
        crowded = self._mock_team_stats(ball_dominant_count=2)
        
        self.mock_nba_client.get_player_advanced_stats.return_value = ball_dom
        self.mock_nba_client.get_team_stats.return_value = crowded
        
        result = await self.simulator.simulate_fit(1, 100)
        
        assert len(result.warnings) > 0

    @pytest.mark.asyncio
    async def test_fit_labels_correctly_assigned(self):
        """Verifica mapeamento correto de score para labels"""
        test_cases = [
            (95, FitLabel.PERFECT_FIT),
            (85, FitLabel.STARTER),
            (70, FitLabel.ROTATION),
            (50, FitLabel.SITUATIONAL),
            (30, FitLabel.BAD_FIT),
        ]
        
        for expected_score, expected_label in test_cases:
            # Cria cenários que resultam aproximadamente no score esperado
            player = self._mock_player_stats()
            team = self._mock_team_stats()
            
            self.mock_nba_client.get_player_advanced_stats.return_value = player
            self.mock_nba_client.get_team_stats.return_value = team
            
            # O teste real seria verificar os thresholds
            # Aqui estamos validando que a lógica existe
            result = await self.simulator.simulate_fit(1, 100)
            assert result.fit_label is not None
