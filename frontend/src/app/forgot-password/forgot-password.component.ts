

import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent {

  email = '';
  otp = '';
  password = '';
  confirmPassword = '';
  step = 1;
  loading = false;

  apiForgot = 'http://127.0.0.1:8000/api/forgot-password/';
  apiReset = 'http://127.0.0.1:8000/api/reset-password/';

  constructor(private http: HttpClient, private router: Router) {}

  sendOtp() {
    this.loading = true;
    this.http.post(this.apiForgot, { email: this.email }).subscribe({
      next: () => {
        this.loading = false;
        alert("OTP sent to email");
        this.step = 2;
      },
      error: (err) => {
        this.loading = false;
        alert(err.error?.error || "Failed to send OTP");
      }
    });
  }

  resetPassword() {
    if (this.password !== this.confirmPassword) {
      alert("Passwords do not match");
      return;
    }
    this.loading = true;
    const body = { email: this.email, otp: this.otp, password: this.password };
    this.http.post(this.apiReset, body).subscribe({
      next: () => {
        this.loading = false;
        alert("Password reset successful");
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.loading = false;
        alert(err.error?.error || "Failed to reset password");
      }
    });
  }

}
