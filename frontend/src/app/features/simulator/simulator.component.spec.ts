import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { SimulatorComponent } from './simulator.component';
import { SimulationService } from '@core/services/simulation.service';
import { of, throwError } from 'rxjs';
import { SimulationResult } from '@core/models/simulation-result.interface';

describe('SimulatorComponent', () => {
  let component: SimulatorComponent;
  let fixture: ComponentFixture<SimulatorComponent>;
  let simulationService: jasmine.SpyObj<SimulationService>;

  const mockTeams = [
    { id: 1, full_name: 'Los Angeles Lakers', abbreviation: 'LAL', city: 'Los Angeles' },
    { id: 2, full_name: 'Boston Celtics', abbreviation: 'BOS', city: 'Boston' }
  ];

  const mockPlayers = [
    { id: 1, full_name: 'LeBron James', is_active: true },
    { id: 2, full_name: 'Stephen Curry', is_active: true }
  ];

  beforeEach(async () => {
    const spy = jasmine.createSpyObj('SimulationService', [
      'getAllTeams',
      'searchPlayers',
      'simulateFit'
    ]);
    spy.getAllTeams.and.returnValue(of(mockTeams));
    spy.searchPlayers.and.returnValue(of(mockPlayers));

    await TestBed.configureTestingModule({
      imports: [
        SimulatorComponent,
        NoopAnimationsModule,
        HttpClientTestingModule
      ],
      providers: [
        { provide: SimulationService, useValue: spy }
      ]
    }).compileComponents();

    simulationService = TestBed.inject(SimulationService) as jasmine.SpyObj<SimulationService>;
    fixture = TestBed.createComponent(SimulatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('initialization', () => {
    it('should load teams on init', () => {
      expect(simulationService.getAllTeams).toHaveBeenCalled();
      expect(component.teams().length).toBe(2);
    });
  });

  describe('player search', () => {
    it('should not search with less than 2 characters', () => {
      component.playerSearchQuery = 'a';
      component.searchPlayers();

      expect(component.players().length).toBe(0);
    });

    it('should search players with valid query', () => {
      component.playerSearchQuery = 'lebron';
      component.searchPlayers();

      expect(simulationService.searchPlayers).toHaveBeenCalledWith('lebron');
      expect(component.players().length).toBe(2);
    });

    it('should select player and clear results', () => {
      const player = { id: 1, full_name: 'LeBron James', is_active: true };
      
      component.selectPlayer(player);

      expect(component.selectedPlayer()).toEqual(player);
      expect(component.playerSearchQuery).toBe('LeBron James');
      expect(component.players().length).toBe(0);
    });
  });

  describe('team selection', () => {
    it('should select team', () => {
      const team = mockTeams[0];
      
      component.selectTeam(team);

      expect(component.selectedTeam()).toEqual(team);
    });
  });

  describe('simulation', () => {
    const mockResult: SimulationResult = {
      player_id: 1,
      player_name: 'LeBron James',
      team_id: 1,
      team_name: 'Lakers',
      fit_score: 85,
      fit_label: 'Starter',
      estimated_minutes: 32,
      projected_role: 'Starter',
      player_archetypes: ['Ball Dominant'],
      team_needs_addressed: ['Playmaking'],
      reasons: ['Bom encaixe'],
      warnings: [],
      breakdown: {}
    };

    it('should show error if player not selected', () => {
      component.selectedTeam.set(mockTeams[0]);
      
      component.simulateFit();

      expect(component.error()).toBe('Selecione um jogador e um time.');
    });

    it('should show error if team not selected', () => {
      component.selectedPlayer.set(mockPlayers[0]);
      
      component.simulateFit();

      expect(component.error()).toBe('Selecione um jogador e um time.');
    });

    it('should call simulation service with correct params', () => {
      simulationService.simulateFit.and.returnValue(of(mockResult));
      component.selectedPlayer.set(mockPlayers[0]);
      component.selectedTeam.set(mockTeams[0]);

      component.simulateFit();

      expect(simulationService.simulateFit).toHaveBeenCalledWith(1, 1);
    });

    it('should set loading state during simulation', () => {
      simulationService.simulateFit.and.returnValue(of(mockResult));
      component.selectedPlayer.set(mockPlayers[0]);
      component.selectedTeam.set(mockTeams[0]);

      component.simulateFit();

      expect(component.loading()).toBe(false);
      expect(component.simulationResult()).toEqual(mockResult);
    });

    it('should handle simulation error', () => {
      simulationService.simulateFit.and.returnValue(throwError(() => new Error('API Error')));
      component.selectedPlayer.set(mockPlayers[0]);
      component.selectedTeam.set(mockTeams[0]);

      component.simulateFit();

      expect(component.error()).toBe('Erro ao simular encaixe. Tente novamente.');
      expect(component.loading()).toBe(false);
    });

    it('should clear previous result on new simulation', () => {
      simulationService.simulateFit.and.returnValue(of(mockResult));
      component.selectedPlayer.set(mockPlayers[0]);
      component.selectedTeam.set(mockTeams[0]);
      component.simulationResult.set(mockResult);

      component.simulateFit();

      expect(component.error()).toBeNull();
    });
  });
});
