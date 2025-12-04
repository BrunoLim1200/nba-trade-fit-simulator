import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/simulator', pathMatch: 'full' },
  { 
    path: 'simulator', 
    loadComponent: () => import('./features/simulator/simulator.component')
      .then(m => m.SimulatorComponent)
  },
];