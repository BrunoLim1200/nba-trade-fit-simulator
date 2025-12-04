from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.infrastructure.database.connection import Base


class PlayerModel(Base):
    """Model para cache de dados de jogadores"""
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    nba_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(100), index=True, nullable=False)
    position = Column(String(20))
    per = Column(Float)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento
    team = relationship("TeamModel", back_populates="players")


class TeamModel(Base):
    """Model para cache de dados de times"""
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    nba_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(100), index=True, nullable=False)
    city = Column(String(50))
    abbreviation = Column(String(5))
    conference = Column(String(10))
    division = Column(String(20))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento
    players = relationship("PlayerModel", back_populates="team")


class SimulationHistoryModel(Base):
    """Model para histórico de simulações"""
    __tablename__ = 'simulation_history'
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, nullable=False)
    team_id = Column(Integer, nullable=False)
    veredito = Column(String(50), nullable=False)
    minutagem_estimada = Column(Float)
    explicacao = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
