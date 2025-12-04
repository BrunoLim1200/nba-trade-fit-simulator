from typing import List
from src.schemas.analysis import PlayerAnalysis, TeamStats, RosterFrictionResult, RosterConflict

class RosterFrictionService:
    """
    Serviço responsável por identificar conflitos de estilo e redundâncias
    entre o jogador novo e o elenco atual.
    """

    def analyze_friction(self, player_analysis: PlayerAnalysis, team_stats: TeamStats) -> RosterFrictionResult:
        """
        Calcula a fricção potencial de adicionar este jogador ao time.
        """
        conflicts = []
        total_penalty = 0
        blocking_players = []

        # 1. Conflito de "Ball Dominant"
        # Se o jogador precisa da bola E o time já tem muitos jogadores assim
        if player_analysis.is_ball_dominant:
            if team_stats.ball_dominant_count >= 2:
                conflict = RosterConflict(
                    conflict_type="Too Many Cooks",
                    severity="high",
                    penalty_points=30,
                    description="O time já possui múltiplos jogadores que dominam a bola. Adicionar mais um pode gerar problemas de química."
                )
                conflicts.append(conflict)
                total_penalty += 30
                blocking_players.append("Existing Stars")
            elif team_stats.ball_dominant_count == 1:
                conflict = RosterConflict(
                    conflict_type="Usage Clash",
                    severity="medium",
                    penalty_points=15,
                    description="Haverá disputa por posse de bola com a estrela atual."
                )
                conflicts.append(conflict)
                total_penalty += 15

        # 2. Conflito de Pace (Ritmo)
        # Se o jogador é lento (ex: pivô clássico) e o time corre muito
        # Simplificação: assumindo que pivôs pesados têm pouca mobilidade
        is_heavy_center = "C" in player_analysis.position and not player_analysis.is_elite_shooter
        team_runs_fast = team_stats.pace_rank <= 5  # Top 5 em Pace (mais rápido)
        
        if is_heavy_center and team_runs_fast:
            conflict = RosterConflict(
                conflict_type="Pace Mismatch",
                severity="medium",
                penalty_points=20,
                description="O estilo de jogo do time é muito rápido para este jogador."
            )
            conflicts.append(conflict)
            total_penalty += 20

        # 3. Redundância Posicional (Simplificado)
        # Em uma implementação real, checaríamos o depth chart do time
        # Aqui vamos assumir que não temos o depth chart completo ainda, 
        # então focamos nos atributos principais.

        # Determinar papel sugerido baseado na penalidade
        suggested_role = "Starter"
        if total_penalty > 40:
            suggested_role = "Bad Fit"
        elif total_penalty > 20:
            suggested_role = "Sixth Man / Rotation"
        elif total_penalty > 0:
            suggested_role = "Starter (with adjustments)"
        else:
            suggested_role = "Perfect Fit"

        return RosterFrictionResult(
            total_penalty=total_penalty,
            conflicts=conflicts,
            suggested_role=suggested_role,
            blocking_players=blocking_players
        )
