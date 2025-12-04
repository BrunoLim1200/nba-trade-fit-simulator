from typing import List, Dict
from src.schemas.analysis import PlayerAdvancedStats, PlayerAnalysis, PlayerArchetype


class PlayerArchetypeService:
    """Classifica jogadores em arquétipos baseado em estatísticas."""

    def analyze_player(self, stats: PlayerAdvancedStats) -> PlayerAnalysis:
        archetypes = []
        scores = {}

        sniper_score = 0
        if stats.fg3a >= 5.0:
            if stats.fg3_pct >= 0.40:
                sniper_score = 100
            elif stats.fg3_pct >= 0.37:
                sniper_score = 85
            elif stats.fg3_pct >= 0.35:
                sniper_score = 60
        
        if sniper_score >= 80:
            archetypes.append(PlayerArchetype.SNIPER)
        scores[PlayerArchetype.SNIPER] = sniper_score

        ball_dom_score = 0
        if stats.usg_pct:
            if stats.usg_pct >= 0.30:
                ball_dom_score = 100
            elif stats.usg_pct >= 0.25:
                ball_dom_score = 80
            elif stats.usg_pct >= 0.20:
                ball_dom_score = 50
        
        if ball_dom_score >= 80:
            archetypes.append(PlayerArchetype.BALL_DOMINANT)
        scores[PlayerArchetype.BALL_DOMINANT] = ball_dom_score

        playmaker_score = 0
        if stats.ast >= 8.0:
            playmaker_score = 100
        elif stats.ast >= 6.0:
            playmaker_score = 85
        elif stats.ast >= 4.0:
            playmaker_score = 60
            
        if stats.ast_pct and stats.ast_pct > 0.30:
            playmaker_score = max(playmaker_score, 90)

        if playmaker_score >= 80:
            archetypes.append(PlayerArchetype.PLAYMAKER)
        scores[PlayerArchetype.PLAYMAKER] = playmaker_score

        rim_prot_score = 0
        if stats.blk >= 2.0:
            rim_prot_score = 100
        elif stats.blk >= 1.5:
            rim_prot_score = 85
        elif stats.blk >= 1.0:
            rim_prot_score = 60
            
        if rim_prot_score >= 80:
            archetypes.append(PlayerArchetype.RIM_PROTECTOR)
        scores[PlayerArchetype.RIM_PROTECTOR] = rim_prot_score

        hustle_score = 0
        if stats.reb >= 10.0 or stats.oreb >= 3.0:
            hustle_score = 100
        elif stats.reb >= 8.0 or stats.oreb >= 2.0:
            hustle_score = 85
        elif stats.reb >= 6.0:
            hustle_score = 60
            
        if hustle_score >= 80:
            archetypes.append(PlayerArchetype.HUSTLE)
        scores[PlayerArchetype.HUSTLE] = hustle_score

        three_d_score = 0
        is_good_shooter = stats.fg3_pct >= 0.36 and stats.fg3a >= 3.0
        is_good_defender = stats.stl >= 1.0 or stats.blk >= 0.8
        
        if is_good_shooter and is_good_defender:
            three_d_score = 90
        elif is_good_shooter and (stats.stl >= 0.8 or stats.blk >= 0.6):
            three_d_score = 75
            
        if three_d_score >= 80:
            archetypes.append(PlayerArchetype.THREE_AND_D)
        scores[PlayerArchetype.THREE_AND_D] = three_d_score

        stretch_score = 0
        is_big = "C" in stats.position or "F" in stats.position
        if is_big and stats.fg3_pct >= 0.35 and stats.fg3a >= 2.0:
            stretch_score = 90
        
        if stretch_score >= 80:
            archetypes.append(PlayerArchetype.STRETCH_BIG)
        scores[PlayerArchetype.STRETCH_BIG] = stretch_score

        is_ball_dominant = ball_dom_score >= 80
        is_elite_shooter = sniper_score >= 90
        is_defensive_anchor = rim_prot_score >= 90

        return PlayerAnalysis(
            player_id=stats.player_id,
            player_name=stats.player_name,
            position=stats.position,
            stats=stats,
            archetypes=archetypes,
            archetype_scores=scores,
            is_ball_dominant=is_ball_dominant,
            is_elite_shooter=is_elite_shooter,
            is_defensive_anchor=is_defensive_anchor,
            per=stats.per,
            estimated_minutes=stats.min
        )
