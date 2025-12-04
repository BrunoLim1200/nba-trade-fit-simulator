from pydantic import BaseModel, Field
from typing import Optional, List


class PlayerBase(BaseModel):
    """Schema base para jogador"""
    name: str = Field(..., min_length=1, max_length=100)
    position: str = Field(..., description="Posição do jogador (G, F, C, G-F, etc)")


class PlayerCreate(PlayerBase):
    """Schema para criar jogador"""
    nba_id: int
    per: Optional[float] = None
    team_id: Optional[int] = None


class PlayerResponse(PlayerBase):
    """Schema de resposta com dados do jogador"""
    id: int
    nba_id: int
    per: Optional[float] = None
    team_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class PlayerSearchResponse(BaseModel):
    """Schema para resultado de busca de jogadores"""
    id: int
    full_name: str
    is_active: bool
    
    class Config:
        from_attributes = True


class PlayerWithStats(PlayerResponse):
    """Schema com estatísticas detalhadas"""
    minutes_per_game: Optional[float] = None
    points_per_game: Optional[float] = None
    assists_per_game: Optional[float] = None
    rebounds_per_game: Optional[float] = None