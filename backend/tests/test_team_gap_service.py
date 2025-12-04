import pytest
from src.domain.services.team_gap_service import TeamGapService
from src.schemas.analysis import TeamStats, TeamNeed


class TestTeamGapService:
    """Testes para validar regras de negócio de identificação de lacunas do time"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = TeamGapService()

    def test_shooting_gap_bottom_10_teams(self, team_needs_shooting):
        """Time no bottom 10 em 3P% (rank > 20) precisa de Shooting"""
        needs = self.service.analyze_team_needs(team_needs_shooting)
        
        assert TeamNeed.SHOOTING in needs.needs
        assert needs.needs_priority[TeamNeed.SHOOTING] == 10

    def test_defense_gap_identifies_both_needs(self, team_needs_defense):
        """Time com defesa fraca precisa de Perimeter Defense E Rim Protection"""
        needs = self.service.analyze_team_needs(team_needs_defense)
        
        assert TeamNeed.PERIMETER_DEFENSE in needs.needs
        assert TeamNeed.RIM_PROTECTION in needs.needs

    def test_balanced_team_fewer_needs(self, balanced_team):
        """Time equilibrado não tem necessidades críticas"""
        needs = self.service.analyze_team_needs(balanced_team)
        
        assert len(needs.needs) == 0
        assert len(needs.style_alerts) == 0

    def test_needs_are_prioritized(self):
        """Necessidades são ordenadas por prioridade"""
        team = TeamStats(
            team_id=1,
            team_name="Multi-Need Team",
            fg3_pct_rank=25,
            reb_rank=22,
            ast_rank=24,
            pace_rank=15,
            def_rating_rank=10,
            off_rating_rank=23,
            fg3_pct=0.30,
            ball_dominant_count=0
        )
        needs = self.service.analyze_team_needs(team)
        
        assert len(needs.needs) >= 3
        # Scoring e Shooting devem ter prioridade 10
        assert needs.needs_priority.get(TeamNeed.SCORING) == 10
        assert needs.needs_priority.get(TeamNeed.SHOOTING) == 10

    def test_playmaking_gap_detected(self):
        """Time com ast_rank > 20 precisa de Playmaking"""
        team = TeamStats(
            team_id=1,
            team_name="No Playmakers",
            fg3_pct_rank=10,
            reb_rank=10,
            ast_rank=26,
            pace_rank=15,
            def_rating_rank=10,
            off_rating_rank=10,
            fg3_pct=0.36,
            ball_dominant_count=0
        )
        needs = self.service.analyze_team_needs(team)
        
        assert TeamNeed.PLAYMAKING in needs.needs

    def test_rebounding_gap_detected(self):
        """Time com reb_rank > 20 precisa de Rebounding"""
        team = TeamStats(
            team_id=1,
            team_name="No Boards",
            fg3_pct_rank=10,
            reb_rank=28,
            ast_rank=10,
            pace_rank=15,
            def_rating_rank=10,
            off_rating_rank=10,
            fg3_pct=0.36,
            ball_dominant_count=0
        )
        needs = self.service.analyze_team_needs(team)
        
        assert TeamNeed.REBOUNDING in needs.needs

    def test_scoring_gap_from_offensive_rating(self):
        """Time com off_rating_rank > 20 precisa de Scoring"""
        team = TeamStats(
            team_id=1,
            team_name="Offensive Struggles",
            fg3_pct_rank=10,
            reb_rank=10,
            ast_rank=10,
            pace_rank=15,
            def_rating_rank=10,
            off_rating_rank=25,
            fg3_pct=0.36,
            ball_dominant_count=0
        )
        needs = self.service.analyze_team_needs(team)
        
        assert TeamNeed.SCORING in needs.needs

    def test_moderate_weakness_lower_priority(self):
        """Fraqueza moderada (rank 16-20) tem prioridade menor"""
        team = TeamStats(
            team_id=1,
            team_name="Moderate Weakness",
            fg3_pct_rank=18,
            reb_rank=10,
            ast_rank=10,
            pace_rank=15,
            def_rating_rank=10,
            off_rating_rank=10,
            fg3_pct=0.34,
            ball_dominant_count=0
        )
        needs = self.service.analyze_team_needs(team)
        
        assert TeamNeed.SHOOTING in needs.needs
        assert needs.needs_priority[TeamNeed.SHOOTING] == 5

    def test_alerts_generated_for_critical_gaps(self, team_needs_shooting):
        """Alertas são gerados para lacunas críticas"""
        needs = self.service.analyze_team_needs(team_needs_shooting)
        
        assert len(needs.style_alerts) > 0
        assert any("3 pontos" in alert for alert in needs.style_alerts)

    def test_team_stats_preserved_in_result(self, team_needs_shooting):
        """TeamStats original é preservado no resultado"""
        needs = self.service.analyze_team_needs(team_needs_shooting)
        
        assert needs.team_stats is not None
        assert needs.team_stats.team_id == team_needs_shooting.team_id
