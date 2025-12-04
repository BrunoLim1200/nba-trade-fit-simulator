export type FitVerdict = 'Titular' | '6º Homem' | 'Rotação' | 'Banco/Garbage Time';

export interface PositionComparison {
  player_position: string;
  current_starter_per: number | null;
  current_backup_per: number | null;
}

export interface SimulationResult {
  veredito: FitVerdict;
  minutagem_estimada: number;
  explicacao: string;
  player_name?: string;
  player_per?: number;
  team_name?: string;
  position_comparison?: PositionComparison;
}