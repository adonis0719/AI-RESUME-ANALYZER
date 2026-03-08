import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  private themeSubject = new BehaviorSubject<'light' | 'dark'>('light');
  theme$ = this.themeSubject.asObservable();

  constructor() {
    if (typeof localStorage !== 'undefined') {
      const saved = localStorage.getItem('theme') as 'light' | 'dark' | null;
      if (saved === 'light' || saved === 'dark') this.setTheme(saved);
      else this.setTheme('dark');
    }
  }

  getTheme(): 'light' | 'dark' {
    return this.themeSubject.value;
  }

  setTheme(theme: 'light' | 'dark') {
    this.themeSubject.next(theme);
    localStorage.setItem('theme', theme);
    document.body.setAttribute('data-theme', theme);
    if (theme === 'dark') {
      document.body.style.background = 'linear-gradient(135deg, #1e1b4b 0%, #312e81 30%, #1e293b 70%, #0f172a 100%)';
    } else {
      document.body.style.background = '#f8fafc';
    }
    document.body.style.color = theme === 'dark' ? '#f8fafc' : '#0f172a';
  }

  toggleTheme() {
    const next = this.themeSubject.value === 'light' ? 'dark' : 'light';
    this.setTheme(next);
    return next;
  }
}
