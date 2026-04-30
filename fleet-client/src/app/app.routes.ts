import { Routes } from '@angular/router';
import { Vehicles } from './components/vehicles/vehicles';
import { Drivers } from './components/drivers/drivers';
import { Deliveries } from './components/deliveries/deliveries';

export const routes: Routes = [
  { path: '', redirectTo: 'deliveries', pathMatch: 'full' },
  { path: 'vehicles', component: Vehicles },
  { path: 'drivers', component: Drivers },
  { path: 'deliveries', component: Deliveries },
];
