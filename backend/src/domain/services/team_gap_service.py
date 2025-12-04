from typing import List, Dict
from src.schemas.analysis import TeamStats, TeamNeeds, TeamNeed

class TeamGapService:
    """
    Serviço responsável por analisar as estatísticas de um time
    e identificar suas maiores necessidades (Gaps).
    """

    def analyze_team_needs(self, team_stats: TeamStats) -> TeamNeeds:
        """
        Analisa as estatísticas do time e retorna uma lista priorizada de necessidades.
        """
        needs = []
        priorities = {}
        alerts = []

        # 1. Shooting Gap
        # Se o time é bottom 10 em 3P% (Rank > 20)
        if team_stats.fg3_pct_rank > 20:
            needs.append(TeamNeed.SHOOTING)
            priorities[TeamNeed.SHOOTING] = 10  # Alta prioridade
            alerts.append("Time está entre os piores em aproveitamento de 3 pontos.")
        elif team_stats.fg3_pct_rank > 15:
            needs.append(TeamNeed.SHOOTING)
            priorities[TeamNeed.SHOOTING] = 5

        # 2. Rebounding Gap
        # Se o time é bottom 10 em Rebotes
        if team_stats.reb_rank > 20:
            needs.append(TeamNeed.REBOUNDING)
            priorities[TeamNeed.REBOUNDING] = 8
            alerts.append("Time sofre para controlar os rebotes.")

        # 3. Playmaking Gap
        # Se o time é bottom 10 em Assistências
        if team_stats.ast_rank > 20:
            needs.append(TeamNeed.PLAYMAKING)
            priorities[TeamNeed.PLAYMAKING] = 9
            alerts.append("Ataque estagnado: pouca criação de jogadas.")

        # 4. Defense Gap
        # Se Def Rating Rank > 20
        if team_stats.def_rating_rank > 20:
            needs.append(TeamNeed.PERIMETER_DEFENSE)
            needs.append(TeamNeed.RIM_PROTECTION)
            priorities[TeamNeed.PERIMETER_DEFENSE] = 8
            priorities[TeamNeed.RIM_PROTECTION] = 8
            alerts.append("Defesa porosa: precisa de especialistas defensivos.")

        # 5. Scoring Gap
        # Se Off Rating Rank > 20
        if team_stats.off_rating_rank > 20:
            needs.append(TeamNeed.SCORING)
            priorities[TeamNeed.SCORING] = 10
            alerts.append("Ataque ineficiente: precisa de pontuadores.")

        # Ordenar necessidades por prioridade
        sorted_needs = sorted(needs, key=lambda n: priorities.get(n, 0), reverse=True)

        return TeamNeeds(
            team_id=team_stats.team_id,
            team_name=team_stats.team_name,
            needs=sorted_needs,
            needs_priority=priorities,
            style_alerts=alerts,
            team_stats=team_stats
        )
