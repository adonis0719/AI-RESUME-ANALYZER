import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html'
})
export class RegisterComponent {

  username = '';
  email = '';
  password = '';

  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient, private router: Router) {}

  register() {
    this.http.post(`${this.apiUrl}/register/`, {
      username: this.username,
      email: this.email,
      password: this.password
    }).subscribe({
      next: () => {
        alert("Registration successful");
        this.router.navigate(['/login']);
      },
      error: (err) => {
        alert("Registration failed");
        console.log(err);
      }
    });
  }
}
