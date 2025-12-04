from typing import List, Dict
from src.schemas.analysis import TeamStats, TeamNeeds, TeamNeed


class TeamGapService:
    """Identifica lacunas e necessidades do time baseado em rankings."""

    def analyze_team_needs(self, team_stats: TeamStats) -> TeamNeeds:
        needs = []
        priorities = {}
        alerts = []

        if team_stats.fg3_pct_rank > 20:
            needs.append(TeamNeed.SHOOTING)
            priorities[TeamNeed.SHOOTING] = 10  # Alta prioridade
            alerts.append("Time está entre os piores em aproveitamento de 3 pontos.")
        elif team_stats.fg3_pct_rank > 15:
            needs.append(TeamNeed.SHOOTING)
            priorities[TeamNeed.SHOOTING] = 5

        if team_stats.reb_rank > 20:
            needs.append(TeamNeed.REBOUNDING)
            priorities[TeamNeed.REBOUNDING] = 8
            alerts.append("Time sofre para controlar os rebotes.")

        if team_stats.ast_rank > 20:
            needs.append(TeamNeed.PLAYMAKING)
            priorities[TeamNeed.PLAYMAKING] = 9
            alerts.append("Ataque estagnado: pouca criação de jogadas.")

        if team_stats.def_rating_rank > 20:
            needs.append(TeamNeed.PERIMETER_DEFENSE)
            needs.append(TeamNeed.RIM_PROTECTION)
            priorities[TeamNeed.PERIMETER_DEFENSE] = 8
            priorities[TeamNeed.RIM_PROTECTION] = 8
            alerts.append("Defesa porosa: precisa de especialistas defensivos.")

        if team_stats.off_rating_rank > 20:
            needs.append(TeamNeed.SCORING)
            priorities[TeamNeed.SCORING] = 10
            alerts.append("Ataque ineficiente: precisa de pontuadores.")

        sorted_needs = sorted(needs, key=lambda n: priorities.get(n, 0), reverse=True)

        return TeamNeeds(
            team_id=team_stats.team_id,
            team_name=team_stats.team_name,
            needs=sorted_needs,
            needs_priority=priorities,
            style_alerts=alerts,
            team_stats=team_stats
        )
