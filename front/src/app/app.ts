import { Component, inject } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';
import { AuthService } from './services/auth.service';
import { Router } from '@angular/router';            // <-- adicione

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  private auth = inject(AuthService);
  private router = inject(Router);                   // <-- injete o Router

  logout() {
    this.auth.logout();
    this.router.navigateByUrl('/', { replaceUrl: true }); // <-- volta pra inicial
    // alternativa: this.router.navigate(['/'], { replaceUrl: true });
  }
}
