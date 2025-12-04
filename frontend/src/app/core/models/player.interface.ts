export interface Player {
  id: number;
  nba_id: number;
  name: string;
  position: string;
  per: number | null;
  team_name?: string;
}

export interface PlayerSearchResult {
  id: number;
  full_name: string;
  is_active: boolean;
}