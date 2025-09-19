import { Routes } from '@angular/router';
// import { HomeComponent } from './pages/home/home.component';
// import { LoginComponent } from './pages/login/login.component';
import { AutoresPage } from './pages/autores/autores.page';
import { authGuard } from './auth/auth.guard';

export const routes: Routes = [
  // { path: '', component: HomeComponent, title: 'Início' },
  // { path: 'login', component: LoginComponent, title: 'Login' },

  // Exemplo de rota protegida:
  { path: 'autores', component: AutoresPage, title: 'Autores', canActivate: [authGuard] },

  { path: '**', redirectTo: '' }
];