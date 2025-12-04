from typing import Any, Dict, List, Optional
from dataclasses import dataclass

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
    id: int
    full_name: str
    position: str
    team_id: Optional[int] = None
    team_name: Optional[str] = None


class NBAApiClient:
    """Cliente para buscar dados da API oficial da NBA."""
    
    def __init__(self):
        self.current_season = "2024-25"

    def search_player_by_name(self, name: str) -> List[Dict[str, Any]]:
        all_players = players.get_players()
        return [p for p in all_players if name.lower() in p['full_name'].lower()]
    
    def get_player_info(self, player_id: int) -> Optional[PlayerInfo]:
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
            print(f"[NBAApiClient] Erro ao buscar jogador {player_id}: {e}")
            return None

    def get_player_advanced_stats(self, player_id: int) -> Optional[PlayerAdvancedStats]:
        try:
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=self.current_season,
                per_mode_detailed="PerGame"
            )
            df = stats.get_data_frames()[0]
            player_row = df[df['PLAYER_ID'] == player_id]
            
            if player_row.empty:
                stats = leaguedashplayerstats.LeagueDashPlayerStats(
                    season="2023-24",
                    per_mode_detailed="PerGame"
                )
                df = stats.get_data_frames()[0]
                player_row = df[df['PLAYER_ID'] == player_id]
                
                if player_row.empty:
                    return None

            row = player_row.iloc[0]
            
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
                reb=row['REB'],
                oreb=row['OREB'],
                blk=row['BLK'],
                stl=row['STL'],
                min=row['MIN'],
                position=""
            )
            
        except Exception as e:
            print(f"[NBAApiClient] Erro ao buscar stats {player_id}: {e}")
            return None

    def get_team_stats(self, team_id: int) -> Optional[TeamStats]:
        try:
            stats = leaguedashteamstats.LeagueDashTeamStats(
                season=self.current_season,
                per_mode_detailed="PerGame"
            )
            df = stats.get_data_frames()[0]
            
            team_row = df[df['TEAM_ID'] == team_id]
            if team_row.empty:
                return None

            df['FG3_PCT_RANK'] = df['FG3_PCT'].rank(ascending=False)
            df['REB_RANK'] = df['REB'].rank(ascending=False)
            df['AST_RANK'] = df['AST'].rank(ascending=False)
            df['PACE_RANK'] = df['FGA'].rank(ascending=False)
            
            row = df[df['TEAM_ID'] == team_id].iloc[0]

            return TeamStats(
                team_id=team_id,
                team_name=row['TEAM_NAME'],
                fg3_pct_rank=int(row['FG3_PCT_RANK']),
                reb_rank=int(row['REB_RANK']),
                ast_rank=int(row['AST_RANK']),
                pace_rank=int(row['PACE_RANK']),
                def_rating_rank=15,
                off_rating_rank=15,
                pace=0.0,
                fg3_pct=row['FG3_PCT'],
                ball_dominant_count=0
            )

        except Exception as e:
            print(f"[NBAApiClient] Erro ao buscar stats do time {team_id}: {e}")
            return None

    def get_all_teams(self) -> List[Dict[str, Any]]:
        return teams.get_teams()
    
    def get_team_roster(self, team_id: int) -> List[Dict[str, Any]]:
        try:
            roster = commonteamroster.CommonTeamRoster(
                team_id=team_id,
                season=self.current_season
            )
            df = roster.get_data_frames()[0]
            return df.to_dict('records')
        except Exception as e:
            print(f"[NBAApiClient] Erro ao buscar roster {team_id}: {e}")
            return []