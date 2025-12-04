export interface PlayerSearchComponent {
  playerName: string;
  playerId: string;
  searchPlayer(): void;
  onPlayerSelected(playerId: string): void;
}