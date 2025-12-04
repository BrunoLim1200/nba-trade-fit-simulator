from typing import Optional, List
from src.infrastructure.external.nba_api_client import NBAApiClient
from src.schemas.simulation import SimulationResponse
from src.schemas.analysis import FitLabel, TradeResult

from src.domain.services.player_archetype_service import PlayerArchetypeService
from src.domain.services.team_gap_service import TeamGapService
from src.domain.services.roster_friction_service import RosterFrictionService

class FitSimulator:

    def __init__(self, nba_client: Optional[NBAApiClient] = None):
        self.nba_client = nba_client or NBAApiClient()
        self.archetype_service = PlayerArchetypeService()
        self.gap_service = TeamGapService()
        self.friction_service = RosterFrictionService()

    async def simulate_fit(self, player_id: int, team_id: int) -> SimulationResponse:
        player_stats = self.nba_client.get_player_advanced_stats(player_id)
        if not player_stats:
            return self._create_error_response(player_id, team_id, "Dados do jogador não encontrados.")
        team_stats = self.nba_client.get_team_stats(team_id)
        if not team_stats:
            return self._create_error_response(player_id, team_id, "Dados do time não encontrados.")
        player_analysis = self.archetype_service.analyze_player(player_stats)
        team_needs = self.gap_service.analyze_team_needs(team_stats)
        friction_result = self.friction_service.analyze_friction(player_analysis, team_stats)
        fit_score, fit_label, reasons = self._calculate_final_verdict(
            player_analysis, team_needs, friction_result
        )

        return SimulationResponse(
            player_id=player_id,
            player_name=player_analysis.player_name,
            team_id=team_id,
            team_name=team_stats.team_name,
            fit_score=fit_score,
            fit_label=fit_label,
            estimated_minutes=player_analysis.estimated_minutes, # Pode ser ajustado pelo friction
            projected_role=friction_result.suggested_role,
            player_archetypes=[a.value for a in player_analysis.archetypes],
            team_needs_addressed=[n.value for n in team_needs.needs],
            reasons=reasons,
            warnings=[c.description for c in friction_result.conflicts],
            breakdown={
                "archetype_match": 80, # Placeholder
                "need_match": 70,      # Placeholder
                "friction_penalty": friction_result.total_penalty
            },
            player_analysis=player_analysis,
            team_needs=team_needs,
            friction_result=friction_result
        )

    def _calculate_final_verdict(self, player, needs, friction):
        score = 75 # Base score
        reasons = []

        needs_met = 0
        for need in needs.needs:
            if need.value == "Shooting" and ("Sniper" in player.archetypes or "Stretch Big" in player.archetypes):
                score += 15
                needs_met += 1
                reasons.append("Atende a necessidade crítica de Arremesso.")
            
            if need.value == "Rim Protection" and "Rim Protector" in player.archetypes:
                score += 15
                needs_met += 1
                reasons.append("Preenche a lacuna de Proteção de Aro.")

            if need.value == "Playmaking" and "Playmaker" in player.archetypes:
                score += 15
                needs_met += 1
                reasons.append("Traz a criação de jogadas necessária.")

        score -= friction.total_penalty
        if friction.total_penalty > 0:
            reasons.append(f"Penalidade de fricção: -{friction.total_penalty} pontos.")

        score = max(0, min(100, score))
        
        if score >= 90:
            label = FitLabel.PERFECT_FIT
        elif score >= 80:
            label = FitLabel.STARTER
        elif score >= 60:
            label = FitLabel.ROTATION
        elif score >= 40:
            label = FitLabel.SITUATIONAL
        else:
            label = FitLabel.BAD_FIT

        return score, label, reasons

    def _create_error_response(self, pid, tid, msg):
        return SimulationResponse(
            player_id=pid, player_name="Unknown", team_id=tid, team_name="Unknown",
            fit_score=0, fit_label=FitLabel.BAD_FIT, reasons=[msg]
        )
