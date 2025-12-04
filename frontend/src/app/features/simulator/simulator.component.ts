import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { MatAutocompleteModule } from '@angular/material/autocomplete';

import { SimulationService } from '@core/services/simulation.service';
import { SimulationResult } from '@core/models/simulation-result.interface';
import { PlayerSearchResult } from '@core/models/player.interface';
import { Team } from '@core/models/team.interface';

@Component({
  selector: 'app-simulator',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    MatSelectModule,
    MatProgressSpinnerModule,
    MatIconModule,
    MatAutocompleteModule
  ],
  templateUrl: './simulator.component.html',
  styleUrl: './simulator.component.scss'
})
export class SimulatorComponent {
  private readonly simulationService = inject(SimulationService);

  playerSearchQuery = '';
  selectedPlayer = signal<PlayerSearchResult | null>(null);
  selectedTeam = signal<Team | null>(null);
  players = signal<PlayerSearchResult[]>([]);
  teams = signal<Team[]>([]);
  simulationResult = signal<SimulationResult | null>(null);
  loading = signal(false);
  error = signal<string | null>(null);

  constructor() {
    this.loadTeams();
  }

  loadTeams(): void {
    this.simulationService.getAllTeams().subscribe({
      next: (teams) => this.teams.set(teams),
      error: (err) => console.error('Erro ao carregar times:', err)
    });
  }

  searchPlayers(): void {
    if (this.playerSearchQuery.length < 2) {
      this.players.set([]);
      return;
    }

    this.simulationService.searchPlayers(this.playerSearchQuery).subscribe({
      next: (players) => this.players.set(players),
      error: (err) => console.error('Erro ao buscar jogadores:', err)
    });
  }

  selectPlayer(player: PlayerSearchResult): void {
    this.selectedPlayer.set(player);
    this.playerSearchQuery = player.full_name;
    this.players.set([]);
  }

  selectTeam(team: Team): void {
    this.selectedTeam.set(team);
  }

  simulateFit(): void {
    const player = this.selectedPlayer();
    const team = this.selectedTeam();

    if (!player || !team) {
      this.error.set('Selecione um jogador e um time.');
      return;
    }

    this.loading.set(true);
    this.error.set(null);
    this.simulationResult.set(null);

    this.simulationService.simulateFit(player.id, team.id).subscribe({
      next: (result) => {
        this.simulationResult.set(result);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set('Erro ao simular encaixe. Tente novamente.');
        this.loading.set(false);
        console.error(err);
      }
    });
  }

  getVerdictColor(label: string): string {
    const colors: Record<string, string> = {
      'Franchise Savior': '#FFD700',
      'Perfect Fit': '#4CAF50',
      'Starter': '#8BC34A',
      '6th Man': '#2196F3',
      'Rotation Player': '#FF9800',
      'Situational': '#FF5722',
      'Bad Fit': '#f44336',
      'Redundant': '#9E9E9E'
    };
    return colors[label] || '#757575';
  }
}