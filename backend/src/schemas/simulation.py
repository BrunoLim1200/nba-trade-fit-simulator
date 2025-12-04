from pydantic import BaseModel, Field
from typing import Optional
from src.schemas.analysis import TradeResult, FitLabel

# Manter FitVerdict para compatibilidade ou migrar para FitLabel
# Vamos usar FitLabel como o novo padrão

class SimulationRequest(BaseModel):
    """Request para simulação de encaixe"""
    player_id: int = Field(..., description="ID do jogador na NBA API")
    team_id: int = Field(..., description="ID do time alvo")

# SimulationResponse agora é um alias ou extensão de TradeResult
class SimulationResponse(TradeResult):
    """Response com resultado da simulação de encaixe (Estendido)"""
    pass
