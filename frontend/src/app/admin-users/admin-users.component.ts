import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-admin-users',
  templateUrl: './admin-users.component.html',
  styleUrls: ['./admin-users.component.css']
})
export class AdminUsersComponent implements OnInit {

  apiUrl = 'http://127.0.0.1:8000/api/admin';
  users: any[] = [];
  filteredUsers: any[] = [];
  searchQuery = '';
  error = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadUsers();
  }

  loadUsers() {
    this.http.get<any[]>(`${this.apiUrl}/users/`).subscribe({
      next: (res) => {
        this.users = res;
        this.applySearch();
      },
      error: (err) => { this.error = err?.error?.error || 'Failed to load users'; }
    });
  }

  onSearchInput() {
    this.applySearch();
  }

  applySearch() {
    const q = this.searchQuery.trim().toLowerCase();
    if (!q) {
      this.filteredUsers = [...this.users];
      return;
    }
    this.filteredUsers = this.users.filter(u =>
      (u.username || '').toLowerCase().includes(q) ||
      (u.email || '').toLowerCase().includes(q) ||
      String(u.id).includes(q)
    );
  }

  deleteUser(id: number) {
    if (!confirm('Are you sure you want to delete this user? This cannot be undone.')) return;
    this.http.delete(`${this.apiUrl}/users/${id}/`).subscribe({
      next: () => this.loadUsers(),
      error: (err) => alert(err?.error?.error || 'Failed to delete user')
    });
  }
}
