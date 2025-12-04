export type FitLabel = 
  | 'Franchise Savior' 
  | 'Perfect Fit' 
  | 'Starter' 
  | '6th Man' 
  | 'Rotation Player' 
  | 'Situational' 
  | 'Bad Fit' 
  | 'Redundant';

export interface PlayerAnalysis {
  player_id: number;
  player_name: string;
  position: string;
  archetypes: string[];
  is_ball_dominant: boolean;
  is_elite_shooter: boolean;
  is_defensive_anchor: boolean;
  per: number | null;
  estimated_minutes: number;
}

export interface TeamNeeds {
  team_id: number;
  team_name: string;
  needs: string[];
  style_alerts: string[];
}

export interface RosterFrictionResult {
  total_penalty: number;
  conflicts: RosterConflict[];
  suggested_role: string;
  blocking_players: string[];
}

export interface RosterConflict {
  conflict_type: string;
  severity: string;
  penalty_points: number;
  description: string;
}

export interface SimulationResult {
  player_id: number;
  player_name: string;
  team_id: number;
  team_name: string;
  fit_score: number;
  fit_label: FitLabel;
  estimated_minutes: number;
  projected_role: string;
  player_archetypes: string[];
  team_needs_addressed: string[];
  reasons: string[];
  warnings: string[];
  breakdown: Record<string, number>;
  player_analysis?: PlayerAnalysis;
  team_needs?: TeamNeeds;
  friction_result?: RosterFrictionResult;
}