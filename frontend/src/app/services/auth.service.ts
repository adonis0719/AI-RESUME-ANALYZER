import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) { }

  login(identifier: string, password: string) {

    return this.http.post(`${this.apiUrl}/login/`, {
      identifier: identifier,
      password: password
    });

  }

  saveToken(token: string, isAdmin = false) {
    localStorage.setItem('access_token', token);
    localStorage.setItem('is_admin', String(isAdmin));
  }

  getToken() {
    return localStorage.getItem('access_token');
  }

  isAdmin(): boolean {
    return localStorage.getItem('is_admin') === 'true';
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('is_admin');
  }

  getResumes() {
  return this.http.get(`${this.apiUrl}/resumes/`);
  }

  getProfile() {
    return this.http.get(`${this.apiUrl}/profile/`);
  }


  updateProfile(username: string, profile_name: string) {
    return this.http.put(`${this.apiUrl}/profile/update/`, {
      username,
      profile_name
    });
  }

  changePassword(current_password: string, new_password: string) {
    return this.http.post(`${this.apiUrl}/change-password/`, {
      current_password,
      new_password
    });
  }



}