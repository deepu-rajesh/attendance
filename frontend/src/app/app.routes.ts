import { Routes } from '@angular/router';
import { Login } from './features/login/login';
import { Signup } from './features/signup/signup';
import { EmployeeDashboard } from './features/employee-dashboard/employee-dashboard';
import { ManagerDashboard } from './features/manager-dashboard/manager-dashboard';
import { AdminDashboard } from './features/admin-dashboard/admin-dashboard';
import { authGuard } from './core/guards/auth-guard';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: Login },
  { path: 'signup', component: Signup },
  { path: 'employee', component: EmployeeDashboard, canActivate: [authGuard] },
  { path: 'manager', component: ManagerDashboard, canActivate: [authGuard] },
  { path: 'admin', component: AdminDashboard, canActivate: [authGuard] },
];
