export interface TeamSelectorComponent {
  teams: any[]; // Replace 'any' with a more specific type if available
  selectedTeam: any; // Replace 'any' with a more specific type if available

  ngOnInit(): void;
  onTeamSelect(team: any): void; // Replace 'any' with a more specific type if available
}