from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import pandas as pd

# NBA API imports
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import (
    commonplayerinfo,
    leaguedashplayerstats,
    leaguedashteamstats,
    commonteamroster
)
from src.schemas.analysis import PlayerAdvancedStats, TeamStats

@dataclass
class PlayerInfo:
    """Dados básicos do jogador"""
    id: int
    full_name: str
    position: str
    team_id: Optional[int] = None
    team_name: Optional[str] = None


class NBAApiClient:
    """Cliente para buscar dados da API oficial da NBA"""
    
    def __init__(self):
        self.current_season = "2024-25"

    def search_player_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Busca jogadores pelo nome"""
        all_players = players.get_players()
        matched = [p for p in all_players if name.lower() in p['full_name'].lower()]
        return matched
    
    def get_player_info(self, player_id: int) -> Optional[PlayerInfo]:
        """Retorna informações básicas do jogador"""
        try:
            info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
            data = info.get_normalized_dict()
            player_data = data['CommonPlayerInfo'][0]
            
            return PlayerInfo(
                id=player_id,
                full_name=player_data['DISPLAY_FIRST_LAST'],
                position=player_data['POSITION'],
                team_id=player_data.get('TEAM_ID'),
                team_name=player_data.get('TEAM_NAME')
            )
        except Exception as e:
            print(f"Erro ao buscar jogador {player_id}: {e}")
            return None

    def get_player_advanced_stats(self, player_id: int) -> Optional[PlayerAdvancedStats]:
        """
        Busca estatísticas detalhadas do jogador para análise de arquétipo.
        Usa leaguedashplayerstats para pegar médias da temporada.
        """
        try:
            # Busca stats de TODOS os jogadores e filtra (mais eficiente que buscar 1 a 1 se tiver cache, 
            # mas aqui vamos buscar direto filtrando se possível, ou buscar tudo e filtrar no pandas)
            # A API do leaguedashplayerstats não filtra por ID facilmente, retorna a liga toda.
            # Para performance em prod, isso deveria ser cacheado.
            
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=self.current_season,
                per_mode_detailed="PerGame"
            )
            df = stats.get_data_frames()[0]
            
            # Filtrar pelo ID
            player_row = df[df['PLAYER_ID'] == player_id]
            
            if player_row.empty:
                # Tentar temporada anterior se não tiver dados na atual
                stats = leaguedashplayerstats.LeagueDashPlayerStats(
                    season="2023-24",
                    per_mode_detailed="PerGame"
                )
                df = stats.get_data_frames()[0]
                player_row = df[df['PLAYER_ID'] == player_id]
                
                if player_row.empty:
                    return None

            row = player_row.iloc[0]
            
            # Mapear para o Schema
            return PlayerAdvancedStats(
                player_id=player_id,
                player_name=row['PLAYER_NAME'],
                pts=row['PTS'],
                fga=row['FGA'],
                fg_pct=row['FG_PCT'],
                fg3a=row['FG3A'],
                fg3_pct=row['FG3_PCT'],
                ast=row['AST'],
                tov=row['TOV'],
                # ast_pct e usg_pct não vêm no endpoint padrão PerGame, precisaria do Advanced
                # Vamos estimar ou deixar None por enquanto para simplificar a chamada
                reb=row['REB'],
                oreb=row['OREB'],
                blk=row['BLK'],
                stl=row['STL'],
                min=row['MIN'],
                # Posição não vem nas stats, pegamos do info se necessário, ou passamos vazio
                position="" 
            )
            
        except Exception as e:
            print(f"Erro ao buscar stats avançadas {player_id}: {e}")
            return None

    def get_team_stats(self, team_id: int) -> Optional[TeamStats]:
        """
        Busca estatísticas e rankings do time.
        """
        try:
            # Busca stats de todos os times
            stats = leaguedashteamstats.LeagueDashTeamStats(
                season=self.current_season,
                per_mode_detailed="PerGame"
            )
            df = stats.get_data_frames()[0]
            
            team_row = df[df['TEAM_ID'] == team_id]
            if team_row.empty:
                return None
                
            row = team_row.iloc[0]
            
            # Calcular Rankings (baseado no DataFrame inteiro)
            # Rank 1 é o maior valor
            df['FG3_PCT_RANK'] = df['FG3_PCT'].rank(ascending=False)
            df['REB_RANK'] = df['REB'].rank(ascending=False)
            df['AST_RANK'] = df['AST'].rank(ascending=False)
            # Pace não vem no PerGame padrão, precisaria do Advanced. Vamos usar FGA como proxy de Pace por enquanto
            df['PACE_RANK'] = df['FGA'].rank(ascending=False) 
            
            # Recalcular row com rankings
            row = df[df['TEAM_ID'] == team_id].iloc[0]

            return TeamStats(
                team_id=team_id,
                team_name=row['TEAM_NAME'],
                fg3_pct_rank=int(row['FG3_PCT_RANK']),
                reb_rank=int(row['REB_RANK']),
                ast_rank=int(row['AST_RANK']),
                pace_rank=int(row['PACE_RANK']),
                def_rating_rank=15, # Placeholder sem endpoint Advanced
                off_rating_rank=15, # Placeholder
                pace=0.0, # Placeholder
                fg3_pct=row['FG3_PCT'],
                ball_dominant_count=0 # Será preenchido externamente analisando o roster
            )

        except Exception as e:
            print(f"Erro ao buscar stats do time {team_id}: {e}")
            return None

    def get_all_teams(self) -> List[Dict[str, Any]]:
        """Retorna lista de todos os times da NBA"""
        return teams.get_teams()
    
    def get_team_roster(self, team_id: int) -> List[Dict[str, Any]]:
        """Retorna o elenco atual do time"""
        try:
            roster = commonteamroster.CommonTeamRoster(
                team_id=team_id,
                season=self.current_season
            )
            df = roster.get_data_frames()[0]
            return df.to_dict('records')
        except Exception as e:
            print(f"Erro ao buscar roster do time {team_id}: {e}")
            return []