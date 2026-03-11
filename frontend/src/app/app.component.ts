import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { ThemeService } from './services/theme.service';
import { filter } from 'rxjs/operators';

const AUTH_ROUTES = ['/login', '/register', '/forgot-password'];

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  showNavbar = false;

  constructor(
    private router: Router,
    public themeService: ThemeService
  ) {}

  ngOnInit() {
    this.themeService.setTheme(this.themeService.getTheme());
    this.updateNavbarVisibility();
    this.router.events.pipe(
      filter((e): e is NavigationEnd => e instanceof NavigationEnd)
    ).subscribe(() => this.updateNavbarVisibility());
  }

  private updateNavbarVisibility(): void {
    const url = this.router.url.split('?')[0];
    const isAuthRoute = AUTH_ROUTES.some(r => url === r || url.startsWith(r + '/'));
    const isLoggedIn = !!localStorage.getItem('access_token');
    this.showNavbar = isLoggedIn && !isAuthRoute;
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem('access_token');
  }

  logout() {
    localStorage.removeItem('access_token');
    this.updateNavbarVisibility();
    this.router.navigate(['/login']);
  }

  toggleTheme() {
    this.themeService.toggleTheme();
  }
}