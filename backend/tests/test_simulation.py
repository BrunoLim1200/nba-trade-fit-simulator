from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class SimulationResult(BaseModel):
    veredito: str
    minutagem_estimada: int
    explicacao: str

@router.get("/simulate-fit", response_model=SimulationResult)
async def simulate_fit(player_id: str, team_id: str):
    # TODO: Implement the logic to fetch player and team data,
    # analyze fit based on PER, and return the appropriate response.
    pass