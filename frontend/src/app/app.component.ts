import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  darkMode = false;

  constructor(private router: Router) {}

  isLoggedIn(): boolean {
    return !!localStorage.getItem('access_token');
  }

  logout() {
    localStorage.removeItem('access_token');
    this.router.navigate(['/login']);
  }

  toggleTheme() {
    this.darkMode = !this.darkMode;

    if (this.darkMode) {
      document.body.style.backgroundColor = "#121212";
      document.body.style.color = "#ffffff";
    } else {
      document.body.style.backgroundColor = "#ffffff";
      document.body.style.color = "#000000";
    }
  }
}