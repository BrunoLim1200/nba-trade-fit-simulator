from fastapi import APIRouter, HTTPException, Query
from typing import List

from src.schemas.simulation import SimulationResponse, SimulationRequest
from src.schemas.player import PlayerSearchResponse
from src.schemas.team import TeamSearchResponse
from src.domain.services.fit_simulator import FitSimulator
from src.infrastructure.external.nba_api_client import NBAApiClient

router = APIRouter()
nba_client = NBAApiClient()
fit_simulator = FitSimulator(nba_client)


@router.get("/simulate-fit", response_model=SimulationResponse)
async def simulate_fit(
    player_id: int = Query(..., description="ID do jogador na NBA API"),
    team_id: int = Query(..., description="ID do time alvo")
):
    try:
        result = await fit_simulator.simulate_fit(player_id, team_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar simulação: {str(e)}"
        )


@router.get("/players/search", response_model=List[PlayerSearchResponse])
async def search_players(
    name: str = Query(..., min_length=2, description="Nome do jogador para busca")
):
    try:
        players = nba_client.search_player_by_name(name)
        return [
            PlayerSearchResponse(
                id=p['id'],
                full_name=p['full_name'],
                is_active=p.get('is_active', False)
            )
            for p in players[:10]  # Limita a 10 resultados
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar jogadores: {str(e)}"
        )


@router.get("/teams", response_model=List[TeamSearchResponse])
async def get_all_teams():
    try:
        teams = nba_client.get_all_teams()
        return [
            TeamSearchResponse(
                id=t['id'],
                full_name=t['full_name'],
                abbreviation=t['abbreviation'],
                city=t['city']
            )
            for t in teams
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar times: {str(e)}"
        )