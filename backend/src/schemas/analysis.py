from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class PlayerArchetype(str, Enum):
    SNIPER = "Sniper"
    BALL_DOMINANT = "Ball Dominant"
    RIM_PROTECTOR = "Rim Protector"
    PLAYMAKER = "Playmaker"
    HUSTLE = "Hustle"
    THREE_AND_D = "3&D"
    STRETCH_BIG = "Stretch Big"
    TWO_WAY = "Two-Way Player"


class TeamNeed(str, Enum):
    SHOOTING = "Shooting"
    REBOUNDING = "Rebounding"
    PLAYMAKING = "Playmaking"
    RIM_PROTECTION = "Rim Protection"
    PERIMETER_DEFENSE = "Perimeter Defense"
    SCORING = "Scoring"
    PACE_FIT = "Pace Fit"


class FitLabel(str, Enum):
    FRANCHISE_SAVIOR = "Franchise Savior"
    PERFECT_FIT = "Perfect Fit"
    STARTER = "Starter"
    SIXTH_MAN = "6th Man"
    ROTATION = "Rotation Player"
    SITUATIONAL = "Situational"
    BAD_FIT = "Bad Fit"
    REDUNDANT = "Redundant"


class PlayerAdvancedStats(BaseModel):
    player_id: int
    player_name: str
    pts: float = 0.0
    fga: float = 0.0
    fg_pct: float = 0.0
    fg3a: float = 0.0
    fg3_pct: float = 0.0
    ast: float = 0.0
    tov: float = 0.0
    ast_pct: Optional[float] = None
    usg_pct: Optional[float] = None
    reb: float = 0.0
    oreb: float = 0.0
    oreb_pct: Optional[float] = None
    blk: float = 0.0
    stl: float = 0.0
    dfg_pct: Optional[float] = None
    deflections: Optional[float] = None
    per: Optional[float] = None
    net_rating: Optional[float] = None
    min: float = 0.0
    position: str = ""

    @property
    def ast_to_ratio(self) -> float:
        if self.tov and self.tov > 0:
            return self.ast / self.tov
        return self.ast if self.ast > 0 else 0.0


class PlayerAnalysis(BaseModel):
    player_id: int
    player_name: str
    position: str
    stats: PlayerAdvancedStats
    archetypes: List[PlayerArchetype] = Field(default_factory=list)
    archetype_scores: Dict[str, float] = Field(default_factory=dict)
    is_ball_dominant: bool = False
    is_elite_shooter: bool = False
    is_defensive_anchor: bool = False
    per: Optional[float] = None
    estimated_minutes: float = 0.0


class TeamStats(BaseModel):
    team_id: int
    team_name: str
    fg3_pct_rank: int = Field(default=15, ge=1, le=30)
    reb_rank: int = Field(default=15, ge=1, le=30)
    ast_rank: int = Field(default=15, ge=1, le=30)
    pace_rank: int = Field(default=15, ge=1, le=30)
    def_rating_rank: int = Field(default=15, ge=1, le=30)
    off_rating_rank: int = Field(default=15, ge=1, le=30)
    pace: float = 100.0
    fg3_pct: float = 0.35
    ball_dominant_count: int = 0


class TeamNeeds(BaseModel):
    team_id: int
    team_name: str
    needs: List[TeamNeed] = Field(default_factory=list)
    needs_priority: Dict[str, int] = Field(default_factory=dict)
    style_alerts: List[str] = Field(default_factory=list)
    team_stats: Optional[TeamStats] = None


class RosterConflict(BaseModel):
    conflict_type: str
    severity: str = "medium"
    affected_players: List[str] = Field(default_factory=list)
    penalty_points: int = Field(default=0, ge=0, le=50)
    description: str = ""


class RosterFrictionResult(BaseModel):
    total_penalty: int = Field(default=0, ge=0, le=100)
    conflicts: List[RosterConflict] = Field(default_factory=list)
    suggested_role: str = "Rotation"
    blocking_players: List[str] = Field(default_factory=list)


class TradeResult(BaseModel):
    player_id: int
    player_name: str
    team_id: int
    team_name: str
    fit_score: int = Field(..., ge=0, le=100)
    fit_label: FitLabel
    estimated_minutes: float = Field(default=0.0, ge=0, le=48)
    projected_role: str = "Rotation"
    player_archetypes: List[str] = Field(default_factory=list)
    team_needs_addressed: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    breakdown: Dict[str, int] = Field(default_factory=dict)
    player_analysis: Optional[PlayerAnalysis] = None
    team_needs: Optional[TeamNeeds] = None
    friction_result: Optional[RosterFrictionResult] = None
