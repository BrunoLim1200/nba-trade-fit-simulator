from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

# ============================================
# ENUMS - Arquétipos e Necessidades
# ============================================

class PlayerArchetype(str, Enum):
    """Arquétipos possíveis para um jogador"""
    SNIPER = "Sniper"
    BALL_DOMINANT = "Ball Dominant"
    RIM_PROTECTOR = "Rim Protector"
    PLAYMAKER = "Playmaker"
    HUSTLE = "Hustle"
    THREE_AND_D = "3&D"
    STRETCH_BIG = "Stretch Big"
    TWO_WAY = "Two-Way Player"


class TeamNeed(str, Enum):
    """Necessidades que um time pode ter"""
    SHOOTING = "Shooting"
    REBOUNDING = "Rebounding"
    PLAYMAKING = "Playmaking"
    RIM_PROTECTION = "Rim Protection"
    PERIMETER_DEFENSE = "Perimeter Defense"
    SCORING = "Scoring"
    PACE_FIT = "Pace Fit"


class FitLabel(str, Enum):
    """Labels finais de encaixe"""
    FRANCHISE_SAVIOR = "Franchise Savior"
    PERFECT_FIT = "Perfect Fit"
    STARTER = "Starter"
    SIXTH_MAN = "6th Man"
    ROTATION = "Rotation Player"
    SITUATIONAL = "Situational"
    BAD_FIT = "Bad Fit"
    REDUNDANT = "Redundant"


# ============================================
# SCHEMAS - Estatísticas de Jogador
# ============================================

class PlayerAdvancedStats(BaseModel):
    """Estatísticas avançadas do jogador para análise de arquétipo"""
    player_id: int
    player_name: str
    
    # Shooting
    pts: float = Field(default=0.0, description="Pontos por jogo")
    fga: float = Field(default=0.0, description="Arremessos tentados")
    fg_pct: float = Field(default=0.0, description="% de arremessos")
    fg3a: float = Field(default=0.0, description="Arremessos de 3 tentados")
    fg3_pct: float = Field(default=0.0, description="% de 3 pontos")
    
    # Playmaking
    ast: float = Field(default=0.0, description="Assistências por jogo")
    tov: float = Field(default=0.0, description="Turnovers por jogo")
    ast_pct: Optional[float] = Field(default=None, description="% de assistências")
    usg_pct: Optional[float] = Field(default=None, description="Usage Rate %")
    
    # Rebounding
    reb: float = Field(default=0.0, description="Rebotes por jogo")
    oreb: float = Field(default=0.0, description="Rebotes ofensivos")
    oreb_pct: Optional[float] = Field(default=None, description="% rebotes ofensivos")
    
    # Defense
    blk: float = Field(default=0.0, description="Tocos por jogo")
    stl: float = Field(default=0.0, description="Roubos por jogo")
    dfg_pct: Optional[float] = Field(default=None, description="DFG% no aro")
    deflections: Optional[float] = Field(default=None, description="Deflexões por jogo")
    
    # Efficiency
    per: Optional[float] = Field(default=None, description="Player Efficiency Rating")
    net_rating: Optional[float] = Field(default=None, description="Net Rating")
    min: float = Field(default=0.0, description="Minutos por jogo")
    
    # Position
    position: str = Field(default="", description="Posição do jogador")

    @property
    def ast_to_ratio(self) -> float:
        """Calcula AST/TO Ratio"""
        if self.tov and self.tov > 0:
            return self.ast / self.tov
        return self.ast if self.ast > 0 else 0.0


class PlayerAnalysis(BaseModel):
    """Resultado da análise completa de um jogador"""
    player_id: int
    player_name: str
    position: str
    
    # Stats resumidas
    stats: PlayerAdvancedStats
    
    # Arquétipos detectados
    archetypes: List[PlayerArchetype] = Field(default_factory=list)
    archetype_scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Score de confiança para cada arquétipo (0-100)"
    )
    
    # Flags especiais
    is_ball_dominant: bool = False
    is_elite_shooter: bool = False
    is_defensive_anchor: bool = False
    
    # PER e eficiência
    per: Optional[float] = None
    estimated_minutes: float = 0.0


# ============================================
# SCHEMAS - Análise de Time
# ============================================

class TeamStats(BaseModel):
    """Estatísticas do time para análise de lacunas"""
    team_id: int
    team_name: str
    
    # Rankings (1-30, onde 1 é melhor)
    fg3_pct_rank: int = Field(default=15, ge=1, le=30)
    reb_rank: int = Field(default=15, ge=1, le=30)
    ast_rank: int = Field(default=15, ge=1, le=30)
    pace_rank: int = Field(default=15, ge=1, le=30)
    def_rating_rank: int = Field(default=15, ge=1, le=30)
    off_rating_rank: int = Field(default=15, ge=1, le=30)
    
    # Valores absolutos
    pace: float = Field(default=100.0, description="Pace do time")
    fg3_pct: float = Field(default=0.35, description="% de 3 pontos")
    
    # Contagem de arquétipos no elenco
    ball_dominant_count: int = Field(default=0, description="Qtd de Ball Dominant no elenco")


class TeamNeeds(BaseModel):
    """Necessidades identificadas do time"""
    team_id: int
    team_name: str
    
    # Lista de necessidades priorizadas
    needs: List[TeamNeed] = Field(default_factory=list)
    needs_priority: Dict[str, int] = Field(
        default_factory=dict,
        description="Prioridade de cada necessidade (1-10)"
    )
    
    # Alertas de estilo
    style_alerts: List[str] = Field(default_factory=list)
    
    # Estatísticas do time
    team_stats: Optional[TeamStats] = None


# ============================================
# SCHEMAS - Conflitos e Fricção
# ============================================

class RosterConflict(BaseModel):
    """Representa um conflito/redundância no elenco"""
    conflict_type: str = Field(..., description="Tipo de conflito")
    severity: str = Field(default="medium", description="low/medium/high")
    affected_players: List[str] = Field(default_factory=list)
    penalty_points: int = Field(default=0, ge=0, le=50)
    description: str = Field(default="")


class RosterFrictionResult(BaseModel):
    """Resultado da análise de fricção no elenco"""
    total_penalty: int = Field(default=0, ge=0, le=100)
    conflicts: List[RosterConflict] = Field(default_factory=list)
    suggested_role: str = Field(default="Rotation")
    blocking_players: List[str] = Field(
        default_factory=list,
        description="Jogadores que bloqueiam o titular"
    )


# ============================================
# SCHEMAS - Resultado Final do Trade
# ============================================

class TradeResult(BaseModel):
    """Resultado final da simulação de trade/fit"""
    # Identificação
    player_id: int
    player_name: str
    team_id: int
    team_name: str
    
    # Score e Label principal
    fit_score: int = Field(..., ge=0, le=100, description="Score de fit (0-100)")
    fit_label: FitLabel = Field(..., description="Label final do encaixe")
    
    # Minutagem estimada
    estimated_minutes: float = Field(default=0.0, ge=0, le=48)
    projected_role: str = Field(default="Rotation")
    
    # Detalhes da análise
    player_archetypes: List[str] = Field(default_factory=list)
    team_needs_addressed: List[str] = Field(default_factory=list)
    
    # Explicações (para o frontend)
    reasons: List[str] = Field(
        default_factory=list,
        description="Lista de motivos explicando o veredito"
    )
    warnings: List[str] = Field(
        default_factory=list,
        description="Alertas sobre potenciais problemas"
    )
    
    # Dados para gráficos
    breakdown: Dict[str, int] = Field(
        default_factory=dict,
        description="Breakdown do score por categoria"
    )
    
    # Análises detalhadas (opcional)
    player_analysis: Optional[PlayerAnalysis] = None
    team_needs: Optional[TeamNeeds] = None
    friction_result: Optional[RosterFrictionResult] = None
