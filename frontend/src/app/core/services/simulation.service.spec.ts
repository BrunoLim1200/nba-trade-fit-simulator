import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { SimulationService } from './simulation.service';
import { SimulationResult } from '../models/simulation-result.interface';
import { environment } from '../../../environments/environment';

describe('SimulationService', () => {
  let service: SimulationService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SimulationService]
    });
    service = TestBed.inject(SimulationService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  describe('simulateFit', () => {
    it('should call simulate-fit endpoint with correct params', () => {
      const playerId = 123;
      const teamId = 456;

      service.simulateFit(playerId, teamId).subscribe();

      const req = httpMock.expectOne(
        r => r.url.includes('simulate-fit') && 
             r.params.get('player_id') === '123' &&
             r.params.get('team_id') === '456'
      );
      expect(req.request.method).toBe('GET');
    });

    it('should return simulation result with fit score', () => {
      const mockResult: SimulationResult = {
        player_id: 1,
        player_name: 'LeBron James',
        team_id: 100,
        team_name: 'Lakers',
        fit_score: 85,
        fit_label: 'Starter',
        estimated_minutes: 32,
        projected_role: 'Starter',
        player_archetypes: ['Ball Dominant', 'Playmaker'],
        team_needs_addressed: ['Playmaking'],
        reasons: ['Atende necessidades do time'],
        warnings: [],
        breakdown: { archetype_match: 80 }
      };

      service.simulateFit(1, 100).subscribe(result => {
        expect(result.fit_score).toBe(85);
        expect(result.fit_label).toBe('Starter');
        expect(result.player_archetypes).toContain('Ball Dominant');
      });

      const req = httpMock.expectOne(r => r.url.includes('simulate-fit'));
      req.flush(mockResult);
    });

    it('should handle perfect fit response', () => {
      const mockResult: SimulationResult = {
        player_id: 1,
        player_name: 'Klay Thompson',
        team_id: 100,
        team_name: 'Test Team',
        fit_score: 95,
        fit_label: 'Perfect Fit',
        estimated_minutes: 34,
        projected_role: 'Perfect Fit',
        player_archetypes: ['Sniper', '3&D'],
        team_needs_addressed: ['Shooting'],
        reasons: ['Atende necessidade crítica de arremesso'],
        warnings: [],
        breakdown: {}
      };

      service.simulateFit(1, 100).subscribe(result => {
        expect(result.fit_score).toBeGreaterThanOrEqual(90);
        expect(result.fit_label).toBe('Perfect Fit');
      });

      const req = httpMock.expectOne(r => r.url.includes('simulate-fit'));
      req.flush(mockResult);
    });

    it('should handle bad fit response with warnings', () => {
      const mockResult: SimulationResult = {
        player_id: 1,
        player_name: 'Usage Heavy Star',
        team_id: 100,
        team_name: 'Star Packed Team',
        fit_score: 30,
        fit_label: 'Bad Fit',
        estimated_minutes: 15,
        projected_role: 'Bad Fit',
        player_archetypes: ['Ball Dominant'],
        team_needs_addressed: [],
        reasons: ['Penalidade de fricção: -30 pontos'],
        warnings: ['Time já possui múltiplos jogadores que dominam a bola'],
        breakdown: { friction_penalty: 30 }
      };

      service.simulateFit(1, 100).subscribe(result => {
        expect(result.fit_score).toBeLessThan(40);
        expect(result.warnings.length).toBeGreaterThan(0);
      });

      const req = httpMock.expectOne(r => r.url.includes('simulate-fit'));
      req.flush(mockResult);
    });
  });

  describe('searchPlayers', () => {
    it('should call search endpoint with name param', () => {
      service.searchPlayers('lebron').subscribe();

      const req = httpMock.expectOne(
        r => r.url.includes('players/search') && 
             r.params.get('name') === 'lebron'
      );
      expect(req.request.method).toBe('GET');
    });

    it('should return array of player results', () => {
      const mockPlayers = [
        { id: 1, full_name: 'LeBron James', is_active: true },
        { id: 2, full_name: 'LeBron James Jr.', is_active: false }
      ];

      service.searchPlayers('lebron').subscribe(players => {
        expect(players.length).toBe(2);
        expect(players[0].full_name).toContain('LeBron');
      });

      const req = httpMock.expectOne(r => r.url.includes('players/search'));
      req.flush(mockPlayers);
    });
  });

  describe('getAllTeams', () => {
    it('should return all NBA teams', () => {
      const mockTeams = [
        { id: 1, full_name: 'Los Angeles Lakers', abbreviation: 'LAL', city: 'Los Angeles' },
        { id: 2, full_name: 'Boston Celtics', abbreviation: 'BOS', city: 'Boston' }
      ];

      service.getAllTeams().subscribe(teams => {
        expect(teams.length).toBe(2);
        expect(teams[0].abbreviation).toBe('LAL');
      });

      const req = httpMock.expectOne(r => r.url.includes('teams'));
      req.flush(mockTeams);
    });
  });
});
