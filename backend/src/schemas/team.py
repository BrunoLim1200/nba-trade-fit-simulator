from pydantic import BaseModel, Field
from typing import Optional, List


class TeamBase(BaseModel):
    """Schema base para time"""
    name: str = Field(..., min_length=1, max_length=100)
    city: str = Field(..., min_length=1, max_length=50)


class TeamCreate(TeamBase):
    """Schema para criar time"""
    nba_id: int
    abbreviation: str = Field(..., max_length=5)
    conference: str
    division: str


class TeamResponse(TeamBase):
    """Schema de resposta com dados do time"""
    id: int
    nba_id: int
    abbreviation: str
    conference: str
    division: str
    
    class Config:
        from_attributes = True


class TeamWithRoster(TeamResponse):
    """Schema com elenco do time"""
    roster: List[dict] = Field(default_factory=list)


class TeamSearchResponse(BaseModel):
    """Schema para busca de times"""
    id: int
    full_name: str
    abbreviation: str
    city: str
    
    class Config:
        from_attributes = True