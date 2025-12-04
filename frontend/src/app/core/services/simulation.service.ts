import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { SimulationResult } from '../models/simulation-result.interface';
import { PlayerSearchResult } from '../models/player.interface';
import { Team } from '../models/team.interface';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SimulationService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = environment.apiUrl;

  simulateFit(playerId: number, teamId: number): Observable<SimulationResult> {
    const params = new HttpParams()
      .set('player_id', playerId.toString())
      .set('team_id', teamId.toString());
    
    return this.http.get<SimulationResult>(`${this.apiUrl}/simulate-fit`, { params });
  }

  searchPlayers(name: string): Observable<PlayerSearchResult[]> {
    const params = new HttpParams().set('name', name);
    return this.http.get<PlayerSearchResult[]>(`${this.apiUrl}/players/search`, { params });
  }

  getAllTeams(): Observable<Team[]> {
    return this.http.get<Team[]>(`${this.apiUrl}/teams`);
  }
}