import pytest
from src.domain.services.player_archetype_service import PlayerArchetypeService
from src.schemas.analysis import PlayerAdvancedStats, PlayerArchetype


class TestPlayerArchetypeService:
    """Testes para validar regras de negócio de classificação de arquétipos"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.service = PlayerArchetypeService()

    def test_sniper_archetype_high_volume_elite_efficiency(self, sniper_stats):
        """Sniper: 3PA >= 5.0 E 3P% >= 40% deve ter score máximo"""
        analysis = self.service.analyze_player(sniper_stats)
        
        assert PlayerArchetype.SNIPER in analysis.archetypes
        assert analysis.archetype_scores[PlayerArchetype.SNIPER] == 100
        assert analysis.is_elite_shooter is True

    def test_sniper_requires_volume_and_efficiency(self):
        """Sniper: alto volume sem eficiência NÃO qualifica"""
        stats = PlayerAdvancedStats(
            player_id=1,
            player_name="Volume Chucker",
            fg3a=8.0,
            fg3_pct=0.30,
            position="SG"
        )
        analysis = self.service.analyze_player(stats)
        
        assert PlayerArchetype.SNIPER not in analysis.archetypes
        assert analysis.archetype_scores[PlayerArchetype.SNIPER] < 80

    def test_ball_dominant_high_usage(self, ball_dominant_stats):
        """Ball Dominant: USG% >= 30% deve ter score máximo"""
        analysis = self.service.analyze_player(ball_dominant_stats)
        
        assert PlayerArchetype.BALL_DOMINANT in analysis.archetypes
        assert analysis.is_ball_dominant is True

    def test_ball_dominant_moderate_usage(self):
        """Ball Dominant: USG% 25-30% qualifica com score menor"""
        stats = PlayerAdvancedStats(
            player_id=1,
            player_name="Secondary Star",
            usg_pct=0.26,
            position="SG"
        )
        analysis = self.service.analyze_player(stats)
        
        assert PlayerArchetype.BALL_DOMINANT in analysis.archetypes
        assert analysis.archetype_scores[PlayerArchetype.BALL_DOMINANT] == 80

    def test_playmaker_high_assists(self, playmaker_stats):
        """Playmaker: AST >= 8.0 deve ter score máximo"""
        analysis = self.service.analyze_player(playmaker_stats)
        
        assert PlayerArchetype.PLAYMAKER in analysis.archetypes
        assert analysis.archetype_scores[PlayerArchetype.PLAYMAKER] == 100

    def test_playmaker_boosted_by_ast_percentage(self):
        """Playmaker: AST% alto (> 30%) boost o score"""
        stats = PlayerAdvancedStats(
            player_id=1,
            player_name="Floor General",
            ast=5.0,
            ast_pct=0.35,
            position="PG"
        )
        analysis = self.service.analyze_player(stats)
        
        assert PlayerArchetype.PLAYMAKER in analysis.archetypes
        assert analysis.archetype_scores[PlayerArchetype.PLAYMAKER] >= 90

    def test_rim_protector_elite_blocker(self, rim_protector_stats):
        """Rim Protector: BLK >= 2.0 deve ter score máximo"""
        analysis = self.service.analyze_player(rim_protector_stats)
        
        assert PlayerArchetype.RIM_PROTECTOR in analysis.archetypes
        assert analysis.is_defensive_anchor is True
        assert analysis.archetype_scores[PlayerArchetype.RIM_PROTECTOR] == 100

    def test_rim_protector_moderate_blocker(self):
        """Rim Protector: BLK 1.5-2.0 qualifica com score menor"""
        stats = PlayerAdvancedStats(
            player_id=1,
            player_name="Shot Alterer",
            blk=1.7,
            position="C"
        )
        analysis = self.service.analyze_player(stats)
        
        assert PlayerArchetype.RIM_PROTECTOR in analysis.archetypes
        assert analysis.archetype_scores[PlayerArchetype.RIM_PROTECTOR] == 85

    def test_hustle_player_elite_rebounder(self, hustle_player_stats):
        """Hustle: REB >= 10 OU OREB >= 3.0 deve ter score máximo"""
        analysis = self.service.analyze_player(hustle_player_stats)
        
        assert PlayerArchetype.HUSTLE in analysis.archetypes
        assert analysis.archetype_scores[PlayerArchetype.HUSTLE] == 100

    def test_hustle_player_offensive_boards_specialist(self):
        """Hustle: especialista em rebotes ofensivos qualifica"""
        stats = PlayerAdvancedStats(
            player_id=1,
            player_name="Glass Cleaner",
            reb=7.0,
            oreb=3.5,
            position="PF"
        )
        analysis = self.service.analyze_player(stats)
        
        assert PlayerArchetype.HUSTLE in analysis.archetypes

    def test_three_and_d_requires_both_skills(self, three_and_d_stats):
        """3&D: precisa de ambos - shooting E defense"""
        analysis = self.service.analyze_player(three_and_d_stats)
        
        assert PlayerArchetype.THREE_AND_D in analysis.archetypes

    def test_three_and_d_shooter_only_not_qualify(self):
        """3&D: bom shooter sem defesa NÃO qualifica"""
        stats = PlayerAdvancedStats(
            player_id=1,
            player_name="Just Shooter",
            fg3a=5.0,
            fg3_pct=0.40,
            stl=0.3,
            blk=0.2,
            position="SG"
        )
        analysis = self.service.analyze_player(stats)
        
        assert PlayerArchetype.THREE_AND_D not in analysis.archetypes

    def test_stretch_big_center_with_range(self, stretch_big_stats):
        """Stretch Big: pivô (C ou F) com 3P% >= 35% e volume"""
        analysis = self.service.analyze_player(stretch_big_stats)
        
        assert PlayerArchetype.STRETCH_BIG in analysis.archetypes

    def test_stretch_big_guard_not_qualify(self):
        """Stretch Big: guards NÃO qualificam mesmo com bom arremesso"""
        stats = PlayerAdvancedStats(
            player_id=1,
            player_name="Sharp Shooting Guard",
            fg3a=5.0,
            fg3_pct=0.42,
            position="SG"
        )
        analysis = self.service.analyze_player(stats)
        
        assert PlayerArchetype.STRETCH_BIG not in analysis.archetypes

    def test_player_can_have_multiple_archetypes(self, ball_dominant_stats):
        """Jogador pode ter múltiplos arquétipos simultaneamente"""
        analysis = self.service.analyze_player(ball_dominant_stats)
        
        assert PlayerArchetype.BALL_DOMINANT in analysis.archetypes
        assert PlayerArchetype.PLAYMAKER in analysis.archetypes
        assert len(analysis.archetypes) >= 2

    def test_role_player_no_archetypes(self):
        """Role player mediano pode não ter nenhum arquétipo forte"""
        stats = PlayerAdvancedStats(
            player_id=1,
            player_name="Average Joe",
            pts=8.0,
            fg3a=2.0,
            fg3_pct=0.33,
            ast=2.0,
            reb=4.0,
            blk=0.3,
            stl=0.5,
            position="SF"
        )
        analysis = self.service.analyze_player(stats)
        
        assert len(analysis.archetypes) == 0

    def test_archetype_thresholds_boundary_values(self):
        """Teste de valores limítrofes para thresholds"""
        # Exatamente no threshold de Sniper (3PA=5.0, 3P%=37%)
        stats = PlayerAdvancedStats(
            player_id=1,
            player_name="Threshold Player",
            fg3a=5.0,
            fg3_pct=0.37,
            position="SG"
        )
        analysis = self.service.analyze_player(stats)
        
        assert PlayerArchetype.SNIPER in analysis.archetypes
        assert analysis.archetype_scores[PlayerArchetype.SNIPER] == 85
