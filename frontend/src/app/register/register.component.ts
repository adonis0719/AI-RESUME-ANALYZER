import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  username = '';
  email = '';
  password = '';
  confirmPassword = '';
  otp = '';
  step = 1;
  loading = false;

  apiSendOtp = 'http://127.0.0.1:8000/api/send-otp/';
  apiVerifyOtp = 'http://127.0.0.1:8000/api/verify-otp/';


  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient, private router: Router) {}




  sendOtp() {
    if (this.password !== this.confirmPassword) {
      alert("Passwords do not match");
      return;
    }
    this.loading = true;
    const body = { email: this.email };
    this.http.post(this.apiSendOtp, body).subscribe({
      next: () => {
        this.loading = false;
        alert("OTP sent to your email");
        this.step = 2;
      },
      error: () => {
        this.loading = false;
        alert("Failed to send OTP");
      }
    });
  }


  verifyOtp() {
    this.loading = true;
    const body = {
      username: this.username,
      email: this.email,
      otp: this.otp,
      password: this.password
    };
    this.http.post(this.apiVerifyOtp, body).subscribe({
      next: () => {
        this.loading = false;
        alert("Account created successfully");
        this.router.navigate(['/login']);
      },
      error: () => {
        this.loading = false;
        alert("Invalid OTP");
      }
    });
  }



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
